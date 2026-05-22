# Business Requirement Document: Màn Hình Đăng Nhập (Login Screen)

Tài liệu này định nghĩa các yêu cầu nghiệp vụ và kỹ thuật cho tính năng Đăng nhập trong ứng dụng.

---

## 1. Yêu Cầu Giao Diện (UI Requirements)
Màn hình đăng nhập cần chứa các phần tử giao diện sau:
* **Tiêu đề**: "Chào mừng quay trở lại" (Font size: 24, Bold).
* **Trường nhập Email** (`EmailTextField`):
  * Placeholder: "Nhập email của bạn".
  * Có biểu tượng icon email ở trước.
* **Trường nhập Mật khẩu** (`PasswordTextField`):
  * Placeholder: "Nhập mật khẩu".
  * Có biểu tượng icon khóa ở trước.
  * Có nút ẩn/hiện mật khẩu (toggle visibility) ở cuối trường.
* **Nút bấm Đăng nhập** (`LoginButton`):
  * Text hiển thị: "Đăng Nhập".
  * Chiều rộng kéo dài hết chiều ngang (full width).
  * Màu nền chủ đạo (Primary color).

---

## 2. Quy Tắc Ràng Buộc & Validation (Business Rules)
* **Email Validation**:
  * Định dạng email phải hợp lệ (phải chứa ký tự `@` và domain hợp lệ).
  * Nếu trống hoặc không hợp lệ, khi nhấn nút Đăng nhập phải hiển thị lỗi: "Email không hợp lệ".
* **Password Validation**:
  * Mật khẩu phải có độ dài tối thiểu là 6 ký tự.
  * Nếu trống hoặc dưới 6 ký tự, khi nhấn nút Đăng nhập phải hiển thị lỗi: "Mật khẩu phải từ 6 ký tự trở lên".
* **Trạng thái Loading**:
  * Khi người dùng nhấn nút Đăng nhập hợp lệ, hệ thống sẽ thực hiện tiến trình xác thực (Loading).
  * Ở trạng thái loading, nút bấm Đăng nhập sẽ bị vô hiệu hóa (disabled) và hiển thị một vòng xoay loading (`CircularProgressIndicator`) thay cho chữ "Đăng Nhập".

---

## 3. Các Kịch Bản Kiểm Thử Yêu Cầu (Test Scenarios)
Bộ Widget Test tương ứng phải đảm bảo xác thực các kịch bản sau:
1. **Kiểm tra UI ban đầu**: Màn hình hiển thị đầy đủ tiêu đề, email field, password field và nút Đăng nhập ở trạng thái hoạt động bình thường.
2. **Kiểm tra ẩn/hiện mật khẩu**: Nhấp vào icon ẩn/hiện mật khẩu phải chuyển đổi thuộc tính `obscureText` của password field từ true sang false và ngược lại.
3. **Kiểm tra lỗi validate email**: Nhập sai định dạng email và bấm Đăng nhập -> Kiểm tra hiển thị thông báo lỗi "Email không hợp lệ".
4. **Kiểm tra lỗi validate mật khẩu**: Nhập mật khẩu dưới 6 ký tự và bấm Đăng nhập -> Kiểm tra hiển thị thông báo lỗi "Mật khẩu phải từ 6 ký tự trở lên".
5. **Kiểm tra trạng thái Loading**: Khi kích hoạt tiến trình đăng nhập, nút bấm chuyển sang hiển thị vòng xoay loading và người dùng không thể nhấn nút được nữa.
