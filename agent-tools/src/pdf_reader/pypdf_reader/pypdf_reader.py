"""module to read PDF using pypdf"""
from dataclasses import dataclass
from pypdf import PdfReader
from loguru import logger

@dataclass
class PDFPage:
    """represent a single page document"""
    page_number: int
    text: str

class PDFReaderError(Exception):
    """Raise when PDF reader error"""

class PDFReader:
    """reader for PDF reader"""

    def read_pdf(self, path: str) -> list[PDFPage]:
        """read a pdf and extract text from each page
        Args:
            path (str): path to PDF file
        Returns:
            list[PDFPage]: a list of pdf page objects
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
        
        except Exception as e:
            error = PDFReaderError(f"failed to read PDF: {path}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e
