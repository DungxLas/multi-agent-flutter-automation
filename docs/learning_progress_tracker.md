# Tiến Trình Học Tập: Flutter to AI Agent (Python)

Tài liệu này ghi nhận tiến độ học tập dựa trên lộ trình tại [learning_roadmap_flutter_to_ai_agent.md](file:///Volumes/OtherSpace/DEV/multi_ai/docs/learning_roadmap_flutter_to_ai_agent.md).

## Trạng thái hiện tại
- **Mục tiêu**: Lập trình viên Flutter nghiên cứu Python, LLM API, MCP và Multi-Agent.
- **Cập nhật lần cuối**: 25/05/2026

---

## Bảng Theo Dõi Tiến Độ

### Giai Đoạn 1: Làm Quen Với Python Căn Bản
- [x] So sánh & Chuyển dịch cú pháp từ Dart sang Python (Class, Async/Await, List/Map).
- [x] Tìm hiểu Type Hinting trong Python (để code an toàn như Dart).
- [x] Xử lý bất đồng bộ với `asyncio`.
- [x] Quản lý môi trường ảo với `venv` và `pip` (Đã có script [setup_env.sh](file:///Volumes/OtherSpace/DEV/multi_ai/setup_env.sh)).

### Giai Đoạn 2: Khái Niệm Cốt Lõi về LLM & API (Python SDK)
- [/] Cài đặt & Gọi thử Gemini API bằng SDK `google-genai` (Chuẩn bị thực hiện).
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
- **25/05/2026**: Bắt đầu dự án. Đã có cấu trúc codebase prototype Python, nắm bắt lý thuyết tổng quan về MCP và workflow phối hợp 2 Agent UI & Test. Bắt đầu Giai đoạn 1: Đã cung cấp tài liệu hướng dẫn học tập chi tiết [learning_content_phase1.md](file:///Volumes/OtherSpace/DEV/multi_ai/docs/learning_content_phase1.md) so sánh Dart và Python cho người học. Môi trường ảo Python (`venv`) đã được thiết lập qua script `setup_env.sh`.
- **25/05/2026 (Tiếp tục)**: Người học đã hoàn thành Giai đoạn 1. Đã xây dựng và kiểm thử thành công các bài tập thực hành trong [practice_solutions.py](file:///Volumes/OtherSpace/DEV/multi_ai/scratch/practice_solutions.py) bao gồm kế thừa lớp Widget, xử lý/phân tích chuỗi logs, và giả lập login bất đồng bộ. Sẵn sàng chuyển tiếp sang Giai đoạn 2.
