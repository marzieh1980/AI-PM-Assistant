# 🤖 AI PM Assistant

## 📌 Overview

This project is a Streamlit-based AI assistant for IT project managers and support teams.

It provides four powerful specialized tools:

* **Your Assistant** - A powerful AI chat that answers any question from general knowledge
* **Knowledge Hub** - Multi-turn Q&A with document search (infinite follow-up questions)
* **Meeting Assistant** - Automatic meeting note analysis with decision extraction
* **Risk Analyzer** - Project risk assessment with business impact analysis

All features powered by local LM Studio models with no external API calls needed.

---

## 🎯 Features

### 🤖 Your Assistant
* **Pure AI Chat** - Ask any question, get instant answers
* No document upload required
* Uses local LM Studio model for responses
* Works as a general knowledge AI assistant
* Single-turn interactions (ask question → get answer → clear)

### 📄 Knowledge Hub
* **Multi-Turn Q&A with Documents** - Upload and ask infinite questions
* Upload multiple `.txt` and `.pdf` documents
* **Conversation history** shows all Q&A pairs
* Ask follow-up questions in the same interface
* Smart text chunking (preserves small documents <2000 chars)
* Enhanced PDF extraction with `pdfplumber` for tables
* Embeddings with `all-MiniLM-L6-v2`
* FAISS similarity search (k=8 most relevant chunks)
* Info message when answer not found in document

### 📝 Meeting Assistant  
* Upload `.txt` or `.docx` meeting notes
* Automatic extraction of:
  * Participants list
  * Date & time of meeting
  * Meeting summary
  * Decisions made
  * Action items
* Follow-up questions appear **AFTER** summary is generated
* Clean button to refresh

### ⚠️ Risk Analyzer
* Analyzes `.txt` or `.docx` project documents
* Identifies key risks (Low / Medium / High)
* Assesses business impact and dependencies
* Professional markdown formatted output
* Clean button to refresh analysis

---

## 📁 Project Structure

```
rag-chatbot/
│
├── app.py              # Streamlit app with tabbed interface
├── rag_core.py         # RAG data loading, vector DB, and response pipeline
├── meeting_assistant.py# Meeting-note summarization logic
├── risk_analyzer.py    # Project risk analysis using LM Studio local API
├── data/               # Default knowledge base text and PDF files
├── data_meet-assistant/# Additional meeting data files
└── README.md
```

---

## 🔧 Dependencies

Install the required Python packages before running the app.

```bash
pip install streamlit langchain-community langchain-text-splitters faiss-cpu transformers torch pdfplumber requests python-docx
```

> If you use a GPU, install the matching `torch` package from the official PyTorch instructions.

---

## 🚀 Run Locally

1. Add `.txt` and `.pdf` documents to the `data/` folder for the default knowledge base.
2. Open **LM Studio**, load your model (e.g. `llama-3.2-3b-instruct`) and start the local server on `localhost:1234`.
3. Start the Streamlit app:

```bash
streamlit run app.py
```

4. Open the URL shown in the terminal, typically:

```bash
http://localhost:8501
```

---

## 🧩 How It Works

### RAG Assistant (Knowledge Hub)

1. `app.py` loads documents with `load_documents()` or `load_uploaded_documents()` from `rag_core.py`
2. For PDFs, `pdfplumber` extracts text with better table support than basic parsers
3. Documents are split into chunks with `RecursiveCharacterTextSplitter` (chunk_size=1000, overlap=200), except for small documents which remain whole
4. Embeddings are created using `HuggingFaceEmbeddings` with `all-MiniLM-L6-v2`
5. FAISS stores the vector embeddings for efficient similarity search
6. Query similarity search retrieves the top 8 most relevant excerpts
7. The retrieved context and question are sent to **LM Studio** via its OpenAI-compatible API (`POST /v1/chat/completions`)
8. The model generates an answer using only the retrieved context, following strict context-only instructions

### Meeting Assistant

1. Upload a `.txt` meeting notes file
2. `read_uploaded_file()` loads the text
3. `summarize_meeting()` cleans the notes and builds a prompt
4. The LM Studio local model returns a structured summary with key points, decisions, and action items

### Risk Analyzer

1. Input a project description via text area, or upload a `.txt` / `.docx` file
2. `analyze_risk()` builds a structured prompt for risk assessment
3. Sends a `POST` request to LM Studio's local API at `localhost:1234/v1/chat/completions`
4. Returns a structured report covering:
   - Key Risks (rated Low / Medium / High)
   - Business Impact
   - Dependencies
   - SLA Risks

---

## 📌 Usage Notes

* Supported document formats: `.txt` and `.pdf` for Knowledge Hub; `.txt` and `.docx` for Risk Analyzer
* PDF processing handles tables and structured content better with `pdfplumber`
* Meeting assistant expects plaintext meeting notes
* Both the Knowledge Hub and Risk Analyzer require **LM Studio** running with a loaded model and the local server started on `localhost:1234`
* The API used is OpenAI-compatible: `POST http://localhost:1234/v1/chat/completions`
* Responses are generated using only the provided document context (Knowledge Hub) or the project description (Risk Analyzer)
* If the context is insufficient, the RAG assistant returns:
  "I don't have enough information in the provided documents."
* The app does not require any external API key — all inference runs locally via LM Studio

---

## 💡 Example Use Cases

* Answering questions from internal IT documentation
* Finding process details from support knowledge files
* Summarizing meeting outcomes for project updates
* Extracting decisions and action items from notes
* Analyzing project risks and dependencies

---

## ⚠️ Known Limitations

* Only `.txt` files are supported for meeting notes
* The summarization model may require good input formatting
* Both the Knowledge Hub LLM and Risk Analyzer require LM Studio running on `localhost:1234` with a model loaded and server started
* No persistent database or long-term history storage is implemented
* The app loads embedding models at startup, so the first run may take longer

---

## 📎 Notes

This project is a proof of concept combining RAG, meeting-note summarization, and risk analysis for comprehensive project management support.

---
