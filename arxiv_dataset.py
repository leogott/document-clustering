#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
import shelve
from urllib.parse import urlencode
from urllib.request import urlopen

logger = logging.getLogger()
log = logger.debug


class ArXiVDataset:
    """Abstraction layer for downloading, caching, loading PDFs from ArXiV"""

    @staticmethod
    def query_metadata(arxiv_id):
        # query the arXiv
        url = "http://export.arxiv.org/api/query?"
        params = {"id_list": arxiv_id, "start": 0, "max_results": 1}
        data = urlopen(url + urlencode(params))
        print(data.read().decode('utf-8'))

    @staticmethod
    def arxiv_cached_download(arxiv_id) -> bytes:
        with shelve.open("arxiv_cache") as db:
            if arxiv_id not in db:
                log(f"{arxiv_id} was not found in the local db. Requesting…")
                url = f"https://arxiv.org/pdf/{arxiv_id}"
                with urlopen(url) as s:
                    db[arxiv_id] = s.read()
            return db.get(arxiv_id)  # type: ignore

    @classmethod
    def get(cls, arxiv_id):
        return cls.arxiv_cached_download(arxiv_id)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    pass
