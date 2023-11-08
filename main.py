#!/usr/bin/env python3
"""
Module Docstring

conda env update --file environment.yml
"""

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
from pypdf import PdfReader
from pdfminer.high_level import extract_text
from poppler import load_from_file
import sys
import shelve
from urllib.request import urlopen
# from difflib import unified_diff
from io import BytesIO

logger = logging.getLogger()
log = logger.debug


class ArXiVDataset:
    """Abstraction layer for downloading, caching, loading PDFs from ArXiV"""
    
    @staticmethod
    def arxiv_cached_download(arxiv_id) -> bytes:
        with shelve.open("arxiv_cache") as db:
            if arxiv_id not in db:
                log("{id} was not found in the local db. Requesting…".format(id=arxiv_id))
                url = "https://arxiv.org/pdf/{id}".format(id=arxiv_id)
                with urlopen(url) as s:
                    db[arxiv_id] = s.read
            return db.get(arxiv_id)
    
    @classmethod
    def get(cls, arxiv_id):
        return cls.arxiv_cached_download(arxiv_id)


def main():
    """ Main entry point of the app """
    # s1 = pypdf_extract("example.pdf")
    # s2 = pdfminersix_extract("example.pdf")
    # s3 = poppler_extract("example.pdf")
    # with open("s1.txt", "w") as file:
    #     file.write(s1)
    # with open("s2.txt", "w") as file:
    #     file.write(s2)
    # with open("s3.txt", "w") as file:
    #     file.write(s3)
    # print(pdfminer_layout_extract("example.pdf"))
    # sys.stdout.writelines(unified_diff(s1, s2, fromfile='before.py', tofile='after.py'))
    # meld s1.txt s2.txt
    paper = ArXiVDataset.get("2301.06511")
    print(len(paper))
    print(type(paper))
    print(pypdf_extract(BytesIO(paper)))
    

def pypdf_extract(arg) -> str:
    # https://pypdf.readthedocs.io/en/stable/user/post-processing-in-text-extraction.html
    # https://pypdf.readthedocs.io/en/stable/user/extract-text.html
    reader = PdfReader(arg)
    page = reader.pages[0]
    # print(reader.metadata)
    return page.extract_text()

def pdfminersix_extract(arg) -> str:
    # https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html
    # https://www.unixuser.org/~euske/python/pdfminer/programming.html
    return extract_text(arg)


def poppler_extract(arg) -> str:
    pdf_document = load_from_file(arg)
    page_1 = pdf_document.create_page(0)
    page_1_text = page_1.text()
    return page_1_text

""" def pdfminer_layout_extract(arg) -> str:
    # https://denis.papathanasiou.org/archive/2010.08.04.post.pdf
    pages=layout_scanner.get_pages(arg)
    return pages[0]

def pdftotext_extract(arg) -> str:
    with open(arg, "rb") as f:
        pdf = pdftotext.PDF(f)
    return pdf[0]

def pdftextract_extract(arg) -> str:
    pdf = XPdf(arg)
    return pdf.to_text() """



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
