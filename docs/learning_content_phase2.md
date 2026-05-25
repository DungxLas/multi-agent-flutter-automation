# Tài Liệu Học Tập Giai Đoạn 2: Khái Niệm Cốt Lõi về LLM & API (google-genai Python SDK)

Chào mừng bạn đến với **Giai Đoạn 2**. Ở giai đoạn này, chúng ta sẽ kết nối mã nguồn Python với bộ não AI Gemini bằng SDK chính thức mới nhất của Google (`google-genai`). Bạn sẽ học cách viết Prompt động, bắt buộc AI trả về cấu trúc dữ liệu JSON chính xác thông qua **Pydantic** và sử dụng **Function Calling (Tool Use)**.

---

## 1. Cài đặt và Khởi tạo Client

Để bắt đầu, hãy đảm bảo môi trường ảo của bạn đã được kích hoạt và cài đặt thư viện `google-genai` (nằm trong file `requirements.txt`).

```bash
# Kích hoạt venv (nếu chưa)
source venv/bin/activate

# Cài đặt hoặc cập nhật thư viện
pip install google-genai pydantic python-dotenv
```

### Cách khởi tạo Client:
Chúng ta sử dụng `dotenv` để tải `GEMINI_API_KEY` từ file `.env` ẩn.

```python
import os
from dotenv import load_dotenv
from google import genai

# Tải biến môi trường từ file .env
load_dotenv()

# Lấy API Key từ môi trường
api_key = os.getenv("GEMINI_API_KEY")

# Khởi tạo client chính thức
client = genai.Client(api_key=api_key)
```

> [!IMPORTANT]
> Hãy chắc chắn bạn đã thay đổi `your_gemini_api_key_here` trong file `.env` thành API Key thật của bạn được lấy từ Google AI Studio.

---

## 2. Gọi Thử Gemini API và Prompt Engineering Dùng f-string

Trong Python, cách tốt nhất để xây dựng Prompt động (tương tự như ghép chuỗi bằng `$` trong Dart) là sử dụng **f-strings** (formatted string literals).

### Ví dụ cơ bản:

```python
def generate_flutter_class_prompt(class_name: str, fields: list[str]) -> str:
    # f-string cho phép nhúng trực tiếp biến hoặc code vào trong chuỗi bằng dấu ngoặc nhọn {}
    fields_str = "\n".join([f"  final String {field};" for field in fields])
    
    prompt = f"""
    Hãy tạo một Class Dart Flutter có tên là {class_name} với các thuộc tính sau:
    {fields_str}
    
    Hãy viết constructor hoàn chỉnh và phương thức toJson/fromJson.
    """
    return prompt

# Tạo prompt động
prompt = generate_flutter_class_prompt("UserModel", ["id", "name", "email"])

# Gọi Gemini sinh nội dung
response = client.models.generate_content(
    model='gemini-2.5-flash', # Model khuyên dùng cho tốc độ và hiệu năng tốt nhất
    contents=prompt,
)

print(response.text)
```

---

## 3. Structured Output: Ép AI Trả Về Dữ Liệu Cấu Trúc (Pydantic)

Đây là tính năng cực kỳ mạnh mẽ. Thay vì nhận về text thô (Markdown) rồi viết regex để parse (rất dễ lỗi), chúng ta định nghĩa một class **Pydantic Model** (tương tự như class Model trong Dart) và truyền cho Gemini. AI sẽ bắt buộc phải trả về đúng cấu trúc JSON đó.

### Ví dụ thực tế: Định nghĩa cấu trúc phân tích lỗi Flutter

```python
from pydantic import BaseModel, Field

# 1. Định nghĩa cấu trúc dữ liệu mong muốn
class FlutterBugReport(BaseModel):
    error_summary: str = Field(description="Tóm tắt ngắn gọn lỗi là gì")
    file_location: str = Field(description="Đường dẫn file gây ra lỗi (nếu có trong log)")
    probable_cause: str = Field(description="Nguyên nhân dự đoán gây ra lỗi")
    fix_suggestions: list[str] = Field(description="Các gợi ý sửa lỗi tương ứng")

# 2. Tạo prompt
log_data = "Error: Assertion failed: file:///app/lib/main.dart:45:12: 'counter >= 0' is not true."

prompt = f"Hãy phân tích log lỗi sau đây từ dự án Flutter:\n{log_data}"

# 3. Gọi API với response_schema
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=FlutterBugReport, # Ép kiểu trả về
        temperature=0.1, # Thiết lập nhiệt độ thấp để AI trả về chính xác, ít sáng tạo linh tinh
    ),
)

# 4. Trích xuất kết quả đã được parse tự động thành Object Python
bug_analysis: FlutterBugReport = response.parsed
print(f"Lỗi: {bug_analysis.error_summary}")
print(f"Gợi ý sửa: {bug_analysis.fix_suggestions[0]}")
```

---

## 4. Function Calling (Tool Use): Cho Phép AI Gọi Hàm Python Của Bạn

Function Calling giúp bạn khai báo các hàm Python thông thường (ví dụ: đọc file, ghi file, chạy terminal) và gửi thông tin hàm đó cho LLM. Khi LLM thấy yêu cầu của người dùng cần đến hàm đó, nó sẽ không tự trả lời bằng văn bản mà trả về yêu cầu chạy hàm kèm tham số. Sau đó, code Python của bạn sẽ chạy hàm và gửi kết quả lại cho LLM.

*Lưu ý:* SDK `google-genai` có thể tự động chạy hàm cho bạn nếu bạn khai báo nó trong `config.tools`.

### Ví dụ thực tế: Tạo tool chạy lệnh Flutter Test cho AI

```python
import subprocess
from google.genai import types

# 1. Định nghĩa hàm Python với Type Hinting và Docstring rõ ràng (AI sẽ đọc docstring để biết khi nào cần dùng hàm)
def run_local_command(cmd: str) -> str:
    """
    Thực thi một lệnh shell dưới hệ thống local và trả về kết quả output.
    
    Args:
        cmd: Câu lệnh terminal cần thực thi (ví dụ: 'flutter test', 'ls').
    """
    try:
        # Chạy lệnh shell an toàn trong dự án
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Lỗi thực thi lệnh: {str(e)}"

# 2. Khai báo tool và gọi Gemini
prompt = "Hãy chạy kiểm thử bằng lệnh 'flutter test' và cho tôi biết kết quả có pass không?"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        # Đưa hàm vào danh sách công cụ AI được quyền gọi
        tools=[run_local_command],
        # Tự động thực thi hàm local nếu AI yêu cầu (automatic function calling)
        # Chỉ có ở google-genai SDK
    )
)

print(response.text)
```

---

## 5. Bài Tập Thực Hành Giai Đoạn 2

Hãy tạo file `scratch/practice_phase2.py` để giải quyết các bài tập sau:

### Bài Tập 1: Trích xuất Widget từ bản mô tả
* **Yêu cầu**: Hãy định nghĩa một Pydantic Model `WidgetSpecs` chứa: `widget_name` (str), `parameters` (list[str]), `state_management` (str - ví dụ: StatefulWidget, StatelessWidget, Riverpod).
* Viết hàm gọi Gemini API truyền vào một đoạn văn mô tả Widget (ví dụ: *"Tôi muốn làm một nút bấm gửi mã OTP, khi bấm vào sẽ vô hiệu hóa và đếm ngược 60 giây, sử dụng StatefulWidget"*). Bắt AI trả về cấu trúc dữ liệu `WidgetSpecs` đã được phân tích.

### Bài Tập 2: Hệ thống Agent sửa lỗi tự động (Mini Self-healing Loop)
* **Yêu cầu**: Viết một chương trình nhỏ mô phỏng:
  1. Đọc một file code Dart lỗi giả định (ví dụ: thiếu dấu chấm phẩy `;`).
  2. Dùng Gemini phân tích lỗi và trả về code Dart đã sửa dưới dạng Structured Output chứa: `fixed_code` (str) và `explanation` (str).
  3. Ghi đè code đã sửa vào file giả định đó.

---

> [!NOTE]
> Giải quyết xong các bài tập này sẽ giúp bạn hoàn toàn tự tin chuyển sang **Giai đoạn 3: Model Context Protocol (MCP)** để bắt đầu tự động hóa thật sự trên IDE.
