import os
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from .utils import generate_content_with_retry

class GeneratedCode(BaseModel):
    file_path: str = Field(description="Đường dẫn lưu file code, ví dụ: lib/presentation/pages/login_page.dart")
    code_content: str = Field(description="Mã nguồn Flutter hoàn chỉnh")
    explanation: str = Field(description="Giải thích ngắn gọn cấu trúc và state management được sử dụng")

class UIAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        # Kiểm tra xem API Key có hợp lệ không, tránh lỗi crash nếu người dùng chưa cấu hình
        self.is_mocked = not self.api_key or self.api_key == "your_gemini_api_key_here"
        
        if not self.is_mocked:
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = os.getenv("GEMINI_PRIMARY_MODEL", "gemini-3.5-flash")
            self.fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash")
        else:
            print("[UI Agent] Đang hoạt động ở chế độ giả lập (Mock Mode) vì chưa có GEMINI_API_KEY hợp lệ.")

    def generate_ui(self, ba_document: str, design_desc: str = None) -> GeneratedCode:
        """Sinh mã nguồn Flutter UI dựa trên tài liệu BA và mô tả thiết kế."""
        if self.is_mocked:
            return self._generate_mock_ui()
            
        system_instruction = (
            "Bạn là một Senior Flutter Developer. Nhiệm vụ của bạn là đọc hiểu tài liệu BA "
            "và thiết kế để viết mã nguồn Flutter UI sạch, chuẩn hóa, sử dụng quản lý trạng thái StatefulWidget. "
            "Code của bạn phải sẵn sàng để biên dịch và không chứa các placeholder chưa hoàn thiện."
        )
        
        prompt = f"""
        Dựa trên tài liệu BA dưới đây, hãy sinh code cho Widget/Màn hình Flutter hoàn chỉnh.
        
        Tài liệu BA:
        {ba_document}
        
        Mô tả thiết kế:
        {design_desc or "Theo thiết kế chuẩn Material 3, responsive."}
        """
        
        try:
            # Gọi Gemini API với Structured Output qua Pydantic sử dụng retry helper
            response = generate_content_with_retry(
                client=self.client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=GeneratedCode,
                    temperature=0.2,
                ),
                primary_model=self.model_name,
                fallback_model=self.fallback_model
            )
            
            # SDK sẽ tự động parse JSON sang Object Pydantic nhờ response_schema
            return response.parsed
        except Exception as e:
            print(f"[UI Agent] Gặp lỗi khi gọi API: {e}. Tự động chuyển sang Mock Mode.")
            return self._generate_mock_ui()

    def _generate_mock_ui(self) -> GeneratedCode:
        """Hàm giả lập trả về code Flutter UI mẫu trong trường hợp không có mạng hoặc chưa nhập API Key."""
        mock_code = """import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;
  bool _isLoading = false;

  void _handleLogin() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
      });
      
      // Giả lập gọi API đăng nhập
      await Future.delayed(const Duration(seconds: 2));
      
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(self) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chào mừng quay trở lại')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Nhập email của bạn',
                  prefixIcon: Icon(Icons.email),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty || !value.contains('@')) {
                    return 'Email không hợp lệ';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _passwordController,
                obscureText: _obscurePassword,
                decoration: InputDecoration(
                  labelText: 'Nhập mật khẩu',
                  prefixIcon: const Icon(Icons.lock),
                  suffixIcon: IconButton(
                    icon: Icon(_obscurePassword ? Icons.visibility : Icons.visibility_off),
                    onPressed: () {
                      setState(() {
                        _obscurePassword = !_obscurePassword;
                      });
                    },
                  ),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty || value.length < 6) {
                    return 'Mật khẩu phải từ 6 ký tự trở lên';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _isLoading ? null : _handleLogin,
                child: _isLoading 
                    ? const CircularProgressIndicator()
                    : const Text('Đăng Nhập'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
"""
        return GeneratedCode(
            file_path="lib/presentation/pages/login_screen.dart",
            code_content=mock_code,
            explanation="Widget LoginScreen được thiết kế dạng StatefulWidget, quản lý việc hiển thị password obscure và validate email/mật khẩu tại chỗ."
        )
