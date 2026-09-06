"""integration test for pypdf reader packages"""
from unittest import TestCase
from pdf_reader.pypdf_reader import (
    PDFReader,
    PDFPage,
    PDFReaderError
)

class IntegrationTestPyPDFReader(TestCase):
    """test suite for pypdf reader"""

    def setUp(self) -> None:
        self.pdf_reader = PDFReader()

    def test_read_pdf(self) -> None:
        """test method read pdf files"""
        pdf_pages = self.pdf_reader.read_pdf(
            path="./tests/integration/file-sample_150kB.pdf")

        for index, content in enumerate(pdf_pages):
            self.assertEqual(index+1, content.page_number)
            self.assertIsNotNone(content.text)

        
