import os
import sys
import asyncio
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Thêm thư mục gốc dự án vào sys.path để import agents.utils
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.utils import generate_content_with_retry

# Tải cấu hình từ .env
load_dotenv()

# Khởi tạo client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model_name = 'gemini-3.5-flash'
fallback_model = 'gemini-2.5-flash'

# =====================================================================
# BÀI TẬP 1: TRÍCH XUẤT WIDGET TỪ BẢN MÔ TẢ
# =====================================================================

class WidgetSpecs(BaseModel):
    widget_name: str = Field(description="Tên của widget (ví dụ: OTPButton, PasswordField)")
    parameters: list[str] = Field(description="Danh sách các tham số đầu vào cần thiết cho widget")
    state_management: str = Field(description="Phương thức quản lý trạng thái phù hợp (ví dụ: StatefulWidget, StatelessWidget, Riverpod)")
    explanation: str = Field(description="Giải thích ngắn gọn lý do chọn cấu trúc này")

def extract_widget_specs(description: str) -> WidgetSpecs:
    """Gọi Gemini API để trích xuất thông tin WidgetSpecs từ mô tả text."""
    system_instruction = (
        "Bạn là một chuyên gia thiết kế hệ thống UI Flutter. Nhiệm vụ của bạn là phân tích "
        "mô tả yêu cầu Widget và trích xuất ra các thông số kỹ thuật chuẩn hóa dưới dạng JSON."
    )
    
    prompt = f"""
    Hãy phân tích mô tả Widget dưới đây và trích xuất các thông tin kỹ thuật:
    
    Mô tả yêu cầu:
    "{description}"
    """
    
    try:
        response = generate_content_with_retry(
            client=client,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=WidgetSpecs,
                temperature=0.1,
            )
        )
        return response.parsed
    except Exception as e:
        print(f"Lỗi gọi API ở Bài tập 1: {e}")
        # Trả về mock data nếu lỗi
        return WidgetSpecs(
            widget_name="OTPCountdownButton",
            parameters=["duration", "onTimerFinished", "phoneNumber"],
            state_management="StatefulWidget",
            explanation="Cần quản lý trạng thái countdown timer (giảm dần từ 60 về 0) và trạng thái disable nút bấm."
        )


# =====================================================================
# BÀI TẬP 2: MINI SELF-HEALING LOOP (TỰ SỬA LỖI CODE DART)
# =====================================================================

class FixedCodeReport(BaseModel):
    fixed_code: str = Field(description="Mã nguồn Dart đã được sửa lỗi hoàn chỉnh và sạch sẽ")
    explanation: str = Field(description="Giải thích chi tiết lỗi đã được phát hiện và cách khắc phục")

def self_healing_dart_code(broken_code: str, error_log: str) -> FixedCodeReport:
    """Sử dụng Gemini API để phân tích lỗi và sửa code Dart."""
    system_instruction = (
        "Bạn là một Senior Dart/Flutter Developer có khả năng phân tích log lỗi biên dịch/run-time "
        "và sửa chữa mã nguồn tự động. Hãy trả về code sạch và chạy được, không chứa placeholder."
    )
    
    prompt = f"""
    Mã nguồn Dart bị lỗi:
    ```dart
    {broken_code}
    ```
    
    Log lỗi nhận được từ hệ thống:
    {error_log}
    
    Hãy tìm lỗi, sửa nó và giải thích nguyên nhân.
    """
    
    try:
        response = generate_content_with_retry(
            client=client,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=FixedCodeReport,
                temperature=0.1,
            ),
            primary_model='gemini-3.1-pro-preview',
            fallback_model=model_name
        )
        return response.parsed
    except Exception as e:
        print(f"Lỗi gọi API ở Bài tập 2: {e}")
        return FixedCodeReport(
            fixed_code=broken_code,
            explanation=f"Không thể tự động sửa lỗi do API error: {e}"
        )


# =====================================================================
# MAIN FUNCTION ĐỂ KIỂM THỬ
# =====================================================================

async def main():
    print("=========================================================")
    print("BÀI TẬP THỰC HÀNH GIAI ĐOẠN 2: LLM API & STRUCTURED OUTPUT")
    print("=========================================================")

    # 1. Chạy thử Bài tập 1
    print("\n--- BÀI TẬP 1: Trích xuất Widget từ mô tả ---")
    desc = "Tôi muốn làm một nút bấm gửi mã OTP, khi bấm vào sẽ vô hiệu hóa và đếm ngược 60 giây, sử dụng StatefulWidget"
    print(f"Mô tả đầu vào: '{desc}'")
    print("Đang gọi Gemini API...")
    
    specs = extract_widget_specs(desc)
    print("\n[Kết quả phân tích từ AI]:")
    print(f"  - Tên Widget: {specs.widget_name}")
    print(f"  - Các tham số: {specs.parameters}")
    print(f"  - Quản lý trạng thái: {specs.state_management}")
    print(f"  - Giải thích: {specs.explanation}")

    # 2. Chạy thử Bài tập 2 (Self-healing)
    print("\n--- BÀI TẬP 2: Tự động sửa lỗi code (Self-healing Loop) ---")
    
    # Tạo một file Dart giả định bị lỗi cú pháp (thiếu dấu ; ở dòng print)
    mock_file_path = "scratch/temp_broken_widget.dart"
    broken_code = """
import 'package:flutter/material.dart';

class SimpleCard extends StatelessWidget {
  final String title
  
  const SimpleCard({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Text(title)
    );
  }
}
"""
    # Ghi file lỗi
    with open(mock_file_path, "w", encoding="utf-8") as f:
        f.write(broken_code)
    
    print(f"Đã tạo file Dart lỗi tại: {mock_file_path}")
    print("Lỗi giả định: Thiếu dấu chấm phẩy ';' ở khai báo thuộc tính 'title' và trong widget Text(title).")
    
    error_log = "Error: Expected to find ';' at line 5 and line 12."
    print("Đang gọi Gemini để thực hiện Self-healing...")
    
    healing_result = self_healing_dart_code(broken_code, error_log)
    
    print("\n[Giải thích sửa lỗi của AI]:")
    print(healing_result.explanation)
    
    # Ghi đè file code đã sửa
    with open(mock_file_path, "w", encoding="utf-8") as f:
        f.write(healing_result.fixed_code)
    
    print(f"\n✔ Đã tự động ghi đè code đã sửa vào file: {mock_file_path}")
    print("Nội dung file sau khi sửa:")
    print("---------------------------------")
    with open(mock_file_path, "r", encoding="utf-8") as f:
        print(f.read())
    print("---------------------------------")

    # Dọn dẹp file tạm
    if os.path.exists(mock_file_path):
        os.remove(mock_file_path)
        print("Đã dọn dẹp file tạm.")

if __name__ == "__main__":
    asyncio.run(main())
