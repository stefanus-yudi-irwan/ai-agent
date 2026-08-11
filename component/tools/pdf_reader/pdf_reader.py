"""module to read PDF"""
from dataclasses import dataclass
from pypdf import PdfReader

@dataclass
class PDFPage:
    """represent a single page document"""
    page_number: int
    text: str

class PDFReader:
    """reader for PDF reader"""

    def read_pdf(self, path: str) -> list[PDFPage]:
        """read a pdf and extract text from each page
        Args:
            path (str): path to PDF file
        Returns:
            list[DocumentPage]: a list of pdf page objects
        """
        try:
            reader = PdfReader(path)
            pages: list[PDFPage] = []
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text is None:
                    text = ""
                pages.append(PDFPage(page_number=page_number, text=text))
            return pages
        except Exception as error:
            raise RuntimeError(f"failed to read PDF: {path}") from error
