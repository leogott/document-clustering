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
# from difflib import unified_diff
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

def strip_urls(text: str) -> str:
    # Todo implement with regex
    text.replace()


def main():
    """ Main entry point of the app """
    from pypdf import PdfReader

    paper = ArXiVDataset.get("2301.06511")
    # print(PDFDocument(paper).extract_text())
    # ArXiVDataset.query_metadata("2301.06511")

    print("# Suspicious monograms")
    # bag_of_chars(PdfDocument(paper).extract_text())

    reader = PdfReader(BytesIO(paper))

    page = reader.pages[3]
    # print(page.extract_text())

    parts = dict()

    def visitor_body(text, cm, tm, font_dict, font_size):
        font = dict.get(font_dict, "/BaseFont", "") if font_dict else "None"
        if font in parts:
            parts[font].update(Counter(text))
        else:
            parts[font] = Counter(text)

    page.extract_text(visitor_text=visitor_body)
    text_body = "".join(parts)

    df = pd.DataFrame(parts)
    print(df)

    print(text_body)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
