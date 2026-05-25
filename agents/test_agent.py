import os
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from .utils import generate_content_with_retry

class GeneratedTest(BaseModel):
    file_path: str = Field(description="Đường dẫn lưu file test, ví dụ: test/presentation/pages/login_page_test.dart")
    test_code_content: str = Field(description="Mã nguồn Flutter Widget Test hoàn chỉnh")
    test_scenarios_covered: list[str] = Field(description="Danh sách các kịch bản test đã được bao phủ trong code này")

class HealedCode(BaseModel):
    ui_code_content: str = Field(description="Mã nguồn Flutter UI (LoginPage) sau khi đã sửa đổi để vượt qua bài test")
    test_code_content: str = Field(description="Mã nguồn Flutter Widget Test sau khi đã sửa đổi để vượt qua bài test")
    explanation: str = Field(description="Giải thích chi tiết lỗi nào đã được tìm thấy và các chỉnh sửa đã thực hiện ở cả UI và Test")

class TestAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.is_mocked = not self.api_key or self.api_key == "your_gemini_api_key_here"
        
        if not self.is_mocked:
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = os.getenv("GEMINI_PRIMARY_MODEL", "gemini-3.5-flash")
            self.fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash")
        else:
            print("[Test Agent] Đang hoạt động ở chế độ giả lập (Mock Mode) vì chưa có GEMINI_API_KEY hợp lệ.")

    def generate_tests(self, ba_document: str, ui_code_content: str, package_name: str = None) -> GeneratedTest:
        """Sinh mã nguồn Flutter Widget Test dựa trên BA và mã nguồn UI thực tế."""
        if self.is_mocked:
            return self._generate_mock_tests()
            
        system_instruction = (
            "Bạn là một chuyên gia viết Widget Test và Integration Test cho Flutter. "
            "Nhiệm vụ của bạn là đọc hiểu mã nguồn UI và tài liệu BA để viết các bài test "
            "bao phủ tất cả kịch bản nghiệp vụ (validation, loading, user interactions). "
            "Hãy sử dụng thư viện flutter_test mặc định.\n"
            "LƯU Ý QUAN TRỌNG: Trong Flutter Widget Test, lớp TextFormField không có getter công khai tên là 'decoration'. "
            "Để tìm TextFormField theo hintText, hãy tìm lớp TextField thay thế (ví dụ: widget is TextField && widget.decoration?.hintText == hintText). "
            "Tránh sử dụng 'widget is TextFormField && widget.decoration' vì nó sẽ gây lỗi biên dịch."
        )
        
        import_instruction = ""
        if package_name:
            import_instruction = f"Hãy chú ý: Tên package của dự án Flutter là '{package_name}'. Bạn bắt buộc phải import file UI bằng đường dẫn package đầy đủ, ví dụ: import 'package:{package_name}/presentation/pages/login_page.dart'; chứ không được dùng import tương đối hay giả định tên package khác."
        else:
            import_instruction = "Hãy đảm bảo import đúng đường dẫn đến file UI."

        prompt = f"""
        Đầu vào của bạn gồm:
        1. Tài liệu BA:
        {ba_document}
        
        2. Mã nguồn UI đã viết:
        {ui_code_content}
        
        Hãy viết bộ Widget Test hoàn chỉnh để kiểm thử Widget UI trên.
        {import_instruction}
        """
        
        try:
            # Gọi Gemini API với Structured Output qua Pydantic sử dụng retry helper
            response = generate_content_with_retry(
                client=self.client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=GeneratedTest,
                    temperature=0.2,
                ),
                primary_model=self.model_name,
                fallback_model=self.fallback_model
            )
            
            return response.parsed
        except Exception as e:
            print(f"[Test Agent] Gặp lỗi khi gọi API: {e}. Tự động chuyển sang Mock Mode.")
            return self._generate_mock_tests()

    def _generate_mock_tests(self) -> GeneratedTest:
        """Giả lập trả về code Widget Test mẫu."""
        mock_test_code = """import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
// Giả định import màn hình login_screen
import 'package:login_app/presentation/pages/login_screen.dart';

void main() {
  Widget createWidgetUnderTest() {
    return const MaterialApp(
      home: LoginScreen(),
    );
  }

  testWidgets('Hiển thị đầy đủ UI ban đầu', (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    expect(find.text('Chào mừng quay trở lại'), findsOneWidget);
    expect(find.byType(TextFormField), findsNWidgets(2)); // Email & Password
    expect(find.text('Đăng Nhập'), findsOneWidget);
  });

  testWidgets('Lỗi validate email khi nhập sai định dạng', (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    // Nhập sai email
    await tester.enterText(find.byType(TextFormField).first, 'invalid-email');
    await tester.enterText(find.byType(TextFormField).last, '123456'); // Pass hợp lệ
    
    // Nhấp đăng nhập
    await tester.tap(find.text('Đăng Nhập'));
    await tester.pump(); // Cập nhật UI

    // Mong đợi thông báo lỗi
    expect(find.text('Email không hợp lệ'), findsOneWidget);
  });

  testWidgets('Lỗi validate mật khẩu dưới 6 ký tự', (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    // Nhập email đúng, mật khẩu quá ngắn
    await tester.enterText(find.byType(TextFormField).first, 'test@gmail.com');
    await tester.enterText(find.byType(TextFormField).last, '12345');
    
    await tester.tap(find.text('Đăng Nhập'));
    await tester.pump();

    expect(find.text('Mật khẩu phải từ 6 ký tự trở lên'), findsOneWidget);
  });

  testWidgets('Ẩn hiện mật khẩu khi nhấn icon suffix', (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    // Tìm ô password (ở vị trí thứ 2)
    final passwordFieldFinder = find.byType(TextFormField).last;
    
    // Mặc định obscureText phải là true
    TextField passwordField = tester.widget<TextField>(
      find.descendant(of: passwordFieldFinder, matching: find.byType(TextField))
    );
    expect(passwordField.obscureText, isTrue);

    // Bấm vào suffix icon (IconButton)
    await tester.tap(find.byType(IconButton));
    await tester.pump();

    // obscureText bây giờ phải là false
    passwordField = tester.widget<TextField>(
      find.descendant(of: passwordFieldFinder, matching: find.byType(TextField))
    );
    expect(passwordField.obscureText, isFalse);
  });
}
"""
        return GeneratedTest(
            file_path="test/presentation/pages/login_screen_test.dart",
            test_code_content=mock_test_code,
            test_scenarios_covered=[
                "Hiển thị đầy đủ UI ban đầu",
                "Lỗi validate email khi nhập sai định dạng",
                "Lỗi validate mật khẩu dưới 6 ký tự",
                "Ẩn hiện mật khẩu khi nhấn icon suffix"
            ]
        )

    def heal_code(self, ba_document: str, ui_code_content: str, test_code_content: str, error_log: str, package_name: str = None) -> HealedCode:
        """Tự động sửa lỗi cho cả UI code và Test code dựa trên log lỗi test thất bại."""
        if self.is_mocked:
            # Trong chế độ Mock, chỉ cần trả về phiên bản sửa đổi chuỗi SnackBar
            healed_ui = ui_code_content.replace("Đăng nhập thành công! (Chỉ là mô phỏng)", "Đăng nhập thành công! (Demo)")
            return HealedCode(
                ui_code_content=healed_ui,
                test_code_content=test_code_content,
                explanation="Giả lập tự động đồng bộ hóa thông điệp SnackBar thành công ở file UI giống file Test."
            )

        system_instruction = (
            "Bạn là một Senior Flutter Developer và QA Automation Lead. "
            "Nhiệm vụ của bạn là phân tích log lỗi kiểm thử (flutter test), tìm ra điểm không khớp hoặc lỗi "
            "trong mã nguồn UI hoặc mã nguồn Test, sửa đổi chúng để tất cả các bài test đều vượt qua thành công.\n"
            "LƯU Ý QUAN TRỌNG: Trong Flutter Widget Test, lớp TextFormField không có getter công khai tên là 'decoration'. "
            "Để tìm TextFormField theo hintText, hãy tìm lớp TextField thay thế (ví dụ: widget is TextField && widget.decoration?.hintText == hintText). "
            "Tránh sử dụng 'widget is TextFormField && widget.decoration' vì nó sẽ gây lỗi biên dịch."
        )

        prompt = f"""
        Chúng tôi đã chạy kiểm thử Widget Test cho màn hình LoginPage và gặp lỗi.
        
        1. Tài liệu BA:
        {ba_document}
        
        2. Mã nguồn UI hiện tại:
        {ui_code_content}
        
        3. Mã nguồn Test hiện tại:
        {test_code_content}
        
        4. Log lỗi từ lệnh 'flutter test':
        {error_log}
        
        Hãy phân tích nguyên nhân lỗi, quyết định xem cần sửa file UI (LoginPage), file Test hay cả hai để khớp logic.
        Trả về mã nguồn hoàn chỉnh đã sửa cho cả hai file và giải thích chi tiết.
        Đảm bảo giữ nguyên các import package hợp lệ.
        """

        try:
            response = generate_content_with_retry(
                client=self.client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=HealedCode,
                    temperature=0.1,
                ),
                primary_model=os.getenv("GEMINI_HEAL_MODEL", "gemini-3.1-pro-preview"),
                fallback_model=self.model_name
            )
            return response.parsed
        except Exception as e:
            print(f"[Test Agent] Gặp lỗi khi gọi API Self-healing: {e}. Trả về code cũ.")
            return HealedCode(
                ui_code_content=ui_code_content,
                test_code_content=test_code_content,
                explanation=f"Không thể tự động sửa do lỗi gọi API: {str(e)}"
            )
