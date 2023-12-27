#!/usr/bin/env python3
# ruff: noqa: S301
"""Abstraction layer for ArXiV."""


__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
import shelve
from io import BytesIO
from urllib.parse import urlencode
from urllib.request import urlopen

logger = logging.getLogger()
log = logger.debug


class ArXiVDataset:
    """Abstraction layer for downloading, caching, loading PDFs from ArXiV."""

    @staticmethod
    def query_metadata(arxiv_id):
        """Query the ArXiV-Dataset for metadata.

        arxiv_id: (required) Provide a specific ID.
        """
        # query the arXiv
        url = "http://export.arxiv.org/api/query?"
        params = {"id_list": arxiv_id, "start": 0, "max_results": 1}
        data = urlopen(url + urlencode(params))
        return data.read().decode("utf-8")

    @staticmethod
    def _arxiv_download(arxiv_id: str) -> bytes:
        url = f"https://arxiv.org/pdf/{arxiv_id}"
        with urlopen(url) as s:
            return s.read()

    @classmethod
    def _arxiv_cached_download(cls, arxiv_id: str) -> bytes:
        """Return the downloaded pdf, using shelve as a cache."""
        with shelve.open("arxiv_cache") as db:
            if arxiv_id not in db:
                log(f"{arxiv_id} was not found in the local db. Requesting…")
                db[arxiv_id] = cls._arxiv_download(arxiv_id)
            return db.get(arxiv_id)

    @classmethod
    def get(cls, arxiv_id) -> bytes:
        """Return the binary content of the requested paper's pdf."""
        return cls._arxiv_cached_download(arxiv_id)

    @classmethod
    def stream(cls, arxiv_id: str) -> BytesIO:
        """Return a buffered stream of the requested paper's pdf.

        Behaves very similar to builtin open().
        """
        return BytesIO(cls.get(arxiv_id))
