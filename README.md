# 🤖 AI PM Assistant

A powerful Streamlit-based AI assistant for project managers with task extraction, effort estimation, and intelligent document analysis.

---

## 🎯 Features

### 📄 **Knowledge Hub** - Document Q&A
- Upload `.txt` or `.pdf` documents
- Ask unlimited follow-up questions
- Conversation history shows all Q&A pairs
- Get "Not found" message if answer not in document

### 📋 **Task & Effort Planner** - Extract & Estimate
- Upload project description (`.txt`)
- Automatically extract tasks with priorities
- Estimate effort for each task
- Download results as Excel files
- Get actionable project breakdown

### 📝 **Meeting Assistant** - Meeting Analysis
- Upload meeting notes (`.txt` or `.docx`)
- Auto-extract: Participants, Summary, Decisions, Action Items
- Ask follow-up questions about the meeting
- Get structured meeting insights

### ⚠️ **Risk Analyzer** - Risk Assessment
- Upload project document (`.txt` or `.docx`)
- Identify risks (Low/Medium/High)
- Assess business impact and dependencies
- Professional structured output

### 🤖 **Your Assistant** - General AI Chat
- Ask any question without documents
- Get instant AI answers from local model
- Simple, stateless chat interface

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install streamlit langchain-community langchain-text-splitters faiss-cpu transformers torch pdfplumber requests python-docx
```

### 2. Setup LM Studio
- Download [LM Studio](https://lmstudio.ai)
- Load a model (e.g., `llama-3.2-3b-instruct:2`)
- Start server on `localhost:1234`

### 3. Run the App
```bash
streamlit run app.py
```

Open: `http://localhost:8501`

---

## 📊 How to Use Each Tab

| Tab | Use Case | Steps |
|-----|----------|-------|
| 📄 Knowledge Hub | Document Q&A | 1. Upload docs → 2. Ask questions → 3. Keep asking follow-ups |
| 📋 Task Planner | Plan projects | 1. Upload description → 2. Generate tasks → 3. Estimate effort → 4. Download Excel |
| 📝 Meeting Assistant | Analyze meetings | 1. Upload notes → 2. Get summary → 3. Ask follow-ups |
| ⚠️ Risk Analyzer | Risk assessment | 1. Upload document → 2. Analyze risks → 3. Review report |
| 🤖 Your Assistant | General questions | 1. Type question → 2. Get answer |

---

## 💾 Project Structure

```
AI-PM-Assistant/
├── app.py                    # Main Streamlit application
├── rag_core.py              # Document search & embedding
├── meeting_assistant.py     # Meeting analysis logic
├── task_extractor.py        # Task extraction
├── effort_estimator.py      # Effort estimation
├── risk_analyzer.py         # Risk analysis
├── storage.py               # Database (SQLite)
├── sample_data/             # Example files
└── README.md                # This file
```

---

## ⚙️ Settings

Access via ⚙️ button in sidebar:

- **LM Studio Model**: Change model name
- **Font Size**: Adjust text (12-22px)
- **Accent Color**: Theme color
- **Sidebar Color**: Sidebar background

---

## 🔧 Configuration

**Model**: Works with any LM Studio compatible model  
**API**: OpenAI-compatible API on `localhost:1234`  
**Database**: SQLite (auto-created)  
**Vector DB**: In-memory FAISS (session-based)

---

## 📝 File Support

| Feature | .txt | .pdf | .docx |
|---------|------|------|-------|
| Knowledge Hub | ✅ | ✅ | ❌ |
| Task Planner | ✅ | ❌ | ❌ |
| Meeting Assistant | ✅ | ❌ | ✅ |
| Risk Analyzer | ✅ | ❌ | ✅ |

---

## 🐛 Troubleshooting

**"Cannot connect to localhost:1234"**
- Make sure LM Studio is running and server is started

**"No documents uploaded"**
- Upload files first before asking questions

**"Streamlit keeps rerunning"**
- This is normal - just wait for the operation to complete

---

## 📄 Additional Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick how-to guide for each feature
- **[USAGE_EXAMPLES_v3.md](USAGE_EXAMPLES_v3.md)** - Real-world scenarios

---

## 📦 Dependencies

- **streamlit** - Web UI framework
- **langchain** - LLM orchestration
- **faiss-cpu** - Vector search
- **transformers** - NLP models
- **pdfplumber** - PDF extraction
- **python-docx** - DOCX handling

---

## 📅 Version

**v3.0** - Streamlined & optimized for task extraction and effort estimation

---

## 📞 Support

For issues or questions, check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

