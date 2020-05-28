[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.581183.svg)](https://doi.org/10.5281/zenodo.581183)

# Installation

Using Anaconda, create an environment with the required packages, and activate it:

```shell
$ conda env create --file environment.yml
$ source activate bayesian-mfa-paper     # remove the word "source" on Windows
```

The last successfully used package versions are listed in
[exact-package-versions.txt](exact-package-versions.txt).

Enable the environment IPython kernel and the Sankey widget

```shell
$ python -m ipykernel install --sys-prefix
$ jupyter nbextension enable --py --sys-prefix widgetsnbextension
$ jupyter nbextension enable --py --sys-prefix ipysankeywidget
```

Run the Jupyter notebook server:

```shell
$ jupyter notebook
```
