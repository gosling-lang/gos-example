rule aggregate_multivec:
	input:
		chromsizes = "data/hg38.chrom.sizes",
		multivec = "data/density.mv5"
	output: "data/agg/density.multires.mv5"
	shell: """
	clodius aggregate multivec \
		--chromsizes-filename {input.chromsizes} \
		--starting-resolution 1 \
		--output-file {output} \
		{input.multivec}
	"""

rule aggregate_bed:
	input:
		chromsizes = "data/hg38.chrom.sizes",
		bed = "data/clinvar.bed"
	output: "data/agg/clinvar.bed.beddb"
	shell: """
	clodius aggregate bedfile \
		--chromsizes-filename {input.chromsizes} \
		--delimiter $'\t' \
		--importance-column 6 \
		--max-per-tile 80 \
		--output-file {output} \
		{input.bed}
	"""

rule convert_vcf:
	input:
		vcf = "data/clinvar.vcf",
		chromsizes = "data/hg38.chrom.sizes",
	output:
		bed = "data/clinvar.bed",
		multivec = "data/density.mv5"
	shell: """
	python scripts/prepare.py \
		--vcf {input.vcf} \
		--chromsizes {input.chromsizes} \
		--bed {output.bed} \
		--multivec {output.multivec}
	"""

rule download_vcf:
	output: "data/clinvar.vcf"
	shell: """
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz -O {output}.gz
	gunzip {output}.gz
	"""

rule download_chromsizes:
	output: "data/hg38.chrom.sizes"
	shell: """
	wget https://raw.githubusercontent.com/igvteam/igv/329449af409bfb7f60e4db5e7793882bd8b5f602/genomes/sizes/hg38.chrom.sizes -O {output}
	"""
