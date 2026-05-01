# Usage Examples - AI PM Assistant v2.0

## 📚 Real-World Scenarios

---

## Scenario 1: Analyzing an SLA Document

### Step 1: Upload Document
1. Go to **Knowledge Hub** tab (📄)
2. Click upload area
3. Select `sla_policy.txt` from your files
4. Click **"✅ Load documents into Your Assistant"**

### Step 2: Chat About SLA
1. Switch to **Your Assistant** tab (🤖)
2. Create new assistant chat (click 🤖 in sidebar)
3. Name it: "SLA Policy Review"
4. Ask questions:
   - "What are the response times for critical incidents?"
   - "What are the penalties for SLA violations?"
   - "What support hours are covered?"

### Result
- Quick answers from SLA document
- Only information from uploaded document
- Save conversation for future reference

---

## Scenario 2: Processing Meeting Minutes

### Step 1: Extract Meeting Info
1. Go to **Meeting Assistant** tab (📝)
2. Upload `verbale_meet_assitant.txt`
3. Click **"📝 Analyze Meeting"**

### Result (Automatic Extraction)
```
List of participants:
- Marco Rossi (PM)
- Laura Bianchi (Developer)
- Paolo Verdi (QA)

Date & time of call:
- April 20, 2024 - 14:00 CET

Summary of call:
- Discussed Q2 release timeline
- Database optimization reviewed
- Testing strategy updated

Decisions Made:
- Release postponed to May 15
- Database refactoring approved
- New QA process implemented

Action Items:
- Complete database migration - Laura
- Update test cases - Paolo
- Schedule stakeholder review - Marco
```

### Step 2: Follow Up
- Use **🧹 Clean** to clear and analyze another meeting
- Or keep in **Your Assistant** chat for discussion

---

## Scenario 3: Risk Assessment on Project

### Step 1: Analyze Risks
1. Go to **Risk Analyzer** tab (⚠️)
2. Upload `risk_project_doc.txt`
3. Click **"🔍 Analyze Risks"**

### Result (Structured Report)
```
**Key Risks**
- Data Integration: Medium
  Potential delays in API connectivity
- Resource Availability: High
  Team members allocated to multiple projects

**Business Impact**
- 3-week delay costs €50K in penalties
- Customer satisfaction may drop 15%

**Dependencies**
- Third-party API (external vendor)
- Cloud infrastructure availability
- Contractor availability

**SLA Risks**
- 99.9% uptime requirement at risk if API unstable
- Response time SLA (15min) depends on monitoring system

**Certainties**
- Budget allocation: €200K approved
- Timeline: Must complete by July 2024
- Team size: 5 developers available

**Uncertainties**
- Third-party vendor commitment timing
- Exact user adoption rate
- Market competition impact

**Potential Scenarios**
- Positive: Early delivery (15% chance)
  All external dependencies met
- Negative: 4-week delay (35% chance)
  API availability issues extended

**Assumptions Made**
- Third-party vendor performs as expected
- No major team turnover
- No significant scope changes
```

### Step 2: Use for Planning
- Export/screenshot for stakeholders
- Reference in project meetings
- Use as risk monitoring checklist

---

## Scenario 4: Knowledge Base Research

### Step 1: Build Comprehensive Knowledge Base
1. Go to **Knowledge Hub** (📄)
2. Upload multiple documents:
   - `KB_Risk_analyzer.txt`
   - `incident_resolution.txt`
   - `password_reset.txt`
   - `sla_policy.txt`
3. Click **"✅ Load documents into Your Assistant"**

### Step 2: Query Your Knowledge Base
1. Go to **Your Assistant** (🤖)
2. Create chat: "Company Knowledge Base"
3. Ask questions across all documents:
   - "How do I reset a password?"
   - "What's the process for active incidents?"
   - "When should we escalate to management?"
   - "What SLA applies to emergency tickets?"

### Result
- Answers pulled from all relevant documents
- Comprehensive, context-aware responses
- Building institutional knowledge

---

## Scenario 5: Multi-Chat Workflow

### Organize Different Topics
1. Create separate chats for:
   - "Q2 Budget Analysis" (budget documents)
   - "Security Policy Review" (policy docs)
   - "Product Requirements" (spec documents)

2. Sidebar shows all organized:
```
🤖 Your Assistant Chats
▶ Q2 Budget Analysis    [✕]
  Security Policy      [✕]
  Product Reqs         [✕]
  Meeting Notes - Apr  [✕]
```

3. Click to switch between contexts instantly

---

## Scenario 6: Custom Analysis with Prompts

### When Creating a Chat
1. Click 🤖 in sidebar under "New Chat"
2. Enter name: "Financial Risk Analysis"
3. Enter copilot prompt:
```
You are a financial risk expert. 
Analyze every statement for:
- Financial exposure
- Potential liabilities
- Cost optimization opportunities
- Cash flow risks

Use technical finance terminology but explain clearly.
```
4. Upload financial documents
5. Ask: "What are our biggest financial risks?"

Result: Specialized analysis using your custom expertise

---

## Scenario 7: Real-Time Decision Making

### During a Meeting
1. Project manager has questions NOW
2. Upload recent board minutes to Knowledge Hub
3. Go to Your Assistant
4. Ask: "What were the board's concerns about timeline?"
5. Get instant answer from minutes
6. Share answer in real-time chat

No need to search through documents!

---

## Scenario 8: Compliance & Audit Trail

### Document Everything
1. Create chat: "Audit Trail - April 2024"
2. Upload compliance documents
3. Ask: "Do we meet GDPR requirements?"
4. System stores every question and answer
5. Export for audit verification

Benefits:
- Clear decision records
- Compliance documentation
- Decision traceability

---

## Common Question Patterns

### Questions for Knowledge Hub
- "What is the process for...?"
- "When should we...?"
- "What are the requirements for...?"
- "Summarize the section on...?"
- "What's included in the SLA?"
- "How do we handle...?"

### Questions for Your Assistant (After Upload)
- "Find all incidents related to..."
- "What common issues appear in...?"
- "Compare the procedures for...?"
- "Extract all dates and owners for..."
- "What would you recommend based on...?"

### For Meeting Analysis
- Gets: Participants, date, summary, decisions, actions
- You ask: "Who owns the database task?"
- You ask: "What's the new release date?"

### For Risk Analysis
- Gets: Comprehensive risk assessment
- You ask: "What are high-risk items?"
- You ask: "Which risks need management?"

---

## Tips & Tricks

### 💡 Tip 1: Clear Naming
Good chat names:
- "SLA Review - April 24"
- "Q2 Invoice Processing"
- "Release Planning v2"

Avoid:
- "Chat 1", "Analysis", "Q&A"

### 💡 Tip 2: Custom Prompts
Use prompts for specific expertise:
- Security expert
- Financial analyst
- Legal reviewer
- Technical architect

### 💡 Tip 3: Document Organization
- Group related documents
- One chat = One project/topic
- Keep separate knowledge bases

### 💡 Tip 4: Batch Processing
1. Upload 5 meeting notes
2. Go through each systematically
3. Keep organized notes for later

### 💡 Tip 5: Regular Cleanup
- Delete old chats when done
- This keeps sidebar clean
- Use 🧹 Clean button often

---

## Troubleshooting Examples

### Problem: "I don't have enough information..."
**Solution**: Document doesn't contain answer
- Try different phrasing
- Upload more relevant documents
- Check if document is correct

Example:
```
You: "What's the cost of the project?"
Bot: "I don't have enough information..."
Action: Upload budget document
You: "What's our Q2 budget allocated?"
Bot: "According to the budget document, €200K was approved..."
```

### Problem: Question takes too long
**Solution**: LM Studio is processing
- Wait a few seconds
- Check server is running
- Try shorter question

### Problem: Can't find old chat
**Solution**: Check sidebar
1. Make sure you're on Your Assistant tab
2. Scroll sidebar to see all chats
3. Or create new chat with similar name

---

## Best Practices

✅ **DO:**
- Name chats meaningfully
- Use specific questions
- Reference the document in questions
- Keep related conversations together

❌ **DON'T:**
- Expect hallucinated information
- Ask questions outside document scope
- Upload unrelated documents together
- Forget to clean after analysis

---

**Version**: 2.0
**Last Updated**: April 24, 2026
