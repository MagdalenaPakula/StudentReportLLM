from qdrant_client import QdrantClient

qdrant_client = QdrantClient(host="localhost", port=6333)
qdrant_collection = qdrant_client.get_collection("report_analysis")