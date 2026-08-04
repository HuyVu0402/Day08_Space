"""
Task 1 — Thu thập văn bản chính sách thương mại điện tử / hỗ trợ khách hàng (Lazada).

Nhiệm vụ:
    1. Tạo ít nhất 3-4 file PDF chính sách Lazada vào data/landing/legal/
    2. Gắn metadata `customer_role` ('buyer', 'seller', hoặc 'both') cho từng tài liệu.
    3. Lưu thông tin metadata mapping vào data/landing/legal/document_roles.json
"""

import json
from pathlib import Path
from fpdf import FPDF

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"

LEGAL_DOCUMENTS = [
    {
        "filename": "lazada_dieu_khoan_su_dung.pdf",
        "title": "Dieu Khoan Su Dung Lazada Vietnam (Terms of Use)",
        "customer_role": "both",
        "url": "https://www.lazada.vn/terms-of-use/",
        "sections": [
            {
                "heading": "1. Quy dinh chung ve Tai khoan va Dich vu",
                "content": (
                    "Quy dinh nay ap dung cho toan bo nguoi dung (bao gom Nguoi mua va Nguoi ban) khi truy cap "
                    "va su dung nen tang thuong mai dien tu Lazada Vietnam. Nguoi dung phai tu bao mat thong tin "
                    "tai khoan, mat khau va chiu trach nhiem cho moi hoat dong dien ra duoi tai khoan cua minh. "
                    "Lazada co quyen tam khoa hoac hoan tac tai khoan neu phat hien hanh vi gian lan, vi pham "
                    "phap luat hoac vi pham dieu khoan su dung cua san."
                )
            },
            {
                "heading": "2. Quyen so huu tri tue va Quy tac ung xu",
                "content": (
                    "Toan bo noi dung, logo, thuong hieu, hinh anh va ma nguon tren Lazada thuoc quyen so huu cua "
                    "Lazada Group. Nghiem cam hanh vi sao chep, phat hanh lai hoac khai thai thuong mai khi chua co "
                    "su dong y bang van ban. Nguoi dung khong duoc dang tai cac noi dung xuc pham, gia moc hoac "
                    "phat tan ma doc tren nen tang."
                )
            },
            {
                "heading": "3. Giai quyet tranh chap va Gioi han trach nhiem",
                "content": (
                    "Lazada dong vai tro trung gian ket noi Nguoi mua va Nguoi ban. Moi tranh chap phat sinh se duoc "
                    "uu tien hoa giai dua tren quy dinh cua phap luat Vietnam va chinh sach cua Lazada. Lazada khong "
                    "chiu trach nhiem cho cac thiet hai gian tiep phat sinh tu viec giat doan dich vu hoac loi tu phia "
                    "nha cung cap dich vu ben thu ba."
                )
            }
        ]
    },
    {
        "filename": "lazada_chinh_sach_doi_tra_hoan_tien.pdf",
        "title": "Chinh Sach Doi Tra va Hoan Tien Lazada Vietnam (Return & Refund Policy)",
        "customer_role": "buyer",
        "url": "https://www.lazada.vn/helpcenter/returns-refunds/",
        "sections": [
            {
                "heading": "1. Thoi han va Dieu kien Tra hang / Hoan tien",
                "content": (
                    "Nguoi mua co quyen gui yeu cau Tra hang / Hoan tien trong vong 30 ngay doi voi san pham LazMall "
                    "va Choice, va trong vong 15 ngay doi voi san pham tu Nha ban hang thuong tinh tu ngay nhan hang. "
                    "San pham doi tra phai con nguyen tem mac, bao boi ban dau, chua qua su dung va co day du phu kien "
                    "kem theo. Lazada ho tro tra hang voi ly do Doi y doi voi cac gian hang du dieu kien."
                )
            },
            {
                "heading": "2. Quy trinh gui san pham va Ban giao don vi van chuyen",
                "content": (
                    "Sau khi yeu cau Tra hang duoc chap nhan tren ung dung Lazada, Nguoi mua chon phuong thuc gui hang: "
                    "Thu gom tai nha (Pick-up) hoac Gui tai buu cuc (Drop-off). Nguoi mua can dong goi san pham can than, "
                    "dan ma van don doi tra va ban giao cho don vi van chuyen trong vong 3 ngay lam viec. Chi phi van "
                    "chuyen doi tra se duoc Lazada ho tro neu yeu cau hop le."
                )
            },
            {
                "heading": "3. Phuong thuc va Thoi gian Xuly Hoan tien",
                "content": (
                    "Sau khi Nha ban hang hoac Kho Lazada nhan va kiem tra hang tra lai thanh cong, tien hoan se duoc "
                    "chuyen den Nguoi mua. Cac phuong thuc hoan tien bao gom: Vi LazPayLater (hoan lai han muc ngay), "
                    "The tin dung/ghi no (3-5 ngay lam viec), Vi dien tu ZaloPay/Momo (1-2 ngay lam viec), hoac "
                    "Chuyen khoan ngan hang (3-7 ngay lam viec)."
                )
            }
        ]
    },
    {
        "filename": "lazada_quy_dinh_dang_ban_nha_ban_hang.pdf",
        "title": "Quy Dinh Dang Ban va Phi San Danh cho Nha Ban Hang Lazada (Seller Policy)",
        "customer_role": "seller",
        "url": "https://sellercenter.lazada.vn/policy/",
        "sections": [
            {
                "heading": "1. Danh muc San pham Cam dang ban va Quy dinh Hang hoa",
                "content": (
                    "Nha ban hang khong duoc dang ban hang gia, hang nhai, hang vi pham quyen so huu tri tue, "
                    "vu khi, chat no, thuoc kich thich, thuc pham khong ro nguon goc va cac mat hang bi cam theo quy dinh "
                    "phap luat Vietnam. Vi pham se bi xoa san pham, tru diem uy tin (NC point) hoac khoa gian hang vinh vien."
                )
            },
            {
                "heading": "2. Bieu phi Dich vu va Phi Thanh toan cho Nha ban hang",
                "content": (
                    "Nha ban hang chiu cac khoan phi bao gom: Phi thanh toan co dinh (2.2% gia tri don hang), Phi hoa hong "
                    "san (tuy theo danh muc nganh hang tu 2% den 8%), va Phi tham gia cac chuong trinh uu dai nhu "
                    "Freeship Max, Voucher Max. Doanh thu thuc nhan se duoc Lazada doi sot va thanh toan hang tuan."
                )
            },
            {
                "heading": "3. Chi so Van hanh va Quy trinh Xu ly Don hang (SLA)",
                "content": (
                    "Nha ban hang phai xac nhan va dong goi don hang trong vong 24 gio ke tu khi don hang duoc tao. "
                    "Ty le huy don do loi Nha ban hang khong duoc vuot qua 1%. Neu ty le giao hang tre hoac huy don cao, "
                    "gian hang se bi giam luong truy cap (search traffic) va bi han che tham gia cac campaign lon."
                )
            }
        ]
    },
    {
        "filename": "lazada_dieu_khoan_lazpaylater.pdf",
        "title": "Dieu Khoan va Quy Dinh San Pham LazPayLater (LazPayLater Terms)",
        "customer_role": "buyer",
        "url": "https://pages.lazada.vn/wow/gcp/lazada/channel/vn/lazpaylater/cau-hoi-thuong-gap",
        "sections": [
            {
                "heading": "1. Gioi thieu va Han muc Tinh dung LazPayLater",
                "content": (
                    "LazPayLater la dich vu Mua truoc Tra sau hop tac giua Lazada va ngan hang doi tac. Khach hang hop le "
                    "co the duoc cap han muc tinh dung len den 10.000.000 VND de mua sam tren Lazada va tra sau vao ky thanh "
                    "toan tiep theo hoac trag gop nhieu ky (3, 6, 12 thang)."
                )
            },
            {
                "heading": "2. Thanh toan Du no va Phi cham tro",
                "content": (
                    "Sao ke LazPayLater duoc chot vao ngay 25 hang thang va thoi han thanh toan la ngay 5 cua thang ke tiep. "
                    "Khach hang co the thanh toan du no qua Vi ZaloPay, Chuyen khoan ngan hang hoac The ATM noi dia. Neu thanh "
                    "toan tre han, phi phat cham tra se duoc tinh theo quy dinh 0.1%/ngay tren so tien qua han."
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
    """Tạo file PDF từ thông tin document."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Header title
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, doc_info["title"], new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    # Metadata info inside PDF
    pdf.set_font("Helvetica", style="I", size=10)
    pdf.cell(0, 6, f"URL Source: {doc_info['url']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Customer Role: {doc_info['customer_role']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Sections
    for sec in doc_info["sections"]:
        pdf.set_font("Helvetica", style="B", size=12)
        pdf.cell(0, 8, sec["heading"], new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", size=10)
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
    print("\n--- Task 1: Generating Lazada Legal Documents ---")
    for doc in LEGAL_DOCUMENTS:
        filepath = create_pdf(doc)
        roles_mapping[doc["filename"]] = {
            "title": doc["title"],
            "customer_role": doc["customer_role"],
            "url": doc["url"],
            "size_bytes": filepath.stat().st_size
        }
        
    # Save mapping file
    mapping_file = DATA_DIR / "document_roles.json"
    mapping_file.write_text(json.dumps(roles_mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Saved document roles mapping to: {mapping_file}")


if __name__ == "__main__":
    generate_legal_docs()
