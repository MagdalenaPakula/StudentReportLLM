import os
import docx2txt
import pdfplumber
import re
from lib.database.mongo import mongo_collection
from lib.logging.logstash_logger import LogStashLogger

logger = LogStashLogger.get_logger()


def save_to_mongodb(collection, file_name, text):
    try:
        document = {
            "file_name": file_name,
            "text": text
        }
        result = collection.insert_one(document)
        logger.info(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error inserting document: {e}")


def convert_to_txt(input_file):
    try:
        file_extension = os.path.splitext(input_file)[1].lower()

        if file_extension == ".docx":
            logger.info(f"Processing DOCX file: {input_file}")
            text = docx2txt.process(input_file)
        elif file_extension == ".tex":
            logger.info(f"Processing LaTeX file: {input_file}")
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()

            main_content_match = re.search(r'\\begin{document}(.*?)\\end{document}', content, re.DOTALL)
            if main_content_match:
                text = main_content_match.group(1)
            else:
                raise ValueError("Could not find main content in the LaTeX file.")

            text = text.replace("\n", "")
        elif file_extension == ".pdf":
            logger.info(f"Processing PDF file: {input_file}")
            with pdfplumber.open(input_file) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages])
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        logger.info(f"Conversion successful for file: {input_file}")
        save_to_mongodb(mongo_collection, input_file, text)
        return text
    except Exception as e:
        logger.error(f"Error during conversion for file {input_file}: {e}")