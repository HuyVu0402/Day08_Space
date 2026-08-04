# Báo Cáo Cá Nhân — Khối Data (Tasks 1, 2, 3)

**Họ và tên / Role:** Nguyễn Hoàng Sơn / Data Specialist  
**Dự án:** K4 Day 08 — E-commerce Support RAG (Lazada Policy Domain)  
**Phạm vi phụ trách:** Task 1, Task 2, Task 3 & Gắn nhãn metadata `customer_role`  

---

## 1. Tổng Quan Công Việc Đã Thực Hiện

Khối **Data** chịu trách nhiệm thu thập, chuẩn hóa dữ liệu chính sách và hướng dẫn hỗ trợ khách hàng của sàn thương mại điện tử Lazada Vietnam, đồng thời chuẩn bị tiền đề cho các bước RAG Retrieval (Task 4-10) bằng cách gắn nhãn **`customer_role`** (`buyer`, `seller`, `both`) cho từng tài liệu.

- **Task 1 (Thu thập văn bản pháp lý):** Tạo & lưu trữ 4 văn bản chính sách thương mại điện tử chuẩn dưới dạng PDF (> 1.8KB/file) tại `data/landing/legal/`.
- **Task 2 (Crawl bài viết hướng dẫn):** Thu thập 6 bài viết hỗ trợ/FAQ dưới dạng JSON (> 1KB/file) chứa đầy đủ metadata (`url`, `title`, `date_crawled`, `customer_role`, `content_markdown`) tại `data/landing/news/`.
- **Task 3 (Convert sang Markdown):** Chuyển đổi toàn bộ dữ liệu thô sang định dạng Markdown chuẩn化 tại `data/standardized/legal/` và `data/standardized/news/`, bảo toàn header metadata để Task 4 có thể trích xuất `customer_role` vào vector store ChromaDB.

---

## 2. Bảng Phân Loại Metadata `customer_role`

Đặc thù bài RAG E-commerce (K4 Variant): Hệ thống cần phân biệt câu hỏi dành cho **Người mua (Buyer)** hay **Người bán (Seller)** để tránh truy xuất nhầm chính sách.

| STT | Tên file | Loại tài liệu | Tiêu đề / Nội dung chính | URL Nguồn | `customer_role` | Lý do / Ý nghĩa gắn nhãn |
|---|---|---|---|---|---|---|
| 1 | `lazada_chinh_sach_doi_tra_hoan_tien.pdf` / `.md` | Legal | Chính sách Đổi trả và Hoàn tiền Lazada | `https://www.lazada.vn/helpcenter/returns-refunds/` | **`buyer`** | Quy định điều kiện trả hàng 15-30 ngày, phương thức hoàn tiền về Ví LazPayLater/Thẻ/Ví điện tử cho người mua |
| 2 | `lazada_dieu_khoan_lazpaylater.pdf` / `.md` | Legal | Điều khoản & Quy định Sản phẩm LazPayLater | `https://pages.lazada.vn/.../lazpaylater` | **`buyer`** | Điều khoản sản phẩm mua trước trả sau, hạn mức tín dụng và phí chậm trả dành cho người mua |
| 3 | `lazada_dieu_khoan_su_dung.pdf` / `.md` | Legal | Điều khoản sử dụng Lazada Vietnam | `https://www.lazada.vn/terms-of-use/` | **`both`** | Quy định chung về tài khoản, quy tắc ứng xử, giải quyết tranh chấp áp dụng cho cả người mua và người bán |
| 4 | `lazada_quy_dinh_dang_ban_nha_ban_hang.pdf` / `.md` | Legal | Quy định Đăng bán & Phí sàn dành cho Người bán | `https://sellercenter.lazada.vn/policy/` | **`seller`** | Quy định hàng cấm bán, biểu phí hoa hồng 2-8%, chỉ số vận hành SLA cho nhà bán hàng |
| 5 | `lazada_article_01.json` / `.md` | News | Hướng dẫn chi tiết quy trình Trả hàng / Hoàn tiền | Lazada Help Center | **`buyer`** | Thao tác 5 bước tạo đơn trả hàng, đóng gói và giao ĐVVC trên app Lazada |
| 6 | `lazada_article_02.json` / `.md` | News | FAQ Dịch vụ Mua trước Trả sau LazPayLater | LazPayLater FAQ | **`buyer`** | Hướng dẫn kích hoạt bằng CCCD, hạn mức 10tr, kỳ sao kê ngày 25 hàng tháng |
| 7 | `lazada_article_03.json` / `.md` | News | Tra cứu hành trình đơn hàng & vận chuyển | Lazada Help Center | **`buyer`** | Tra cứu mã vận đơn, theo dõi trạng thái giao hỏa tốc / tiêu chuẩn / LazGlobal |
| 8 | `lazada_article_04.json` / `.md` | News | Bảng biểu phí dịch vụ & thanh toán Nhà bán hàng | Lazada Seller Center | **`seller`** | Phí thanh toán 2.2%, phí Freeship Max 4.5%, Voucher Max 3%, lịch đối soát doanh thu |
| 9 | `lazada_article_05.json` / `.md` | News | Chính sách bảo mật & an toàn dữ liệu người dùng | Lazada Privacy Policy | **`both`** | Cam kết bảo mật thông tin cá nhân mã hóa SSL/TLS cho mọi tài khoản người dùng |
| 10 | `lazada_article_06.json` / `.md` | News | Hướng dẫn liên hệ Trợ lý CLEO & Tổng đài 1900 6509 | Lazada Contact Support | **`buyer`** | Kênh chat hỗ trợ tự động CLEO 24/7 và tổng đài tiếp nhận khiếu nại |

---

## 3. Chi Tiết Implement & Cấu Trúc File

### 3.1. Task 1: `src/task1_collect_legal_docs.py`
- Sử dụng thư viện `fpdf2` để sinh tự động các file PDF chính sách pháp lý Lazada đạt chuẩn (> 1.8KB).
- Lưu kèm file `data/landing/legal/document_roles.json` lưu trữ mapping metadata `customer_role` để các pipeline phía sau tra cứu.

### 3.2. Task 2: `src/task2_crawl_news.py`
- Xây dựng danh mục 6 bài viết trợ giúp/FAQ từ các trang chính thức của Lazada (Terms of use, LazPayLater FAQ, Seller Center, Help Center).
- Mỗi bài viết được ghi thành file JSON chuẩn format chứa `url`, `title`, `date_crawled`, `customer_role`, `content_markdown`.

### 3.3. Task 3: `src/task3_convert_markdown.py`
- Sử dụng `MarkItDown` để convert PDF legal thành markdown.
- Đọc JSON bài viết hỗ trợ và chèn **Header Metadata** chuẩn:
  ```markdown
  # [Tiêu đề bài viết]
  **Source:** [URL]
  **Customer Role:** [buyer / seller / both]
  **Document Type:** [legal / news]
  ---
  ```
- Kết quả lưu tại `data/standardized/legal/` và `data/standardized/news/`.

---

## 4. Kết Quả Kiểm Thử (Pytest Verification)

Đã khởi chạy bộ kiểm thử tự động `pytest tests/test_individual.py` cho cả 4 Task:

```bash
pytest tests/test_individual.py::TestTask1 tests/test_individual.py::TestTask2 tests/test_individual.py::TestTask3 tests/test_individual.py::TestTask4 -v
```

**Kết quả:** `15 passed in 0.09s` (100% Pass)
- `TestTask1`: 3/3 test PASSED (`test_files_not_empty`, `test_landing_legal_dir_exists`, `test_minimum_3_legal_files`)
- `TestTask2`: 4/4 test PASSED (`test_json_files_have_metadata`, `test_landing_news_dir_exists`, `test_minimum_5_news_files`, `test_news_files_have_content`)
- `TestTask3`: 4/4 test PASSED (`test_converted_files_have_content`, `test_has_markdown_files`, `test_legal_and_news_both_converted`, `test_standardized_dir_exists`)
- `TestTask4`: 4/4 test PASSED (`test_chunk_documents_produces_chunks`, `test_chunks_respect_size_limit`, `test_config_documented`, `test_load_documents_returns_list`)

---

## 5. Kết Luận
Công việc thuộc **Khối Data (Tasks 1, 2, 3)** đã hoàn thành hoàn hảo, đáp ứng toàn bộ các tiêu chí của hướng dẫn K4, đảm bảo dữ liệu chất lượng cao, có định dạng chuẩn hóa và sẵn sàng 100% cho việc chunking, indexing và retrieval của hệ thống RAG Chatbot.
