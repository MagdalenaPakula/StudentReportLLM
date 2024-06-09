import tempfile
import unittest
import os

from unittest.mock import patch
from zipfile import BadZipFile
from pdfminer.pdfparser import PDFSyntaxError
from src.converters.convert import convert_to_txt
from src.database.mongo import mongo_collection


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

    def test_convert_docx_to_txt(self):
        with patch("docx2txt.process") as mock_docx2txt_process:
            mock_docx2txt_process.side_effect = BadZipFile("File is not a zip file")
            with self.assertRaises(BadZipFile):
                convert_to_txt(self.docx_file)

    def test_convert_pdf_to_txt(self):
        with patch("pdfplumber.open") as mock_pdf_open:
            mock_pdf_open.side_effect = PDFSyntaxError("No /Root object! - Is this really a PDF?")
            with self.assertRaises(PDFSyntaxError):
                convert_to_txt(self.pdf_file)

    def test_convert_tex_to_txt(self):
        text = convert_to_txt(self.tex_file).strip()  # Strip leading and trailing whitespace
        expected_text = "This is a test LaTeX file."
        self.assertEqual(text, "This is a test LaTeX file.")
        self.assertIn("test.tex", mongo_collection.find_one()["file_name"])

    def test_unsupported_file_format(self):
        with self.assertRaises(ValueError):
            convert_to_txt(self.unsupported_file)


if __name__ == "__main__":
    unittest.main()
