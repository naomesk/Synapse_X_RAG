import streamlit as st
import logging
import os
from typing import Dict, List
import random
from initialize_rag import RAGInitializer

# --- New Helper Function for File Saving ---
def save_uploaded_files(uploaded_files):
    """Saves files to the data/raw directory."""
    raw_path = "data/raw"
    if not os.path.exists(raw_path):
        os.makedirs(raw_path)
    
    saved_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(raw_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)
    return saved_paths

def process_query(query: str,
                 retriever,
                 reranker,
                 response_generator,
                 process_config: Dict,
                 send_nb_chunks_to_llm=1) -> Dict:
    try:
        if process_config['retrieval']['use_query_expansion']:
            expanded_query = response_generator.expand_query(query)
            logging.info(f"Expanded query: {expanded_query}")
        else:
            expanded_query = query
            
        if process_config['retrieval']['use_bm25']:
            retrieved_results = retriever.retrieve_with_method(
                expanded_query,
                method="hybrid",
                top_k=process_config['retrieval']['top_k']
            )
        else:
            retrieved_results = retriever.retrieve_with_method(
                expanded_query,
                method="vector",
                top_k=process_config['retrieval']['top_k']
            )
        
        if process_config['retrieval']['use_reranking']:
            reranked_results = reranker.rerank(
                query,
                [r.document for r in retrieved_results],
                top_k=send_nb_chunks_to_llm
            )
            relevant_docs = [r.document for r in reranked_results]
            best_score = reranked_results[0].score if reranked_results else 0.0
        else:
            relevant_docs = [r.document for r in retrieved_results]
            best_score = retrieved_results[0].score if retrieved_results else 0.0
        
        response_data = response_generator.generate_answer(
            query,
            relevant_docs,
            metadata={'retrieval_score': best_score}
        )
        
        return {
            'Query': query,
            'Response': response_data['response'],
            'Score': best_score,
            'Sources': relevant_docs
        }
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return {'Query': query, 'Response': "An error occurred.", 'Score': 0.0, 'Sources': []}

def initialize_session_state():
    if "rag_components" not in st.session_state:
        st.session_state.rag_components = None
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Ingestion"

def display_response(content: str, sources: List, score: float) -> None:
    formatted_content = content.replace("\n-", "\n\n-").replace("\n ", "\n").strip()
    st.subheader("Answer")
    st.markdown(formatted_content)

    if sources:
        with st.expander("View Sources Used"):
            for idx, source in enumerate(sources, 1):
                st.markdown(f"**Source {idx}:**")
                st.text_area(
                    label=f"Source {idx} content",
                    value="From : " + source.metadata.get("source", "unknown") + "\n\nContent : \n" + source.page_content,
                    height=200,
                    label_visibility="collapsed",
                    key=f"source_{idx}_{hash(source.page_content+str(random.random()*1000000))}",
                )

    if score is not None:
        normalized_score = max(0.0, min(abs(score), 1.0))
        st.progress(normalized_score, text=f"Confidence: {normalized_score:.2%}")
        def ensure_rag_initialized(force=False) -> bool:
    if st.session_state.rag_components is not None and not force:
        return True

    with st.spinner("Initializing RAG system..."):
        try:
            initializer = RAGInitializer("config/init_config.yaml", "config/process_config.yaml")
            components = initializer.initialize()
            components.retriever.initialize(components.original_chunks)
            st.session_state.rag_components = components
            return True
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return False

def render_ingestion_view():
    st.title("📂 Document Ingestion & Indexing")
    
    # --- New File Upload Section ---
    st.subheader("Upload New Documents")
    uploaded_files = st.file_uploader(
         "Upload Documents, Code, or Notebooks", 
        accept_multiple_files=True, 
        type=['pdf', 'txt', 'md', 'py', 'js', 'ts', 'java', 'ipynb', 'csv']
    )
    
    if st.button("🚀 Upload and Rebuild Index", type="primary"):
        if uploaded_files:
            save_uploaded_files(uploaded_files)
            st.success(f"Saved {len(uploaded_files)} files to data/raw")
        
        if ensure_rag_initialized(force=True):
            st.success("RAG Index rebuilt successfully with new documents!")

    st.divider()
    components = st.session_state.rag_components
    if components is not None:
        st.subheader("Current Index Summary")
        num_chunks = len(components.original_chunks)
        unique_sources = len({c.metadata.get("source", "unknown") for c in components.original_chunks})
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Chunks", num_chunks)
        with col2: st.metric("Source Files", unique_sources)
        with col3: st.metric("LLM Context Chunks", components.process_config["retrieval"]["send_nb_chunks_to_llm"])

def render_query_view():
    st.title("🔍 Query Input & Response")
    if not ensure_rag_initialized(): st.stop()

    components = st.session_state.rag_components
    
    # Используем форму, чтобы ввод текста и кнопка работали как одно целое
    with st.form(key='query_form'):
        query = st.text_area("Enter your question", value="", height=100)
        submit_button = st.form_submit_button(label='Run Query')

    if submit_button and query.strip():
        # СРАЗУ очищаем старый результат, чтобы он не "маячил"
        st.session_state.last_result = None
        st.session_state.last_query = query
        
        with st.spinner("Thinking..."):
            result = process_query(
                query, 
                components.retriever, 
                components.reranker, 
                components.response_generator, 
                components.process_config, 
                components.process_config["retrieval"]["send_nb_chunks_to_llm"]
            )
            st.session_state.last_result = result
            # Вынуждаем Streamlit обновить экран сразу после получения результата
            st.rerun() 

    # Отображаем результат только если он есть
    if st.session_state.last_result:
        display_response(
            st.session_state.last_result["Response"], 
            st.session_state.last_result["Sources"], 
            st.session_state.last_result["Score"]
        )
def render_dashboard_view():
    st.title("📊 RAG Processing Dashboard")
    components = st.session_state.rag_components
    if components is None:
        st.info("System not initialized.")
        return

    st.subheader("Data & Index Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chunks", len(components.original_chunks))
    col2.metric("Files", len({c.metadata.get("source", "unknown") for c in components.original_chunks}))
    col3.metric("Train Data", len(components.train_df) if components.train_df is not None else 0)
    col4.metric("Test Data", len(components.test_df) if components.test_df is not None else 0)

def main():
    st.set_page_config(page_title="Offline RAG Demo", layout="wide")
    initialize_session_state()
    # --- Presentable Button Navigation ---
    with st.sidebar:
        st.title("Navigation")
        st.markdown("---")
        if st.button("📁 1. Ingestion & Upload"):
            st.session_state.active_tab = "Ingestion"
        if st.button("🔍 2. Query & Answer"):
            st.session_state.active_tab = "Query"
        if st.button("📊 3. System Dashboard"):
            st.session_state.active_tab = "Dashboard"
        st.markdown("---")
        st.caption("Status: Connected (Local)")

    # Routing
    if st.session_state.active_tab == "Ingestion":
        render_ingestion_view()
    elif st.session_state.active_tab == "Query":
        render_query_view()
    else:
        render_dashboard_view()

if name == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()