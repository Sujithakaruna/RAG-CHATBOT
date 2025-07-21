from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import uuid

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION_NAME = "docs"

client = QdrantClient(":memory:")  # Use Qdrant local or memory

def init_qdrant():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )

def store_chunks(docs):
    points = []
    for i, doc in enumerate(docs):
        embedding = EMBED_MODEL.encode(doc["text"]).tolist()
        meta = {
            "filename": doc["filename"],
            "page": doc["page"],
            "chunk_id": i,
            "text": doc["text"]
        }
        points.append(models.PointStruct(id=uuid.uuid4().int >> 64, vector=embedding, payload=meta))
    client.upsert(collection_name=COLLECTION_NAME, points=points)
