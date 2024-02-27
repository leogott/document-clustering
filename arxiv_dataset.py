#!/usr/bin/env python3
# ruff: noqa: S301
"""Abstraction layer for downloading, caching, loading PDFs from ArXiV."""


__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import feedparser
from sklearn.utils import Bunch

from pdf_extract import is_pdf
from utils import shelve_memoize

logger = logging.getLogger(__name__)
log = logger.debug


@shelve_memoize("arxiv_metadata_cache")
def query_metadata(arxiv_id):
    """Query the ArXiV-Dataset for metadata.

    arxiv_id: (required) Provide a specific ID.

    arXiv provides an API in the form of an Atom feed. This function conveniently
    returns a Dict-like (and also Bunch-like) object containing a paper's metadata.

    Ref: <https://feedparser.readthedocs.io/en/latest/common-atom-elements.html>
    """
    url = "http://export.arxiv.org/api/query?"
    params = {"id_list": arxiv_id, "start": 0, "max_results": 1}
    return feedparser.parse(url + urlencode(params)).entries[0]


@shelve_memoize("arxiv_cache")
def get(arxiv_id) -> bytes:
    """Return the binary content of the requested paper's pdf."""
    url = f"https://export.arxiv.org/pdf/{arxiv_id}"
    with urlopen(url) as s:
        pdf = s.read()
        if not is_pdf(pdf):
            raise RuntimeError("arxiv did not return a pdf for {}", arxiv_id)
        return pdf


def stream(arxiv_id: str) -> BytesIO:
    """Return a buffered stream of the requested paper's pdf.

    Behaves very similar to builtin open().
    """
    return BytesIO(get(arxiv_id))


def fetch_arxiv_sample(file=Path("sample/test_sample.txt")):
    """
    Return a Bunch (Dict-like) of the specified papers and some metadata.

    Beware: data is just a list of pdfs in byte form.
    """
    ids = []
    titles = []
    dates = []
    corpus = []
    for line in file.read_text().splitlines():
        metadata = query_metadata(line)

        # for line in Path("sample/arxiv_sample.json").read_text().splitlines():
        # paper = json.loads(line)
        logger.debug("Processing: %s", line)

        ids.append(line)
        titles.append(metadata.title)
        dates.append(metadata.updated)

        corpus.append(get(line))
    return Bunch(data=corpus, ids=ids, titles=titles, dates=dates)
