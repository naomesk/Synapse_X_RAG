# pyright: reportMissingImports=false
from pathlib import Path
import shutil
import chromadb
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
)
from llama_index.core.prompts import PromptTemplate
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

Settings.llm = Ollama(
    model="llama3:8b",
    temperature=0.0,
    request_timeout=1500,
    context_window=16384,
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434",
    embed_batch_size=32,
)
CHROMA_PATH = "./chroma_db_universal"
STORAGE_PATH = "./index_storage_universal"
if Path(CHROMA_PATH).exists():
    shutil.rmtree(CHROMA_PATH)
if Path(STORAGE_PATH).exists():
    shutil.rmtree(STORAGE_PATH)
Path(CHROMA_PATH).mkdir()
Path(STORAGE_PATH).mkdir()
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
chroma_collection = chroma_client.get_or_create_collection(name="universal_rag_capstone")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

print("Loading documents...")
documents = SimpleDirectoryReader(
    input_dir="data",
    recursive=True,
    required_exts=[".pdf"],
    filename_as_id=True,
).load_data()
if not documents:
    raise RuntimeError("No documents found.")
print(f"Loaded {len(documents)} documents")
node_parser = SentenceSplitter(
    chunk_size=2048,
    chunk_overlap=512,
    paragraph_separator=r"\n{2,}",
    secondary_chunking_regex=r"[.!?]\s+",
)
print("Building index...")
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    transformations=[node_parser],
    show_progress=True,
)
index.storage_context.persist(persist_dir=STORAGE_PATH)
print("Index ready.")
qa_prompt = PromptTemplate(
    template="""
You are a STRICT document-based question answering system.
RULES (MUST FOLLOW):
- Use ONLY information from the provided context.
- Answer in a complete sentence if the question asks for a title, name, period, goal etc.
- Copy key phrases EXACTLY from the document.
- Do NOT add information that is not in the context.
- Do NOT paraphrase unless necessary for sentence structure.
- Do NOT explain or add extra words unless the question asks for explanation.
- If no exact information → respond EXACTLY with:
  "The information is not present in the provided documents."
Context:
{context_str}
Question:
{query_str}
Answer (complete sentence):
"""
)
query_engine = index.as_query_engine(
    similarity_top_k=200,
    response_mode="tree_summarize",
    text_qa_template=qa_prompt,
)
print("\nRAG READY\n")
while True:
    q = input("Your question: ").strip()
    if q.lower() in {"exit", "quit", "q"}:
        break
    if not q:
        continue
    print("-" * 80)
    response = query_engine.query(q)
    print("\nANSWER:")
    print(response.response.strip())
    print("\nSOURCES:")
    for i, node in enumerate(response.source_nodes[:8], 1):
        fname = node.metadata.get("file_name", "unknown")
        page = node.metadata.get("page_label", "?")
        score = node.score or 0.0
        preview = node.text[:120].replace("\n", " ") + "..."
        print(f"{i}. [{score:.3f}] {fname} page {page}")
        print(f" {preview}\n")
