from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

COLLECTION_NAME = "docs"
client = QdrantClient(":memory:")
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
LLM = Llama(model_path="models/your_llm_model.gguf", n_ctx=2048)

def search_docs(query):
    q_vec = EMBED_MODEL.encode(query).tolist()
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=q_vec,
        limit=5
    )
    return hits

def generate_answer(results, query):
    context = "\n".join([r.payload["text"] for r in results])
    prompt = f"""Use the below context to answer the user's question strictly from the documents.
    
### Context:
{context}

### Question:
{query}

### Answer:"""
    output = LLM(prompt, max_tokens=256)
    return output["choices"][0]["text"].strip()
