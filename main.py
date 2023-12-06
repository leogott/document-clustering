#!/usr/bin/env python3
"""Experimenting and Messy Code."""

# ruff: noqa: D103, ANN201, ANN202

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
import re
from collections import Counter
from collections.abc import Callable
from string import ascii_letters
from typing import Any, Iterable
from itertools import chain

from arxiv_dataset import ArXiVDataset
from pdf_extract import PdfDocument

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def bag_of_words():
    pass


def bag_of_chars(arg: str):
    characters = Counter(arg)
    chars_sans_letters = {
        key: count for key, count in characters.items() if key not in ascii_letters
    }
    print(chars_sans_letters, sort_dicts=True)


def replace_ligatures(text: str) -> str:
    """For a given string, replace each ligature with its corresponding characters."""
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


def _debug_replace_urls(text: str) -> str:
    def repl(m):
        print(m.group(0))
        return ""
    return replace_urls(text, repl)

def filter_font_size(stream: Iterable, __filter):
    for item in stream:
        if item.get_font_size() > 10:
            log.debug("Discarded item with text: %s" % item.text)
            continue
        yield item
    

def replace_urls(text: str, replace_with: str|Callable[..., str]="") -> str:
    """Replace urls using the given string or function."""
    p = re.compile(
        r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)")
    return re.sub(p, replace_with, text)


def main():
    log = logging.getLogger("main")
    log.setLevel(logging.INFO)
    paper = ArXiVDataset.get("2301.06511")

    # print("# Suspicious monograms")
    # bag_of_chars(PdfDocument(paper).extract_text())

    text_boxes = PdfDocument(paper).poppler_text_list()

    for item in filter_font_size(chain(*text_boxes), None):
        log.debug(item.text)
        # log.debug(item.get_font_name())
        log.debug(item.get_font_size())
        # log.debug(item.has_space_after)
    

    replace_urls(
        "https://example.org?query=a&something /n www.website.de http://another.org/")


if __name__ == "__main__":
    # This is executed when run from the command line
    main()
