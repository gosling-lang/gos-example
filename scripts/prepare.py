import argparse
import csv
import dataclasses
import random

import h5py
import numpy as np
import vcf
from rich import print

CHR_FILTER = set(map(str, range(1, 23))).union({"X", "Y"})

SIGNIFICANCE_FILTER = [
    "Benign",
    "Benign/Likely_benign",
    "Likely_benign",
    "Uncertain_significance",
    "Likely_pathogenic",
    "Pathogenic/Likely_pathogenic",
    "Pathogenic",
    "risk_factor",
    "Conflicting_interpretations_of_pathogenicity",
]

GOLD_STARS_FILTER = [
    "criteria_provided,_multiple_submitters,_no_conflicts",
    "criteria_provided,_single_submitter",
    "criteria_provided,_conflicting_interpretations",
    "no_assertion_criteria_provided",
    "reviewed_by_expert_panel",
    "practice_guideline",
    "no_interpretation_for_the_single_variant",
    "no_assertion_provided",
]


def calc_gold_stars(gold_stars_str):
    if gold_stars_str == "practice_guideline":
        return 4
    if gold_stars_str == "reviewed_by_expert_panel":
        return 3
    if gold_stars_str == "criteria_provided,_multiple_submitters,_no_conflicts":
        return 2
    if gold_stars_str in [
        "criteria_provided,_single_submitter",
        "criteria_provided,_conflicting_interpretations",
    ]:
        return 1
    return 0


@dataclasses.dataclass
class BedRecord:
    chr: str
    start: int
    end: int
    ref: str
    alt: str
    importance: float
    gold_stars: int
    significance: str
    significance_conf: str
    variant_type: str
    origin: str
    molecular_consequence: str
    disease_name: str
    hgvs: str

    @classmethod
    def from_vcf(cls, record):
        significance = record.INFO["CLNSIG"][0]
        gold_stars = calc_gold_stars(",".join(record.INFO["CLNREVSTAT"]))
        disease_name = record.INFO["CLNDN"][0] if "CLNDN" in record.INFO else "."
        if disease_name == "not_provided":
            disease_name = "."

        return cls(
            chr="chr" + record.CHROM,
            start=int(record.POS),
            end=int(record.POS) + 1,
            ref=record.REF,
            alt=record.ALT[0].sequence if record.ALT[0] else ".",
            importance=gold_stars + random.random(),
            gold_stars=gold_stars,
            significance=significance,
            significance_conf=",".join(record.INFO.get("CLNSIGCONF", ["."])),
            variant_type=record.INFO.get("CLNVC", "."),
            origin=record.INFO.get("ORIGIN", ["."])[0],
            molecular_consequence=record.INFO.get("MC", ["."])[0],
            disease_name=disease_name,
            hgvs=record.INFO.get("CLNHGVS", ["."])[0].replace("%3D", "="),
        )


class DensityDict(dict):
    def count_record(self, record, column_index):
        self[record.CHROM][record.POS, column_index] += 1

    @classmethod
    def from_chromsizes(cls, filepath: str):
        d = cls()
        with open(filepath, "r") as f:
            for line in f:
                chrom, clen = line.split("\t")
                if chrom.lstrip("chr") in CHR_FILTER:
                    arr = np.zeros(
                        shape=(int(clen), len(SIGNIFICANCE_FILTER)), dtype=np.uint8
                    )
                    d[chrom.lstrip("chr")] = arr
        return d


def parse_args():
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--vcf", required=True, help="the input VCF file")
    parser.add_argument("--bed", required=True, help="the output BED file destination")
    parser.add_argument("--multivec", required=True, help="the output multivec destination")
    parser.add_argument("--chromsizes", required=True, help="the input chromsizes file")
    # fmt: on
    return parser.parse_args()


def main():
    import rich.progress

    args = parse_args()

    density_dict = DensityDict.from_chromsizes(args.chromsizes)

    with open(args.vcf, "r") as fi, open(args.bed, "w") as fo:
        reader = vcf.Reader(fi)
        writer = csv.writer(fo, delimiter="\t")

        for record in rich.progress.track(reader, description="Converting VCF..."):
            if (
                not (record.CHROM in CHR_FILTER)
                or not (
                    "CLNSIG" in record.INFO
                    and record.INFO["CLNSIG"][0] in SIGNIFICANCE_FILTER
                )
                or not (
                    "CLNREVSTAT" in record.INFO
                    and ",".join(record.INFO["CLNREVSTAT"]) in GOLD_STARS_FILTER
                )
            ):
                continue

            bed_record = BedRecord.from_vcf(record)
            row = dataclasses.astuple(bed_record)
            writer.writerow(row)

            # column is significance
            column_index = SIGNIFICANCE_FILTER.index(bed_record.significance)
            # Add frequency by 1
            density_dict.count_record(record, column_index)

    with h5py.File(args.multivec, "w") as f:
        for chrom, data in rich.progress.track(
            density_dict.items(), description="Writing multivec..."
        ):
            f.create_dataset(
                name=f"chr{chrom}",
                data=data,
                compression="gzip",
                chunks=True,
            )


if __name__ == "__main__":
    random.seed(1)
    main()
