"""
Task 7 — Reranking Module (Reciprocal Rank Fusion - RRF).

Ý tưởng cốt lõi:
    Áp dụng thuật toán Reciprocal Rank Fusion:
        RRF(d) = Σ 1 / (60 + r(d))
    để gộp thứ hạng từ Semantic Search và BM25 mà không bị ảnh hưởng bởi khác biệt thang điểm.
"""

from typing import Optional, Union


def rerank_rrf(
    ranked_lists: Union[list[list[dict]], list[dict]],
    top_k: int = 5,
    k: int = 60
) -> list[dict]:
    """
    Reciprocal Rank Fusion — gộp kết quả từ nhiều danh sách ranker.

    RRF(d) = Σ 1 / (k + rank_r(d))

    Args:
        ranked_lists: List các danh sách kết quả (mỗi list từ 1 ranker)
        top_k: Số lượng kết quả cuối cùng
        k: Smoothing constant (mặc định k=60 theo paper Cormack et al. 2009)

    Returns:
        Danh sách top_k candidates đã xếp hạng lại theo RRF score giảm dần.
    """
    if not ranked_lists:
        return []

    # Xử lý trường hợp truyền vào 1 danh sách candidates đơn lẻ
    if isinstance(ranked_lists, list) and len(ranked_lists) > 0 and isinstance(ranked_lists[0], dict):
        ranked_lists = [ranked_lists]

    rrf_scores = {}
    item_map = {}

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, start=1):
            key = item.get("content", str(item))
            rrf_scores[key] = rrf_scores.get(key, 0.0) + (1.0 / (k + rank))
            if key not in item_map:
                item_map[key] = item.copy()

    # Sắp xếp theo điểm RRF giảm dần
    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for content, score in sorted_items[:top_k]:
        res_item = item_map[content].copy()
        res_item["score"] = score
        results.append(res_item)

    return results


def rerank_cross_encoder(
    query: str, candidates: list[dict], top_k: int = 5
) -> list[dict]:
    """
    Cross-encoder rerank fallback (RRF fallback nếu không có API key).
    """
    return rerank_rrf([candidates], top_k=top_k)


def rerank_mmr(
    query_embedding: list[float],
    candidates: list[dict],
    top_k: int = 5,
    lambda_param: float = 0.7,
) -> list[dict]:
    """
    MMR fallback.
    """
    return rerank_rrf([candidates], top_k=top_k)


def rerank(
    query: str,
    candidates: Union[list[dict], list[list[dict]]],
    top_k: int = 5,
    method: str = "rrf",
) -> list[dict]:
    """
    Giao diện Rerank hợp nhất.

    Args:
        query: Câu truy vấn
        candidates: Danh sách hoặc danh sách các danh sách candidates từ retrieval
        top_k: Số lượng kết quả sau rerank
        method: Phương pháp rerank ("rrf", "cross_encoder", "mmr")

    Returns:
        List of top_k reranked candidates.
    """
    if method == "rrf":
        return rerank_rrf(candidates, top_k=top_k)
    elif method == "cross_encoder":
        if isinstance(candidates, list) and len(candidates) > 0 and isinstance(candidates[0], list):
            return rerank_rrf(candidates, top_k=top_k)
        return rerank_cross_encoder(query, candidates, top_k=top_k)
    elif method == "mmr":
        if isinstance(candidates, list) and len(candidates) > 0 and isinstance(candidates[0], list):
            return rerank_rrf(candidates, top_k=top_k)
        return rerank_rrf([candidates], top_k=top_k)
    else:
        return rerank_rrf(candidates, top_k=top_k)


if __name__ == "__main__":
    print("=" * 50)
    print("Task 7: Reranking (Reciprocal Rank Fusion - RRF)")
    print("=" * 50)

    # Test với dữ liệu mẫu từ 2 nguồn (Semantic Search & BM25 Search)
    semantic_results = [
        {"content": "Chính sách đổi trả và hoàn tiền Lazada trong 30 ngày", "score": 0.88, "metadata": {"customer_role": "buyer"}},
        {"content": "Hướng dẫn sử dụng ví LazPayLater mua trước trả sau", "score": 0.75, "metadata": {"customer_role": "buyer"}},
        {"content": "Điều khoản sử dụng chung cho người mua và người bán", "score": 0.65, "metadata": {"customer_role": "both"}},
    ]

    bm25_results = [
        {"content": "Hướng dẫn sử dụng ví LazPayLater mua trước trả sau", "score": 12.5, "metadata": {"customer_role": "buyer"}},
        {"content": "Chính sách đổi trả và hoàn tiền Lazada trong 30 ngày", "score": 9.2, "metadata": {"customer_role": "buyer"}},
        {"content": "Quy định phí dịch vụ cho nhà bán hàng Lazada", "score": 7.1, "metadata": {"customer_role": "seller"}},
    ]

    print("\n--- Test RRF Fusion (Semantic + BM25) ---")
    fused_results = rerank_rrf([semantic_results, bm25_results], top_k=3)
    for i, r in enumerate(fused_results, 1):
        content_preview = r['content'][:50].replace('\n', ' ')
        print(f"Top {i} [RRF Score: {r['score']:.4f}] - {content_preview.encode('ascii', 'replace').decode('ascii')}")

    print("\n[OK] Task 7 completed successfully!")
