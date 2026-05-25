# Kế hoạch triển khai: Dự án Multi-Agent tự động hóa Flutter (Python)

Kế hoạch này giúp thiết lập cấu trúc dự án Python trong workspace của bạn (`/Volumes/OtherSpace/DEV/multi_ai`) để vừa phục vụ việc nghiên cứu lý thuyết vừa có mã nguồn chạy thử nghiệm (prototype) thực tế song song.

---

## Các thành phần đề xuất trong Workspace

Chúng ta sẽ tạo ra một dự án có cấu trúc như sau:

```
multi_ai/
│
├── docs/                     # Lưu trữ tài liệu nghiên cứu và hướng dẫn
│   └── mcp_architecture.md   # Lý thuyết chi tiết về MCP & Agent
│
├── inputs/                   # Thư mục chứa tài liệu BA và Design (đầu vào)
│   └── login_feature_ba.md   # Tài liệu BA mẫu cho tính năng Login
│
├── agents/                   # Mã nguồn Python định nghĩa các Agent
│   ├── __init__.py
│   ├── ui_agent.py           # Logic của UI Agent
│   └── test_agent.py         # Logic của Test Agent
│
├── orchestrator.py           # Script chính điều phối 2 Agent và chạy test
├── requirements.txt          # Các thư viện Python cần dùng (pydantic, google-genai, mcp)
└── setup_env.sh              # Script tự động khởi tạo môi trường ảo Python
```

---

## Các Bước Triển Khai Chi Tiết

### Bước 1: Khởi tạo cấu trúc thư mục & File Cấu Hình
* Tạo thư mục `docs/`, `inputs/`, `agents/`.
* Viết file `requirements.txt` định nghĩa các thư viện cần thiết:
  * `google-genai` (để gọi Gemini 2.5/3.5).
  * `pydantic` (định nghĩa cấu trúc đầu ra).
  * `rich` (để hiển thị log console đẹp mắt cho tiến trình của các Agent).
* Viết script `setup_env.sh` để tạo và kích hoạt Python Virtual Environment (`venv`), cài đặt thư viện.

### Bước 2: Tạo Tài Liệu BA Mẫu & Nghiên Cứu Tài Liệu
* Viết file `inputs/login_feature_ba.md` mô tả một yêu cầu nghiệp vụ thực tế (màn hình Login có validation email, password, hiển thị nút loading).
* Tạo file tài liệu nghiên cứu `docs/mcp_architecture.md` mô tả chi tiết cách viết một MCP server bằng Python cho Flutter CLI.

### Bước 3: Tạo Agent Prototype đầu tiên (Python)
* **`agents/ui_agent.py`**: Chứa code gọi Gemini API, đọc tài liệu BA và xuất ra code Dart cho Widget.
* **`agents/test_agent.py`**: Chứa code đọc BA và code Widget sinh ra để tạo Widget Test tương ứng.
* **`orchestrator.py`**: File chạy chính. Nó sẽ:
  1. Đọc BA mẫu.
  2. Gọi `ui_agent` để gen code UI.
  3. Gọi `test_agent` để gen code Test.
  4. Lưu các file này vào một thư mục mô phỏng (mock output) để bạn xem kết quả.

---

## Kế hoạch kiểm thử & Xác thực (Verification Plan)

### Kiểm thử thủ công
1. Chạy file `setup_env.sh` để cài đặt môi trường.
2. Cấu hình file `.env` chứa API Key của Gemini.
3. Chạy lệnh `python orchestrator.py` để xem các Agent làm việc song song, xuất ra các file Dart UI và Test thực tế trong thư mục đầu ra.
4. Xem log tiến trình hiển thị trực quan trên màn hình terminal.
