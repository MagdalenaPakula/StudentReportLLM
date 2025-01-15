import logging
import os
import re

import docx2txt
import pdfplumber
import openai

from conversion.database.mongo import mongo_collection
from conversion.database.qdrant import qdrant_collection


def save_to_mongodb(collection, file_name, text):
    logger = logging.getLogger(__name__ + '.save_to_mongodb')
    try:
        document = {
            "file_name": file_name,
            "text": text
        }
        result = collection.insert_one(document)
        logger.info(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error inserting document: {e}")

def save_to_qdrant(collection, file_name, text):
    logger = logging.getLogger(__name__ + '.save_to_qdrant')
    try:
        document = {
            "file_name": file_name,
            "text": text
        }
        result = collection.insert_one(document)
        logger.info(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error inserting document: {e}")

def generate_embedding(text):
    openai.api_key = ""
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']



def convert_to_txt(input_file):
    logger = logging.getLogger(__name__ + '.convert_to_txt')
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
