"""
Task 4 — Chunking & Indexing vào Vector Store (ChromaDB) kèm metadata `customer_role`.

Nhiệm vụ:
    1. Đọc toàn bộ markdown files từ data/standardized/
    2. Chiết xuất metadata (bao gồm `customer_role`: buyer/seller/both)
    3. Split text bằng RecursiveCharacterTextSplitter
    4. Index vào ChromaDB collection `ecommerce_support_docs`
"""

import os
import sys
import site
from pathlib import Path

# Add user site packages if needed
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
CHUNKING_METHOD = "recursive"
EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DIM = 1024
VECTOR_STORE = "chromadb"
COLLECTION_NAME = "ecommerce_support_docs"


def extract_customer_role(content: str) -> str:
    """Trích xuất customer_role từ metadata header trong Markdown."""
    for line in content.splitlines():
        if "**Customer Role:**" in line:
            return line.split("**Customer Role:**")[-1].strip().lower()
    return "both"


def load_documents() -> list[dict]:
    """
    Đọc toàn bộ markdown files từ data/standardized/ kèm customer_role.
    """
    documents = []
    if not STANDARDIZED_DIR.exists():
        return documents

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        doc_type = "legal" if "legal" in str(md_file) else "news"
        role = extract_customer_role(content)
        documents.append({
            "content": content,
            "metadata": {
                "source": md_file.name,
                "type": doc_type,
                "customer_role": role,
            }
        })
    return documents


class SimpleTextSplitter:
    """Fallback text splitter when langchain_text_splitters is unavailable."""
    def __init__(self, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> list[str]:
        if len(text) <= self.chunk_size:
            return [text]
        chunks = []
        start = 0
        step = self.chunk_size - self.chunk_overlap
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            if end >= len(text):
                break
            start += step
        return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Chunk documents theo RecursiveCharacterTextSplitter và bảo toàn customer_role.
    """
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    except Exception:
        splitter = SimpleTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(splits):
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    **doc["metadata"],
                    "chunk_index": i,
                    "customer_role": doc["metadata"].get("customer_role", "both")
                }
            })
    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Embed toàn bộ chunks bằng sentence-transformers.
    """
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [c["content"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb.tolist()
    return chunks


def index_to_vectorstore(chunks: list[dict]):
    """
    Lưu chunks vào ChromaDB collection `ecommerce_support_docs`.
    """
    import chromadb

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [f"{c['metadata']['source']}_chunk_{c['metadata']['chunk_index']}" for c in chunks]
    collection.upsert(
        ids=ids,
        documents=[c["content"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )
    print(f"[OK] Indexed {len(chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'")


def run_pipeline():
    """Chạy toàn bộ pipeline: load → chunk → embed → index."""
    print("=" * 50)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: {VECTOR_STORE}")
    print("=" * 50)

    docs = load_documents()
    print(f"\n[OK] Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"[OK] Created {len(chunks)} chunks")

    chunks = embed_chunks(chunks)
    print(f"[OK] Embedded {len(chunks)} chunks")

    index_to_vectorstore(chunks)
    print("[OK] Task 4 pipeline finished successfully!")


if __name__ == "__main__":
    run_pipeline()
