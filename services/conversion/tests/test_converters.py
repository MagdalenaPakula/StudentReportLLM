import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from zipfile import BadZipFile

from pdfminer.pdfparser import PDFSyntaxError

from services.conversion.src.conversion.convert import convert_to_txt
from services.conversion.src.conversion.database.mongo import mongo_collection


class TestTextConversion(unittest.TestCase):
    def setUp(self):
        # Create temporary files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docx_file = os.path.join(self.temp_dir.name, "test.docx")
        self.pdf_file = os.path.join(self.temp_dir.name, "test.pdf")
        self.tex_file = os.path.join(self.temp_dir.name, "test.tex")
        self.unsupported_file = os.path.join(self.temp_dir.name, "test.jpg")

        # Write sample content to the temporary files
        with open(self.docx_file, "w") as f:
            f.write("This is a test DOCX file.")
        with open(self.pdf_file, "w") as f:
            f.write("This is a test PDF file.")
        with open(self.tex_file, "w") as f:
            f.write("\\documentclass{article}\n\\begin{document}\nThis is a test LaTeX file.\n\\end{document}")
        with open(self.unsupported_file, "w") as f:
            f.write("This is an unsupported file format.")

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    @patch("conversion.convert.save_to_mongodb")
    def test_convert_docx_to_txt(self, mock_save_to_mongodb):
        with patch("docx2txt.process") as mock_docx2txt_process:
            mock_docx2txt_process.side_effect = BadZipFile("File is not a zip file")
            with self.assertRaises(BadZipFile):
                convert_to_txt(self.docx_file)

            # Verify that save_to_mongodb wasn't called
            self.assertFalse(mock_save_to_mongodb.called)

    @patch("conversion.convert.save_to_mongodb")
    def test_convert_pdf_to_txt(self, mock_save_to_mongodb):
        with patch("pdfplumber.open") as mock_pdf_open:
            mock_pdf_open.side_effect = PDFSyntaxError("No /Root object! - Is this really a PDF?")
            with self.assertRaises(PDFSyntaxError):
                convert_to_txt(self.pdf_file)

            # Verify that save_to_mongodb wasn't called
            self.assertFalse(mock_save_to_mongodb.called)

    @patch("conversion.convert.save_to_mongodb")
    def test_convert_tex_to_txt(self, mock_save_to_mongodb):
        # Mock the return value of save_to_mongodb
        mock_save_to_mongodb.return_value = MagicMock()

        with patch("pdfplumber.open") as mock_pdf_open:
            text = convert_to_txt(self.tex_file).strip()  # Strip leading and trailing whitespace
            expected_text = "This is a test LaTeX file."
            self.assertEqual(text, expected_text)

            # Verify that save_to_mongodb was called with the correct arguments
            mock_save_to_mongodb.assert_called_once_with(mongo_collection, self.tex_file, expected_text.strip())

    @patch("conversion.convert.save_to_mongodb")
    def test_unsupported_file_format(self, mock_save_to_mongodb):
        with self.assertRaises(ValueError):
            convert_to_txt(self.unsupported_file)

        # Verify that save_to_mongodb wasn't called
        self.assertFalse(mock_save_to_mongodb.called)

    @patch("conversion.convert.save_to_mongodb")
    def test_convert_tex_missing_document_block(self, mock_save_to_mongodb):
        invalid_latex_file = os.path.join(self.temp_dir.name, "invalid.tex")
        with open(invalid_latex_file, "w") as f:
            f.write(r"\documentclass{article}\nNo document block here.")

        with self.assertRaisesRegex(ValueError, "Could not find main content"):
            convert_to_txt(invalid_latex_file)

        mock_save_to_mongodb.assert_not_called()

    @patch("conversion.convert.failed_conversions.add")
    @patch("conversion.convert.save_to_mongodb")
    def test_docx2txt_unexpected_exception(self, mock_save_to_mongodb, mock_failed_counter):
        with patch("docx2txt.process") as mock_docx2txt_process:
            mock_docx2txt_process.side_effect = RuntimeError("Unexpected Error")

            with self.assertRaises(RuntimeError):
                convert_to_txt(self.docx_file)

            mock_failed_counter.assert_called_once()
            mock_save_to_mongodb.assert_not_called()

    @patch("conversion.convert.save_to_mongodb")
    def test_convert_docx_valid_document(self, mock_save_to_mongodb):
        with patch("docx2txt.process") as mock_docx2txt_process:
            mock_docx2txt_process.return_value = "Valid DOCX content."

            text = convert_to_txt(self.docx_file)
            self.assertEqual(text, "Valid DOCX content.")

            mock_save_to_mongodb.assert_called_once_with(
                mongo_collection, self.docx_file, "Valid DOCX content."
            )

    @patch("conversion.convert.save_to_mongodb")
    def test_convert_pdf_with_multiple_pages(self, mock_save_to_mongodb):
        mock_pdf = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1 content."
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page 2 content."
        mock_pdf.pages = [mock_page1, mock_page2]

        with patch("pdfplumber.open", MagicMock()) as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            text = convert_to_txt(self.pdf_file)

        self.assertEqual(text, "Page 1 content.\nPage 2 content.")

        mock_save_to_mongodb.assert_called_once_with(
            mongo_collection, self.pdf_file, "Page 1 content.\nPage 2 content."
        )

if __name__ == "__main__":
    unittest.main()
