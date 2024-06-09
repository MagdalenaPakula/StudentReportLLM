import os
import docx2txt
import pdfplumber
import re
from src.database.mongo import mongo_collection


def save_to_mongodb(collection, file_name, text):
    # Create a document to insert
    document = {
        "file_name": file_name,
        "text": text
    }
    # Insert the document into the collection
    result = collection.insert_one(document)
    print(f"Inserted document with ID: {result.inserted_id}")


def convert_to_txt(input_file):
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == ".docx":
        text = docx2txt.process(input_file)
    elif file_extension == ".tex":
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        main_content_match = re.search(r'\\begin{document}(.*?)\\end{document}', content, re.DOTALL)
        if main_content_match:
            text = main_content_match.group(1)
        else:
            raise ValueError("Could not find main content in the LaTeX file.")

        text = text.replace("\n", "")
    elif file_extension == ".pdf":
        with pdfplumber.open(input_file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages])
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    # Save the text to MongoDB
    save_to_mongodb(mongo_collection, input_file, text)
    return text
