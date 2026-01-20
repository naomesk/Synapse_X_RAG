import streamlit as st

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Data Control Center",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# SYSTEM LOGIC (AI ASSISTANT)
# ======================================================
def system_response(user_input: str) -> str:
    text = user_input.lower()
    if "document" in text:
        return "📄 1 document loaded and available for analysis."
    elif "index" in text:
        return "📚 Vector index is up to date."
    elif "chunk" in text:
        return "🧩 8 chunks currently stored in memory."
    elif "status" in text:
        return "🟢 System operational. No issues detected."
    else:
        return "🤖 Query received. Searching indexed knowledge base..."

# ======================================================
# GLOBAL CSS
# ======================================================
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #070b18;
    color: #e5e7eb;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* ===== FIXED TOP BAR ===== */
.hmi-topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 72px;
    z-index: 1000;
    background: linear-gradient(90deg, #091a3a, #0b2a66);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 56px;
    box-shadow: 0 6px 30px rgba(0,0,0,0.7);
}

.hmi-title {
    font-size: 22px;
    font-weight: 800;
}

/* ===== NAV ===== */
.hmi-nav {
    display: flex;
    gap: 16px;
}

.hmi-nav button {
    background: rgba(255,255,255,0.06);
    color: #c7d7ff;
    border: 1px solid rgba(59,130,246,0.45);
    border-radius: 12px;
    padding: 9px 20px;
    cursor: pointer;
    font-weight: 600;
    transition: 0.25s;
}

.hmi-nav button:hover {
    background: #2563eb;
    color: white;
    box-shadow: 0 0 20px rgba(37,99,235,0.9);
}

/* ===== CONTENT OFFSET ===== */
.block-container {
    padding-top: 110px;
    padding-left: 56px;
    padding-right: 56px;
    padding-bottom: 40px;
}

/* ===== CARD ===== */
.hmi-card {
    background: linear-gradient(180deg, #0f1b38, #0a122b);
    border-radius: 22px;
    padding: 26px 30px;
    box-shadow: 0 14px 50px rgba(0,0,0,0.8);
    margin-bottom: 28px;
}

/* ===== STAT ROW ===== */
.stat-row {
    display: flex;
    gap: 36px;
    align-items: center;
}

.stat {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 500;
}

.dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
}

.blue { background: #3b82f6; }
.green { background: #22c55e; }
.purple { background: #a855f7; }

/* ===== CHAT ===== */
.stChatMessage.user {
    background: rgba(37,99,235,0.18);
    border-radius: 14px;
    padding: 14px;
}

.stChatMessage.assistant {
    background: rgba(34,197,94,0.15);
    border-radius: 14px;
    padding: 14px;
}

/* ===== INPUT ===== */
textarea, input {
    background-color: #0b1430 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE
# ======================================================
if "page" not in st.session_state:
    st.session_state.page = "overview"

if "chat" not in st.session_state:
    st.session_state.chat = []

# ======================================================
# TOP BAR
# ======================================================
st.markdown("""
<div class="hmi-topbar">
    <div class="hmi-title">🧠 AI Data Control Center</div>
    <div class="hmi-nav">
        <form method="get">
            <button name="page" value="overview">📊 Overview</button>
            <button name="page" value="chat">🤖 AI Assistant</button>
            <button name="page" value="query">🧠 Data Query</button>
            <button name="page" value="upload">⬆ Upload</button>
        </form>
    </div>
</div>
""", unsafe_allow_html=True)

params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

# ======================================================
# OVERVIEW PAGE (DOCUMENT STATS)
# ======================================================
if st.session_state.page == "overview":
    st.markdown("""
    <div class="hmi-card">
        <div class="stat-row">
            <div class="stat">
                <div class="dot blue"></div>
                <strong>1</strong> document
            </div>
            <div class="stat">
                <div class="dot green"></div>
                <strong>1</strong> indexed
            </div>
            <div class="stat">
                <div class="dot purple"></div>
                <strong>8</strong> chunks
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# CHAT PAGE
# ======================================================
elif st.session_state.page == "chat":
    st.markdown('<div class="hmi-card">', unsafe_allow_html=True)
    st.subheader("🤖 AI Knowledge Assistant")

    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.write(msg)

    user_input = st.chat_input("Ask about documents, indexing, chunks, or status…")
    if user_input:
        st.session_state.chat.append(("user", user_input))
        st.session_state.chat.append(("assistant", system_response(user_input)))
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# DATA QUERY PAGE
# ======================================================
elif st.session_state.page == "query":
    st.markdown('<div class="hmi-card">', unsafe_allow_html=True)
    st.subheader("🧠 Semantic Data Query")
    q = st.text_area("", placeholder="Find references to safety procedures…")
    if st.button("▶ Execute"):
        st.success("Query executed successfully")
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# UPLOAD PAGE
# ======================================================
elif st.session_state.page == "upload":
    st.markdown('<div class="hmi-card">', unsafe_allow_html=True)
    st.subheader("⬆ Upload Documents")
    f = st.file_uploader("Upload PDF / TXT / DOCX", type=["pdf","txt","docx"])
    if f:
        st.success(f"📄 {f.name} uploaded and ready for indexing")
    st.markdown('</div>', unsafe_allow_html=True)




