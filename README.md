# Crawl Dữ liệu Văn bản Chính phủ

Dự án này sử dụng Python để thu thập danh sách văn bản từ trang `vanban.chinhphu.vn`, tải thông tin chi tiết và file PDF, sau đó trích xuất số ký hiệu từ dữ liệu đã tải.

## Yêu cầu
- **Python**: >= 3.10
- **Thư viện**:
  ```bash
  pip install requests beautifulsoup4 selenium
  ```
- **Trình duyệt**: Firefox và GeckoDriver (đặt trong PATH).
- **Hệ thống**: Git Bash hoặc terminal tương tự.

## Cấu trúc dự án
- `crawl_urls.py`: Crawl danh sách URL văn bản.
- `download_docs.py`: Tải thông tin và file PDF.
- `extract_so_ky_hieu.py`: Trích xuất số ký hiệu.
- `documents.txt`: Lưu danh sách URL.
- `downloads/`: Thư mục chứa dữ liệu tải về (được ignore trong Git).

## Hướng dẫn sử dụng

### 1. Crawl danh sách URL
- **File**: `crawl.py`
- **Chạy**:
  ```bash
  python crawl.py
  ```
- **Kết quả**: File `documents.txt` chứa danh sách URL.

### 2. Tải thông tin và PDF
- **File**: `crawl_post.py`
- **Chạy**:
  ```bash
  python crawl_post.py
  ```
- **Kết quả**: Thư mục `downloads/<doc_id>/` chứa `document_info.json` và file PDF.

### 3. Trích xuất số ký hiệu
- **File**: `get_document_number.py`
- **Chạy**:
  ```bash
  python get_document_number.py
  ```
- **Kết quả**: File `downloads/so_ky_hieu_list.txt` chứa danh sách số ký hiệu.

## Lưu ý
- Điều chỉnh đường dẫn tải về trong `crawl_post.py` nếu cần.