# Nghiên Cứu Chuyên Sâu: Model Context Protocol (MCP) & Flutter Integration

Tài liệu này cung cấp kiến thức nền tảng chi tiết về **Model Context Protocol (MCP)** và cách tự xây dựng một MCP Server bằng **Python** phục vụ cho việc tự động hóa kiểm thử và phát triển ứng dụng Flutter.

---

## 1. Kiến Trúc MCP (Model Context Protocol)

MCP hoạt động theo mô hình Client-Server chuẩn, dựa trên giao thức truyền tin JSON-RPC 2.0 thông qua Standard Input/Output (stdin/stdout) hoặc SSE (Server-Sent Events) qua HTTP.

```
┌────────────────────────┐
│     AI Agent / IDE     │  (Ví dụ: Cursor, Claude Desktop, Custom Agent)
│        (Client)        │
└───────────┬────────────┘
            │
            │  stdin / stdout (JSON-RPC)
            │
┌───────────▼────────────┐
│    Python MCP Server   │  (Chương trình Python chạy ở nền local máy)
│      (FastMCP SDK)     │
└───────────┬────────────┘
            │
    ┌───────┼───────┐
    │       │       │
┌───▼───┐┌──▼───┐┌──▼───┐
│ Files ││ Shell││ API  │   (Tài nguyên & Công cụ thực tế trên máy của bạn)
└───────┘└──────┘└──────┘
```

### Các Thành Phần Chính của MCP:
1. **Host/Client**: Phần mềm tương tác trực tiếp với người dùng và LLM (như Cursor, VS Code, Claude Desktop, hoặc Script Python Orchestrator của bạn). Client chịu trách nhiệm kết nối, gửi yêu cầu dịch vụ đến MCP Server.
2. **Server**: Một ứng dụng chạy ngầm (trong trường hợp này là script Python của chúng ta) cung cấp 3 tính năng cốt lõi qua giao thức MCP:
   * **Prompts**: Các mẫu prompt viết sẵn mà Client có thể nạp vào LLM.
   * **Resources**: Các nguồn dữ liệu chỉ đọc (tài liệu BA, logs, file cấu hình).
   * **Tools**: Các hàm thực thi có thể làm thay đổi trạng thái hệ thống (tạo file, chạy lệnh shell `flutter test`).

---

## 2. Cách Viết Một Custom MCP Server Bằng Python Cho Flutter

Để điều khiển được môi trường Flutter, chúng ta cần viết một MCP Server có khả năng tương tác với các công cụ CLI của Flutter.

### Khởi tạo Dự Án MCP Server
Đầu tiên, cài đặt SDK MCP chính thức của Anthropic dành cho Python:
```bash
pip install mcp
```

### Script Python MCP Server mẫu (`mcp_flutter_server.py`):
Dưới đây là cấu trúc mã nguồn hoàn chỉnh của một Server MCP dùng để kiểm soát Flutter:

```python
import subprocess
from mcp.server.fastmcp import FastMCP

# Khởi tạo MCP Server với tên định danh
mcp = FastMCP("FlutterDeveloperTools")

@mcp.tool()
def run_flutter_test(project_path: str, test_file_path: str = None) -> str:
    """
    Chạy bộ kiểm thử (Widget / Unit Test) trong dự án Flutter.
    
    Args:
        project_path: Đường dẫn tuyệt đối đến thư mục gốc của dự án Flutter.
        test_file_path: (Tùy chọn) Đường dẫn cụ thể đến file test muốn chạy (ví dụ: test/widget_test.dart).
    """
    command = ["flutter", "test"]
    if test_file_path:
        command.append(test_file_path)
        
    try:
        # Chạy lệnh shell
        result = subprocess.run(
            command,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120 # Giới hạn 2 phút
        )
        
        # Tạo chuỗi phản hồi rõ ràng cho AI Agent đọc
        response = f"Mã thoát (Exit Code): {result.returncode}\n\n"
        if result.returncode == 0:
            response += "=== KẾT QUẢ: TẤT CẢ TEST CASES ĐỀU ĐẠT (PASS) ===\n"
            response += result.stdout
        else:
            response += "=== KẾT QUẢ: CÓ TEST CASE THẤT BẠI (FAIL) ===\n"
            response += f"--- STDOUT ---\n{result.stdout}\n"
            response += f"--- STDERR ---\n{result.stderr}\n"
            
        return response
    except subprocess.TimeoutExpired:
        return "Lỗi: Lệnh chạy test bị quá thời gian cho phép (Timeout 120s)."
    except Exception as e:
        return f"Lỗi không xác định khi chạy lệnh: {str(e)}"

@mcp.tool()
def run_flutter_analyze(project_path: str) -> str:
    """
    Chạy công cụ phân tích cú pháp (Linter/Analyzer) của Flutter để tìm lỗi cú pháp.
    
    Args:
        project_path: Đường dẫn tuyệt đối đến thư mục gốc của dự án Flutter.
    """
    try:
        result = subprocess.run(
            ["flutter", "analyze"],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return "Flutter Analyze: Không phát hiện lỗi cú pháp nào! Code sạch."
        else:
            return f"Phát hiện lỗi phân tích cú pháp:\n{result.stdout}"
    except Exception as e:
        return f"Lỗi khi chạy flutter analyze: {str(e)}"

if __name__ == "__main__":
    # Chạy server ở chế độ Standard Input/Output (stdin/stdout)
    # Đây là chế độ mặc định giúp IDE (như Cursor) hoặc Orchestrator kết nối trực tiếp.
    mcp.run()
```

---

## 3. Cách Kết Nối MCP Server Vào IDE (Ví dụ: Cursor / Claude Desktop)

Khi bạn muốn tích hợp MCP Server trên vào IDE của mình để chat trực tiếp với AI và nhờ nó chạy test, hãy làm theo các bước sau:

### Cấu hình trong Cursor:
1. Mở Cursor -> **Settings** -> **Features** -> **MCP**.
2. Nhấp vào **+ Add New MCP Server**.
3. Điền các thông tin:
   * **Name**: `FlutterTools`
   * **Type**: `command`
   * **Command**: `/Đường/dẫn/đến/venv/bin/python /Đường/dẫn/đến/mcp_flutter_server.py`
4. Nhấp **Save**. Cursor sẽ kết nối ngầm qua stdin/stdout và bạn sẽ thấy danh sách các công cụ `run_flutter_test`, `run_flutter_analyze` xuất hiện màu xanh lá cây hoạt động.

Bây giờ bạn có thể chat với Cursor AI: 
> *"Hãy chạy kiểm thử file test/login_test.dart trong dự án của tôi giúp tôi"*
Cursor AI sẽ tự động gọi hàm Python bạn vừa viết, lấy kết quả hiển thị trực tiếp trong cuộc hội thoại!

---

## 4. Ứng Dụng Trong Mô Hình Multi-Agent Song Song
Trong dự án của chúng ta, chúng ta sẽ không gọi qua IDE mà sử dụng **Orchestrator bằng Python** để tự khởi tạo và gọi các Agent. 

* **UI Agent** sẽ được cung cấp công cụ ghi file (`write_file`).
* **Test Agent** được cung cấp công cụ ghi file test (`write_file`) và đọc code của UI Agent.
* **Orchestrator** sẽ chạy kịch bản tự động gọi lệnh kiểm thử, phản hồi log lỗi giữa các Agent cho đến khi chạy lệnh `flutter test` thành công mà không cần con người can thiệp.
