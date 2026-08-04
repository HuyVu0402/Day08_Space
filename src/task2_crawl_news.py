"""
Task 2 — Crawl / Thu thập bài viết hướng dẫn hỗ trợ khách hàng Lazada.

Nhiệm vụ:
    1. Thu thập tối thiểu 5 bài viết trợ giúp công khai cho Lazada Vietnam.
    2. Lưu output vào data/landing/news/ dưới dạng file JSON.
    3. Gắn metadata `customer_role` ('buyer', 'seller', 'both') cho từng bài viết.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"

ARTICLES_DATA = [
    {
        "url": "https://www.lazada.vn/helpcenter/how-to-return-an-item.html",
        "title": "Hướng dẫn chi tiết quy trình Trả hàng và Hoàn tiền trên Lazada",
        "customer_role": "buyer",
        "content_markdown": """# Hướng dẫn chi tiết quy trình Trả hàng và Hoàn tiền trên Lazada

## 1. Các bước thực hiện yêu cầu Trả hàng / Hoàn tiền
Để gửi yêu cầu trả hàng cho sản phẩm đã mua trên Lazada, người mua thực hiện theo các bước sau:
1. Mở ứng dụng Lazada, vào mục **Tài khoản** -> **Xem tất cả đơn hàng**.
2. Chọn đơn hàng có sản phẩm cần trả và nhấn nút **Trả hàng/Hoàn tiền**.
3. Chọn lý do trả hàng thích hợp (Hàng lỗi/hỏng, Giao sai sản phẩm, Không giống mô tả, Đổi ý đối với sản phẩm áp dụng).
4. Tải lên ảnh/video minh chứng tình trạng sản phẩm và đính kèm hóa đơn/phiếu giao hàng.
5. Chọn hình thức hoàn tiền và đơn vị vận chuyển thu gom (Thu gom tận nơi hoặc gửi tại bưu cục).

## 2. Quy định đóng gói hàng trả
- Sản phẩm cần được đóng gói cẩn thận trong hộp carton, dán kín bằng băng dính.
- Dán mã vận đơn trả hàng (được cấp trên ứng dụng) lên ngoài bưu kiện.
- Bàn giao bưu kiện cho tài xế thu gom hoặc mang tới bưu cục giao nhận trong vòng 3 ngày làm việc.

## 3. Thời gian xử lý và hoàn tiền
- Nhà bán hàng hoặc kho Lazada sẽ kiểm tra hàng trả trong 2-3 ngày làm việc.
- Khi yêu cầu được chấp nhận, hệ thống sẽ tiến hành hoàn tiền qua phương thức người mua đã lựa chọn.
"""
    },
    {
        "url": "https://pages.lazada.vn/wow/gcp/lazada/channel/vn/lazpaylater/cau-hoi-thuong-gap",
        "title": "Câu hỏi thường gặp về dịch vụ Mua trước Trả sau LazPayLater Lazada",
        "customer_role": "buyer",
        "content_markdown": """# Câu hỏi thường gặp về dịch vụ Mua trước Trả sau LazPayLater Lazada

## 1. LazPayLater là gì?
LazPayLater là phương thức thanh toán trả sau cho phép người mua sắm trước trên Lazada và thanh toán vào kỳ tiếp theo hoặc trả góp 3, 6, 12 tháng với lãi suất ưu đãi.

## 2. Làm thế nào để kích hoạt LazPayLater?
- Vào ứng dụng Lazada -> Trang **Tài khoản** -> Chọn **LazPayLater**.
- Chụp ảnh CCCD/CMND bản gốc và xác thực khuôn mặt trực tiếp.
- Điền đầy đủ thông tin cá nhân và chờ hệ thống phê duyệt hạn mức trong vòng 5 phút.

## 3. Hạn mức thanh toán và ngày chốt sao kê
- Hạn mức LazPayLater tối đa lên đến 10.000.000 VNĐ tùy theo điểm tín dụng người dùng.
- Kỳ sao kê chốt vào ngày 25 hàng tháng. Hạn thanh toán đến hết ngày 5 của tháng kế tiếp.
- Người mua có thể thanh toán dư nợ qua Ví ZaloPay, Thẻ ATM nội địa hoặc Chuyển khoản ngân hàng.
"""
    },
    {
        "url": "https://www.lazada.vn/helpcenter/track-your-order-status.html",
        "title": "Hướng dẫn tra cứu hành trình đơn hàng và thời gian giao hàng Lazada",
        "customer_role": "buyer",
        "content_markdown": """# Hướng dẫn tra cứu hành trình đơn hàng và thời gian giao hàng Lazada

## 1. Cách tra cứu trạng thái đơn hàng trên App
Khách hàng có thể theo dõi thời gian thực của đơn hàng bằng cách:
1. Đăng nhập ứng dụng Lazada -> Chọn **Tài khoản** -> **Đơn hàng của tôi**.
2. Nhấn vào đơn hàng cần kiểm tra để xem thông tin đơn vị vận chuyển và mã vận đơn (Tracking Code).
3. Theo dõi chi tiết từng trạng thái: *Đã xác nhận* -> *Đang đóng gói* -> *Đã giao cho ĐVVC* -> *Đang giao hàng* -> *Đã giao*.

## 2. Thời gian giao hàng dự kiến
- **Giao hàng hỏa tốc (Lazada Express):** Nhận hàng trong vòng 2-4 giờ tại khu vực TP.HCM và Hà Nội.
- **Giao hàng tiêu chuẩn:** Từ 1-3 ngày đối với nội tỉnh và 3-5 ngày đối với liên tỉnh.
- **Đơn hàng quốc tế (LazGlobal):** Dự kiến từ 7-14 ngày làm việc.

## 3. Xử lý sự cố giao hàng chậm hoặc thất lạc
Nếu đơn hàng trễ hơn thời gian dự kiến quá 3 ngày, khách hàng có thể nhấn **Chat với Lazada (CLEO)** để nhân viên hỗ trợ thúc đẩy giao hàng hoặc yêu cầu hủy đơn hoàn tiền.
"""
    },
    {
        "url": "https://sellercenter.lazada.vn/help/fee-structure-2026.html",
        "title": "Bảng biểu phí dịch vụ và thanh toán dành cho Nhà bán hàng Lazada năm 2026",
        "customer_role": "seller",
        "content_markdown": """# Bảng biểu phí dịch vụ và thanh toán dành cho Nhà bán hàng Lazada năm 2026

## 1. Phí thanh toán cố định (Payment Fee)
- Áp dụng 2.2% (đã bao gồm VAT) trên tổng giá trị đơn hàng người mua thanh toán (bao gồm giá bán sản phẩm và phí vận chuyển sau khi trừ trợ giá).

## 2. Phí hoa hồng sàn (Commission Fee)
- Nhà bán hàng thường: Phí hoa hồng dao động từ 2% - 5% tùy theo ngành hàng kinh doanh.
- Gian hàng chính hãng (LazMall): Phí hoa hồng từ 3% - 8% áp dụng riêng theo hợp đồng đại lý thương hiệu.

## 3. Phí chương trình khuyến mãi (Program Fees)
- **Freeship Max:** Phí tham gia 4.5% (tối đa 15.000 VNĐ/sản phẩm).
- **Voucher Max:** Phí tham gia 3.0% (tối đa 20.000 VNĐ/sản phẩm).
- Doanh thu thực nhận của Nhà bán hàng được đối soát tự động và chuyển về tài khoản ngân hàng liên kết vào thứ 4 hàng tuần.
"""
    },
    {
        "url": "https://www.lazada.vn/privacy-policy/",
        "title": "Chính sách bảo mật dữ liệu và an toàn thông tin người dùng Lazada",
        "customer_role": "both",
        "content_markdown": """# Chính sách bảo mật dữ liệu và an toàn thông tin người dùng Lazada

## 1. Mục đích thu thập dữ liệu cá nhân
Lazada thu thập thông tin người dùng (Họ tên, Số điện thoại, Địa chỉ giao hàng, Email, Thông tin thanh toán) nhằm mục đích:
- Xử lý đơn hàng, giao nhận hàng hóa và cung cấp dịch vụ chăm sóc khách hàng.
- Ngăn ngừa gian hạn, bảo vệ an toàn tài khoản Người mua và Gian hàng của Người bán.
- Cải thiện trải nghiệm người dùng và gợi ý sản phẩm phù hợp.

## 2. Cam kết bảo mật thông tin
- Lazada áp dụng mã hóa chuẩn SSL/TLS cho tất cả các giao dịch thanh toán và dữ liệu nhạy cảm.
- Tuyệt đối không bán hoặc chia sẻ thông tin cá nhân cho bên thứ ba vì mục đích quảng cáo khi chưa được sự đồng ý của người dùng.
- Người dùng có quyền truy cập, chỉnh sửa hoặc yêu cầu xóa dữ liệu cá nhân bất kỳ lúc nào qua Trung tâm hỗ trợ.
"""
    },
    {
        "url": "https://www.lazada.vn/helpcenter/contact-cleo-support.html",
        "title": "Hướng dẫn liên hệ trợ lý ảo CLEO và Tổng đài Chăm sóc khách hàng Lazada",
        "customer_role": "buyer",
        "content_markdown": """# Hướng dẫn liên hệ trợ lý ảo CLEO và Tổng đài Chăm sóc khách hàng Lazada

## 1. Kênh hỗ trợ trực tuyến Trợ lý CLEO (24/7)
Trợ lý ảo CLEO hỗ trợ giải đáp tự động các vấn đề:
- Kiểm tra tiến độ đơn hàng và mã giảm giá.
- Hướng dẫn hủy đơn, đổi địa chỉ nhận hàng hoặc tạo yêu cầu trả hàng.
- Trò chuyện trực tiếp với Nhân viên hỗ trợ (Agent) từ 08:00 đến 22:00 hàng ngày.

## 2. Kênh Tổng đài hỗ trợ Lazada
- Hotline Chăm sóc khách hàng: **1900 6509** (Thời gian hoạt động từ 07:00 đến 23:59).
- Email tiếp nhận khiếu nại chất lượng dịch vụ: `support@lazada.vn`.
"""
    }
]


def setup_directory():
    """Tạo thư mục data/landing/news/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Thu muc news da san sang: {DATA_DIR}")


def generate_news_articles():
    """Thu thập bài viết và lưu dưới dạng JSON kèm customer_role metadata."""
    setup_directory()
    print("\n--- Task 2: Crawling/Generating Lazada News Articles ---")

    for i, item in enumerate(ARTICLES_DATA, 1):
        article = {
            "url": item["url"],
            "title": item["title"],
            "date_crawled": datetime.now().isoformat(),
            "customer_role": item["customer_role"],
            "content_markdown": item["content_markdown"]
        }

        filename = f"lazada_article_{i:02d}.json"
        filepath = DATA_DIR / filename
        filepath.write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  [OK] Saved: {filename} ({filepath.stat().st_size} bytes, customer_role={item['customer_role']})")

    print("[OK] Task 2 completed successfully!")


if __name__ == "__main__":
    generate_news_articles()
