```bash
conda env create -f environment.yaml
conda activate gos-example
# preprocess data
snakemake -c all data/agg/clinvar.bed.beddb data/agg/density.multires.mv5
# run the notebook
jupyter notebook 
```
