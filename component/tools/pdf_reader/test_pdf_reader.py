"""test for pdf reader"""
from unittest import TestCase
from .pdf_reader import PDFReader

class PDFReaderTestSuite(TestCase):
    """test suite for PDF Reader"""
    def setUp(self) -> None:
        """set up test dependencies"""
        self.reader = PDFReader()

    def tearDown(self) -> None:
        """clean up test resources"""

    def test_read_pdf(self) -> None:
        """test reading pdf files"""
        pdf_pages = self.reader.read_pdf(
            path="/home/st_yudi/personal-github-repository/"
                "ai-agent/component/tools/pdf_reader/sample/"
                "file-sample_150kB.pdf"
        )

        self.assertGreater(len(pdf_pages), 0)

        for pdf_page in pdf_pages:
            self.assertIsNotNone(pdf_page)
            self.assertIsInstance(pdf_page.page_number, int)
            self.assertIsInstance(pdf_page.text, str)