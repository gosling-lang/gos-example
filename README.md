# gos-example

This repo contains a set of Jupyter notebooks introducing key features of the [`gos`](https://github.com/gosling-lang/gos) genomics visualization library for Python.

The notebooks can be run via Google Colab,

- `getting-started.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gosling-lang/gos-example/blob/main/notebooks/getting-started.ipynb)

- `data-loading.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gosling-lang/gos-example/blob/main/notebooks/data-loading.ipynb)

- `clinvar.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gosling-lang/gos-example/blob/main/notebooks/clinvar.ipynb)

or locally with Jupyter,

```bash
jupyter notebook notebooks/
```

> **Note**  The `clinvar.ipynb` notebook contains the option to load large datasets locally rather than via a remote HiGlass server.
> The `Snakemake` workflow contained in this repo will generate those files if desired, but running these scripts are optional.

```bash
conda env create -f environment.yaml
conda activate gos-example
# preprocess data
snakemake -c all data/agg/clinvar.bed.beddb data/agg/density.multires.mv5
# run the notebook
jupyter notebook 
```
