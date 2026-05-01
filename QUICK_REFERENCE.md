# Quick Reference - Updated AI PM Assistant v3.0

## 🎯 How to Use Each Tab

### 1️⃣ Your Assistant (🤖) - Pure AI Chat
```
1. Open "Your Assistant" tab
2. Type any question in the text box
3. Click "🔍 Send"
4. Get instant AI answer (no documents needed)
5. Click "🧹 Clear" to clear the answer and start fresh
```
**Best for**: Quick questions, general knowledge, brainstorming

### 2️⃣ Knowledge Hub (📄) - Multi-Turn Document Q&A
```
1. Upload .txt or .pdf documents
2. You'll see uploaded file names and conversation history
3. Type your first question in the text box
4. Click "Search 🔍"
5. Get answer from document
6. **Continue asking follow-up questions** in the same box
7. ALL previous Q&A pairs stay visible in history
8. Use "🧹 Clean" to clear everything and start over
```
**Features**:
- ✅ Conversation history shows all questions and answers
- ✅ Ask as many follow-up questions as you want
- ✅ Message "ℹ️ No information found in the document" if answer not found
- ✅ Smart document chunking (preserves context)

### 3️⃣ Meeting Assistant (📝) - Meeting Analysis
```
1. Upload .txt or .docx meeting notes
2. You'll see "✅ Loaded: [filename]" message
3. Click "📝 Summary of Meeting"
4. Review the extracted summary
5. **AFTER summary appears**, follow-up section shows below
6. Ask follow-up questions if needed
7. Click "🧹 Clean" to refresh
```
**Auto-Extracts**:
- ✅ Participants
- ✅ Date & time of meeting
- ✅ Meeting summary
- ✅ Decisions made
- ✅ Action items

### 4️⃣ Risk Analyzer (⚠️) - Project Risk Assessment
```
1. Upload .txt or .docx project document
2. Click "🔍 Analyze Risks"
3. Review risk report with:
   - Key Risks (Low/Medium/High)
   - Business Impact
   - Dependencies
   - Professional formatted output
4. Use "🧹 Clean" to refresh analysis
```

---

## 📋 Sidebar Structure

```
🤖 AI PM
👤 [username]

[⚙️ Settings] [📚 Prompts] [🚪 Logout]

⚙️ Settings Panel (when toggled)
  - LM Studio model selection
  - Font size adjustment
  - Accent color picker
  - Sidebar color picker

📚 Prompt Library (when toggled)
  - Saved prompts for each tab
  - Save/Edit/Delete prompts
```

**Note**: Your Assistant now uses stateless chat (simpler interface, no saved chats)

---

## 🖱️ Control Buttons

| Button | Function | Location | Error Fix |
|--------|----------|----------|----------|
| 🔍 Send | Send question to AI | Your Assistant tab | ✅ No errors |
| 🧹 Clear | Clear answer | Your Assistant tab | ✅ No errors |
| Search 🔍 | Ask document question | Knowledge Hub | ✅ No errors |
| 🧹 Clean | Clear all docs & history | Knowledge Hub | ✅ No errors |
| 📝 Summary of Meeting | Analyze meeting | Meeting Assistant | ✅ No errors |
| Search 🔍 (Follow-up) | Ask follow-up (after summary) | Meeting Assistant | ✅ No errors |
| 🧹 Clean | Clear meeting data | Meeting Assistant | ✅ No errors |
| 🔍 Analyze Risks | Get risk report | Risk Analyzer | ✅ No errors |
| 🧹 Clean | Clear analysis | Risk Analyzer | ✅ No errors |

---

## 💾 Your Assistant (Stateless Chat)

Your Assistant now operates as a **stateless, single-turn chat**:
- Type question → Get answer → Clear to start fresh
- No saved chat history
- No sidebar chat list
- Simpler, cleaner interface
- Perfect for quick questions

**For document conversations**: Use **Knowledge Hub** instead, which maintains full conversation history!

---

## 📄 Supported File Formats

| Feature | .txt | .pdf | .docx |
|---------|------|------|-------|
| Knowledge Hub | ✅ | ✅ | ❌ |
| Meeting Assistant | ✅ | ❌ | ✅ |
| Risk Analyzer | ✅ | ❌ | ✅ |

---

## ⚠️ Important Notes

✅ **RAG-Based**: Your Assistant only answers from documents you upload
- If information isn't in docs, it will say: "I don't have enough information in the provided documents"
- No hallucinations or made-up answers

✅ **Document Storage**: 
- Documents are stored in-memory (vector DB not saved)
- Your chat history IS saved to database
- Always keep original documents if you need them later

✅ **Meeting Analysis**:
- Automatically removes timestamps and speaker names
- Extracts key information
- Summarizes without copying original text

✅ **Risk Analysis**:
- Provides comprehensive scenario planning
- Identifies uncertainties and assumptions
- Professional, structured output

---

## 🔧 Settings

Access via ⚙️ button in sidebar:

- **LM Studio Model**: Model name (default: "llama-3.2-3b-instruct:2")
- **Font Size**: Adjust text size (12-22px)
- **Accent Color**: Theme color picker
- **Sidebar Color**: Sidebar background color

All settings save to your profile!

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Upload documents and click Load first" | Go to Knowledge Hub, upload files, click "Load documents..." |
| "I don't have enough information" | Document doesn't contain answer. Try asking differently or upload different docs |
| "LM Studio not running" | Start LM Studio server on localhost:1234 |
| Chat disappeared | Check sidebar - it may be filtered by tab or deleted |

---

## 🎨 Customization Tips

1. **Custom Prompts**: Add specialized instructions when creating chats
   - "You are a security expert..."
   - "Focus on cost-effectiveness..."
   - "Use technical jargon..."

2. **Save Prompt Templates**: Use Prompt Library (📚) to save reusable prompts

3. **Organize Chats**: Name chats meaningfully
   - "Q3 Budget Analysis"
   - "Security Audit - May 2024"
   - "Release Planning"

---

**Last Updated**: April 24, 2026
**Version**: 2.0 (Architecture Redesigned)
