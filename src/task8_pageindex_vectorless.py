"""
Task 8 — PageIndex Vectorless RAG.

Đăng ký tài khoản tại: https://pageindex.ai/
SDK & sample code: https://github.com/VectifyAI/PageIndex

PageIndex cho phép RAG mà không cần vector store — sử dụng
structural understanding của document thay vì embedding.

Cài đặt:
    pip install pageindex

Hướng dẫn:
    1. Đăng ký account tại pageindex.ai
    2. Lấy API key
    3. Upload documents
    4. Query sử dụng PageIndex API

Lưu ý: API `/retrieval` của PageIndex hiện đã deprecated (vẫn hoạt động, nhưng response
có field "deprecation" cảnh báo) và trả kết quả trong "retrieved_nodes" — mỗi node có
"relevant_contents": list[list[{section_title, relevant_content}]]. In response thật ra
(json.dumps(...)) trước khi viết logic parse, đừng đoán schema từ ví dụ code cũ.
"""

import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv

try:
    from fpdf import FPDF
except Exception:  # pragma: no cover - optional dependency
    FPDF = None

try:
    from pageindex.client import PageIndexClient
except Exception:  # pragma: no cover - optional dependency
    PageIndexClient = None

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
PDF_DIR = Path(__file__).parent.parent / "data" / "pdf"
DOC_ID_FILE = Path(__file__).parent.parent / "data" / "pageindex_doc_ids.json"


def _register_unicode_font(pdf):
    if FPDF is None:
        return None

    candidates = []
    if os.name == "nt":
        candidates.extend(
            [
                r"C:\Windows\Fonts\arialuni.ttf",
                r"C:\Windows\Fonts\arial.ttf",
                r"C:\Windows\Fonts\simsun.ttc",
                r"C:\Windows\Fonts\msgothic.ttc",
                r"C:\Windows\Fonts\msyh.ttc",
            ]
        )
    else:
        candidates.extend(
            [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/opentype/noto/NotoSans-Regular.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ]
        )

    for font_path in candidates:
        if not os.path.exists(font_path):
            continue
        try:
            pdf.add_font("UnicodeFont", "", font_path, uni=True)
            return "UnicodeFont"
        except Exception:
            continue

    return None


def _fallback_search(query: str, top_k: int = 5):
    terms = [term for term in re.findall(r"\w+", query.lower()) if len(term) > 2]
    if not terms:
        return []

    results = []
    for md_file in sorted(STANDARDIZED_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        text_lower = text.lower()
        score = sum(1 for term in terms if term in text_lower)

        if score > 0:
            snippets = [line.strip() for line in text.splitlines() if line.strip()]
            snippet = " ".join(snippets[:3])[:180]
            results.append(
                {
                    "content": snippet or md_file.stem,
                    "score": float(score),
                    "metadata": {
                        "document": md_file.name,
                        "section": "local_fallback",
                    },
                    "source": "pageindex",
                }
            )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


def upload_documents():
    PDF_DIR.mkdir(exist_ok=True)

    if not PAGEINDEX_API_KEY or PageIndexClient is None:
        print("⚠ PageIndex unavailable or API key missing; skipping upload.")
        return {}

    if FPDF is None:
        print("⚠ fpdf2 not installed; skipping PDF generation.")
        return {}

    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
    doc_ids = {}

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        pdf_path = PDF_DIR / f"{md_file.stem}.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(True, margin=15)

        unicode_font = _register_unicode_font(pdf)
        if unicode_font:
            pdf.set_font(unicode_font, size=10)
        else:
            pdf.set_font("Helvetica", size=10)

        with open(md_file, encoding="utf-8") as handle:
            for line in handle:
                pdf.multi_cell(0, 6, line)

        pdf.output(str(pdf_path))

        print(f"Uploading {pdf_path.name}...")

        try:
            resp = client.submit_document(str(pdf_path))
            print(resp)
            doc_id = resp.get("doc_id") or resp.get("id")

            if doc_id:
                doc_ids[pdf_path.name] = doc_id
                print(f"✓ Uploaded -> {doc_id}")
        except Exception as exc:  # pragma: no cover - network/external service
            print(f"⚠ Failed to upload {pdf_path.name}: {exc}")

    with open(DOC_ID_FILE, "w", encoding="utf-8") as handle:
        json.dump(doc_ids, handle, indent=2, ensure_ascii=False)

    return doc_ids


def pageindex_search(query: str, top_k: int = 5):
    if not PAGEINDEX_API_KEY or PageIndexClient is None:
        return _fallback_search(query, top_k)

    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    try:
        with open(DOC_ID_FILE, encoding="utf-8") as handle:
            doc_ids = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        doc_ids = upload_documents()

    if not doc_ids:
        return _fallback_search(query, top_k)

    results = []

    for doc_name, doc_id in doc_ids.items():
        try:
            resp = client.submit_query(doc_id, query)
            retrieval_id = resp.get("retrieval_id") or resp.get("id")

            retrieval = {}
            for _ in range(20):
                retrieval = client.get_retrieval(retrieval_id)
                if retrieval.get("status") == "completed":
                    break
                time.sleep(1)

            rank = 0
            for node in retrieval.get("retrieved_nodes", []):
                for group in node.get("relevant_contents", []):
                    for item in group:
                        results.append(
                            {
                                "content": item.get("relevant_content", ""),
                                "score": 1.0 / (rank + 1),
                                "metadata": {
                                    "document": doc_name,
                                    "section": item.get("section_title", ""),
                                },
                                "source": "pageindex",
                            }
                        )
                        rank += 1
        except Exception as exc:  # pragma: no cover - network/external service
            print(f"⚠ PageIndex query failed for {doc_name}: {exc}")

    results.sort(key=lambda item: item["score"], reverse=True)

    if results:
        return results[:top_k]

    return _fallback_search(query, top_k)


if __name__ == "__main__":
    if not PAGEINDEX_API_KEY:
        print("⚠ Hãy set PAGEINDEX_API_KEY trong file .env")
        print("  Đăng ký tại: https://pageindex.ai/")
    else:
        print("Uploading documents...")
        upload_documents()

        print("\nTest query:")
        results = pageindex_search("danh sách sản phẩm cấm đăng bán", top_k=3)
        for result in results:
            print(f"[{result['score']:.3f}] {result['content'][:100]}...")
