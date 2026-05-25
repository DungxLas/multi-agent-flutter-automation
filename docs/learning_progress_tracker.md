# Tiến Trình Học Tập: Flutter to AI Agent (Python)

Tài liệu này ghi nhận tiến độ học tập dựa trên lộ trình tại [learning_roadmap_flutter_to_ai_agent.md](file:///Volumes/OtherSpace/DEV/multi_ai/docs/learning_roadmap_flutter_to_ai_agent.md).

## Trạng thái hiện tại
- **Mục tiêu**: Lập trình viên Flutter nghiên cứu Python, LLM API, MCP và Multi-Agent.
- **Cập nhật lần cuối**: 25/05/2026

---

## Bảng Theo Dõi Tiến Độ

### Giai Đoạn 1: Làm Quen Với Python Căn Bản
- [ ] So sánh & Chuyển dịch cú pháp từ Dart sang Python (Class, Async/Await, List/Map).
- [/] Tìm hiểu Type Hinting trong Python (để code an toàn như Dart).
- [ ] Xử lý bất đồng bộ với `asyncio`.
- [/] Quản lý môi trường ảo với `venv` và `pip` (Đã có script [setup_env.sh](file:///Volumes/OtherSpace/DEV/multi_ai/setup_env.sh)).

### Giai Đoạn 2: Khái Niệm Cốt Lõi về LLM & API (Python SDK)
- [ ] Cài đặt & Gọi thử Gemini API bằng SDK `google-genai` (Sắp thực hiện).
- [ ] Viết Prompt Engineering động bằng f-string trong Python.
- [ ] Sử dụng Structured Output với **Pydantic** để định nghĩa cấu trúc trả về bắt buộc cho AI.
- [ ] Khai báo và sử dụng Function Calling (Tools).

### Giai Đoạn 3: Model Context Protocol (MCP) với Python
- [ ] Cài đặt SDK `mcp`.
- [ ] Viết MCP Server Python cơ bản chạy dưới local.
- [ ] Định nghĩa các tools tương tác với Flutter CLI (ví dụ: `flutter test`, `flutter analyze`).
- [ ] Cấu hình IDE Client (Cursor/Claude Desktop) kết nối đến MCP Server local.

### Giai Đoạn 4: Framework Điều Phối Agent (Orchestration)
- [ ] Nghiên cứu mô hình Sequential vs Parallel Agents.
- [ ] Nghiên cứu thư viện **CrewAI** (Phân vai Role, Task, gán Tools).
- [ ] Nghiên cứu **LangGraph** để xây dựng đồ thị trạng thái kiểm thử tự động (Feedback Loop sửa lỗi).

### Giai Đoạn 5: Thực Chiến & Tự Động Hóa Flutter
- [ ] Tự động hóa CLI Flutter bằng module `subprocess` của Python.
- [ ] Đọc & phân tích kết quả log lỗi từ Flutter CLI truyền lại cho AI.
- [ ] Xử lý ảnh chụp thiết kế (Multimodal) bằng Gemini API và thư viện `Pillow`.

---

## Nhật Ký Học Tập & Ghi Chú
- **25/05/2026**: Bắt đầu dự án. Đã có cấu trúc code base prototype Python. Đã nắm được lý thuyết tổng quan về MCP và luồng phối hợp 2 Agent UI & Test. Chuẩn bị chạy thực tế dự án mẫu để học Python và Gemini SDK.
