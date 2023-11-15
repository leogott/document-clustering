from pdfminer.high_level import extract_text
from poppler import load_from_data
from pypdf import PdfReader


from io import BytesIO


class PdfDocument:
    def __init__(self, arg):
        self.content = arg

    @classmethod
    def from_file(cls, path):
        with open(path, "rb") as file:
            content = file.read()
        return cls(content)

    def extract_text(self) -> str:
        return self.pypdf_extract_text(BytesIO(self.content))

    @staticmethod
    def pypdf_extract_text(arg) -> str:
        """"""
        # https://pypdf.readthedocs.io/en/stable/user/post-processing-in-text-extraction.html
        # https://pypdf.readthedocs.io/en/stable/user/extract-text.html
        reader = PdfReader(arg)
        pages = []
        for page in reader.pages:
         pages.append(page.extract_text())
        # print(reader.metadata)
        return str(pages)
    
    @staticmethod
    def pypdf_extract(arg) -> str:
        reader = PdfReader(arg)
        
        return reader.pages

    @staticmethod
    def pdfminersix_extract(arg) -> str:
        # https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html
        # https://www.unixuser.org/~euske/python/pdfminer/programming.html
        return extract_text(arg)

    @staticmethod
    def poppler_extract(arg) -> str:
        pdf_document = load_from_data(arg)
        page_1 = pdf_document.create_page(0)
        page_1_text = page_1.text()
        return page_1_text