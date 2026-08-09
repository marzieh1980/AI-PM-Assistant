import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


# -------------------------
# READ FILE CONTENT (.txt and .docx)
# -------------------------
def read_uploaded_file(uploaded_file):
    """Read content from .txt or .docx files"""
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == "txt":
        content = uploaded_file.read().decode("utf-8")
        return content

    elif file_extension == "docx":
        try:
            from docx import Document
            doc = Document(uploaded_file)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return content
        except ImportError:
            return "❌ Error: python-docx library not installed. Please install it with: pip install python-docx"

    else:
        return f"❌ Unsupported file format: {file_extension}. Please use .txt or .docx"


def analyze_risk(user_input, model_name="mistral"):
    """Analyze risk using Ollama local server."""

    full_prompt = f"""You are a highly experienced scenario planner who understands the
factors that affect the success of a project. I want you to help
me identify the potential outcomes of this project.

Analyze the following project description and generate a structured report with:

**Key Risks** (each rated Low / Medium / High)
**Business Impact**
**Dependencies**
**SLA Risks**
**List of certainties**
**List of uncertainties**
**Potential scenarios** (both positive and negative, with likelihood comments)
**Research recommendations** (to give more certainty)
**Assumptions made**

Project:
{user_input}

Format your response with clear headings and bullet points. Remove excessive spacing and use concise, professional language."""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": model_name,
            "prompt": full_prompt,
            "temperature": 0.7,
            "stream": False
        }, timeout=120)
        result = response.json()
        if "response" not in result:
            return f"❌ Unexpected response format from Ollama: {result}"
        return result["response"].strip()
    except requests.exceptions.ConnectionError:
        return "❌ Ollama is not running or the local server is not started. Check port 11434."
    except Exception as e:
        return f"❌ Error contacting Ollama: {str(e)}. Check if Ollama is running."
