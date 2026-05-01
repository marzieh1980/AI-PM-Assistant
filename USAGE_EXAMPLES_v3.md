# Usage Examples - AI PM Assistant v3.0

## 📚 Real-World Scenarios

---

## Scenario 1: Quick Question to AI

### Use Your Assistant Tab
1. Go to **Your Assistant** tab (🤖)
2. Type: "What are best practices for project management?"
3. Click "🔍 Send"
4. Get instant AI answer
5. Click "🧹 Clear" to ask another question

**Perfect for**: General knowledge, quick advice, brainstorming

---

## Scenario 2: Multi-Turn Document Analysis

### Step 1: Upload and Start Q&A
1. Go to **Knowledge Hub** tab (📄)
2. Upload `sla_policy.txt`
3. Conversation history appears (empty initially)
4. Type question: "What are the response times for critical incidents?"
5. Click "Search 🔍"

### Step 2: See History and Continue
1. Answer appears with Q1/A1 in conversation history
2. **Keep asking follow-ups in the same input box**:
   - "What are SLA penalties?"
   - "What support hours are covered?"
3. Each new answer adds to the history
4. See all previous Q&A pairs

### Result - Conversation History
```
Q1: What are the response times for critical incidents?
A1: Based on the SLA document, critical incidents require response within 1 hour...

Q2: What are SLA penalties?
A2: The document specifies that failure to meet SLA targets results in...

Q3: What support hours are covered?
A3: Support is provided Monday-Friday 8 AM - 6 PM EST...
```

**Note**: If answer not found, you'll see "ℹ️ No information found in the document for this question"

---

## Scenario 3: Meeting Analysis with Follow-Up

### Step 1: Upload and Generate Summary
1. Go to **Meeting Assistant** tab (📝)
2. Upload `verbale_meet_assitant.txt`
3. You'll see "✅ Loaded: [filename]" message
4. Click "📝 Summary of Meeting"

### Step 2: Review Auto-Extracted Information
```
Participants: Marco Rossi, Laura Bianchi, Paolo Verdi
Date & Time: April 20, 2024 - 14:00 CET
Summary: Discussed Q2 release, database optimization, testing strategy
Decisions: Release postponed to May 15, database refactoring approved
Action Items: Complete DB migration, update test cases, schedule review
```

### Step 3: Ask Follow-Up Questions (NOW VISIBLE)
1. **Follow-up section appears BELOW the summary**
2. Ask: "Who is responsible for database migration?"
3. Click "Search 🔍"
4. Get follow-up answer

---

## Scenario 4: Risk Assessment

### Step 1: Upload and Analyze
1. Go to **Risk Analyzer** tab (⚠️)
2. Upload `project_risk_doc.txt`
3. Click "🔍 Analyze Risks"

### Step 2: Review Risk Report
```
**Key Risks**

Data Integration (Medium Risk)
  Impact: Integration delays could affect Q2 launch
  Dependency: Third-party API availability
  
Resource Availability (High Risk)
  Impact: Team shortage could delay development
  Dependency: Hiring timeline
  
External Dependencies (Low Risk)
  Impact: Third-party API delays manageable
  Mitigation: Use fallback providers
```

---

## Comparison: When to Use Each Tab

| Need | Tab | Example |
|------|-----|---------|
| Quick general question | 🤖 Your Assistant | "What's a PMP methodology?" |
| Multi-turn doc analysis | 📄 Knowledge Hub | Long SLA doc with multiple follow-ups |
| Meeting extraction | 📝 Meeting Assistant | Video call transcript |
| Project health check | ⚠️ Risk Analyzer | Project plan risk assessment |
| Simple chat | 🤖 Your Assistant | Brainstorming, quick advice |

