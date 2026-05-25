# Tiến Trình Nghiên Cứu & Phát Triển Dự Án: Multi-Agent Flutter Automation

Tài liệu này ghi nhận tiến độ thực hiện dự án dựa trên kế hoạch tại [implementation_plan_multi_ai.md](file:///Volumes/OtherSpace/DEV/multi_ai/docs/implementation_plan_multi_ai.md).

## Trạng thái hiện tại
- **Mục tiêu**: Xây dựng hệ thống Multi-Agent gồm UI Agent (viết giao diện từ BA + Design) và Test Agent (viết Widget Test tương ứng), kết nối tự động chạy test.
- **Cập nhật lần cuối**: 25/05/2026

---

## Danh Sách Công Việc (Task Checklist)

- [x] **Bước 1: Khởi tạo cấu trúc thư mục & File Cấu Hình**
  - [x] Tạo cấu trúc thư mục `docs/`, `inputs/`, `agents/`, `outputs/`.
  - [x] Viết file [requirements.txt](file:///Volumes/OtherSpace/DEV/multi_ai/requirements.txt) (google-genai, pydantic, rich, python-dotenv).
  - [x] Viết script [setup_env.sh](file:///Volumes/OtherSpace/DEV/multi_ai/setup_env.sh) để tự tạo venv và cài thư viện.
- [x] **Bước 2: Tạo Tài Liệu BA Mẫu & Nghiên Cứu Lý Thuyết**
  - [x] Viết tài liệu BA mẫu cho màn hình Login tại [login_feature_ba.md](file:///Volumes/OtherSpace/DEV/multi_ai/inputs/login_feature_ba.md).
  - [x] Nghiên cứu lý thuyết kết hợp 2 Agent (UI & Test) tuần tự + MCP.
- [/] **Bước 3: Tạo Agent Prototype đầu tiên (Python)**
  - [x] Viết code khung xương [orchestrator.py](file:///Volumes/OtherSpace/DEV/multi_ai/orchestrator.py) điều phối tiến trình.
  - [x] Định nghĩa [UIAgent](file:///Volumes/OtherSpace/DEV/multi_ai/agents/ui_agent.py) có Mock Mode và API Mode (sử dụng Gemini 2.5/3.5).
  - [x] Định nghĩa [TestAgent](file:///Volumes/OtherSpace/DEV/multi_ai/agents/test_agent.py) có Mock Mode và API Mode.
  - [ ] Kiểm thử kết quả chạy thực tế với API Key thật (sinh code UI & Test thật).
- [ ] **Bước 4: Nâng cấp Đa phương thức (Multimodal Input)**
  - [ ] Cài đặt thư viện xử lý ảnh `Pillow`.
  - [ ] Cấu hình [UIAgent](file:///Volumes/OtherSpace/DEV/multi_ai/agents/ui_agent.py) để gửi kèm file ảnh thiết kế UI khi gọi Gemini API.
- [ ] **Bước 5: Tự động hóa chạy kiểm thử & Phản hồi (Feedback Loop)**
  - [ ] Tích hợp chạy lệnh `flutter test` tự động bằng Python `subprocess`.
  - [ ] Đọc log lỗi test fail và truyền ngược lại để AI tự động sửa code (Self-healing).
- [ ] **Bước 6: Tích hợp MCP Server cho Flutter**
  - [ ] Viết MCP Server bằng Python hỗ trợ các tool Flutter.
  - [ ] Kết nối vào Cursor để kiểm chứng khả năng tự động hóa trên IDE.

---

## Nhật Ký Thực Hiện
- **25/05/2026**: Dự án đã có sẵn code skeleton chạy Mock thành công. Đã tạo file theo dõi tiến độ để lưu trữ context cho các phiên làm việc tiếp theo.
