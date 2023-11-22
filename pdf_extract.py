from pdfminer.high_level import extract_text
from poppler import load_from_data
from pypdf import PdfReader


from io import BytesIO


class PdfDocument:
    def __init__(self, file):
        self.content = file

    @classmethod
    def from_file(cls, path):
        with open(path, "rb") as file:
            content = file.read()
        return cls(content)

    def extract_text(self) -> str:
        return self.poppler_extract_text()

    def pypdf_extract_text(self) -> str:
        # https://pypdf.readthedocs.io/en/stable/user/post-processing-in-text-extraction.html
        # https://pypdf.readthedocs.io/en/stable/user/extract-text.html
        reader = PdfReader(self.content)
        pages = []
        for page in reader.pages:
         pages.append(page.extract_text())
        # print(reader.metadata)
        return " ".join(pages)

    def pdfminersix_extract_text(self) -> str:
        # https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html
        # https://www.unixuser.org/~euske/python/pdfminer/programming.html
        return extract_text(self.content)

    def poppler_extract_text(self) -> str:
        pdf_document = load_from_data(self.content)
        text_pages = []
        for page_index in range(pdf_document.pages):
            pdf_page = pdf_document.create_page(page_index)
            text_pages += pdf_page.text()
        return " ".join(text_pages)
    
    def poppler_text_list(self) -> list:
        """Returns a list of TextBox objects with attached style information
        
        Output structure subject to change"""
        pdf_data = self.content
        pdf_document = load_from_data(pdf_data)

        # Possibly replace with itertools chain
        boxes = []
        for page_index in range(pdf_document.pages):
            pdf_page = pdf_document.create_page(page_index)
            boxes.append(pdf_page.text_list(pdf_page.TextListOption.text_list_include_font))
        return boxes
