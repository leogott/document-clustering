# ACoLi Document Clustering

Clustering documents according to document similarity, with a focus on scientific publications.

[![PyPI - Version](https://img.shields.io/pypi/v/document-clustering.svg)](https://pypi.org/project/document-clustering)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/document-clustering.svg)](https://pypi.org/project/document-clustering)

-----

**Table of Contents**

- [ACoLi Document Clustering](#acoli-document-clustering)
  - [Getting started](#getting-started)
  - [Earlier work](#earlier-work)
  - [License](#license)

## Getting started

`generate_sample.py` is a good starting point. The code is very readable and hackable.

The recommended way to use this software is with a conda-managed python-environment.
Make sure conda is installed and create a new environment `conda create --file environment.yml`.

(You can later update it with `conda env update -f environment.yml`.)

`conda activate document-clustering && python generate_sample.py`
will run the code, but after activating the conda-env,
`./generate_sample.py` should work just as well.
(I personally prefer `ipython -i generate_sample.py`)

The script will start by fetching the sample of documents from arxiv, and terminate on error,
however all completed downloads are saved on disk, and will be re-used for successive runs,
(as long as the `cache/` directory remains in the same relative location).

## Earlier work

The code was mostly written from scratch and by referencing the scikit-learn documentation (it's pretty good).

But there are several earlier in-house implementations in the `old/` directory, that I also had a look at:

- `old/2019-beta-writer`: plain cosine-based document clustering
- `old/2021-beta-writer`: minor revision of `2019-beta-writer` with duplicate avoidance


## License

`document-clustering` (excluding the `old` subdirectory) is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
