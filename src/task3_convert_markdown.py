"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown.

Sử dụng MarkItDown của Microsoft:
    https://github.com/microsoft/markitdown
"""

import json
from pathlib import Path
from markitdown import MarkItDown

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs():
    """Convert PDF/DOCX files trong data/landing/legal/ sang markdown."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    roles_file = legal_dir / "document_roles.json"
    roles_meta = {}
    if roles_file.exists():
        roles_meta = json.loads(roles_file.read_text(encoding="utf-8"))

    md = MarkItDown()

    for filepath in legal_dir.iterdir():
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"Converting: {filepath.name}")
            result = md.convert(str(filepath))
            output_path = output_dir / f"{filepath.stem}.md"

            role_info = roles_meta.get(filepath.name, {})
            customer_role = role_info.get("customer_role", "both")
            doc_title = role_info.get("title", filepath.stem.replace("_", " ").title())
            doc_url = role_info.get("url", "https://www.lazada.vn/")

            header = f"# {doc_title}\n\n"
            header += f"**Source:** {doc_url}\n"
            header += f"**Customer Role:** {customer_role}\n"
            header += f"**Document Type:** legal\n\n---\n\n"

            content = header + result.text_content
            output_path.write_text(content, encoding="utf-8")
            print(f"  [OK] Saved: {output_path.name}")


def convert_news_articles():
    """Convert JSON crawled articles trong data/landing/news/ sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in news_dir.iterdir():
        if filepath.suffix.lower() == ".json":
            print(f"Converting: {filepath.name}")
            data = json.loads(filepath.read_text(encoding="utf-8"))
            output_path = output_dir / f"{filepath.stem}.md"

            header = f"# {data.get('title', 'Unknown')}\n\n"
            header += f"**Source:** {data.get('url', 'N/A')}\n"
            header += f"**Crawled:** {data.get('date_crawled', 'N/A')}\n"
            header += f"**Customer Role:** {data.get('customer_role', 'both')}\n"
            header += f"**Document Type:** news\n\n---\n\n"

            content = header + data.get("content_markdown", "")
            output_path.write_text(content, encoding="utf-8")
            print(f"  [OK] Saved: {output_path.name}")


def convert_all():
    """Convert toàn bộ files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown (MarkItDown)")
    print("=" * 50)

    print("\n--- Legal Documents ---")
    convert_legal_docs()

    print("\n--- News Articles ---")
    convert_news_articles()

    print("\n[OK] Done! Output tai:", OUTPUT_DIR)


if __name__ == "__main__":
    convert_all()
