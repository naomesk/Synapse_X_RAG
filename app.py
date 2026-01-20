import streamlit as st

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="AI Agent Dashboard",
    layout="wide"
)

# ----------------------------
# Custom CSS (for closer visual match)
# ----------------------------
st.markdown("""
<style>
    .title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 18px;
        color: #4b5563;
        margin-top: 0px;
        margin-bottom: 20px;
    }
    .status-row {
        display: flex;
        gap: 24px;
        margin-bottom: 20px;
        color: #374151;
        font-size: 14px;
    }
    .status-dot {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .green { background-color: #22c55e; }
    .blue { background-color: #3b82f6; }

    .query-box {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        background: #ffffff;
    }

    .dataset-card {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        background: #ffffff;
        max-width: 520px;
    }

    .indexed-badge {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }

    .placeholder-box {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 60px;
        text-align: center;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown('<div class="title">AI Agent Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Offline HMI Data & Documentation Interface</div>',
    unsafe_allow_html=True
)

# ----------------------------
# Status indicators
# ----------------------------
st.markdown("""
<div class="status-row">
    <div><span class="status-dot green"></span>1 dataset loaded</div>
    <div><span class="status-dot blue"></span>System indexed</div>
    <div><span class="status-dot blue"></span>24 data segments</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Tabs
# ----------------------------
tab_query, tab_datasets, tab_upload = st.tabs(
    ["Data Query", "Datasets (1)", "Upload Data"]
)

# ======================================================
# Data Query Tab
# ======================================================
with tab_query:
    st.markdown('<div class="query-box">', unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            label="",
            placeholder="Ask a question about plant operations, equipment status, or system logs..."
        )
        st.caption("Press Enter to search through locally indexed operational data")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Run Query", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# Datasets Tab
# ======================================================
with tab_datasets:
    left, right = st.columns([1, 1])

    with left:
        st.markdown('<div class="dataset-card">', unsafe_allow_html=True)

        st.markdown("### 📄 Turbine_Operation_Logs_Q1")
        st.markdown("Uploaded Jan 14, 2026 • 24 data segments")

        col_a, col_b = st.columns([3, 1])
        with col_b:
            st.markdown('<span class="indexed-badge">Indexed</span>', unsafe_allow_html=True)

        st.markdown("")

        icon_col1, icon_col2, icon_col3 = st.columns(3)
        icon_col1.button("👁 View", use_container_width=True)
        icon_col2.button("🔄 Reindex", use_container_width=True)
        icon_col3.button("🗑 Delete", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="placeholder-box">
            📄<br><br>
            Select a dataset to view operational details
        </div>
        """, unsafe_allow_html=True)

# ======================================================
# Upload Data Tab
# ======================================================
with tab_upload:
    st.markdown("""
    <div class="placeholder-box">
        ⬆️<br><br>
        <strong>Upload Operational Data</strong><br><br>
        Supported formats: PDF<br><br>
        All data remains on the local power plant server (offline mode)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.file_uploader(
        label="",
        type=["pdf"],
        accept_multiple_files=False
    )





