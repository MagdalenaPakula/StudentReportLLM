import logging
from qdrant_client import QdrantClient
from os import getenv

logger = logging.getLogger(__name__)

QDRANT_HOST = getenv('QDRANT_HOST')
QDRANT_PORT = getenv('QDRANT_PORT')

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

collection_name = "report_analysis"

try:
    client.get_collection(collection_name)
    logger.info(f"Connected to existing collection: {collection_name}")
except Exception:
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": 1536, "distance": "Cosine"}
    )
    logger.info(f"Created new collection: {collection_name}")

qdrant_collection = client.get_collection(collection_name)
