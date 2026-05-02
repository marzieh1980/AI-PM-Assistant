import rag_core

def estimate_effort(tasks_text, model_name):
    prompt = f"""
You are a senior Project Manager.

Estimate effort for the following tasks.

For each task include:
- Estimated Hours
- Hourly Rate (assume realistic industry rates)
- Total Cost
- Complexity (Low/Medium/High)
- Contingency (% buffer)
- Final Adjusted Cost
- Suggested Role (who should do it)

Return in this format:

TASK:
• Name:
• Estimated Hours:
• Rate:
• Total Cost:
• Complexity:
• Contingency:
• Final Cost:
• Assigned Role:

Rules:
- Use bullet points
- Be realistic
- No JSON
- No tables

Tasks:
{tasks_text}
"""

    return rag_core.ask_general(prompt, model_name=model_name)