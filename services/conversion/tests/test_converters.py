import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from zipfile import BadZipFile

from pdfminer.pdfparser import PDFSyntaxError

from conversion.convert import convert_to_txt
from conversion.database.mongo import mongo_collection


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

    @patch("services.conversion.convert.save_to_mongodb")
    def test_convert_docx_to_txt(self, mock_save_to_mongodb):
        with patch("docx2txt.process") as mock_docx2txt_process:
            mock_docx2txt_process.side_effect = BadZipFile("File is not a zip file")
            with self.assertRaises(BadZipFile):
                convert_to_txt(self.docx_file)

            # Verify that save_to_mongodb wasn't called
            self.assertFalse(mock_save_to_mongodb.called)

    @patch("services.conversion.convert.save_to_mongodb")
    def test_convert_pdf_to_txt(self, mock_save_to_mongodb):
        with patch("pdfplumber.open") as mock_pdf_open:
            mock_pdf_open.side_effect = PDFSyntaxError("No /Root object! - Is this really a PDF?")
            with self.assertRaises(PDFSyntaxError):
                convert_to_txt(self.pdf_file)

            # Verify that save_to_mongodb wasn't called
            self.assertFalse(mock_save_to_mongodb.called)

    @patch("services.conversion.convert.save_to_mongodb")
    def test_convert_tex_to_txt(self, mock_save_to_mongodb):
        # Mock the return value of save_to_mongodb
        mock_save_to_mongodb.return_value = MagicMock()

        with patch("pdfplumber.open") as mock_pdf_open:
            text = convert_to_txt(self.tex_file).strip()  # Strip leading and trailing whitespace
            expected_text = "This is a test LaTeX file."
            self.assertEqual(text, expected_text)

            # Verify that save_to_mongodb was called with the correct arguments
            mock_save_to_mongodb.assert_called_once_with(mongo_collection, self.tex_file, expected_text.strip())

    @patch("services.conversion.convert.save_to_mongodb")
    def test_unsupported_file_format(self, mock_save_to_mongodb):
        with self.assertRaises(ValueError):
            convert_to_txt(self.unsupported_file)

        # Verify that save_to_mongodb wasn't called
        self.assertFalse(mock_save_to_mongodb.called)


if __name__ == "__main__":
    unittest.main()
