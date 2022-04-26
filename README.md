```bash
conda env create -f environment.yaml
conda activate gos-use-case
snakemake -c all data/agg/clinvar.bed.beddb data/agg/density.multires.mv5
```
