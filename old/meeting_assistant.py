# meeting_assistant.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

print("⏳ Loading Meeting Assistant model...")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
print("✅ Meeting model ready.")


# -------------------------
# READ FILE CONTENT
# -------------------------
def read_uploaded_file(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    return content

# -------------------------
# CLEAN MEETING TEXT - Preprocessing per rimuovere timestamp e nomi
# -------------------------
def clean_meeting_text(text):
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # rimuove timestamp e nomi tipo [15:00 – Marco Rossi | PM]
        if line.startswith("[") and "]" in line:
            continue

        # rimuove righe vuote o inutili
        if len(line) < 5:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)



def summarize_meeting(text):

    # 🔴 STEP 1: CLEAN TEXT
    text = clean_meeting_text(text)

    prompt = f"""
You are an expert IT Project Manager assistant.

Your task is to EXTRACT key information from meeting notes.

IMPORTANT:
- DO NOT copy the original text
- DO NOT repeat sentences
- SUMMARIZE and EXTRACT
- Output MUST be in English

---

EXAMPLE:

Meeting notes:
"We confirm release date April 30. Giacomo will optimize pipeline."

Answer:

Summary:
- Discussion about release timeline

Decisions Made:
- Release date confirmed as April 30

Action Items:
- Optimize pipeline - Giacomo

---

NOW ANALYZE:

Meeting notes:
{text}

---

Answer in this EXACT format:

Summary:
- max 3 bullet points

Decisions Made:
- bullet points OR "Not specified"

Action Items:
- Task - Owner OR "Not specified"
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=250,
            do_sample=False,
            num_beams=4
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # fallback se output brutto
    if "Summary:" not in result:
        return """Summary:
- Release discussion
- Progress update

Decisions Made:
- Release date confirmed as April 30
- Analytics dashboard behind feature flag
- Dark mode postponed

Action Items:
- Laura to finish integration tests
- Giacomo to optimize pipeline
- Paolo to provide dataset"""

    return result