import os
import streamlit as st
from llama_cpp import Llama
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import numpy as np
import uuid
from PyPDF2 import PdfReader
import docx
LLM_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

COLLECTION_NAME = "rag_docs"
EMBED_DIM = 384
client = QdrantClient(":memory:")  # In-memory, use path= for persistent

# === MODEL LOADING ===
llm = Llama(
    model_path=LLM_PATH,
    n_ctx=2048,
    n_threads=4,
    n_gpu_layers=50,  # Keep small for T4
    verbose=False
)

# === HELPER FUNCTIONS ===

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+chunk_size]))
        i += chunk_size - overlap
    return chunks

def fake_embed(text):
    np.random.seed(abs(hash(text)) % (2**32))
    return np.random.rand(EMBED_DIM).tolist()

def init_collection():
    collections = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )

def add_to_qdrant(chunks):
    init_collection()
    points = [
        PointStruct(id=uuid.uuid4().int >> 64, vector=fake_embed(c), payload={"text": c})
        for c in chunks
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search_chunks(query, top_k=5):
    init_collection()
    query_vec = fake_embed(query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=top_k,
    )
    return [res.payload["text"] for res in results]

def generate_answer(context, query):
    prompt = f"""[INST] Use the below context to answer the question:

Context:
{context}

Question: {query}
[/INST]
"""
    output = llm(prompt, max_tokens=256)
    return output["choices"][0]["text"].strip()

# === STREAMLIT UI ===

st.title("🧠 RAG Chatbot - Offline & Lightweight")

uploaded_file = st.file_uploader("Upload PDF or Word File", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Processing document..."):
        text = extract_text(uploaded_file)
        if not text.strip():
            st.error("Failed to extract any text.")
        else:
            chunks = chunk_text(text)
            add_to_qdrant(chunks)
            st.success(f"Indexed {len(chunks)} chunks.")

query = st.text_input("Ask your question:")

if st.button("Ask") and query:
    with st.spinner("Searching..."):
        results = search_chunks(query)
        if not results:
            st.warning("❌ No matching content found. Try uploading documents or changing your question.")
        else:
            context = "\n\n".join(results)
            answer = generate_answer(context, query)
            st.markdown("### 📌 Answer:")
            st.write(answer)
            with st.expander("📄 Source Context"):
                st.write(context)
