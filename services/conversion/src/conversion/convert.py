import logging
import os
import re
import traceback

import docx2txt
import pdfplumber
from opentelemetry import metrics, trace
from opentelemetry.trace import Span
from opentelemetry.trace.span import StatusCode as SpanStatusCode

from conversion.database.mongo import mongo_collection

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
successful_conversions = meter.create_counter("conversion.converted_documents")
failed_conversions = meter.create_counter("conversion.conversion_errors")


def save_to_mongo(file_id, text):
    logger = logging.getLogger(__name__ + '.save_to_mongodb')
    try:
        document = {
            "file_id": file_id,
            "text": text
        }
        result = mongo_collection.insert_one(document)
        logger.info(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error inserting document: {str(e)}")


def _save_to_mongodb(grading_request_id: str, document_text: str):
    # todo: implement saving to mongo
    pass


def convert_to_txt(input_file) -> str:
    logger = logging.getLogger(__name__ + '.convert_to_txt')

    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension not in [".docx", ".tex", ".pdf"]:
        logger.warning("Unsupported file format for file %s", input_file)
        failed_conversions.add(1, {"conversion.document.type": "other"})
        raise ValueError(f"Unsupported file format: {file_extension}")

    attributes = {
        "conversion.document.type": file_extension
    }

    try:
        with tracer.start_as_current_span("conversion", attributes=attributes) as span:
            span: Span
            try:
                if file_extension == ".docx":
                    text = convert_from_docx(input_file, logger)
                elif file_extension == ".tex":
                    text = convert_from_tex(input_file, logger)
                elif file_extension == ".pdf":
                    text = convert_from_pdf(input_file, logger)
                else:
                    # Should never happen, because format is checked beforehand
                    raise Exception(f"Unsupported file format: {file_extension}")
            except Exception as e:
                # catch exception to register it in span, then rethrow
                span.set_attributes({
                    "exception.message": str(e),
                    "exception.type": str(type(e)),
                    "exception.stacktrace": traceback.format_exc(),
                })
                span.set_status(SpanStatusCode.ERROR)
                raise

        logger.info(f"Conversion successful for file: {input_file}")
        successful_conversions.add(1, attributes=attributes)
        # _save_to_mongodb(mongo_collection, input_file, text)
        return text

    except Exception as e:
        # catch exception to log it and register failed conversion; then, rethrow
        logger.error(f"Error during conversion for file {input_file}: {str(e)}")
        failed_conversions.add(1, attributes=attributes)
        raise


def convert_from_pdf(input_file, logger):
    logger.info(f"Processing PDF file: {input_file}")
    with pdfplumber.open(input_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages])
    return text


def convert_from_tex(input_file, logger):
    logger.info(f"Processing LaTeX file: {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    main_content_match = re.search(r'\\begin{document}(.*?)\\end{document}', content, re.DOTALL)
    if main_content_match:
        text = main_content_match.group(1)
    else:
        raise ValueError("Could not find main content in the LaTeX file.")
    text = text.replace("\n", "")
    return text


def convert_from_docx(input_file, logger):
    logger.info(f"Processing DOCX file: {input_file}")
    text = docx2txt.process(input_file)
    return text
