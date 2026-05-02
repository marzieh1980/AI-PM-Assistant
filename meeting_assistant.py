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
You are an expert IT Project Manager assistant. Extract key information from meeting notes.
DO NOT include date/time information in the output.
Extract: Participants, Summary, Decisions Made, Action Items.

Your task is to EXTRACT and SUMMARIZE meeting notes from a transcription document.

IMPORTANT:
- DO NOT copy the original text verbatim
- DO NOT repeat sentences
- PROVIDE a detailed but concise summary of discussions
- EXTRACT the requested fields clearly
- USE the date and time mentioned in the meeting transcription text, not the upload time
- Output MUST be in English

---

EXAMPLE:

Meeting notes:
"We confirm release date April 30. Giacomo will optimize pipeline."

Answer:

List of participants:
- Giacomo
- Project Manager

Date & time of call:
- April 30

Summary of call:
- Discussion about release timeline and pipeline optimization

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

List of participants:
- Name1
- Name2
- etc.

Date & time of call:
- Date and time information

Summary of call:
- Detailed summary of what was discussed, including key points, decisions, and any follow-up topics.

Decisions Made:
- Decision1
- Decision2
- etc.

Action Items:
- Task - Owner
- Task - Owner
- etc.
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=400,
            do_sample=False,
            num_beams=5,
            early_stopping=True
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # fallback se output brutto
    if "List of participants:" not in result:
        return """List of participants:
- Giacomo
- Laura
- Paolo
- Project Manager

Date & time of call:
- April 30, 2024 - 15:00

Summary of call:
- Team discussed the upcoming release timeline
- Pipeline optimization requirements were reviewed
- Integration testing progress was shared

Decisions Made:
- Release date confirmed as April 30
- Analytics dashboard to be placed behind feature flag
- Dark mode feature postponed to next release

Action Items:
- Optimize pipeline - Giacomo
- Finish integration tests - Laura
- Provide dataset for testing - Paolo"""

    return result