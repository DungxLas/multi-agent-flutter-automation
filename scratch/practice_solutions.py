"""
LỜI GIẢI CÁC BÀI TẬP THỰC HÀNH GIAI ĐOẠN 1
Bạn có thể chạy trực tiếp file này bằng lệnh:
python scratch/practice_solutions.py
"""

import asyncio
import random
from typing import List, Dict, Union

# =====================================================================
# BÀI TẬP 1: Class Quản lý Flutter Widget
# =====================================================================
class Widget:
    def __init__(self, name: str, is_renderable: bool = True):
        self.name = name
        self.is_renderable = is_renderable

    def render(self):
        # Phương thức render mặc định
        if self.is_renderable:
            print(f"[Render] Widget: {self.name}")
        else:
            print(f"[Skip] Widget {self.name} không được phép render.")


# Lớp Button kế thừa từ Widget
class Button(Widget):
    def __init__(self, name: str, label: str, is_renderable: bool = True):
        # Gọi constructor của lớp cha (Widget) bằng super()
        super().__init__(name, is_renderable)
        self.label = label

    # Ghi đè phương thức render
    def render(self):
        if self.is_renderable:
            print(f"[Render] Nút bấm: {self.label}")
        else:
            print(f"[Skip] Nút bấm {self.label} không được phép render.")


# =====================================================================
# BÀI TẬP 2: Phân tích Log lỗi của Flutter
# =====================================================================
def parse_flutter_logs(log_data: str) -> List[str]:
    error_lines: List[str] = []
    
    # Tách chuỗi log thành danh sách các dòng dựa vào dấu xuống dòng '\n'
    lines = log_data.split('\n')
    
    for line in lines:
        # Loại bỏ các khoảng trắng thừa ở đầu/cuối dòng (tương đương line.trim() trong Dart)
        cleaned_line = line.strip()
        
        # Kiểm tra xem dòng có bắt đầu bằng "ERROR" hay không
        if cleaned_line.startswith("ERROR"):
            error_lines.append(cleaned_line)
            
    return error_lines


# =====================================================================
# BÀI TẬP 3: Mô phỏng gọi API Đăng nhập bất đồng bộ
# =====================================================================
async def login_request(email: str, password: str) -> Dict[str, Union[bool, str]]:
    # Validate cơ bản
    is_email_valid = "@" in email
    is_password_valid = len(password) >= 6

    if is_email_valid and is_password_valid:
        # Trì hoãn ngẫu nhiên từ 1 đến 2 giây (sử dụng random.uniform)
        delay = random.uniform(1.0, 2.0)
        await asyncio.sleep(delay)
        return {
            "success": True, 
            "token": "mock-token-xyz"
        }
    else:
        return {
            "success": False, 
            "error": "Thông tin đăng nhập không hợp lệ"
        }


# =====================================================================
# HÀM CHẠY KIỂM THỬ LỜI GIẢI (MAIN)
# =====================================================================
async def main():
    print("=========================================================")
    print("CHẠY THỬ NGHIỆM LỜI GIẢI BÀI TẬP THỰC HÀNH GIAI ĐOẠN 1")
    print("=========================================================")

    # 1. Kiểm thử Bài Tập 1
    print("\n--- BÀI TẬP 1: Class & Kế thừa ---")
    btn_active = Button(name="login_btn", label="Đăng Nhập", is_renderable=True)
    btn_inactive = Button(name="submit_btn", label="Gửi đi", is_renderable=False)
    
    btn_active.render()    # Mong muốn in ra: [Render] Nút bấm: Đăng Nhập
    btn_inactive.render()  # Mong muốn in ra: [Skip] Nút bấm Gửi đi không được phép render.

    # 2. Kiểm thử Bài Tập 2
    print("\n--- BÀI TẬP 2: Phân tích Log ---")
    raw_logs = """
    INFO: Application started
    DEBUG: Fetching user configuration
    ERROR: Failed to connect to API gateway (Timeout)
    WARNING: Slow response from server
    ERROR: Flutter widget tree failed to rebuild - Null check operator used on a null value
    INFO: Retrying connection
    """
    errors = parse_flutter_logs(raw_logs)
    print(f"Tìm thấy {len(errors)} dòng lỗi:")
    for err in errors:
        print(f"  -> {err}")

    # 3. Kiểm thử Bài Tập 3
    print("\n--- BÀI TẬP 3: Async/Await Login API ---")
    # Đăng nhập hợp lệ
    print("Đang thử đăng nhập hợp lệ...")
    result_success = await login_request("user@gmail.com", "secret123")
    print(f"Kết quả: {result_success}")

    # Đăng nhập không hợp lệ (sai email & mật khẩu quá ngắn)
    print("\nĐang thử đăng nhập không hợp lệ...")
    result_fail = await login_request("user_gmail.com", "123")
    print(f"Kết quả: {result_fail}")

if __name__ == "__main__":
    asyncio.run(main())
