#!/usr/bin/env -S python3 -i
# ruff: noqa: D103, F401
"""Experimenting and Messy Code."""


__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
import re
from collections import Counter
from collections.abc import Callable, Iterable
from string import ascii_letters

import rich
from glassplitter import Tokenizer

from arxiv_dataset import ArXiVDataset
from pdf_extract import PdfDocument

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def bag_of_words(): ... #TODO (leogott): implement this


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


def filter_font_size(stream: Iterable, __filter):
    for item in stream:
        if item.get_font_size() > 10:
            logger.debug("Discarded item with text: %s", item.text)
            continue
        yield item


def _debug_replace_urls(text: str) -> str:
    def repl(m):
        print(m.group(0))
        return ""

    return replace_urls(text, repl)


def replace_urls(text: str, replace_with: str | Callable[..., str] = "") -> str:
    """Replace urls using the given string or function."""
    p = re.compile(
        r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
    )
    return re.sub(p, replace_with, text)


def bundled(sentence_list, group_data):
    """Re-attach (potentially un-hashable) data-objects.

    Take an iterable of lists of tuples (obj, i),
    and a mapping of i to data,
    enumerate the group data and re-attach it.
    """
    for sentence in sentence_list:
        yield [(a, group_data[i]) for a, i in sentence]


def tokenize(tokenizer: Tokenizer, text_boxes):
    """Tokenize text-boxes.

    Wrap glassplitter tokenizer and re-attach data.
    """
    text_box_dict = dict(enumerate(text_boxes))
    spans = ((item.text, i) for i, item in text_box_dict.items())
    sentence_list = tokenizer.split(spans, trim=True)

    return list(bundled(sentence_list, text_box_dict))


def main() -> list[str]:
    replace_urls(
        "https://example.org?query=a&something /n www.website.de http://another.org/"
    )


if __name__ == "__main__":
    # spans = [("I am a ", {"line": 1}), ("split sentence!", {"line": 2})]
    tokenizer = Tokenizer(lang="en", clean=True, doc_type="pdf")
    # [[("", 0), ("I", 0), ("am", 0), ("a", 0), ("split", 1), ("sentence", 1), ("!", 1), ("", 1)]]
    paper = ArXiVDataset.get("2301.06511")
    text_boxes = PdfDocument(paper).poppler_text_list()[:99]

    out = list(tokenize(tokenizer, text_boxes))
    rich.print(out)
