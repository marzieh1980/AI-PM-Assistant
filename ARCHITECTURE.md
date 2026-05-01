# Architecture Diagram - Updated AI PM Assistant

## System Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AI PM ASSISTANT - MAIN INTERFACE                 │
├──────────────────┬────────────────────────────────────────────────────┤
│   SIDEBAR        │         TABS (4 Sections)                         │
│                  │                                                    │
│  🤖 AI PM        │  ┌──────────────────────────────────────────────┐ │
│  👤 username     │  │ 📄 KNOWLEDGE  │ 📝 MEETING  │ ⚠️ RISK │ 🤖  │
│                  │  │    HUB        │ ASSISTANT   │ANALYZER │ASSIST│
│  ⚙️️⚙  Settings  │  │               │             │         │      │
│  📚 Prompts      │  │               │             │         │      │
│  🚪 Logout       │  │     [TAB 1]   │   [TAB 2]   │ [TAB 3] │[TAB4]│
│                  │  │               │             │         │      │
│  ───────────────  │  └──────────────────────────────────────────────┘
│                  │
│  New Chat        │
│  [📄][📝][⚠️][🤖]│
│                  │
│  ───────────────  │
│                  │
│  🤖 Assistant    │
│     Chats        │
│  ▶ Chat 1    [✕] │
│    Chat 2    [✕] │
│    Chat 3    [✕] │
│                  │
└──────────────────┴────────────────────────────────────────────────────┘
```

---

## Tab 1: Knowledge Hub (📄)

```
┌─────────────────────────────┐
│   📄 KNOWLEDGE HUB          │
├─────────────────────────────┤
│                             │
│  Upload documents           │
│  [.txt, .pdf]               │
│                             │
│  ┌───────────────────────┐  │
│  │  File Upload Area     │  │
│  │  Drag & drop or click │  │
│  └───────────────────────┘  │
│                             │
│  [✅ Load into Assistant]   │
│  [🧹 Clean]                 │
│                             │
│  ✅ Status message          │
│                             │
└─────────────────────────────┘
        ⬇ LOADS INTO
┌─────────────────────────────┐
│ Tab 4: Your Assistant (🤖) │
│ (documents ready to chat)   │
└─────────────────────────────┘
```

---

## Tab 2: Meeting Assistant (📝)

```
┌─────────────────────────────┐
│  📝 MEETING ASSISTANT       │
├─────────────────────────────┤
│                             │
│  Upload meeting notes       │
│  [.txt, .docx]              │
│                             │
│  ┌───────────────────────┐  │
│  │  File Upload Area     │  │
│  │  (.txt or .docx)      │  │
│  └───────────────────────┘  │
│                             │
│  [📝 Analyze Meeting]       │
│  [🧹 Clean]                 │
│                             │
│  ┌───────────────────────┐  │
│  │ Meeting Analysis      │  │
│  │ - Participants        │  │
│  │ - Date & Time         │  │
│  │ - Summary             │  │
│  │ - Decisions           │  │
│  │ - Action Items        │  │
│  └───────────────────────┘  │
│                             │
└─────────────────────────────┘
```

---

## Tab 3: Risk Analyzer (⚠️)

```
┌─────────────────────────────┐
│  ⚠️ RISK ANALYZER           │
├─────────────────────────────┤
│                             │
│  Upload project document    │
│  [.txt, .docx]              │
│                             │
│  ┌───────────────────────┐  │
│  │  File Upload Area     │  │
│  │  (.txt or .docx)      │  │
│  └───────────────────────┘  │
│                             │
│  [🔍 Analyze Risks]         │
│  [🧹 Clean]                 │
│                             │
│  ┌───────────────────────┐  │
│  │ Risk Analysis Report  │  │
│  │ • Key Risks           │  │
│  │ • Business Impact     │  │
│  │ • Dependencies        │  │
│  │ • SLA Risks           │  │
│  │ • Scenarios           │  │
│  │ • Assumptions         │  │
│  └───────────────────────┘  │
│                             │
└─────────────────────────────┘
```

---

## Tab 4: Your Assistant (🤖)

```
┌──────────────────────────────┐
│  🤖 YOUR ASSISTANT           │
├──────────────────────────────┤
│                              │
│  [Chat Name Input]           │
│  [Copilot Prompt Area]       │
│                              │
│  ┌────────────────────────┐  │
│  │  Chat History          │  │
│  │  🧑 User: "How to..."  │  │
│  │  🤖 Bot: "Based on..." │  │
│  │  🧑 User: "Next Q..."  │  │
│  │  🤖 Bot: "Answer..."   │  │
│  └────────────────────────┘  │
│                              │
│  [Chat Input Box]            │
│  [Send ▶]  [🗑️ Clear]       │
│                              │
│  Messages:                   │
│  - Saved to database         │
│  - Accessible from sidebar   │
│  - Can be renamed/deleted    │
│                              │
└──────────────────────────────┘
```

---

## Data Flow

### Upload → Chat Workflow

```
┌─────────────────┐
│  Upload Docs    │
│  (Knowledge Hub)│
└────────┬────────┘
         │
         └──→ Load Documents
              │
              ├──→ Create Vector DB (FAISS)
              │   (Embeddings)
              │
              └──→ Store in "Your Assistant"
                   Chat Object
                   │
                   ├── uploaded_files: [list]
                   ├── upload_db: [vector_db]
                   └── messages: []
                        │
                        └──→ Ready to Chat
                             │
                             ├── User: Question
                             │
                             ├── RAG Query:
                             │   similarity_search(question, k=8)
                             │
                             ├── Context: Top 8 matches
                             │
                             ├── LM Studio:
                             │   Generate answer with context
                             │
                             └── Bot: Answer
```

---

## Database Schema (Updated)

```
users
├── id (PK)
├── username (UNIQUE)
├── password_hash
└── created_at

user_settings
├── user_id (FK, PK)
├── model_name
├── font_size
├── accent_color
└── sidebar_color

chats
├── id (PK)
├── user_id (FK)
├── tab ◄── NOW INCLUDES: "knowledge", "meeting", "risk", "assistant"
├── name
├── system_prompt
├── created_at
└── updated_at

messages
├── id (PK)
├── chat_id (FK)
├── role (user/bot)
├── text
└── created_at

uploaded_files
├── id (PK)
├── chat_id (FK)
└── filename

prompts
├── id (PK)
├── user_id (FK)
├── tab ◄── Now used for all tabs
├── name
├── prompt_text
├── created_at
└── updated_at
```

---

## Processing Pipeline

### Knowledge Hub → RAG Chat
```
Document Upload
    ↓
Text Extraction (.txt, .pdf)
    ↓
Text Splitting (1000 tokens, 200 overlap)
    ↓
Embeddings (all-MiniLM-L6-v2)
    ↓
Vector DB (FAISS) - In Memory
    ↓
Store Reference in Chat
    ↓
User Question
    ↓
Query Vector DB (k=8 similar docs)
    ↓
Retrieve Context
    ↓
Prompt LM Studio with context
    ↓
Generate Answer
    ↓
Chat Display
```

### Meeting Analysis
```
File Upload (.txt, .docx)
    ↓
Text Extraction
    ↓
Clean Text (remove timestamps, names)
    ↓
Flan-T5 Model Process
    ↓
Extract:
  - Participants
  - Date & Time
  - Summary
  - Decisions
  - Action Items
    ↓
Display Results
```

### Risk Analysis
```
File Upload (.txt, .docx)
    ↓
Text Extraction
    ↓
LM Studio Analysis
    ↓
Generate Report:
  - Key Risks
  - Impact
  - Dependencies
  - Scenarios
  - Assumptions
    ↓
Format Output
    ↓
Display Results
```

---

## File Structure

```
AI PM Assistant/
├── app.py                    ◄── MAIN APP (Streamlit)
├── meeting_assistant.py      ◄── Meeting extraction
├── risk_analyzer.py          ◄── Risk analysis
├── rag_core.py              ◄── RAG pipeline
├── storage.py               ◄── Database (SQLite)
├── aipm_data.db             ◄── Data storage
├── UPDATES_SUMMARY.md       ◄── NEW - Change log
├── QUICK_REFERENCE.md       ◄── NEW - User guide
└── old/
    └── [previous versions]
```

---

## Session State Management

```
st.session_state
├── user: {id, username}
├── chat_list: [chat_dicts]
├── active_chat_id: "uuid"
├── show_settings: bool
├── show_prompt_lib: bool
├── edit_prompt_id: "uuid"
├── new_chat_tab: "assistant"|"knowledge"|"meeting"|"risk"
├── meeting_output: str          ◄── NEW
├── risk_output: str             ◄── NEW
├── model_name: str
├── font_size: int
├── accent_color: str
└── sidebar_color: str
```

---

**Architecture Version**: 2.0
**Last Updated**: April 24, 2026
