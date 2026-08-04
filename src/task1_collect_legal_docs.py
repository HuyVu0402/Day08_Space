"""
Task 1 — Thu thập văn bản chính sách thương mại điện tử / hỗ trợ khách hàng (Lazada).

Nhiệm vụ:
    1. Tạo 4 file PDF chính sách Lazada bằng Tiếng Việt có dấu chuẩn vào data/landing/legal/
    2. Gắn metadata `customer_role` ('buyer', 'seller', hoặc 'both') cho từng tài liệu.
    3. Lưu thông tin metadata mapping vào data/landing/legal/document_roles.json
"""

import json
import os
from pathlib import Path
from fpdf import FPDF

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"

LEGAL_DOCUMENTS = [
    {
        "filename": "lazada_dieu_khoan_su_dung.pdf",
        "title": "Điều Khoản Sử Dụng Lazada Việt Nam (Terms of Use)",
        "customer_role": "both",
        "url": "https://www.lazada.vn/terms-of-use/",
        "sections": [
            {
                "heading": "1. Quy định chung về Tài khoản và Dịch vụ",
                "content": (
                    "Quy định này áp dụng cho toàn bộ người dùng (bao gồm Người mua và Người bán) khi truy cập "
                    "và sử dụng nền tảng thương mại điện tử Lazada Việt Nam. Người dùng phải tự bảo mật thông tin "
                    "tài khoản, mật khẩu và chịu trách nhiệm cho mọi hoạt động diễn ra dưới tài khoản của mình. "
                    "Lazada có quyền tạm khóa hoặc hoàn tác tài khoản nếu phát hiện hành vi gian lận, vi phạm "
                    "pháp luật hoặc vi phạm điều khoản sử dụng của sàn."
                )
            },
            {
                "heading": "2. Quyền sở hữu trí tuệ và Quy tắc ứng xử",
                "content": (
                    "Toàn bộ nội dung, logo, thương hiệu, hình ảnh và mã nguồn trên Lazada thuộc quyền sở hữu của "
                    "Lazada Group. Nghiêm cấm hành vi sao chép, phát hành lại hoặc khai thác thương mại khi chưa có "
                    "sự đồng ý bằng văn bản. Người dùng không được đăng tải các nội dung xúc phạm, giả mạo hoặc "
                    "phát tán mã độc trên nền tảng."
                )
            },
            {
                "heading": "3. Giải quyết tranh chấp và Giới hạn trách nhiệm",
                "content": (
                    "Lazada đóng vai trò trung gian kết nối Người mua và Người bán. Mọi tranh chấp phát sinh sẽ được "
                    "ưu tiên hòa giải dựa trên quy định của pháp luật Việt Nam và chính sách của Lazada. Lazada không "
                    "chịu trách nhiệm cho các thiệt hại gián tiếp phát sinh từ việc gián đoạn dịch vụ hoặc lỗi từ phía "
                    "nhà cung cấp dịch vụ bên thứ ba."
                )
            }
        ]
    },
    {
        "filename": "lazada_chinh_sach_doi_tra_hoan_tien.pdf",
        "title": "Chính Sách Đổi Trả và Hoàn Tiền Lazada Việt Nam (Return & Refund Policy)",
        "customer_role": "buyer",
        "url": "https://www.lazada.vn/helpcenter/returns-refunds/",
        "sections": [
            {
                "heading": "1. Thời hạn và Điều kiện Trả hàng / Hoàn tiền",
                "content": (
                    "Người mua có quyền gửi yêu cầu Trả hàng / Hoàn tiền trong vòng 30 ngày đối với sản phẩm LazMall "
                    "và Choice, và trong vòng 15 ngày đối với sản phẩm từ Nhà bán hàng thường tính từ ngày nhận hàng. "
                    "Sản phẩm đổi trả phải còn nguyên tem mác, bao bì ban đầu, chưa qua sử dụng và có đầy đủ phụ kiện "
                    "kèm theo. Lazada hỗ trợ trả hàng với lý do Đổi ý đối với các gian hàng đủ điều kiện."
                )
            },
            {
                "heading": "2. Quy trình gửi sản phẩm và Bàn giao đơn vị vận chuyển",
                "content": (
                    "Sau khi yêu cầu Trả hàng được chấp nhận trên ứng dụng Lazada, Người mua chọn phương thức gửi hàng: "
                    "Thu gom tại nhà (Pick-up) hoặc Gửi tại bưu cục (Drop-off). Người mua cần đóng gói sản phẩm cẩn thận, "
                    "dán mã vận đơn đổi trả và bàn giao cho đơn vị vận chuyển trong vòng 3 ngày làm việc. Chi phí vận "
                    "chuyển đổi trả sẽ được Lazada hỗ trợ nếu yêu cầu hợp lệ."
                )
            },
            {
                "heading": "3. Phương thức và Thời gian Xử lý Hoàn tiền",
                "content": (
                    "Sau khi Nhà bán hàng hoặc Kho Lazada nhận và kiểm tra hàng trả lại thành công, tiền hoàn sẽ được "
                    "chuyển đến Người mua. Các phương thức hoàn tiền bao gồm: Ví LazPayLater (hoàn lại hạn mức ngay), "
                    "Thẻ tín dụng/ghi nợ (3-5 ngày làm việc), Ví điện tử ZaloPay/Momo (1-2 ngày làm việc), hoặc "
                    "Chuyển khoản ngân hàng (3-7 ngày làm việc)."
                )
            }
        ]
    },
    {
        "filename": "lazada_quy_dinh_dang_ban_nha_ban_hang.pdf",
        "title": "Quy Định Đăng Bán và Phí Sàn Dành cho Nhà Bán Hàng Lazada (Seller Policy)",
        "customer_role": "seller",
        "url": "https://sellercenter.lazada.vn/policy/",
        "sections": [
            {
                "heading": "1. Danh mục Sản phẩm Cấm đăng bán và Quy định Hàng hóa",
                "content": (
                    "Nhà bán hàng không được đăng bán hàng giả, hàng nhái, hàng vi phạm quyền sở hữu trí tuệ, "
                    "vũ khí, chất nổ, thuốc kích thích, thực phẩm không rõ nguồn gốc và các mặt hàng bị cấm theo quy định "
                    "pháp luật Việt Nam. Vi phạm sẽ bị xóa sản phẩm, trừ điểm uy tín (NC point) hoặc khóa gian hàng vĩnh viễn."
                )
            },
            {
                "heading": "2. Biểu phí Dịch vụ và Phí Thanh toán cho Nhà bán hàng",
                "content": (
                    "Nhà bán hàng chịu các khoản phí bao gồm: Phí thanh toán cố định (2.2% giá trị đơn hàng), Phí hoa hồng "
                    "sàn (tùy theo danh mục ngành hàng từ 2% đến 8%), và Phí tham gia các chương trình ưu đãi như "
                    "Freeship Max, Voucher Max. Doanh thu thực nhận sẽ được Lazada đối soát và thanh toán hàng tuần."
                )
            },
            {
                "heading": "3. Chỉ số Vận hành và Quy trình Xử lý Đơn hàng (SLA)",
                "content": (
                    "Nhà bán hàng phải xác nhận và đóng gói đơn hàng trong vòng 24 giờ kể từ khi đơn hàng được tạo. "
                    "Tỷ lệ hủy đơn do lỗi Nhà bán hàng không được vượt quá 1%. Nếu tỷ lệ giao hàng trễ hoặc hủy đơn cao, "
                    "gian hàng sẽ bị giảm lượng truy cập (search traffic) và bị hạn chế tham gia các campaign lớn."
                )
            }
        ]
    },
    {
        "filename": "lazada_dieu_khoan_lazpaylater.pdf",
        "title": "Điều Khoản và Quy Định Sản Phẩm LazPayLater (LazPayLater Terms)",
        "customer_role": "buyer",
        "url": "https://pages.lazada.vn/wow/gcp/lazada/channel/vn/lazpaylater/cau-hoi-thuong-gap",
        "sections": [
            {
                "heading": "1. Giới thiệu và Hạn mức Tín dụng LazPayLater",
                "content": (
                    "LazPayLater là dịch vụ Mua trước Trả sau hợp tác giữa Lazada và ngân hàng đối tác. Khách hàng hợp lệ "
                    "có thể được cấp hạn mức tín dụng lên đến 10.000.000 VNĐ để mua sắm trên Lazada và trả sau vào kỳ thanh "
                    "toán tiếp theo hoặc trả góp nhiều kỳ (3, 6, 12 tháng)."
                )
            },
            {
                "heading": "2. Thanh toán Dư nợ và Phí chậm trả",
                "content": (
                    "Sao kê LazPayLater được chốt vào ngày 25 hàng tháng và thời hạn thanh toán là ngày 5 của tháng kế tiếp. "
                    "Khách hàng có thể thanh toán dư nợ qua Ví ZaloPay, Chuyển khoản ngân hàng hoặc Thẻ ATM nội địa. Nếu thanh "
                    "toán trễ hạn, phí phạt chậm trả sẽ được tính theo quy định 0.1%/ngày trên số tiền quá hạn."
                )
            }
        ]
    }
]


def setup_directory():
    """Tạo thư mục data/landing/legal/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Thu muc da san sang: {DATA_DIR}")


def create_pdf(doc_info: dict) -> Path:
    """Tạo file PDF từ thông tin document hỗ trợ tiếng Việt UTF-8."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Load Windows Arial font for UTF-8 Vietnamese support
    font_path = r"C:\Windows\Fonts\arial.ttf"
    font_bold_path = r"C:\Windows\Fonts\arialbd.ttf"
    font_italic_path = r"C:\Windows\Fonts\ariali.ttf"

    use_custom_font = False
    if os.path.exists(font_path):
        try:
            pdf.add_font("ArialVN", "", font_path)
            if os.path.exists(font_bold_path):
                pdf.add_font("ArialVN", "B", font_bold_path)
            if os.path.exists(font_italic_path):
                pdf.add_font("ArialVN", "I", font_italic_path)
            use_custom_font = True
        except Exception:
            use_custom_font = False

    font_family = "ArialVN" if use_custom_font else "Helvetica"

    # Header title
    pdf.set_font(font_family, style="B" if use_custom_font else "B", size=15)
    pdf.cell(0, 10, doc_info["title"], new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    # Metadata info inside PDF
    pdf.set_font(font_family, style="I" if use_custom_font else "I", size=10)
    pdf.cell(0, 6, f"URL Source: {doc_info['url']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Customer Role: {doc_info['customer_role']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Sections
    for sec in doc_info["sections"]:
        pdf.set_font(font_family, style="B" if use_custom_font else "B", size=12)
        pdf.cell(0, 8, sec["heading"], new_x="LMARGIN", new_y="NEXT")

        pdf.set_font(font_family, size=10)
        pdf.multi_cell(0, 6, sec["content"])
        pdf.ln(4)

    filepath = DATA_DIR / doc_info["filename"]
    pdf.output(str(filepath))
    print(f"  [OK] Da tao PDF: {filepath.name} ({filepath.stat().st_size} bytes)")
    return filepath


def generate_legal_docs():
    """Tạo tất cả văn bản chính sách pháp lý Lazada và lưu metadata mapping."""
    setup_directory()

    roles_mapping = {}
    print("\n--- Task 1: Generating Lazada Legal Documents (Accented Vietnamese) ---")
    for doc in LEGAL_DOCUMENTS:
        filepath = create_pdf(doc)
        roles_mapping[doc["filename"]] = {
            "title": doc["title"],
            "customer_role": doc["customer_role"],
            "url": doc["url"],
            "size_bytes": filepath.stat().st_size
        }

    mapping_file = DATA_DIR / "document_roles.json"
    mapping_file.write_text(json.dumps(roles_mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Saved document roles mapping to: {mapping_file}")


if __name__ == "__main__":
    generate_legal_docs()
