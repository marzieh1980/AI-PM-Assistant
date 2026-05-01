import streamlit as st
import uuid
from datetime import datetime
from rag_core import load_documents, load_uploaded_documents, create_vector_db, ask_rag
from meeting_assistant import summarize_meeting, read_uploaded_file
from risk_analyzer import analyze_risk, read_uploaded_file as risk_read_file

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="AI PM Assistant", layout="wide")

# ─────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "model_name":       "llama-3.2-3b-instruct:2",
        "font_size":        15,
        "accent_color":     "#4F8EF7",
        "sidebar_color":    "#1C2333",
        "show_settings":    False,
        "chat_list":        [],
        "active_chat_id":   None,
        "local_db":         None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# DYNAMIC CSS
# ─────────────────────────────────────────────
accent = st.session_state.accent_color
fs     = st.session_state.font_size
sbg    = st.session_state.sidebar_color

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: {fs}px;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] > div:first-child {{
    background: {sbg};
    padding-top: 1rem;
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
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background: {accent}33;
    border-color: {accent};
}}

/* ── Main buttons ── */
.stButton > button {{
    border-radius: 8px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    border-bottom: 2px solid #e0e4ef44;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    letter-spacing: 0.05em;
    padding: 8px 20px;
    border-radius: 8px 8px 0 0;
    background: transparent;
    color: #8892a4;
    border: none;
}}
.stTabs [aria-selected="true"] {{
    color: {accent} !important;
    background: {accent}18 !important;
    border-bottom: 2px solid {accent} !important;
}}

/* ── Chat bubbles ── */
.msg-user {{
    background: {accent}18;
    border-left: 3px solid {accent};
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    margin: 6px 0;
    font-size: {fs}px;
    line-height: 1.55;
}}
.msg-bot {{
    background: #f4f6fb;
    border-left: 3px solid #c5cad6;
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    margin: 6px 0;
    font-size: {fs}px;
    line-height: 1.55;
    color: #2a2f3d;
}}

/* ── Small section labels ── */
.section-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8892a4;
    margin: 16px 0 6px 0;
}}

/* ── Sidebar group headers ── */
.chat-group {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: {accent} !important;
    margin: 14px 0 4px 4px;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT HELPERS
# ─────────────────────────────────────────────
TAB_LABELS = {
    "knowledge": "📄 Knowledge",
    "meeting":   "📝 Meeting",
    "risk":      "⚠️ Risk",
}

def get_chat(cid):
    for c in st.session_state.chat_list:
        if c["id"] == cid:
            return c
    return None

def get_active_chat():
    return get_chat(st.session_state.active_chat_id)

def create_new_chat(tab="knowledge"):
    cid = str(uuid.uuid4())
    n = sum(1 for c in st.session_state.chat_list if c["tab"] == tab) + 1
    chat = {
        "id":             cid,
        "name":           f"New {TAB_LABELS[tab].split()[-1]} {n}",
        "tab":            tab,
        "messages":       [],
        "system_prompt":  "",
        "upload_db":      None,
        "uploaded_files": [],
        "meeting_output": "",
        "risk_output":    "",
        "created_at":     datetime.now().strftime("%d/%m %H:%M"),
    }
    st.session_state.chat_list.insert(0, chat)
    st.session_state.active_chat_id = cid
    return chat

def delete_chat(cid):
    st.session_state.chat_list = [c for c in st.session_state.chat_list if c["id"] != cid]
    remaining = st.session_state.chat_list
    st.session_state.active_chat_id = remaining[0]["id"] if remaining else None

def auto_name(chat, text):
    prefix = f"New {TAB_LABELS[chat['tab']].split()[-1]}"
    if chat["name"].startswith(prefix):
        chat["name"] = text[:36] + ("…" if len(text) > 36 else "")

def get_tab_active(tab_key):
    """Return the active chat if it matches tab, else first chat for that tab, else None."""
    active = get_active_chat()
    if active and active["tab"] == tab_key:
        return active
    tab_chats = [c for c in st.session_state.chat_list if c["tab"] == tab_key]
    return tab_chats[0] if tab_chats else None


# ─────────────────────────────────────────────
# LOAD DEFAULT KNOWLEDGE DB
# ─────────────────────────────────────────────
@st.cache_resource
def setup_local_db():
    return create_vector_db(load_documents())

if st.session_state.local_db is None:
    st.session_state.local_db = setup_local_db()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 AI PM")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings
    with c2:
        if st.button("➕ New Chat", use_container_width=True):
            create_new_chat("knowledge")
            st.rerun()

    if st.session_state.show_settings:
        st.markdown("#### ⚙️ Settings")
        new_model  = st.text_input("LM Studio model", value=st.session_state.model_name)
        new_font   = st.slider("Font size", 12, 22, st.session_state.font_size)
        new_accent = st.color_picker("Accent color", st.session_state.accent_color)
        new_sbg    = st.color_picker("Sidebar color", st.session_state.sidebar_color)
        if st.button("💾 Save Settings"):
            st.session_state.model_name    = new_model
            st.session_state.font_size     = new_font
            st.session_state.accent_color  = new_accent
            st.session_state.sidebar_color = new_sbg
            st.session_state.show_settings = False
            st.rerun()
        st.markdown("---")

    # Chat list grouped by tab
    if not st.session_state.chat_list:
        st.caption("No saved chats yet.\nCreate one from any tab.")
    else:
        for tab_key, tab_label in TAB_LABELS.items():
            tab_chats = [c for c in st.session_state.chat_list if c["tab"] == tab_key]
            if not tab_chats:
                continue
            st.markdown(f'<div class="chat-group">{tab_label}</div>', unsafe_allow_html=True)
            for chat in tab_chats:
                is_active = chat["id"] == st.session_state.active_chat_id
                icon = "▶ " if is_active else "   "
                ca, cb = st.columns([5, 1])
                with ca:
                    if st.button(f"{icon}{chat['name']}", key=f"sel_{chat['id']}", use_container_width=True):
                        st.session_state.active_chat_id = chat["id"]
                        st.rerun()
                with cb:
                    if st.button("✕", key=f"del_{chat['id']}"):
                        delete_chat(chat["id"])
                        st.rerun()


# ─────────────────────────────────────────────
# MAIN AREA — 3 TABS
# ─────────────────────────────────────────────
st.title("🤖 AI PM Assistant")
st.caption("IT project manager AI · Knowledge Hub · Meeting Assistant · Risk Analyzer")

tab_knowledge, tab_meeting, tab_risk = st.tabs([
    "📄 Knowledge Hub",
    "📝 Meeting Assistant",
    "⚠️ Risk Analyzer",
])


# ════════════════════════════════════════════════════════
# TAB 1 — KNOWLEDGE HUB
# ════════════════════════════════════════════════════════
with tab_knowledge:

    cur_k = get_tab_active("knowledge")

    # ── Row 1: Upload + New Chat ─────────────────────────
    st.markdown('<div class="section-label">Document source</div>', unsafe_allow_html=True)
    r1a, r1b, r1c = st.columns([3, 3, 1])
    with r1a:
        knowledge_mode = st.radio(
            "Source",
            ["📘 Default Knowledge", "📤 Upload Documents"],
            horizontal=True,
            label_visibility="collapsed",
            key="kmode_radio"
        )
    with r1b:
        if knowledge_mode == "📤 Upload Documents":
            up_files = st.file_uploader(
                "Upload .txt or .pdf",
                type=["txt", "pdf"],
                accept_multiple_files=True,
                key="k_uploader",
                label_visibility="collapsed"
            )
        else:
            up_files = None
            st.caption("Using documents from the `data/` folder.")
    with r1c:
        if st.button("➕ New Chat", use_container_width=True, key="new_k_chat"):
            cur_k = create_new_chat("knowledge")
            st.rerun()

    # Load uploaded docs button
    if up_files and cur_k and not cur_k["uploaded_files"]:
        if st.button("✅ Load documents into this chat", key="k_load_docs"):
            docs = load_uploaded_documents(up_files)
            cur_k["upload_db"] = create_vector_db(docs)
            cur_k["uploaded_files"] = [f.name for f in up_files]
            st.rerun()
    if cur_k and cur_k["uploaded_files"]:
        st.success(f"✅ Loaded: {', '.join(cur_k['uploaded_files'])}")

    st.markdown("---")

    if cur_k is None:
        st.info("👆 Click **➕ New Chat** to start a Knowledge Hub conversation.")
    else:
        # ── Row 2: Chat name | Prompt ────────────────────
        st.markdown('<div class="section-label">Chat · name and copilot prompt</div>', unsafe_allow_html=True)
        r2a, r2b = st.columns([2, 5])
        with r2a:
            new_kname = st.text_input(
                "name", value=cur_k["name"],
                key=f"kname_{cur_k['id']}",
                label_visibility="collapsed",
                placeholder="Chat name…"
            )
            if new_kname != cur_k["name"]:
                cur_k["name"] = new_kname
        with r2b:
            k_sysp = st.text_input(
                "prompt", value=cur_k.get("system_prompt", ""),
                key=f"ksysp_{cur_k['id']}",
                label_visibility="collapsed",
                placeholder="Optional copilot prompt — e.g. 'You are a security analyst. Always be concise.'"
            )
            cur_k["system_prompt"] = k_sysp

        # ── Conversation history ─────────────────────────
        for msg in cur_k["messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user">🧑 {msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-bot">🤖 {msg["text"]}</div>', unsafe_allow_html=True)

        # ── Row 3: Question input + Send + Clear ─────────
        r3a, r3b, r3c = st.columns([6, 1, 1])
        with r3a:
            question = st.text_input(
                "q", placeholder="Ask something about your documents…",
                key=f"kq_{cur_k['id']}",
                label_visibility="collapsed"
            )
        with r3b:
            send_k = st.button("Send ▶", key=f"ksend_{cur_k['id']}", use_container_width=True)
        with r3c:
            if st.button("🗑️ Clear", key=f"kclr_{cur_k['id']}", use_container_width=True):
                cur_k["messages"] = []
                st.rerun()

        if send_k and question.strip():
            if knowledge_mode == "📤 Upload Documents":
                db = cur_k.get("upload_db")
                if db is None:
                    st.error("❌ Upload documents and click Load first.")
                    st.stop()
            else:
                db = st.session_state.local_db
                if db is None:
                    st.error("❌ No default knowledge. Add files to data/ folder.")
                    st.stop()
            with st.spinner("Thinking…"):
                response = ask_rag(db, question)
            auto_name(cur_k, question)
            cur_k["messages"].append({"role": "user", "text": question})
            cur_k["messages"].append({"role": "bot",  "text": response})
            st.rerun()


# ════════════════════════════════════════════════════════
# TAB 2 — MEETING ASSISTANT
# ════════════════════════════════════════════════════════
with tab_meeting:

    cur_m = get_tab_active("meeting")

    # ── Row 1: Upload + New Chat ─────────────────────────
    st.markdown('<div class="section-label">Meeting notes</div>', unsafe_allow_html=True)
    mr1a, mr1b = st.columns([5, 1])
    with mr1a:
        meet_file = st.file_uploader(
            "Upload meeting notes (.txt)",
            type=["txt"],
            key="meet_uploader",
            label_visibility="collapsed"
        )
    with mr1b:
        if st.button("➕ New Chat", use_container_width=True, key="new_m_chat"):
            cur_m = create_new_chat("meeting")
            st.rerun()

    st.markdown("---")

    if cur_m is None:
        st.info("👆 Click **➕ New Chat** to start a Meeting Assistant session.")
    else:
        # ── Row 2: Chat name | Prompt ────────────────────
        st.markdown('<div class="section-label">Chat · name and copilot prompt</div>', unsafe_allow_html=True)
        mr2a, mr2b = st.columns([2, 5])
        with mr2a:
            new_mname = st.text_input(
                "name", value=cur_m["name"],
                key=f"mname_{cur_m['id']}",
                label_visibility="collapsed",
                placeholder="Chat name…"
            )
            if new_mname != cur_m["name"]:
                cur_m["name"] = new_mname
        with mr2b:
            m_sysp = st.text_input(
                "prompt", value=cur_m.get("system_prompt", ""),
                key=f"msysp_{cur_m['id']}",
                label_visibility="collapsed",
                placeholder="Optional copilot prompt — e.g. 'Focus on action items only. Be concise.'"
            )
            cur_m["system_prompt"] = m_sysp

        # ── Conversation history ─────────────────────────
        for msg in cur_m["messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user">🧑 {msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-bot">🤖 {msg["text"]}</div>', unsafe_allow_html=True)

        # ── Meeting output ───────────────────────────────
        output = cur_m.get("meeting_output", "")
        if output:
            st.markdown("### 📌 Summary")
            st.text_area("", output, height=260, key=f"mout_{cur_m['id']}")

        # ── Row 3: Generate + Clear ──────────────────────
        mr3a, mr3b = st.columns([3, 1])
        with mr3a:
            if st.button("▶ Generate Summary", key=f"mgen_{cur_m['id']}", use_container_width=True,
                         disabled=(meet_file is None)):
                file_content = read_uploaded_file(meet_file)
                with st.spinner("Summarizing…"):
                    summary = summarize_meeting(file_content)
                cur_m["meeting_output"] = summary
                auto_name(cur_m, f"Meeting: {meet_file.name}")
                cur_m["messages"].append({"role": "user", "text": f"📄 {meet_file.name}"})
                cur_m["messages"].append({"role": "bot",  "text": summary})
                st.rerun()
        with mr3b:
            if st.button("🗑️ Clear", key=f"mclr_{cur_m['id']}", use_container_width=True):
                cur_m["meeting_output"] = ""
                cur_m["messages"] = []
                st.rerun()

        if meet_file is None:
            st.caption("⬆ Upload a .txt meeting file, then click Generate Summary.")


# ════════════════════════════════════════════════════════
# TAB 3 — RISK ANALYZER
# ════════════════════════════════════════════════════════
with tab_risk:

    cur_r = get_tab_active("risk")

    # ── Row 1: Input mode + Upload/Paste + New Chat ──────
    st.markdown('<div class="section-label">Project input</div>', unsafe_allow_html=True)
    rr1a, rr1b, rr1c = st.columns([2, 4, 1])
    with rr1a:
        risk_mode = st.radio(
            "Input",
            ["📤 Upload File", "📝 Paste Text"],
            horizontal=False,
            label_visibility="collapsed",
            key="risk_mode_radio"
        )
    with rr1b:
        user_input = ""
        if risk_mode == "📤 Upload File":
            risk_file = st.file_uploader(
                "Upload .txt or .docx",
                type=["txt", "docx"],
                key="risk_uploader",
                label_visibility="collapsed"
            )
            if risk_file is not None:
                fc = risk_read_file(risk_file)
                if fc.startswith("❌"):
                    st.error(fc)
                else:
                    user_input = fc
                    st.success(f"✅ {risk_file.name}")
        else:
            user_input = st.text_area(
                "desc", height=120,
                key="risk_text_area",
                label_visibility="collapsed",
                placeholder="Paste project description or requirements here…"
            )
    with rr1c:
        if st.button("➕ New Chat", use_container_width=True, key="new_r_chat"):
            cur_r = create_new_chat("risk")
            st.rerun()

    st.markdown("---")

    if cur_r is None:
        st.info("👆 Click **➕ New Chat** to start a Risk Analyzer session.")
    else:
        # ── Row 2: Chat name | Prompt ────────────────────
        st.markdown('<div class="section-label">Chat · name and copilot prompt</div>', unsafe_allow_html=True)
        rr2a, rr2b = st.columns([2, 5])
        with rr2a:
            new_rname = st.text_input(
                "name", value=cur_r["name"],
                key=f"rname_{cur_r['id']}",
                label_visibility="collapsed",
                placeholder="Chat name…"
            )
            if new_rname != cur_r["name"]:
                cur_r["name"] = new_rname
        with rr2b:
            r_sysp = st.text_input(
                "prompt", value=cur_r.get("system_prompt", ""),
                key=f"rsysp_{cur_r['id']}",
                label_visibility="collapsed",
                placeholder="Optional copilot prompt — e.g. 'Focus on SLA risks. Rate everything High/Medium/Low.'"
            )
            cur_r["system_prompt"] = r_sysp

        # ── Conversation history ─────────────────────────
        for msg in cur_r["messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user">🧑 {msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-bot">🤖 {msg["text"]}</div>', unsafe_allow_html=True)

        # ── Risk report output ───────────────────────────
        risk_out = cur_r.get("risk_output", "")
        if risk_out:
            st.markdown("### 📊 Risk Report")
            st.markdown(risk_out)

        # ── Row 3: Analyze + Clear ───────────────────────
        rr3a, rr3b = st.columns([3, 1])
        with rr3a:
            if st.button("🔍 Analyze Risks", key=f"ranalyze_{cur_r['id']}", use_container_width=True):
                if user_input.strip():
                    with st.spinner("Analyzing…"):
                        result = analyze_risk(user_input, model_name=st.session_state.model_name)
                    cur_r["risk_output"] = result
                    label = user_input[:40].replace("\n", " ")
                    auto_name(cur_r, label)
                    cur_r["messages"].append({"role": "user", "text": label})
                    cur_r["messages"].append({"role": "bot",  "text": result})
                    st.rerun()
                else:
                    st.warning("⚠️ Upload a file or paste text first.")
        with rr3b:
            if st.button("🗑️ Clear", key=f"rclr_{cur_r['id']}", use_container_width=True):
                cur_r["risk_output"] = ""
                cur_r["messages"] = []
                st.rerun()
