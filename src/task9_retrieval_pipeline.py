"""
Task 9 — Retrieval Pipeline Hoàn Chỉnh.

Kết hợp semantic search + lexical search + reranking + PageIndex fallback
thành một pipeline thống nhất.
"""

import sys
from pathlib import Path

# Fix Windows console UTF-8 printing
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .task5_semantic_search import semantic_search
    from .task6_lexical_search import lexical_search
    from .task7_reranking import rerank, rerank_rrf
    from .task8_pageindex_vectorless import pageindex_search
except (ImportError, ValueError):
    from src.task5_semantic_search import semantic_search
    from src.task6_lexical_search import lexical_search
    from src.task7_reranking import rerank, rerank_rrf
    from src.task8_pageindex_vectorless import pageindex_search

# Configuration
SCORE_THRESHOLD = 0.48   # Nếu best score (cosine gốc) < threshold → fallback PageIndex
DEFAULT_TOP_K = 5
RERANK_METHOD = "rrf"


def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
    use_reranking: bool = True,
) -> list[dict]:
    """
    Retrieval pipeline hoàn chỉnh với fallback logic.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả cuối cùng
        score_threshold: Ngưỡng điểm cosine gốc tối thiểu (KHÔNG phải điểm RRF)
        use_reranking: Có áp dụng reranking hay không

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': str  # 'hybrid' hoặc 'pageindex'
        }
    """
    # Step 1: Song song chạy semantic + lexical
    dense_results = semantic_search(query, top_k=top_k * 2)
    sparse_results = lexical_search(query, top_k=top_k * 2)

    # Step 2: Kiểm tra threshold DÙNG ĐIỂM COSINE GỐC (dense_results), KHÔNG PHẢI RRF
    best_dense_score = dense_results[0]["score"] if dense_results else 0.0

    if best_dense_score < score_threshold:
        print(f"  [Fallback] Semantic best score ({best_dense_score:.3f}) < threshold ({score_threshold}) -> PageIndex Fallback")
        try:
            fallback = pageindex_search(query, top_k=top_k)
            if fallback:
                for item in fallback:
                    item["source"] = "pageindex"
                return fallback[:top_k]
        except Exception as e:
            print(f"  [Warning] PageIndex fallback error: {e}")

    # Step 3: Merge bằng RRF
    merged = rerank_rrf([dense_results, sparse_results], top_k=top_k * 2)
    for item in merged:
        item["source"] = "hybrid"

    # Step 4: Rerank
    if use_reranking and merged:
        final_results = rerank(query, merged, top_k=top_k, method=RERANK_METHOD)
    else:
        final_results = merged[:top_k]

    for item in final_results:
        item["source"] = "hybrid"

    return final_results[:top_k]


if __name__ == "__main__":
    print("=" * 60)
    print("Task 9: Retrieval Pipeline Test")
    print("=" * 60)

    test_queries = [
        "Chính sách đổi trả và hoàn tiền Lazada",
        "Ví LazPayLater thanh toán như thế nào",
        "xyzabc123nonsense_query_khong_ton_tai",  # Query không có kết quả -> test fallback
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print("-" * 60)
        results = retrieve(q, top_k=3)
        for i, r in enumerate(results, 1):
            clean_content = r['content'].replace("\n", " ")[:80]
            print(f"  {i}. [{r['score']:.4f}] [{r['source']}] {clean_content}...")
