# Tài Liệu Học Tập Giai Đoạn 1: Chuyển Dịch Từ Dart Sang Python

Chào mừng bạn bắt đầu hành trình từ **Flutter Developer** trở thành **AI Agent Engineer**. Tài liệu này được biên soạn nhằm giúp bạn tận dụng tối đa kiến thức lập trình Dart sẵn có và chuyển dịch nhanh nhất sang Python.

---

## 1. Class & Object: Bản chất của Hướng Đối Tượng

Trong Dart, bạn đã quen thuộc với khái niệm Class, Hàm khởi tạo (Constructor), và từ khóa `this`. Hãy xem cách Python biểu diễn chúng:

### So sánh cú pháp:

| Đặc điểm | Dart | Python |
| :--- | :--- | :--- |
| **Khai báo Class** | `class User { ... }` | `class User:` (Không dùng dấu ngoặc nhọn `{}`) |
| **Hàm khởi tạo** | Trùng tên Class hoặc dùng Named Constructor | Hàm khởi tạo bắt buộc là `__init__(self, ...)` |
| **Con trỏ trỏ đến chính nó** | `this` (Không bắt buộc ghi ra trừ khi trùng tên) | `self` (Bắt buộc khai báo là tham số đầu tiên trong mọi method) |
| **Khởi tạo instance** | `var user = User(name, age);` | `user = User(name, age)` (Không dùng từ khóa `new`) |

### Ví dụ thực tế:

**Dart:**
```dart
class Student {
  final String name;
  final int age;

  // Constructor
  Student({required this.name, required this.age});

  void introduce() {
    print("Tôi tên là $name, $age tuổi.");
  }
}

void main() {
  final student = Student(name: "Hải", age: 28);
  student.introduce();
}
```

**Python:**
```python
class Student:
    # Constructor nhận tham số khởi tạo và gán vào thuộc tính qua self
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    # Mọi phương thức trong class đều phải nhận 'self' đầu tiên
    def introduce(self):
        print(f"Tôi tên là {self.name}, {self.age} tuổi.")

# Khởi tạo đối tượng (không dùng từ khóa new)
student = Student(name="Hải", age=28)
student.introduce()
```

> [!TIP]
> Trong Python, các phương thức bắt đầu bằng dấu gạch dưới kép (`__`) như `__init__` hay `__str__` được gọi là **Dunder Methods** (hoặc Magic Methods). Chúng được Python gọi ngầm định dưới các tình huống cụ thể (ví dụ: `__init__` gọi khi tạo object, `__str__` gọi khi dùng `print(object)`).

---

## 2. Collections: List, Map (Dict) và Set

Python sở hữu cấu trúc dữ liệu rất linh hoạt và tối ưu. Các cấu trúc này ánh xạ trực tiếp sang các kiểu dữ liệu bạn đã biết trong Dart.

| Loại cấu trúc | Dart | Python | Mô tả |
| :--- | :--- | :--- | :--- |
| **Danh sách** | `List<T>` | `list` hoặc `List[T]` | Lưu trữ có thứ tự, cho phép trùng lặp. |
| **Bản đồ** | `Map<K, V>` | `dict` hoặc `Dict[K, V]` | Cặp Key - Value. |
| **Tập hợp** | `Set<T>` | `set` hoặc `Set[T]` | Tập hợp không trùng lặp, không thứ tự. |

### Các thao tác phổ biến:

**Dart:**
```dart
// 1. List
List<String> fruits = ['Táo', 'Chuối'];
fruits.add('Cam');
print(fruits[0]);

// 2. Map
Map<String, int> scores = {'Toan': 9, 'Van': 8};
scores['Anh'] = 10;

// 3. Set
Set<int> uniqueNumbers = {1, 2, 2}; // Kết quả: {1, 2}
```

**Python:**
```python
# 1. List
fruits = ['Táo', 'Chuối']
fruits.append('Cam')  # Dùng append thay vì add
print(fruits[0])

# 2. Dict (Map)
scores = {'Toan': 9, 'Van': 8}
scores['Anh'] = 10
# Sử dụng phương thức .get() để tránh lỗi crash khi key không tồn tại
print(scores.get('Ly', 0))  # Trả về 0 nếu không tìm thấy key 'Ly'

# 3. Set
unique_numbers = {1, 2, 2}  # Kết quả: {1, 2}
```

---

## 3. Type Hinting: Mang sự an toàn kiểu của Dart vào Python

Dart là một ngôn ngữ **strongly-typed** (kiểm tra kiểu nghiêm ngặt lúc compile). Ngược lại, Python là **dynamically-typed** (chỉ kiểm tra lúc chạy). 
Tuy nhiên, để tránh lỗi ngớ ngẩn và giúp IDE gợi ý code thông minh như VS Code/Android Studio, Python hỗ trợ **Type Hinting** từ phiên bản 3.5.

### Cách viết:

```python
# Biến thông thường
age: int = 25
name: str = "Alice"
is_active: bool = True

# Sử dụng module typing cho cấu trúc phức tạp
from typing import List, Dict, Optional, Union

# Một danh sách các chuỗi
names: List[str] = ["Hải", "Lan"]

# Dictionary có key là str, value là int
config: Dict[str, int] = {"port": 8080, "timeout": 30}

# Hàm nhận vào và trả về giá trị có kiểu xác định
def greet(name: str) -> str:
    return f"Xin chào {name}"

# Kiểu dữ liệu có thể Null (tương đương với String? hay int? trong Dart)
# Sử dụng Optional[type] (tương đương Union[type, None])
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Admin"
    return None  # None tương đương với null trong Dart
```

---

## 4. Xử lý Bất Đồng Bộ: Async/Await & Event Loop

Cả Dart và Python đều sử dụng mô hình **Single-threaded Event Loop** để xử lý bất đồng bộ. Khái niệm `Future` trong Dart tương đương với `Coroutine` hoặc `Task` trong Python.

### So sánh cú pháp:

| Khái niệm | Dart | Python (`asyncio`) |
| :--- | :--- | :--- |
| **Khai báo hàm async** | `Future<void> myFunction() async { ... }` | `async def my_function():` |
| **Chờ kết quả** | `await future;` | `await coroutine` |
| **Trì hoãn thời gian** | `await Future.delayed(Duration(seconds: 1));` | `await asyncio.sleep(1)` |
| **Chạy đồng thời nhiều tác vụ** | `await Future.wait([task1, task2]);` | `await asyncio.gather(task1, task2)` |

### Ví dụ so sánh:

**Dart:**
```dart
Future<String> fetchUserData() async {
  await Future.delayed(Duration(seconds: 2));
  return "Dữ liệu người dùng";
}

void main() async {
  print("Bắt đầu...");
  String data = await fetchUserData();
  print(data);
}
```

**Python:**
```python
import asyncio

async def fetch_user_data() -> str:
    await asyncio.sleep(2)  # Trì hoãn 2 giây không chặn luồng chính
    return "Dữ liệu người dùng"

async def main():
    print("Bắt đầu...")
    data = await fetch_user_data()
    print(data)

# Khởi động Event Loop (Chỉ gọi một lần ở điểm bắt đầu chương trình)
if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. Quản lý Môi trường ảo (Virtual Environment - `venv`)

Khi làm việc với Dart, môi trường dependencies được định nghĩa trong `pubspec.yaml` và lưu trong thư mục toàn cục pub-cache.
Trong Python, nếu cài đặt thư viện trực tiếp bằng lệnh `pip install`, thư viện sẽ cài đè lên toàn bộ hệ thống máy tính, dễ gây xung đột giữa các dự án khác nhau.

Vì vậy, lập trình viên Python luôn sử dụng **Virtual Environment (venv)**.

### Quy trình làm việc thực tế:

1. **Khởi tạo môi trường ảo (venv)**:
   ```bash
   python3 -m venv venv
   ```
   Lệnh này tạo ra một thư mục `venv/` chứa một bản sao độc lập của Python và trình quản lý thư viện `pip`.

2. **Kích hoạt môi trường ảo**:
   * Trên macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   * Trên Windows (Powershell):
     ```cmd
     .\venv\Scripts\Activate.ps1
     ```
   Sau khi kích hoạt, dòng nhắc của Terminal sẽ có chữ `(venv)` ở đầu.

3. **Cài đặt thư viện**:
   Thay vì `pub get`, bạn chạy:
   ```bash
   pip install -r requirements.txt
   ```
   Hoặc cài đặt lẻ:
   ```bash
   pip install google-genai
   ```

4. **Hủy kích hoạt (Khi không code dự án này nữa)**:
   ```bash
   deactivate
   ```

---

## 6. Bài Tập Thực Hành Dành Cho Bạn

Hãy tạo các file code Python của riêng bạn trong thư mục `scratch/` để giải quyết các bài tập sau nhằm củng cố kiến thức:

### Bài Tập 1: Viết Class Quản Lý Flutter Widget
* **Yêu cầu**: Định nghĩa một Class `Widget` có thuộc tính `name` (tên widget) và `is_renderable: bool`. Viết một class con `Button` kế thừa từ `Widget`, bổ sung thêm thuộc tính `label`. Ghi đè phương thức `render()` để in ra màn hình chuỗi: `"[Render] Nút bấm: <label>"` nếu `is_renderable` là True.
* **Mục tiêu**: Làm quen cú pháp kế thừa (`class Child(Parent):`) và constructor trong Python.

### Bài Tập 2: Phân tích Log lỗi của Flutter
* **Yêu cầu**: Viết hàm `parse_flutter_logs(log_data: str) -> List[str]`. Nhận vào một chuỗi log lớn và trả về danh sách chỉ chứa các dòng bắt đầu bằng chữ `"ERROR"`.
* **Gợi ý**: Sử dụng hàm `split('\n')` để tách dòng, và cấu trúc điều kiện `if line.startswith("ERROR"):` của Python.

### Bài Tập 3: Mô phỏng gọi API Đăng nhập bất đồng bộ
* **Yêu cầu**: Viết một coroutine `login_request(email: str, password: str) -> Dict[str, Union[bool, str]]`. 
  * Nếu email hợp lệ (có chứa ký tự `@`) và password dài từ 6 ký tự trở lên: Trì hoãn ngẫu nhiên từ 1 đến 2 giây (dùng `asyncio.sleep`) rồi trả về `{"success": True, "token": "mock-token-xyz"}`.
  * Ngược lại: Trả về `{"success": False, "error": "Thông tin đăng nhập không hợp lệ"}`.
* **Mục tiêu**: Thực hành lập trình async/await, type hinting với Union/Dict và xử lý logic cơ bản.

---

> [!NOTE]
> Bạn có thể viết lời giải cho các bài tập này vào file [scratch/my_practice.py](file:///Volumes/OtherSpace/DEV/multi_ai/scratch/my_practice.py), sau đó chạy lệnh `python scratch/my_practice.py` để tự kiểm chứng kết quả!
