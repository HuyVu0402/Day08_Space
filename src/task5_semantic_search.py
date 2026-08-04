from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional dependency
    SentenceTransformer = None

try:
    import chromadb
except Exception:  # pragma: no cover - optional dependency
    chromadb = None

CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "ecommerce_support_docs"
EMBEDDING_MODEL = "BAAI/bge-m3"


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Dense retrieval bằng cosine similarity trên ChromaDB.
    """

    if SentenceTransformer is None or chromadb is None:
        return []

    # Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Embed query
    query_embedding = model.encode(query).tolist()

    # Load Chroma collection
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    # Search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    output = []

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        score = max(0.0, 1.0 - dist)

        output.append(
            {
                "content": doc,
                "score": round(score, 4),
                "metadata": meta,
            }
        )

    output.sort(key=lambda x: x["score"], reverse=True)
    return output

if __name__ == "__main__":
    # Test
    results = semantic_search("quy định trả hàng hoàn tiền shopee", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
