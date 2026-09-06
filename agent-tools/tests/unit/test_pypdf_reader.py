"""unit test for pypdf reader packages"""
from unittest import TestCase
from unittest.mock import Mock, patch
from pdf_reader.pypdf_reader import (
    PDFReader,
    PDFPage,
    PDFReaderError
)

class UnitTestPyPDFReader(TestCase):
    """test suite for pypdf reader"""

    def setUp(self) -> None:
        self.pdf_reader = PDFReader()

    @patch("pdf_reader.pypdf_reader.pypdf_reader.PdfReader")
    def test_read_pdf(self, mock_pdf_reader) -> None:
        """test method read pdf files"""
        mock_page_1 = Mock()
        mock_page_1.extract_text.return_value = "Page 1 content"

        mock_page_2 = Mock()
        mock_page_2.extract_text.return_value = "Page 2 content"

        mock_pdf_reader.return_value.pages = [
            mock_page_1,
            mock_page_2
        ]

        result = self.pdf_reader.read_pdf(path="test.pdf")
        print(result)

        self.assertEqual(
            result, 
            [
                PDFPage(page_number=1, text="Page 1 content"),
                PDFPage(page_number=2, text="Page 2 content")
            ]
        )

        mock_pdf_reader.assert_called_once_with("test.pdf")

    @patch("pdf_reader.pypdf_reader.pypdf_reader.PdfReader")
    def test_read_pdf_error(self, mock_pdf_reader) -> None:
        """test method read pdf files when error"""
        mock_pdf_reader.side_effect = Exception("Failed to read PDF")

        with self.assertRaises(PDFReaderError) as context:
            self.pdf_reader.read_pdf(path="test.pdf")

        self.assertEqual(
            str(context.exception),
            "failed to read PDF: test.pdf"
        )

        mock_pdf_reader.assert_called_once_with("test.pdf")