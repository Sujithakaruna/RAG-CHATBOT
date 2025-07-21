import fitz  # PyMuPDF
import docx

def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texts = []
    for i, page in enumerate(doc):
        text = page.get_text()
        texts.append({"text": text, "page": i+1, "filename": file.name})
    return texts

def read_docx(file):
    doc = docx.Document(file)
    full_text = "\n".join([p.text for p in doc.paragraphs])
    return [{"text": full_text, "page": 1, "filename": file.name}]
