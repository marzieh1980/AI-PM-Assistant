"""
app.py  —  AI PM Assistant  (refactored)
Architecture:
  • Login / Register via storage.py (SQLite)
  • 3 main tabs: Knowledge Hub | Meeting Assistant | Risk Analyzer
  • Sidebar: New Chat (per tab) + chat list + Settings + Prompt Library
  • All chats, messages and prompts persisted to SQLite
  • Vector DBs (FAISS) are in-memory only (not serialisable); file *names* are persisted
"""

import streamlit as st
import uuid
from datetime import datetime

import storage as db
from rag_core import load_uploaded_documents, create_vector_db, ask_rag, ask_general, ask_with_context
from meeting_assistant import summarize_meeting, read_uploaded_file
from risk_analyzer import analyze_risk, read_uploaded_file as risk_read_file

# ──────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────
st.set_page_config(page_title="AI PM Assistant", layout="wide", initial_sidebar_state="expanded")

# ──────────────────────────────────────────────────────────
# BOOTSTRAP SESSION STATE
# ──────────────────────────────────────────────────────────
def _def(key, val):
    if key not in st.session_state:
        st.session_state[key] = val

_def("user",             None)   # logged-in user dict {id, username}
_def("chat_list",        [])     # list of chat dicts (loaded from DB on login)
_def("active_chat_id",   None)
_def("show_settings",    False)
_def("show_prompt_lib",  False)
_def("edit_prompt_id",   None)   # prompt being edited
_def("new_chat_tab",     None)   # tab for which "New Chat" was pressed
_def("assistant_temp_chat", {
    "id": "temp",
    "tab": "assistant",
    "name": "Assistant session",
    "system_prompt": "",
    "messages": [],
    "uploaded_files": [],
    "upload_db": None,
    "meeting_output": "",
    "risk_output": "",
    "created_at": datetime.now().isoformat(),
    "updated_at": datetime.now().isoformat(),
})

# Knowledge Hub local search state
_def("knowledge_uploaded_files", [])
_def("knowledge_db", None)
_def("knowledge_qa_history", [])  # List of {"query": ..., "answer": ...}
# Assistant chat state (simple stateless chat - no persistence)
_def("assistant_answer", "")
# Meeting assistant follow-up state
_def("meeting_output",   "")     # meeting analysis results
_def("meeting_raw_content", "")
_def("meeting_loaded_name", "")
_def("meeting_followup_query", "")
_def("meeting_followup_answer", "")
_def("risk_output",      "")     # risk analysis results
# Settings (overwritten on login from DB)
_def("model_name",    "llama-3.2-3b-instruct:2")
_def("font_size",     15)
_def("accent_color",  "#4F8EF7")
_def("sidebar_color", "#1C2333")


# ──────────────────────────────────────────────────────────
# DYNAMIC CSS  (re-evaluated every run)
# ──────────────────────────────────────────────────────────
def inject_css():
    ac = st.session_state.accent_color
    fs = st.session_state.font_size
    sb = st.session_state.sidebar_color
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: {fs}px;
}}

/* ── Sidebar ─────────────────────────────── */
section[data-testid="stSidebar"] > div:first-child {{
    background: {sb};
    padding-top: 0.8rem;
}}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {{
    color: #e8eaf0 !important;
}}
section[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    color: #e8eaf0 !important;
    border-radius: 7px;
    font-size: 13px;
    padding: 4px 8px;
    width: 100%;
    text-align: left;
    transition: background 0.15s;
    margin-bottom: 2px;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background: {ac}33;
    border-color: {ac};
}}

/* ── Main area buttons ────────────────────── */
.stButton > button {{
    border-radius: 8px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
}}

/* ── Tabs ─────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    border-bottom: 2px solid #e0e4ef44;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    letter-spacing: 0.05em;
    padding: 8px 22px;
    border-radius: 8px 8px 0 0;
    background: transparent;
    color: #8892a4;
    border: none;
}}
.stTabs [aria-selected="true"] {{
    color: {ac} !important;
    background: {ac}18 !important;
    border-bottom: 2px solid {ac} !important;
}}

/* ── Chat bubbles ─────────────────────────── */
.msg-user {{
    background: {ac}18;
    border-left: 3px solid {ac};
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    margin: 6px 0;
    font-size: {fs}px;
    line-height: 1.6;
    white-space: pre-wrap;
}}
.msg-bot {{
    background: #f4f6fb;
    border-left: 3px solid #c5cad6;
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    margin: 6px 0;
    font-size: {fs}px;
    line-height: 1.6;
    color: #22273a;
    white-space: pre-wrap;
}}

/* ── Sidebar labels ───────────────────────── */
.sb-group {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: {ac} !important;
    margin: 14px 0 3px 2px;
    display: block;
}}
.sb-user {{
    font-size: 12px;
    color: #aab0c0 !important;
    margin-bottom: 6px;
    display: block;
}}

/* ── Section micro-labels ─────────────────── */
.sec-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8892a4;
    margin: 14px 0 4px 0;
}}

/* ── Upload hint box ──────────────────────── */
.upload-hint {{
    background: {ac}0d;
    border: 1px dashed {ac}55;
    border-radius: 10px;
    padding: 16px 20px;
    color: #6b7385;
    font-size: 13px;
    margin-bottom: 10px;
}}

/* ── Prompt card ──────────────────────────── */
.prompt-card {{
    background: #f8f9fc;
    border: 1px solid #e2e6f0;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: {fs - 1}px;
}}
.prompt-name {{
    font-weight: 600;
    color: #2a2f3d;
    font-size: {fs}px;
}}
.prompt-text {{
    color: #6b7385;
    margin-top: 4px;
    white-space: pre-wrap;
}}
</style>
""", unsafe_allow_html=True)

inject_css()


# ──────────────────────────────────────────────────────────
# AUTH  (shown when no user logged in)
# ──────────────────────────────────────────────────────────
def auth_screen():
    st.markdown("## 🤖 AI PM Assistant")
    st.markdown("#### Please log in or create an account to continue.")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### 🔑 Login")
        lu = st.text_input("Username", key="login_u")
        lp = st.text_input("Password", type="password", key="login_p")
        if st.button("Log in", use_container_width=True):
            user = db.login_user(lu, lp)
            if user:
                _load_user_session(user)
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

    with col2:
        st.markdown("### 📝 Register")
        ru = st.text_input("Choose username", key="reg_u")
        rp = st.text_input("Choose password", type="password", key="reg_p")
        rp2 = st.text_input("Confirm password", type="password", key="reg_p2")
        if st.button("Create account", use_container_width=True):
            if rp != rp2:
                st.error("❌ Passwords do not match.")
            elif len(ru.strip()) < 2:
                st.error("❌ Username must be at least 2 characters.")
            elif len(rp) < 4:
                st.error("❌ Password must be at least 4 characters.")
            else:
                user = db.register_user(ru, rp)
                if user:
                    _load_user_session(user)
                    st.rerun()
                else:
                    st.error("❌ Username already taken.")


def _load_user_session(user: dict):
    st.session_state.user = user
    # Load settings
    s = db.load_settings(user["id"])
    st.session_state.model_name    = s["model_name"]
    st.session_state.font_size     = s["font_size"]
    st.session_state.accent_color  = s["accent_color"]
    st.session_state.sidebar_color = s["sidebar_color"]
    # Load chats
    st.session_state.chat_list = db.load_chats(user["id"])
    if st.session_state.chat_list:
        st.session_state.active_chat_id = st.session_state.chat_list[0]["id"]


# ──────────────────────────────────────────────────────────
# CHAT HELPERS
# ──────────────────────────────────────────────────────────
TAB_LABELS = {
    "knowledge": "📄 Knowledge",
    "meeting":   "📝 Meeting",
    "risk":      "⚠️ Risk",
    "assistant": "🤖 Your Assistant",
}

def get_chat(cid):
    for c in st.session_state.chat_list:
        if c["id"] == cid:
            return c
    return None

def get_active_chat():
    return get_chat(st.session_state.active_chat_id)

def get_tab_active(tab_key):
    active = get_active_chat()
    if active and active["tab"] == tab_key:
        return active
    matches = [c for c in st.session_state.chat_list if c["tab"] == tab_key]
    return matches[0] if matches else None


def get_assistant_session():
    active = get_tab_active("assistant")
    if active:
        return active, True
    if "assistant_temp_chat" not in st.session_state:
        st.session_state.assistant_temp_chat = {
            "id": "temp",
            "tab": "assistant",
            "name": "Assistant session",
            "system_prompt": "",
            "messages": [],
            "uploaded_files": [],
            "upload_db": None,
            "meeting_output": "",
            "risk_output": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
    return st.session_state.assistant_temp_chat, False


def persist_assistant_chat(temp_chat: dict, name: str):
    if not name.strip():
        n = sum(1 for c in st.session_state.chat_list if c["tab"] == "assistant") + 1
        name = f"meeting assistant - chat {n}"
    new_chat = create_new_chat("assistant", name=name.strip(), system_prompt=temp_chat.get("system_prompt", ""))
    new_chat["messages"] = [m.copy() for m in temp_chat.get("messages", [])]
    new_chat["uploaded_files"] = list(temp_chat.get("uploaded_files", []))
    new_chat["upload_db"] = temp_chat.get("upload_db")
    for msg in new_chat["messages"]:
        db.append_message(new_chat["id"], msg["role"], msg["text"])
    db.save_chat_files(new_chat["id"], new_chat["uploaded_files"])
    st.session_state.active_chat_id = new_chat["id"]
    st.session_state.assistant_temp_chat = {
        "id": "temp",
        "tab": "assistant",
        "name": "Assistant session",
        "system_prompt": "",
        "messages": [],
        "uploaded_files": [],
        "upload_db": None,
        "meeting_output": "",
        "risk_output": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    st.session_state.assistant_save_open = False
    st.session_state.assistant_save_name = ""
    st.success("Chat saved to sidebar.")
    st.rerun()


def create_new_chat(tab: str, name: str = "", system_prompt: str = "") -> dict:
    user_id = st.session_state.user["id"]
    n = sum(1 for c in st.session_state.chat_list if c["tab"] == tab) + 1
    cid = str(uuid.uuid4())
    now = datetime.now().strftime("%d/%m %H:%M")
    chat = {
        "id":             cid,
        "user_id":        user_id,
        "tab":            tab,
        "name":           name or f"New {TAB_LABELS[tab].split()[-1]} {n}",
        "system_prompt":  system_prompt,
        "messages":       [],
        "uploaded_files": [],
        "upload_db":      None,
        "meeting_output": "",
        "risk_output":    "",
        "created_at":     now,
        "updated_at":     now,
    }
    db.save_chat(user_id, chat)
    st.session_state.chat_list.insert(0, chat)
    st.session_state.active_chat_id = cid
    return chat

def delete_chat(cid: str):
    db.delete_chat_db(cid)
    st.session_state.chat_list = [c for c in st.session_state.chat_list if c["id"] != cid]
    remaining = st.session_state.chat_list
    st.session_state.active_chat_id = remaining[0]["id"] if remaining else None

def push_message(chat: dict, role: str, text: str):
    chat["messages"].append({"role": role, "text": text})
    if chat.get("id") != "temp":
        db.append_message(chat["id"], role, text)
    # update in-memory updated_at
    chat["updated_at"] = datetime.now().isoformat()

def clear_chat_messages(chat: dict):
    chat["messages"] = []
    if chat.get("id") != "temp":
        db.clear_messages(chat["id"])

def save_chat_state(chat: dict):
    if chat.get("id") == "temp":
        return
    db.save_chat(st.session_state.user["id"], chat)

def auto_name(chat: dict, text: str):
    prefix = f"New {TAB_LABELS[chat['tab']].split()[-1]}"
    if chat["name"].startswith(prefix):
        chat["name"] = text[:38] + ("…" if len(text) > 38 else "")
        save_chat_state(chat)

def render_messages(chat: dict):
    for msg in chat["messages"]:
        cls = "msg-user" if msg["role"] == "user" else "msg-bot"
        icon = "🧑" if msg["role"] == "user" else "🤖"
        # escape HTML in message text
        safe = msg["text"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        st.markdown(f'<div class="{cls}">{icon} {safe}</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# PROMPT LIBRARY HELPERS
# ──────────────────────────────────────────────────────────
def render_prompt_library(tab_key: str):
    """Renders the prompt library panel for a given tab inside the main area."""
    uid = st.session_state.user["id"]
    prompts = db.load_prompts(uid, tab_key)

    st.markdown(f'<div class="sec-label">💾 Saved Prompts — {TAB_LABELS[tab_key]}</div>', unsafe_allow_html=True)

    # ── Save new prompt ──────────────────────────
    with st.expander("➕ Save current prompt as…", expanded=False):
        pname = st.text_input("Prompt name", key=f"plib_newname_{tab_key}", placeholder="e.g. Focus on SLA risks")
        ptxt  = st.text_area("Prompt text", key=f"plib_newtxt_{tab_key}", height=80,
                              placeholder="Write the copilot instruction here…")
        if st.button("💾 Save prompt", key=f"plib_save_{tab_key}"):
            if pname.strip() and ptxt.strip():
                db.save_prompt(uid, tab_key, pname.strip(), ptxt.strip())
                st.success("Prompt saved!")
                st.rerun()
            else:
                st.warning("Name and text are both required.")

    if not prompts:
        st.caption("No saved prompts yet for this tab.")
        return

    for p in prompts:
        with st.container():
            st.markdown(f'<div class="prompt-card"><span class="prompt-name">{p["name"]}</span>'
                        f'<div class="prompt-text">{p["prompt_text"][:160]}{"…" if len(p["prompt_text"])>160 else ""}</div></div>',
                        unsafe_allow_html=True)
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                # Apply to active chat
                cur = get_tab_active(tab_key)
                if cur and st.button("↩ Apply to current chat", key=f"plib_apply_{p['id']}"):
                    cur["system_prompt"] = p["prompt_text"]
                    save_chat_state(cur)
                    st.success(f"Prompt '{p['name']}' applied!")
                    st.rerun()
            with c2:
                if st.button("✏️ Edit", key=f"plib_edit_{p['id']}"):
                    st.session_state.edit_prompt_id = p["id"]
                    st.rerun()
            with c3:
                if st.button("🗑 Delete", key=f"plib_del_{p['id']}"):
                    db.delete_prompt(p["id"])
                    st.rerun()

            # Inline edit form
            if st.session_state.edit_prompt_id == p["id"]:
                new_name = st.text_input("Edit name", value=p["name"], key=f"pedit_name_{p['id']}")
                new_txt  = st.text_area("Edit prompt", value=p["prompt_text"],
                                        key=f"pedit_txt_{p['id']}", height=100)
                ec1, ec2 = st.columns(2)
                with ec1:
                    if st.button("💾 Save changes", key=f"pedit_save_{p['id']}"):
                        db.update_prompt(p["id"], new_name.strip(), new_txt.strip())
                        st.session_state.edit_prompt_id = None
                        st.rerun()
                with ec2:
                    if st.button("✕ Cancel", key=f"pedit_cancel_{p['id']}"):
                        st.session_state.edit_prompt_id = None
                        st.rerun()


# ──────────────────────────────────────────────────────────
# NEW CHAT DIALOG  (shown inline in sidebar)
# ──────────────────────────────────────────────────────────
def new_chat_form(tab_key: str):
    """Returns (chat, True) if created, else (None, False)."""
    st.markdown(f"#### ➕ New {TAB_LABELS[tab_key].split()[-1]} Chat")
    cname = st.text_input("Chat name (optional)", key=f"nc_name_{tab_key}",
                          placeholder=f"New {TAB_LABELS[tab_key].split()[-1]} chat…")
    cprompt = st.text_area("Copilot prompt (optional)", key=f"nc_prompt_{tab_key}",
                           height=90,
                           placeholder="e.g. 'You are a security-focused analyst. Always be concise and bullet-point your answers.'")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Create", key=f"nc_create_{tab_key}", use_container_width=True):
            chat = create_new_chat(tab_key, name=cname.strip(), system_prompt=cprompt.strip())
            st.session_state.new_chat_tab = None
            return chat, True
    with c2:
        if st.button("✕ Cancel", key=f"nc_cancel_{tab_key}", use_container_width=True):
            st.session_state.new_chat_tab = None
            st.rerun()
    return None, False


# ──────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        user = st.session_state.user
        st.markdown("### 🤖 AI PM")
        st.markdown(f'<span class="sb-user">👤 {user["username"]}</span>', unsafe_allow_html=True)
        st.markdown("---")

        # ── Top controls ──────────────────────────────
        tb1, tb2, tb3 = st.columns(3)
        with tb1:
            if st.button("⚙️", help="Settings", use_container_width=True):
                st.session_state.show_settings = not st.session_state.show_settings
                st.session_state.show_prompt_lib = False
        with tb2:
            if st.button("📚", help="Prompt Library", use_container_width=True):
                st.session_state.show_prompt_lib = not st.session_state.show_prompt_lib
                st.session_state.show_settings = False
        with tb3:
            if st.button("🚪", help="Log out", use_container_width=True):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # ── Settings panel ────────────────────────────
        if st.session_state.show_settings:
            st.markdown("#### ⚙️ Settings")
            new_model  = st.text_input("LM Studio model",  value=st.session_state.model_name,   key="set_model")
            new_font   = st.slider("Font size", 12, 22,    value=st.session_state.font_size,     key="set_font")
            new_accent = st.color_picker("Accent color",   value=st.session_state.accent_color,  key="set_accent")
            new_sbg    = st.color_picker("Sidebar color",  value=st.session_state.sidebar_color, key="set_sbg")
            if st.button("💾 Save settings", use_container_width=True):
                st.session_state.model_name    = new_model
                st.session_state.font_size     = new_font
                st.session_state.accent_color  = new_accent
                st.session_state.sidebar_color = new_sbg
                db.save_settings(user["id"], new_model, new_font, new_accent, new_sbg)
                st.session_state.show_settings = False
                st.rerun()
            st.markdown("---")




# ──────────────────────────────────────────────────────────
# SHARED: CHAT HEADER (name + prompt editing inline)
# ──────────────────────────────────────────────────────────
def render_chat_header(chat: dict, tab_key: str):
    """Renders editable chat name and copilot prompt inline."""
    st.markdown('<div class="sec-label">Chat — name &amp; copilot prompt</div>', unsafe_allow_html=True)
    h1, h2 = st.columns([2, 5])
    with h1:
        new_name = st.text_input(
            "name", value=chat["name"],
            key=f"cname_{chat['id']}",
            label_visibility="collapsed",
            placeholder="Chat name…"
        )
        if new_name.strip() and new_name != chat["name"]:
            chat["name"] = new_name.strip()
            save_chat_state(chat)
    with h2:
        # Show saved-prompt picker if prompts exist
        saved = db.load_prompts(st.session_state.user["id"], tab_key)
        prompt_options = ["— type a custom prompt —"] + [p["name"] for p in saved]
        chosen = st.selectbox("Load saved prompt", prompt_options,
                              key=f"psel_{chat['id']}", label_visibility="collapsed")
        if chosen != "— type a custom prompt —":
            matched = next((p for p in saved if p["name"] == chosen), None)
            if matched and matched["prompt_text"] != chat.get("system_prompt", ""):
                chat["system_prompt"] = matched["prompt_text"]
                save_chat_state(chat)
                st.rerun()

    new_prompt = st.text_area(
        "Copilot prompt",
        value=chat.get("system_prompt", ""),
        key=f"cprompt_{chat['id']}",
        height=70,
        label_visibility="collapsed",
        placeholder="Copilot prompt — describe what the assistant should do in this chat… (leave blank for default behaviour)"
    )
    if new_prompt != chat.get("system_prompt", ""):
        chat["system_prompt"] = new_prompt
        save_chat_state(chat)

    # Quick-save button
    sq1, sq2 = st.columns([2, 5])
    with sq1:
        if chat.get("system_prompt", "").strip():
            if st.button("💾 Save prompt to library", key=f"qsave_{chat['id']}"):
                st.session_state[f"qsave_open_{chat['id']}"] = True
    if st.session_state.get(f"qsave_open_{chat['id']}", False):
        with sq2:
            qname = st.text_input("Name for this prompt", key=f"qsave_name_{chat['id']}",
                                  placeholder="e.g. SLA Focus")
        if qname.strip():
            if st.button("✅ Confirm save", key=f"qsave_confirm_{chat['id']}"):
                db.save_prompt(st.session_state.user["id"], tab_key,
                               qname.strip(), chat["system_prompt"])
                st.session_state[f"qsave_open_{chat['id']}"] = False
                st.success("Prompt saved to library!")
                st.rerun()

    st.markdown("---")


# ──────────────────────────────────────────────────────────
# MAIN APP (post-login)
# ──────────────────────────────────────────────────────────
def main_app():
    render_sidebar()
    inject_css()  # re-inject after sidebar (settings might have changed)

    st.title("🤖 AI PM Assistant")
    st.caption(f"Logged in as **{st.session_state.user['username']}**  ·  Knowledge Hub · Meeting Assistant · Risk Analyzer · Your Assistant")

    tab_knowledge, tab_meeting, tab_risk, tab_assistant = st.tabs([
        "📄 Knowledge Hub",
        "📝 Meeting Assistant",
        "⚠️ Risk Analyzer",
        "🤖 Your Assistant",
    ])

    # ════════════════════════════════════════════════
    # TAB 1 — KNOWLEDGE HUB
    # ════════════════════════════════════════════════
    with tab_knowledge:
        st.markdown('<div class="sec-label">Knowledge Hub — document search</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="upload-hint">📂 Upload one or more <b>.txt</b> or <b>.pdf</b> documents and then ask a question. '
            'Answers will be based only on the uploaded content.</div>',
            unsafe_allow_html=True
        )
        up_files = st.file_uploader(
            "Documents", type=["txt", "pdf"],
            accept_multiple_files=True,
            key="k_uploader",
            label_visibility="collapsed"
        )

        if up_files:
            new_names = [f.name for f in up_files]
            if new_names != st.session_state.knowledge_uploaded_files:
                st.session_state.knowledge_uploaded_files = new_names
                st.session_state.knowledge_db = None
                st.session_state.knowledge_qa_history = []

        if st.session_state.knowledge_uploaded_files:
            st.success(f"✅ Uploaded: {', '.join(st.session_state.knowledge_uploaded_files)}")
            st.markdown("#### 🔍 Q&A with your documents")
            
            # Display Q&A history
            if st.session_state.knowledge_qa_history:
                st.markdown("**📋 Conversation History:**")
                for i, qa in enumerate(st.session_state.knowledge_qa_history):
                    st.markdown(f'<div style="background: {st.session_state.accent_color}15; padding: 10px; border-radius: 5px; margin: 8px 0;"><b>Q{i+1}:</b> {qa["query"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background: #f5f5f5; padding: 10px; border-radius: 5px; margin: 4px 0 12px 0;"><b>A{i+1}:</b> {qa["answer"]}</div>', unsafe_allow_html=True)
                st.markdown("---")
            
            # Ask follow-up or new question
            col1, col2 = st.columns([4, 1])
            with col1:
                k_query_new = st.text_input(
                    "Ask another question",
                    key="k_query_input",
                    placeholder="🔍 Ask something related to the uploaded documents...",
                    label_visibility="collapsed"
                )
            with col2:
                if st.button("Search 🔍", key="k_search", use_container_width=True):
                    if not k_query_new.strip():
                        st.warning("Please type a question before searching.")
                    else:
                        if st.session_state.knowledge_db is None:
                            with st.spinner("Building the document knowledge base…"):
                                docs = load_uploaded_documents(up_files)
                                st.session_state.knowledge_db = create_vector_db(docs)
                                if st.session_state.knowledge_db is None:
                                    st.error("Unable to load the document content. Please try again.")
                                    st.stop()
                        with st.spinner("Searching the uploaded documents…"):
                            answer = ask_rag(
                                st.session_state.knowledge_db,
                                k_query_new,
                                model_name=st.session_state.model_name
                            )
                            if answer and answer.strip():
                                st.session_state.knowledge_qa_history.append({
                                    "query": k_query_new,
                                    "answer": answer
                                })
                            else:
                                st.warning("ℹ️ No information found in the document for this question. Please try a different question.")
                            st.rerun()
        else:
            st.caption("⬆ Upload one or more .txt or .pdf files above to start searching document content.")

        if st.button("🧹 Clean", key="k_clean", use_container_width=False):
            st.session_state.knowledge_uploaded_files = []
            st.session_state.knowledge_db = None
            st.session_state.knowledge_qa_history = []
            st.rerun()

    # ════════════════════════════════════════════════
    # TAB 2 — MEETING ASSISTANT
    # ════════════════════════════════════════════════
    with tab_meeting:
        st.markdown('<div class="sec-label">Meeting Assistant — summary and follow-up</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="upload-hint">📋 This page prepares a meeting summary from the uploaded transcription. ' 
            'By default it extracts Participants, date & time, Decisions made, and Action items. ' 
            'If you need more detail from the call, ask in the box below.</div>',
            unsafe_allow_html=True
        )
        meet_file = st.file_uploader(
            "Meeting notes", type=["txt", "docx"],
            key="meet_uploader", label_visibility="collapsed"
        )

        st.markdown("---")

        file_content = None
        if meet_file is not None:
            file_content = read_uploaded_file(meet_file)
            if file_content.startswith("❌"):
                st.error(file_content)
            else:
                st.session_state.meeting_raw_content = file_content
                st.session_state.meeting_loaded_name = meet_file.name

        if not st.session_state.meeting_raw_content:
            st.caption("⬆ Upload a .txt or .docx file above, then click Summary of Meeting.")
        else:
            st.success(f"✅ Loaded: {st.session_state.meeting_loaded_name}")
            st.markdown(
                "This page will extract the default information below. If you want something else from the meeting notes, ask in the follow-up box."
            )

            ma, mb = st.columns([3, 1])
            with ma:
                if st.button("📝 Summary of Meeting", key="m_analyze", use_container_width=True):
                    with st.spinner("Summarizing meeting notes…"):
                        summary = summarize_meeting(st.session_state.meeting_raw_content)
                    st.session_state.meeting_output = summary
                    st.rerun()
            with mb:
                if st.button("🧹 Clean", key="m_clean", use_container_width=True):
                    st.session_state.meeting_output = ""
                    st.session_state.meeting_raw_content = ""
                    st.session_state.meeting_loaded_name = ""
                    st.session_state.meeting_followup_answer = ""
                    st.rerun()

            if st.session_state.meeting_output:
                st.markdown("### 📋 Meeting Summary")
                st.text_area("", st.session_state.meeting_output, height=340,
                             key="m_output", label_visibility="collapsed")

                # ── Follow-up section appears AFTER summary is generated ───
                st.markdown("---")
                st.markdown("#### Ask a follow-up question about this meeting")
                follow_input = st.text_input(
                    "Ask for more details from the meeting notes.",
                    key="meeting_followup_input",
                    placeholder="🔍 Ask a follow-up question related to the uploaded meeting notes...",
                    label_visibility="collapsed"
                )
                if st.button("Search 🔍", key="m_followup", use_container_width=False):
                    if not follow_input.strip():
                        st.warning("Please write a follow-up question.")
                    else:
                        with st.spinner("Checking the meeting notes…"):
                            st.session_state.meeting_followup_answer = ask_with_context(
                                st.session_state.meeting_raw_content,
                                follow_input,
                                model_name=st.session_state.model_name
                            )
                        st.rerun()
                
                if st.session_state.meeting_followup_answer:
                    st.markdown("### 💬 Follow-up Answer")
                    st.text_area("", st.session_state.meeting_followup_answer, height=200,
                                 key="m_followup_answer", label_visibility="collapsed")

    # ════════════════════════════════════════════════
    # TAB 3 — RISK ANALYZER
    # ════════════════════════════════════════════════
    with tab_risk:
        st.markdown('<div class="sec-label">Upload project document</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="upload-hint">📁 Upload a <b>.txt</b> or <b>.docx</b> project description. '
            'The assistant will identify risks, impacts, dependencies and scenarios.</div>',
            unsafe_allow_html=True
        )
        risk_file = st.file_uploader(
            "Project document", type=["txt", "docx"],
            key="risk_uploader", label_visibility="collapsed"
        )

        user_input = ""
        if risk_file is not None:
            fc = risk_read_file(risk_file)
            if fc.startswith("❌"):
                st.error(fc)
            else:
                user_input = fc
                st.success(f"✅ Loaded: {risk_file.name}")

        st.markdown("---")

        if not user_input:
            st.caption("⬆ Upload a .txt or .docx file above, then click Analyze Risks.")
        else:
            ra, rb = st.columns([3, 1])
            with ra:
                if st.button("🔍 Analyze Risks", key="r_analyze", use_container_width=True):
                    with st.spinner("Analyzing risks…"):
                        result = analyze_risk(user_input, model_name=st.session_state.model_name)
                    # Store in session state for display
                    st.session_state.risk_output = result
                    st.rerun()
            with rb:
                if st.button("🧹 Clean", key="r_clean", use_container_width=True):
                    st.session_state.risk_output = ""
                    st.rerun()

            # Display results
            if "risk_output" in st.session_state and st.session_state.risk_output:
                st.markdown("### 📊 Risk Analysis Report")
                st.markdown(st.session_state.risk_output)


    # ════════════════════════════════════════════════
    # TAB 4 — YOUR ASSISTANT
    # ════════════════════════════════════════════════
    with tab_assistant:
        st.markdown('<div class="sec-label">Your Assistant — powerful AI chat</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="upload-hint">💬 Ask me any question and I will do my best to give you a precise and helpful answer.</div>',
            unsafe_allow_html=True
        )

        # ── Simple chat interface: Query + Send button ───
        col_q, col_btn = st.columns([5, 1])
        
        with col_q:
            assistant_query_input = st.text_input(
                "Ask a question",
                placeholder="Type your question here...",
                label_visibility="collapsed"
            )
        
        with col_btn:
            st.write("")  # Spacer
            if st.button("🔍 Send", key="assistant_search", use_container_width=True):
                if not assistant_query_input.strip():
                    st.warning("Please enter a question before sending.")
                else:
                    with st.spinner("Generating answer…"):
                        st.session_state.assistant_answer = ask_general(
                            assistant_query_input,
                            model_name=st.session_state.model_name
                        )
                    st.rerun()

        # ── Display answer ────────────────────────
        if st.session_state.assistant_answer:
            st.markdown("### ✅ Answer")
            st.text_area("", st.session_state.assistant_answer, height=360,
                         key="assistant_answer_area", label_visibility="collapsed")
            
            # ── Clear button ──────────────────────────
            if st.button("🧹 Clear", key="assistant_clear", use_container_width=False):
                st.session_state.assistant_answer = ""
                st.rerun()

if st.session_state.user is None:
    auth_screen()
else:
    main_app()
