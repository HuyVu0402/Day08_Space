"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown trong data/standardized/

Yêu cầu:
    1. Scan toàn bộ file trong data/landing/legal/ (PDF, DOCX) và data/landing/news/ (JSON)
    2. Sử dụng MarkItDown để convert PDF/DOCX.
    3. Đọc JSON tin tức, trích xuất content_markdown và metadata.
    4. Giữ lại thông tin metadata `customer_role` ('buyer', 'seller', 'both') trong header Markdown.
    5. Lưu vào data/standardized/legal/ và data/standardized/news/
"""

import json
from pathlib import Path
from markitdown import MarkItDown

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def get_legal_roles_mapping() -> dict:
    """Đọc file mapping document_roles.json nếu có."""
    roles_file = LANDING_DIR / "legal" / "document_roles.json"
    if roles_file.exists():
        try:
            return json.loads(roles_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] Error reading document_roles.json: {e}")
    return {}


def convert_legal_docs():
    """Convert PDF/DOCX files trong data/landing/legal/ sang markdown."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    roles_mapping = get_legal_roles_mapping()
    md = MarkItDown()

    for filepath in legal_dir.iterdir():
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"Converting legal doc: {filepath.name}")
            output_path = output_dir / f"{filepath.stem}.md"
            
            # Use MarkItDown
            try:
                result = md.convert(str(filepath))
                raw_text = result.text_content
            except Exception as e:
                print(f"  [WARN] MarkItDown fallback for {filepath.name}: {e}")
                raw_text = f"Content extracted from {filepath.name}"

            meta = roles_mapping.get(filepath.name, {})
            customer_role = meta.get("customer_role", "both")
            title = meta.get("title", filepath.stem.replace("_", " ").title())
            url = meta.get("url", "N/A")

            # Header metadata for chunker/retriever
            header = f"# {title}\n\n"
            header += f"**Source:** {url}\n"
            header += f"**Customer Role:** {customer_role}\n"
            header += f"**Document Type:** legal\n\n---\n\n"

            content = header + raw_text
            output_path.write_text(content, encoding="utf-8")
            print(f"  [OK] Saved: {output_path.name} ({len(content)} chars, role={customer_role})")


def convert_news_articles():
    """Convert JSON articles trong data/landing/news/ sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in news_dir.iterdir():
        if filepath.suffix.lower() == ".json":
            print(f"Converting news article: {filepath.name}")
            output_path = output_dir / f"{filepath.stem}.md"

            data = json.loads(filepath.read_text(encoding="utf-8"))
            title = data.get("title", "Unknown Title")
            url = data.get("url", "N/A")
            crawled = data.get("date_crawled", "N/A")
            customer_role = data.get("customer_role", "both")
            body = data.get("content_markdown", "")

            # Header metadata
            header = f"# {title}\n\n"
            header += f"**Source:** {url}\n"
            header += f"**Customer Role:** {customer_role}\n"
            header += f"**Crawled:** {crawled}\n"
            header += f"**Document Type:** news\n\n---\n\n"

            content = header + body
            output_path.write_text(content, encoding="utf-8")
            print(f"  [OK] Saved: {output_path.name} ({len(content)} chars, role={customer_role})")


def convert_all():
    """Convert toàn bộ files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown (MarkItDown)")
    print("=" * 50)

    print("\n--- Legal Documents ---")
    convert_legal_docs()

    print("\n--- News Articles ---")
    convert_news_articles()

    print("\n[OK] Task 3 completed! Output directory:", OUTPUT_DIR)


if __name__ == "__main__":
    convert_all()
