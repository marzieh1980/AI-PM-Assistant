# rag_core.py

import os
import requests
from langchain_community.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pdfplumber

# -------------------------
# LOAD DOCUMENTS
# -------------------------
def load_documents(folder_path="data"):
    documents = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return documents
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())
        elif file_name.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                content = ""
                for page in pdf.pages:
                    content += page.extract_text() + "\n"
            documents.append(Document(page_content=content, metadata={"source": file_name}))
    return documents

# -------------------------
# LOAD UPLOADED DOCUMENTS
# -------------------------
def load_uploaded_documents(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        uploaded_file.seek(0)
        if uploaded_file.name.endswith(".txt"):
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            documents.append(Document(page_content=content, metadata={"source": uploaded_file.name}))
        elif uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                content = ""
                for page in pdf.pages:
                    content += page.extract_text() + "\n"
            documents.append(Document(page_content=content, metadata={"source": uploaded_file.name}))
        uploaded_file.seek(0)
    return documents

# -------------------------
# CREATE VECTOR DB
# -------------------------
def create_vector_db(documents):
    if not documents:
        return None
    # If single small document, don't split
    if len(documents) == 1 and len(documents[0].page_content) < 2000:
        docs = documents
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    return db

# -------------------------
# ANSWER WITH OLLAMA (free, local)
# -------------------------
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
LM_STUDIO_MODEL = "llama-3.2-3b-instruct:2"

def answer_question(context, question):
    prompt = f"""You are an expert IT support assistant. Answer using ONLY the provided context...

Context:
{context}

Question:
{question}

Answer:"""

    try:
        response = requests.post(LM_STUDIO_URL, json={
            "model": LM_STUDIO_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }, timeout=120)
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
        if not answer or len(answer) < 10:
            return "I don't have enough information in the provided documents to answer this question."
        return answer
    except requests.exceptions.ConnectionError:
        return "❌ LM Studio is not running or local server is not started."
    except Exception as e:
        return f"❌ Error contacting LM Studio: {str(e)}"

# -------------------------
# PIPELINE (🔥 FIX IMPORTANTE)
# -------------------------
def ask_rag(db, query):
    docs_found = db.similarity_search(query, k=8)

    # 🔴 CONTROLLO FORTE
    if not docs_found:
        return "I don't have enough information in the provided documents."

    context = "\n\n---\n\n".join([
        f"[From: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}" 
        for doc in docs_found
    ])

    # Check if context is substantial enough
    if len(context.strip()) < 50:
        return "I don't have enough information in the provided documents to answer this question."

    response = answer_question(context, query)
    return response