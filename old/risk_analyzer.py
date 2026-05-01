import requests

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"


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


def analyze_risk(user_input, model_name="llama-3.2-3b-instruct:2"):
    """Analyze risk using LM Studio local server."""

    full_prompt = f"""You are a highly experienced scenario planner who understands the
factors that affect the success of a project. I want you to help
me identify the potential outcomes of this.Explore
different possibilities and present your response using markup

Analyze the following project description and generate a structured report with:

1. **Key Risks** (each rated Low / Medium / High)
2. **Business Impact**
3. **Dependencies**
4. **SLA Risks**
5. **List of certainties**
6. **List of uncertainties**
also: 
- a list of multiple potential scenarios - both positive and
negative - with a comment on their likelihood of happening.
- research we should undertake to give us more certainty
- A list of assumptions you've made in your response

Project:
{user_input}
"""

    try:
        response = requests.post(LM_STUDIO_URL, json={
            "model": model_name,
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": 0.7
        }, timeout=120)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        return "❌ LM Studio is not running or the local server is not started. Check port 1234."
    except KeyError:
        return f"❌ Unexpected response format from LM Studio: {result}"
    except Exception as e:
        return f"❌ Error contacting LM Studio: {str(e)}"
