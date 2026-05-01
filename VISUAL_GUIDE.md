# Visual Guide - AI PM Assistant UI 

## 🖥️ Main Interface Layout

```
┌──────────────────────────────────────── TITLE BAR ──────────────────────────────────────┐
│ 🤖 AI PM Assistant                                                                      │
│ Logged in as **john_doe** · Knowledge Hub · Meeting Assistant · Risk Analyzer · Assistant│
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┬────────────────────────────────────────────────────────────────────────┐
│    SIDEBAR      │                         MAIN CONTENT AREA                             │
│                 │                                                                        │
│ 🤖 AI PM        │  ┌─ 📄 KNOWL. ─┬─ 📝 MEETING ─┬─ ⚠️ RISK ─┬─ 🤖 ASST. ──┐        │
│ 👤 john_doe     │  │              │               │            │               │        │
│                 │  │              │               │            │               │        │
│ [⚙️][📚][🚪]    │  │  [Active]    │               │            │               │        │
│                 │  │              │               │            │               │        │
│ ─────────────   │  │  [Content]   │   [Content]   │ [Content] │  [Content]   │        │
│                 │  │              │               │            │               │        │
│ New Chat        │  │              │               │            │               │        │
│ [📄][📝][⚠️][🤖]│  │              │               │            │               │        │
│                 │  │  [Buttons]   │   [Buttons]   │[Buttons]  │  [Buttons]   │        │
│                 │  │              │               │            │               │        │
│ ─────────────   │  └─────────────┴───────────────┴────────────┴───────────────┘        │
│                 │                                                                        │
│ 🤖 Your Asst.   │                                                                        │
│ Chats:          │                                                                        │
│ ▶ Q2 Budget     │                                                                        │
│   Security      │                                                                        │
│   Project Risks │                                                                        │
│                 │                                                                        │
│ [✕][✕][✕]      │                                                                        │
│                 │                                                                        │
└─────────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

## 📄 Tab 1: Knowledge Hub

```
┌────────────────────────────────────────────────────────────┐
│ 📄 KNOWLEDGE HUB                                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ UPLOAD DOCUMENTS                                          │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ 📂 Upload one or more .txt or .pdf documents to     │  │
│ │ build your knowledge base.                          │  │
│ │ Once uploaded, go to "Your Assistant" tab to ask   │  │
│ │ questions about your documents.                     │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ [Choose file]              [Choose file]            │  │
│ │ sla_policy.txt                                       │  │
│ │ kb_risk_analyzer.txt                                 │  │
│ │ (2 files uploaded)                                   │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ [✅ Load documents into Your Assistant]  [🧹 Clean]      │
│                                                            │
│ ✅ Active documents in Your Assistant:                    │
│    sla_policy.txt, kb_risk_analyzer.txt                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 📝 Tab 2: Meeting Assistant

```
┌────────────────────────────────────────────────────────────┐
│ 📝 MEETING ASSISTANT                                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ UPLOAD MEETING NOTES                                      │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ 📋 Upload a .txt or .docx meeting notes file.       │  │
│ │ The assistant will extract key information          │  │
│ │ including participants, date/time, summary,         │  │
│ │ decisions, and action items.                        │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ [Choose file]                                        │  │
│ │                                                      │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ [📝 Analyze Meeting]   [🧹 Clean]                         │
│                                                            │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ ### 📋 Meeting Analysis                              │  │
│ │                                                      │  │
│ │ List of participants:                                │  │
│ │ - Marco Rossi (PM)                                   │  │
│ │ - Laura Bianchi (Dev)                                │  │
│ │ - Paolo Verdi (QA)                                   │  │
│ │                                                      │  │
│ │ Date & time of call:                                 │  │
│ │ - April 20, 2024 - 14:00 CET                         │  │
│ │                                                      │  │
│ │ Summary of call:                                     │  │
│ │ - Discussed Q2 release timeline                      │  │
│ │ - Database optimization reviewed                     │  │
│ │ - Testing strategy updated                           │  │
│ │                                                      │  │
│ │ Decisions Made:                                      │  │
│ │ - Release postponed to May 15                        │  │
│ │ - Database refactoring approved                      │  │
│ │ - New QA process implemented                         │  │
│ │                                                      │  │
│ │ Action Items:                                        │  │
│ │ - Complete database migration - Laura                │  │
│ │ - Update test cases - Paolo                          │  │
│ │ - Schedule stakeholder review - Marco                │  │
│ │                                                      │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Tab 3: Risk Analyzer

```
┌────────────────────────────────────────────────────────────┐
│ ⚠️ RISK ANALYZER                                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ UPLOAD PROJECT DOCUMENT                                   │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ 📁 Upload a .txt or .docx project description.      │  │
│ │ The assistant will identify risks, impacts,         │  │
│ │ dependencies and scenarios.                         │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ [Choose file]      ✅ Loaded: project_plan.docx    │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ [🔍 Analyze Risks]   [🧹 Clean]                           │
│                                                            │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ ### 📊 Risk Analysis Report                           │  │
│ │                                                      │  │
│ │ **Key Risks**                                        │  │
│ │ • Data Integration: Medium - API connectivity       │  │
│ │ • Resource Availability: High - Allocation issues   │  │
│ │                                                      │  │
│ │ **Business Impact**                                  │  │
│ │ • 3-week delay = €50K penalty                        │  │
│ │ • 15% customer satisfaction drop                     │  │
│ │                                                      │  │
│ │ **Dependencies**                                     │  │
│ │ • Third-party API                                    │  │
│ │ • Cloud infrastructure                               │  │
│ │ • Contractor availability                            │  │
│ │                                                      │  │
│ │ [... more content ...]                               │  │
│ │                                                      │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🤖 Tab 4: Your Assistant

```
┌────────────────────────────────────────────────────────────┐
│ 🤖 YOUR ASSISTANT                                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ CHAT — NAME & COPILOT PROMPT                             │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ Name: [Q2 Budget Analysis          ]                │  │
│ │ Saved Prompts: [— type a custom prompt —  ▼]        │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ Copilot prompt:                                           │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ You are a financial expert. Analyze every statement │  │
│ │ for costs and opportunities. Use technical terms.   │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ [💾 Save prompt to library]                               │
│                                                            │
│ ───────────────────────────────────────────────────────   │
│                                                            │
│ CHAT HISTORY:                                             │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ 🧑 You: What's our total Q2 budget?                 │  │
│ │                                                      │  │
│ │ 🤖 Assistant: According to the budget document,     │  │
│ │    our Q2 allocated budget is €200K, broken down    │  │
│ │    as:                                               │  │
│ │    - Product: €120K (60%)                           │  │
│ │    - Operations: €50K (25%)                         │  │
│ │    - Contingency: €30K (15%)                        │  │
│ │                                                      │  │
│ │ 🧑 You: What's the largest expense?                 │  │
│ │                                                      │  │
│ │ 🤖 Assistant: The largest expense is Product        │  │
│ │    development at €120K (60% of total budget),      │  │
│ │    covering...                                       │  │
│ │                                                      │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                            │
│ Ask a question about your documents...                    │
│ ┌─────────────────────────────────────────────────────┐   │
│ │ [What are the cost optimization opportunities?]    │   │
│ │                                    [Send ▶][🗑️Clear]│   │
│ └─────────────────────────────────────────────────────┘   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 Sidebar - In Detail

### Top Controls (Always Visible)
```
🤖 AI PM
👤 john_doe

[⚙️]  [📚]  [🚪]
 │     │     └─ Logout
 │     └─ Prompt Library
 └─ Settings

⚙️ Settings (when clicked):
LM Studio model: [llama-3.2-3b-instruct:2]
Font size:       [15 px]  [slider]
Accent color:    [color picker]
Sidebar color:   [color picker]
[💾 Save settings]

──────────────────────────
```

### New Chat Area
```
New Chat
[📄]  [📝]  [⚠️]  [🤖]
 │     │     │     └─ New Assistant Chat
 │     │     └─ New Risk Chat
 │     └─ New Meeting Chat
 └─ New Knowledge Chat

If clicked, inline form appears:
#### ➕ New Assistant Chat
Chat name (optional):
[Enter chat name...]

Copilot prompt (optional):
┌─────────────────────┐
│ Custom instructions │
│ for this chat...    │
└─────────────────────┘

[✅ Create]  [✕ Cancel]

──────────────────────────
```

### Your Assistant Chats
```
🤖 Your Assistant Chats
▶ Q2 Budget Analysis    [✕]
  Security Policy      [✕]
  Product Requirements [✕]
  Meeting Notes - Apr  [✕]

Legend:
▶ = Currently active chat
[✕] = Delete button
Hover to see full name if truncated

──────────────────────────
```

---

## 🖱️ Button Reference

### Knowledge Hub
```
[✅ Load documents into Your Assistant]
├─ Green button
├─ Icon: Checkmark
├─ Action: Loads docs into vector DB
└─ Result: Docs ready in Your Assistant

[🧹 Clean]
├─ Button
├─ Icon: Broom
├─ Action: Clears documents
└─ Result: Vector DB cleared
```

### Meeting Assistant
```
[📝 Analyze Meeting]
├─ Icon: Document
├─ Action: Extracts meeting info
└─ Result: Shows in text area

[🧹 Clean]
├─ Icon: Broom
├─ Action: Clears analysis
└─ Result: Fresh start
```

### Risk Analyzer
```
[🔍 Analyze Risks]
├─ Icon: Magnifying glass
├─ Action: Analyzes document
└─ Result: Shows risk report

[🧹 Clean]
├─ Icon: Broom
├─ Action: Clears analysis
└─ Result: Fresh start
```

### Your Assistant Chat
```
[Send ▶]
├─ Icon: Arrow
├─ Action: Send message
└─ Result: Gets AI response

[🗑️ Clear]
├─ Icon: Trash
├─ Action: Clears chat history
└─ Result: Messages deleted

[💾 Save prompt to library]
├─ Icon: Save
├─ Action: Saves current prompt
└─ Result: Available for future chats
```

### Sidebar
```
[⚙️] Settings
├─ Icon: Gear
├─ Action: Opens settings panel
└─ Toggles on/off

[📚] Prompts
├─ Icon: Books
├─ Action: Opens prompt library
└─ Toggles on/off

[🚪] Logout
├─ Icon: Door
├─ Action: Logs out user
└─ Clears session

[📄][📝][⚠️][🤖] New Chat
├─ Icons: Tab icons
├─ Action: Shows new chat form
└─ One per tab type
```

---

## 📊 Status Messages

### Success
```
✅ Active documents: sla_policy.txt, kb_risk.txt
✅ Loaded: meeting_notes.docx
✅ Status message displays in green
```

### Error
```
❌ Upload documents first.
❌ LM Studio not running
❌ Error messages display in red
```

### Warning
```
⚠️ Upload a document first
⚠️ Yellow messages for caution
```

### Info
```
ℹ️ Create new Knowledge chat first
👈 Use the 📄 button in sidebar
```

---

## ⏳ Loading States

```
While processing:
⏳ Loading...
🔄 Thinking...
⏸️ Analyzing...
⏱️ Summarizing...

Shows spinner and message
```

---

## 🎨 Color Scheme

Default:
- Accent: `#4F8EF7` (Blue)
- Sidebar: `#1C2333` (Dark Gray)
- Text: Light gray
- Links: Blue (accent color)

Customizable:
- Change accent color in Settings
- Change sidebar color in Settings
- Font size: 12-22px

---

## 📱 Responsive Behavior

```
Desktop (1200px+):
├─ Sidebar: 250px fixed left
├─ Content: Full width
└─ Columns: Full layout

Tablet (800px-1200px):
├─ Sidebar: Collapsible or fixed
├─ Content: Responsive
└─ Columns: 2-col fallback

Mobile (<800px):
├─ Sidebar: Hidden/drawer
├─ Content: Full width
└─ Columns: Stack vertically
```

---

**Last Updated**: April 24, 2026
**Version**: 2.0
