import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any

import poppler
import poppler.page
from pdfminer.high_level import extract_text
from poppler.page import TextBox
from pypdf import PdfReader

logger = logging.getLogger(__name__)

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"


def is_pdf(data: bytes) -> bool:
    """Verify that the data starts with the correct magic bytes."""
    return data.startswith(b"%PDF")


class PdfDocument:
    """Wrapper for pdf utilities."""

    def __init__(self, file):
        self.content = file
        if not is_pdf(self.content):
            msg = "file must be a PDF document"
            raise ValueError(msg)

    @classmethod
    def from_file(cls, path):
        """Alternative constructor from path or path-like."""
        return cls(Path(path).read_bytes())

    def pypdf_extract_text(self) -> str:
        """Return the entire text data of a pdf using pypdf."""
        # https://pypdf.readthedocs.io/en/stable/user/post-processing-in-text-extraction.html
        # https://pypdf.readthedocs.io/en/stable/user/extract-text.html
        reader = PdfReader(self.content)
        pages = [page.extract_text() for page in reader.pages]
        # print(reader.metadata)
        return " ".join(pages)

    def pdfminersix_extract_text(self) -> str:
        """Return the entire text data of a pdf using pdfminer.six."""
        # https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html
        # https://www.unixuser.org/~euske/python/pdfminer/programming.html
        return extract_text(self.content)

    def poppler_extract_text(self) -> str:
        """Return the entire text data of a pdf using poppler."""
        pdf_document = poppler.load_from_data(self.content)
        text_pages = []
        for page_index in range(pdf_document.pages):
            pdf_page = pdf_document.create_page(page_index)
            text_pages += pdf_page.text()
        return " ".join(text_pages)

    def poppler_textboxes_flat(self) -> list[poppler.page.TextBox]:
        """Return a list of TextBox objects with attached style information.

        It may be useful to have another method that returns a generator.
        Name and output not final.
        """
        pdf_data = self.content
        try:
            pdf_document = poppler.load_from_data(pdf_data)
        except ValueError:
            logger.exception(f"Poppler didn't like this pdf file of length {len(pdf_data)}.")
            logger.debug(f"File starts with: {pdf_data[:500]}")
            raise

        # Possibly replace with itertools chain
        boxes = []
        for p, page_index in enumerate(range(pdf_document.pages)):
            pdf_page = pdf_document.create_page(page_index)
            boxes.extend([
                {
                    "text": box.text,
                    "page": p,
                    "font_size": box.get_font_size(),
                    "font_name": _get_font_name(box),
                } for box in pdf_page.text_list(
                    pdf_page.TextListOption.text_list_include_font)
            ])
        return boxes


def _get_font_name(box):
    """Wrap get_font_name method in a try-except.

    fixes problem with paper 0704.0014
    """
    try:
        return box.get_font_name()
    except UnicodeDecodeError:
        logger.exception()
        return "Error"


def unbox_text(text_boxes: list[TextBox])-> Generator[tuple[str, int], Any, None]:
    """Take the output from poppler_textboxes_flat and turn it into something glassplitter can digest."""
    for i, item in enumerate(text_boxes):
        yield item["text"]
