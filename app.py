import streamlit as st

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Industrial HMI Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# SYSTEM LOGIC
# =============================
def system_response(user_input: str) -> str:
    text = user_input.lower()
    if "temperature" in text:
        return "Temperature is within the normal operational range."
    elif "pressure" in text:
        return "Pressure levels are stable."
    elif "status" in text:
        return "All systems are operating normally."
    else:
        return "Request received. Analyzing operational data."

# =============================
# CSS — ONLY TOP PANEL
# =============================
st.markdown("""
<style>

/* hide streamlit chrome */
#MainMenu, footer, header {
    visibility: hidden;
}

/* top panel only */
.hmi-topbar {
    height: 64px;
    width: 100%;
    background: #0b1c3d;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 48px;
    box-sizing: border-box;
}

.hmi-title {
    color: white;
    font-size: 20px;
    font-weight: 600;
}

.hmi-nav {
    display: flex;
    gap: 14px;
}

.hmi-nav button {
    background: transparent;
    color: #c7d7ff;
    border: 1px solid #1f4ed8;
    border-radius: 6px;
    padding: 8px 16px;
    cursor: pointer;
}

.hmi-nav button:hover {
    background: #1f4ed8;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =============================
# SESSION STATE
# =============================
if "page" not in st.session_state:
    st.session_state.page = "chat"

if "chat" not in st.session_state:
    st.session_state.chat = []

# =============================
# TOP BAR
# =============================
st.markdown("""
<div class="hmi-topbar">
    <div class="hmi-title">Industrial HMI Dashboard</div>
    <div class="hmi-nav">
        <form method="get">
            <button name="page" value="chat">💬 AI Assistant</button>
            <button name="page" value="query">📊 Data Query</button>
            <button name="page" value="datasets">🗂 Datasets</button>
            <button name="page" value="upload">⬆ Upload Data</button>
        </form>
    </div>
</div>
""", unsafe_allow_html=True)

# read navigation
params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

# =============================
# CONTENT — DEFAULT STREAMLIT
# =============================
if st.session_state.page == "chat":
    st.subheader("AI Assistant")

    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.write(msg)

    user_input = st.chat_input("Ask about operations, data, anomalies…")
    if user_input:
        st.session_state.chat.append(("user", user_input))
        st.session_state.chat.append(("assistant", system_response(user_input)))
        st.rerun()

elif st.session_state.page == "query":
    st.subheader("Data Query")

    query = st.text_area(
        "",
        placeholder="SELECT * FROM operational_data WHERE temperature > 80"
    )

    if st.button("Run Query"):
        st.success("Query executed")
        st.write("Results will appear here")

elif st.session_state.page == "datasets":
    st.subheader("Datasets")
    st.write("• sensor_data.csv")
    st.write("• production_logs.xlsx")
    st.write("• energy_usage.json")

elif st.session_state.page == "upload":
    st.subheader("Upload Operational Data")

    file = st.file_uploader(
        "Upload operational data",
        type=["csv", "xlsx", "json"]
    )

    if file:
        st.success(f"{file.name} uploaded")



