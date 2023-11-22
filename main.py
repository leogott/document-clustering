#!/usr/bin/env python3
"""
Module Docstring

conda env update --file environment.yml
"""

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

from arxiv_dataset import ArXiVDataset
from pdf_extract import PdfDocument

from collections import Counter
import logging
from urllib.request import urlopen
from io import BytesIO
import pandas as pd

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(levelname)s : %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

log = logger.debug


def bag_of_words():
    pass


def bag_of_chars(arg: str):
    import pandas as pd
    from string import ascii_letters

    characters = Counter(arg)
    chars_sans_letters = {key: count for key,
                          count in characters.items() if key not in ascii_letters}
    print(chars_sans_letters, sort_dicts=True)


def replace_ligatures(text: str) -> str:
    ligatures = {
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
        # "Ꜳ": "AA",
        # "Æ": "AE",
        # "ꜳ": "aa",
    }
    return text.translate(ligatures)

def replace_urls(text: str, replace = None) -> str:
    """replace urls with str or function"""
    import re
    p = re.compile(r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)")
    def repl(m):
        print(m.group(0))
        return ''
    new_text = re.sub(p, repl, text)
    # Todo implement url removal
    return new_text
    # match.span()


def main():
    """ Main entry point of the app """
    from pprint import pprint

    paper = ArXiVDataset.get("2301.06511")
    # print(PDFDocument(paper).extract_text())
    # ArXiVDataset.query_metadata("2301.06511")

    # print("# Suspicious monograms")
    # bag_of_chars(PdfDocument(paper).extract_text())

    text_boxes = PdfDocument(paper).poppler_text_list()

    print(text_boxes[0][5].text)
    print(text_boxes[0][5].get_font_name())
    print(text_boxes[0][5].get_font_size())
    print(text_boxes[0][5].has_space_after)

    print(text_boxes[0][25].text)
    print(text_boxes[0][25].get_font_name())
    print(text_boxes[0][25].get_font_size())
    print(text_boxes[0][25].has_space_after)

    replace_urls( "https://example.org?query=a&something /n www.website.de http://another.org/" )

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
