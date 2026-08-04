"""
Task 6 — Lexical Search Module (BM25).

Mặc định sử dụng BM25. Nếu dùng phương pháp khác (TF-IDF, Elasticsearch,
Weaviate BM25 built-in), hãy giải thích cơ chế trong buổi demo → +5 bonus.

Cài đặt:
    pip install rank-bm25

BM25 hoạt động thế nào:
    - Term Frequency (TF): từ xuất hiện nhiều trong document → điểm cao
    - Inverse Document Frequency (IDF): từ hiếm → quan trọng hơn
    - Document length normalization: document dài không bị ưu tiên quá mức
    - Formula: score(q,d) = Σ IDF(qi) * (tf(qi,d) * (k1+1)) / (tf(qi,d) + k1*(1-b+b*|d|/avgdl))
    - k1=1.5 (term saturation), b=0.75 (length normalization)
"""

import re
from pathlib import Path
from typing import List, Dict

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"

# Corpus loaded from standardized markdown files.
CORPUS: list[dict] = []  # List of {'content': str, 'metadata': dict}


def _normalize_text(text: str) -> str:
    """Chuẩn hoá text để token hoá tốt hơn."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokenize(text: str) -> list[str]:
    """Tách từ đơn giản cho BM25-like scoring."""
    return _normalize_text(text).split()


def build_bm25_index(corpus: list[dict]):
    """
    Xây dựng BM25 index từ corpus.

    Args:
        corpus: List of {'content': str, 'metadata': dict}
    """
    global CORPUS
    CORPUS = corpus

    if not corpus:
        return None

    return {
        "corpus": corpus,
        "tokenized_corpus": [_tokenize(doc.get("content", "")) for doc in corpus],
    }


def _load_corpus_from_disk() -> list[dict]:
    """Đọc markdown từ data/standardized/ nếu corpus chưa được cung cấp."""
    documents: list[dict] = []
    if not STANDARDIZED_DIR.exists():
        return documents

    for md_file in sorted(STANDARDIZED_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        metadata = {
            "source": md_file.name,
            "type": "legal" if "legal" in str(md_file) else "news",
        }
        documents.append({"content": content, "metadata": metadata})

    return documents


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa sử dụng BM25-like scoring.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict
        }
        Sorted by score descending.
    """
    global CORPUS
    if not CORPUS:
        CORPUS = _load_corpus_from_disk()

    if not CORPUS:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    # Simple BM25-like implementation without external dependency.
    doc_term_freqs = []
    doc_lengths = []
    for doc in CORPUS:
        tokens = _tokenize(doc.get("content", ""))
        doc_term_freqs.append({token: tokens.count(token) for token in set(tokens)})
        doc_lengths.append(len(tokens))

    avg_len = sum(doc_lengths) / max(1, len(doc_lengths))
    doc_freq = {}
    for tf_map in doc_term_freqs:
        for term in tf_map:
            doc_freq[term] = doc_freq.get(term, 0) + 1

    results = []
    for idx, doc in enumerate(CORPUS):
        score = 0.0
        for term in query_tokens:
            if term not in doc_term_freqs[idx]:
                continue
            tf = doc_term_freqs[idx][term]
            df = doc_freq.get(term, 1)
            idf = max(0.1, 1.0 + (len(CORPUS) - df + 0.5) / (df + 0.5))
            norm = 1.0 + 1.5 * (1.0 - 0.75 + 0.75 * (doc_lengths[idx] / max(1.0, avg_len)))
            score += idf * (tf * (1.5 + 1)) / (tf + 1.5 * norm)

        if score > 0:
            results.append({
                "content": doc.get("content", ""),
                "score": round(float(score), 4),
                "metadata": doc.get("metadata", {}),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max(1, top_k)]


if __name__ == "__main__":
    # Test
    results = lexical_search("phương thức thanh toán shopee", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
