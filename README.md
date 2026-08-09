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

### 2. Setup Ollama
- Download [Ollama](https://ollama.ai)
- Pull a model: `ollama pull mistral` or `ollama pull llama2`
- Start server: `ollama serve` (runs on `localhost:11434`)

### 3. Run the App
```bash
streamlit run app.py
```

Open: `http://localhost:8501`

---

## 🐳 Docker
Build the container and run the app locally:

```bash
docker build -t ai-pm-assistant .
docker run --rm -p 8501:8501 ai-pm-assistant
```

Then open: `http://localhost:8501`

---

## ▶️ Run (commands)

Install dependencies:
```bash
pip install -r requirements.txt
```

Start normally (creates local SQLite `aipm_data.db`):
```bash
streamlit run app.py
```

Start without creating a DB file (in-memory only):

PowerShell:
```powershell
$env:AIPM_PERSISTENCE = 'false'
streamlit run app.py
```

macOS / Linux (bash):
```bash
export AIPM_PERSISTENCE=false
streamlit run app.py
```

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
├── rag_core.py               # Document search & embedding
├── meeting_assistant.py      # Meeting analysis logic
├── task_extractor.py         # Task extraction
├── effort_estimator.py       # Effort estimation
├── risk_analyzer.py          # Risk analysis
├── storage.py                # Local persistence (SQLite file: aipm_data.db)
├── sample_data/              # Example files
└── README.md                 # This file
```

---

## ⚙️ Settings

Access via ⚙️ button in sidebar:

- **Model**: Change model name
- **Font Size**: Adjust text (12-22px)
- **Accent Color**: Theme color
- **Sidebar Color**: Sidebar background

---

## 🔧 Configuration

**Model**: Works with any Ollama compatible model  
**API**: Native Ollama API on `localhost:11434`  
**Database**: SQLite (auto-created)  
**Vector DB**: In-memory FAISS (session-based)

**Optional (No DB file)**: To run the app without creating a local DB file, start the app with the environment variable `AIPM_PERSISTENCE=false`. This runs an in-memory SQLite DB for the process only (no file is created). Example (Windows PowerShell):

```powershell
$env:AIPM_PERSISTENCE = 'false'
streamlit run app.py
```

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

**"Cannot connect to localhost:11434"**
- Make sure Ollama is running: `ollama serve`

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

