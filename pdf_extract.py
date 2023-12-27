from pathlib import Path

import poppler
import poppler.page
from pdfminer.high_level import extract_text
from poppler import load_from_data
from pypdf import PdfReader

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

# class TextBox(poppler.page.TextBox):
#     # def __dict__(self):...

#     def a(arg: TextBox) -> dict:
#         print(arg.__dict__)
#         return arg


class PdfDocument:
    """Wrapper for pdf utilities."""

    def __init__(self, file):
        self.content = file

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
        pdf_document = load_from_data(self.content)
        text_pages = []
        for page_index in range(pdf_document.pages):
            pdf_page = pdf_document.create_page(page_index)
            text_pages += pdf_page.text()
        return " ".join(text_pages)

    def poppler_text_list(self) -> list[poppler.page.TextBox]:
        """Return a list of TextBox objects with attached style information.

        It may be useful to have another method that returns a generator.
        Name and output not final.
        """
        pdf_data = self.content
        pdf_document = load_from_data(pdf_data)

        # Possibly replace with itertools chain
        boxes = []
        for p, page_index in enumerate(range(pdf_document.pages)):
            pdf_page = pdf_document.create_page(page_index)
            boxes.extend([
                {
                    "text": box.text,
                    "page": p,
                    "font_size": box.get_font_size(),
                    "font_name": box.get_font_name(),
                } for box in pdf_page.text_list(
                    pdf_page.TextListOption.text_list_include_font)
            ])
        return boxes
