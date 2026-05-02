import rag_core

def extract_tasks(text, model_name):
    prompt = f"""
You are a senior IT Project Manager.

From the following project document, extract structured tasks.

For each task include:
- Task Name
- Description
- Priority (High/Medium/Low)
- Type (Feature/Bug/Improvement)
- Dependencies (if any)
- Suggested Assignee (if possible, based on roles mentioned, otherwise leave blank)

Return in this format:

TASK 1:
• Name:
• Description:
• Priority:
• Type:
• Dependencies:
• Assignee:

TASK 2:
...

Rules:
- Use bullet points (•)
- Make it clean and readable
- Do NOT return JSON
- Do NOT return tables

Text:
{text}
"""

    return rag_core.ask_general(prompt, model_name=model_name)