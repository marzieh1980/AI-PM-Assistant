# FAQ & Troubleshooting Guide

## ❓ Frequently Asked Questions

### General Questions

**Q: What's the main difference from the old version?**
A: The app now has 4 tabs instead of 3. Tab 1 (Knowledge Hub) uploads documents, Tab 4 (Your Assistant) is where you chat with them. Tabs 2 & 3 are standalone analysis tools without embedded chats.

**Q: Do I need to keep uploading documents every time?**
A: No! Go to Knowledge Hub → upload once → load into Your Assistant. Your chats are saved in the sidebar. Documents stay in the vector DB until you click "Clean".

**Q: Can I use multiple documents?**
A: Yes! Upload as many `.txt` or `.pdf` files as you want to the Knowledge Hub. They get combined into one knowledge base for Your Assistant.

**Q: Where are my old chats?**
A: All chats are saved in SQLite. Log in with same credentials. Your chats appear in the sidebar under "🤖 Your Assistant Chats".

**Q: Can I rename a chat?**
A: Yes! Go to Your Assistant tab, open the chat, and edit the name in "Chat — name & copilot prompt" section. Changes save automatically.

---

### Knowledge Hub Questions

**Q: Which file formats are supported?**
A: `.txt` and `.pdf` files. Can upload multiple at once.

**Q: What does "Load documents into Your Assistant" do?**
A: Creates embeddings and stores in vector database, ready for chatting in the Your Assistant tab.

**Q: Can I upload again to add more documents?**
A: Yes! Upload new files and click "Load documents..." again. They replace old ones.

**Q: What if I just want to try without uploading?**
A: You can create a chat first in Your Assistant sidebar, then come back to Knowledge Hub to load docs.

---

### Your Assistant (Chat) Questions

**Q: Why can't my chat find the answer?**
A: The answer isn't in your documents. Try:
1. Rephrasing the question
2. Uploading more relevant documents
3. Checking if the right document is loaded

**Q: Can I chat without uploading documents?**
A: You'll get error message "Upload documents first". It's RAG-based - answers come only from documents.

**Q: How long are chats saved?**
A: Forever! Until you delete them. They're stored in SQLite database.

**Q: Can I delete a chat?**
A: Yes! Click the ✕ button next to it in the sidebar. This is permanent.

**Q: Can I export my chat?**
A: Not built-in, but you can screenshot or copy from the text area.

**Q: Why does it say "I don't have enough information"?**
A: One of:
1. Document doesn't contain the answer
2. Vector DB didn't find relevant content
3. Question is too vague

Try more specific questions or different documents.

---

### Meeting Assistant Questions

**Q: Why is Meeting Assistant not working like before?**
A: It's now a standalone analyzer (not a chat). Upload → Click "Analyze Meeting" → See results.

**Q: Does it extract what I specified?**
A: Yes! It extracts:
- Participants
- Date & time
- Summary (what was discussed)
- Decisions Made
- Action Items

**Q: Can I modify the analysis?**
A: You can copy it to a text editor. The analysis is automatic from the AI.

**Q: What file formats work?**
A: `.txt` and `.docx` files only.

**Q: Can I analyze multiple meetings?**
A: Yes! Upload one → analyze → click "Clean" → upload next.

**Q: Why doesn't it extract from my document?**
A: File might be:
- Wrong format (use `.txt` or `.docx`)
- Corrupted
- Not really meeting notes

Try with a simpler `.txt` file first.

---

### Risk Analyzer Questions

**Q: What does Risk Analyzer do?**
A: Analyzes project documents to identify:
- Key risks and ratings
- Business impact
- Dependencies
- Scenarios
- Assumptions

**Q: Can I customize the analysis?**
A: Partially. You can edit the output directly, but automated extraction is standardized.

**Q: What file formats?**
A: `.txt` and `.docx` only.

**Q: Why is the output long?**
A: It's comprehensive! Covers risks, impact, dependencies, scenarios, and assumptions.

**Q: Can I use this for non-project documents?**
A: Yes, but it's optimized for project planning documents. Try it - it might work for other analyses.

---

### Sidebar Questions

**Q: Where do I see my chats?**
A: Look at sidebar under "🤖 Your Assistant Chats". All your saved chats appear there.

**Q: What does the ▶ arrow mean?**
A: Shows which chat is currently open/active.

**Q: How do I create a new chat?**
A: Click 🤖 button under "New Chat" section in sidebar.

**Q: How do I switch between chats?**
A: Click the chat name in the sidebar.

**Q: Can I organize chats into folders?**
A: Not in current version. Use meaningful names, e.g., "Project Q2 - Budget Review".

**Q: How many chats can I have?**
A: Unlimited! They're stored in database.

---

### Settings Questions

**Q: What settings can I change?**
A: Click ⚙️ in sidebar:
- LM Studio model name
- Font size (12-22px)
- Accent color
- Sidebar background color

**Q: Do settings save?**
A: Yes! They're per-user in the database.

**Q: How do I change the AI model?**
A: Settings → Change "LM Studio model" field. Models must be running on localhost:1234.

---

## 🐛 Troubleshooting

### Problem: "LM Studio not running"

**Error**: "LM Studio is not running or local server is not started."

**Solutions**:
1. Start LM Studio application
2. Make sure it's running on `localhost:1234`
3. Check LM Studio is not on different port
4. Restart app if LM Studio starts after app

```
Check: http://localhost:1234 in browser (should respond)
```

---

### Problem: "Upload documents first"

**Error**: Upload documents in Knowledge Hub first.

**Solution**:
1. Go to Knowledge Hub tab (📄)
2. Upload `.txt` or `.pdf` files
3. Click "✅ Load documents into Your Assistant"
4. Go back to Your Assistant tab

---

### Problem: "I don't have enough information"

**Error**: Bot says "I don't have enough information in the provided documents"

**Solutions**:
1. **Try different phrasing**: "What's the timeline?" vs "Timeline?"
2. **Check document**: Does uploaded document actually contain answer?
3. **Upload relevant docs**: Add more documents with the information
4. **Use Clean button**: Clear everything, reload documents

**Debug**:
- Check active documents shown below upload area
- Make sure correct files are uploaded
- Try simpler, more specific questions first

---

### Problem: Text area for analysis is empty

**Error**: After clicking Analyze, nothing appears.

**Solutions**:
1. **Check file**: Did you really upload a file?
2. **Check format**: Must be `.txt` or `.docx`
3. **Wait**: Sometimes takes 10-15 seconds
4. **Check file quality**: Is it readable text?
5. **Try again**: Click Clean, upload new file, analyze again

---

### Problem: Chat not saving

**Error**: Closed chat, came back, chat gone.

**Solution**:
- Make sure you created the chat properly
- Chat should appear in sidebar under "Your Assistant Chats"
- If not there, create new and add manually

**Prevention**:
- Always name chats meaningfully
- They auto-save but messages take 1-2 seconds

---

### Problem: Document file won't upload

**Error**: File upload fails or is greyed out.

**Solutions**:
1. **Check format**: Only `.txt`, `.pdf` allowed (in KB) or `.txt`, `.docx` (in Meeting/Risk)
2. **Check file size**: Files shouldn't be huge (>50MB)
3. **Check file name**: Avoid special characters
4. **Try again**: Sometimes browser caching issue
5. **Refresh page**: Clear browser cache

```
Allowed:
- Knowledge Hub: .txt, .pdf
- Meeting Assistant: .txt, .docx
- Risk Analyzer: .txt, .docx
```

---

### Problem: Takes forever to respond

**Error**: Spy glass ⏳ spinner goes for 30+ seconds.

**Solutions**:
1. **Check LM Studio**: Is it running? Is it stuck?
2. **Check network**: Internet connection stable?
3. **Try simple question**: Long documents take longer
4. **Try simpler file**: Very large files slow down
5. **Restart**: Close app, restart app, try again

**Normal times**:
- RAG chat: 3-10 seconds
- Meeting analysis: 2-5 seconds
- Risk analysis: 5-15 seconds

---

### Problem: Crashes when uploading large file

**Error**: App crashes or becomes unresponsive.

**Solutions**:
1. **Use smaller files**: Break large documents into chunks
2. **Try different format**: `.pdf` → `.txt`
3. **Check file integrity**: File might be corrupted
4. **Increase memory**: Restart app with more resources

**Recommendations**:
- Keep files under 10MB
- Use `.txt` format for better compatibility
- Split very large documents

---

### Problem: Can't find My Chat

**Error**: Created chat but can't see it in sidebar.

**Solutions**:
1. **Check login**: Are you logged in? (Should say username at top)
2. **Check tab**: Make sure you're looking at right tab
3. **Scroll sidebar**: Chat might be below visible area
4. **Check name**: Search by part of name you remember
5. **Recreate**: If still lost, create new chat

**Debug**:
- Look at "Chat — name" section at top of tab
- Confirms which chat is currently active

---

### Problem: Settings not saving

**Error**: Change font size, log out, log in, back to default.

**Solutions**:
1. **Save button**: Click "💾 Save settings" after changes
2. **Wait**: Can take 1-2 seconds to save
3. **Check login**: Different user accounts have different settings
4. **Refresh**: Close and reopen app

---

### Problem: Can't log in

**Error**: "Invalid username or password"

**Solutions**:
1. **Check username/password**: Case-sensitive
2. **Register first**: If new user, must register first
3. **Typo**: Check for spaces or extra characters
4. **Reset**: No built-in reset, need admin help
5. **Database issue**: Delete `aipm_data.db` and restart (loses all data!)

---

### Problem: Permission denied errors

**Error**: "Permission denied" when app starts.

**Solutions**:
1. **Check folder permissions**: Folder must be readable/writable
2. **Check database**: Delete `aipm_data.db` (will recreate)
3. **Run as admin**: Try running Streamlit as administrator
4. **Check antivirus**: Antivirus might be blocking file access

```bash
# Windows - As Administrator:
streamlit run app.py
```

---

## 🔧 Common Fixes

### "Turn It Off and On Again"
1. Close Streamlit app
2. Close LM Studio
3. Wait 5 seconds
4. Start LM Studio
5. Start Streamlit
6. Try again

### Clear Cache
1. Close app
2. Delete `aipm_data.db`
3. Start app (will create fresh database)
4. Register new account

### Reset Single Setting
1. Login
2. Go to Settings (⚙️)
3. Reset value
4. Click Save
5. Refresh

---

## 📞 Advanced Troubleshooting

### Check Database
```python
import sqlite3
con = sqlite3.connect("aipm_data.db")
print(con.execute("SELECT * FROM chats").fetchall())
```

### Check LM Studio
```bash
curl http://localhost:1234/v1/models
```

### View Logs
- Streamlit shows output in terminal
- Check terminal for error messages
- Look for red error text

---

## 🆘 Still Having Issues?

**Check in Order**:
1. ✅ Read relevant Q&A section above
2. ✅ Read troubleshooting section above
3. ✅ Try "Turn It Off and On Again"
4. ✅ Check documentation files
5. ✅ Review QUICK_REFERENCE.md
6. ✅ Review USAGE_EXAMPLES.md

**Still stuck?**
- Check LM Studio is running and responding
- Try with simpler documents
- Try with different file format
- Restart everything

---

## 📋 Quick Checklist

Before reporting issues, verify:
- [ ] LM Studio is running and accessible
- [ ] Using supported file formats
- [ ] Files are not corrupted
- [ ] Have proper disk space
- [ ] Using correct username/password
- [ ] Python version ≥ 3.10
- [ ] All dependencies installed
- [ ] Port 1234 not blocked by firewall
- [ ] Browser cache cleared
- [ ] App restarted after making changes

---

**Last Updated**: April 24, 2026
**Version**: 2.0
