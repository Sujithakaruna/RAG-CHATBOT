
# 🤖 RAG Chatbot – Ask Questions Based on PDF and Word Documents

This project is a **RAG (Retrieval-Augmented Generation)** chatbot that answers your questions based on uploaded **PDF or Word documents**. It uses a local open-source LLM, performs chunk-based document retrieval, and runs efficiently on limited hardware (16GB GPU). It shows **exact citations** from the source documents to prevent hallucinations.

---

## ✅ Setup Instructions

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/RAG-CHATBOT.git
cd RAG-CHATBOT
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate     # On Windows
# OR
source venv/bin/activate  # On Mac/Linux
```

### 3. Install all required packages
```bash
pip install -r requirements.txt
```

### 4. Download and place the model
- Download a GGUF quantized model like `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
- Put it inside the `/models` folder

---

## 🚀 How to Use

1. Run the app:
```bash
streamlit run app.py
```

2. Upload `.pdf` or `.docx` documents
3. Ask questions related to the documents
4. The chatbot will respond with an **answer** and **exact source references**

---

## 🏗️ Architectural Decisions

- **Frontend**: Streamlit – simple and lightweight UI
- **LLM**: `mistral-7b-instruct` (quantized GGUF format run locally using llama-cpp)
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dim, fast and accurate)
- **Vector DB**: Qdrant – fast local vector search with persistent storage
- **File Parser**: `PyMuPDF` for PDFs, `python-docx` for Word files
- No external API, no LangChain – everything runs locally

---

## 🔍 Retrieval Approach

- Each document is split into **small chunks** (300–500 characters with 50-character overlap)
- Chunks are embedded using `sentence-transformers` MiniLM model
- Stored in **Qdrant** using cosine similarity
- On a question, top relevant chunks are retrieved (`top_k = 3`)
- Prompt is constructed using those chunks and fed to the LLM
- The final answer includes references to the source chunks/pages

---

## 🧩 Chunking Strategy

- **Chunk Size**: 300–500 characters
- **Overlap**: 50 characters
- This ensures no context is lost and sentences are not cut awkwardly
- Keeps memory usage low while preserving semantic meaning
- Optimized for retrieval accuracy and speed

---

## 👀 Observations

- Works well for clearly structured documents (e.g., reports, policies, manuals)
- Citation helps reduce hallucinations
- Handles both `.pdf` and `.docx` files
- Local LLM (Mistral) is powerful and runs well when quantized
- Retrieval can fail if document is very short or poorly structured
- Performance remains stable even on limited hardware

---

## 🖥️ Hardware Usage

- ✅ Designed to run on:
  - **GPU**: NVIDIA Tesla T4 (16 GB VRAM)
  - **RAM**: 16–32 GB
- **Model quantization** allows `Mistral 7B` to run within ~14 GB
- Embedding model (`MiniLM`) is lightweight and CPU-friendly
- Efficient enough for hackathons, local testing, and student projects

---

## 📂 Folder Structure

```
rag_chatbot_project/
│
├── app.py                  # Streamlit frontend
├── requirements.txt
├── README.md
├── models/                 # GGUF model files
├── vector_store/           # Qdrant local database
├── utils/
│   ├── chunking.py
│   ├── embedding.py
│   ├── pdf_docx_loader.py
│   └── retrieval.py
```

---

## 📘 Example

Uploaded Document: `health_policy.pdf`

**Question:** What is the maximum coverage mentioned?

**Answer:** The maximum coverage mentioned is ₹5 lakhs. (Source: Page 4)

---

## 📄 License

MIT License – free for personal, academic, and non-commercial use.

---

**✅ Built with love for offline, fast, and accurate document-based question answering.**
