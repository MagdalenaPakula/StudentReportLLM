from qdrant_client import QdrantClient
from os import getenv

client = QdrantClient(host=getenv('QDRANT_HOST'), port=getenv('QDRANT_PORT'))

collection_name = "report_analysis"

try:
    client.get_collection(collection_name)
except Exception:
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "size": 1536, 
            "distance": "Cosine"
        }
    )

qdrant_collection = client.get_collection('report_analysis')
