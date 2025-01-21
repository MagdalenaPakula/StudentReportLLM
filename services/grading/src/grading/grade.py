import logging
import openai
import os

from grading.database.qdrant import client, collection_name

logger = logging.getLogger(__name__)

def save_to_qdrant(file_name, text, embedding):
    try:
        payload = {
            "points": [{
                "id": file_name,
                "vector": embedding,
                "payload": {"file_name": file_name, "text": text}
            }]
        }
        client.upsert(collection_name=collection_name, points=payload['points'])
        logger.info(f"Successfully saved {file_name} to Qdrant.")
    except Exception as e:
        logger.error(f"Error saving to Qdrant: {e}")

def generate_embedding(text):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY", "")
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise
