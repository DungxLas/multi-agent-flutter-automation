import os
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import các Agent tự viết
from agents.ui_agent import UIAgent
from agents.test_agent import TestAgent

# Khởi tạo màn hình Console Rich để hiển thị tiến trình đẹp mắt
console = Console()

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_output_file(file_path: str, content: str):
    # Đảm bảo lưu vào thư mục 'outputs/' trong workspace
    full_path = os.path.join("outputs", file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # Tải cấu hình từ file .env
    load_dotenv()
    
    console.print(Panel.fit(
        "[bold green]HỆ THỐNG ĐIỀU PHỐI MULTI-AGENT CHO DỰ ÁN FLUTTER[/bold green]\n"
        "[dim]Triển khai song song: UI Agent & Test Agent[/dim]",
        border_style="green"
    ))
    
    # 1. Đọc tài liệu BA đầu vào
    ba_path = "inputs/login_feature_ba.md"
    if not os.path.exists(ba_path):
        console.print(f"[bold red]Lỗi:[/bold red] Không tìm thấy tài liệu BA đầu vào tại {ba_path}")
        return
        
    console.print(f"[blue]=> Đang đọc tài liệu BA từ {ba_path}...[/blue]")
    ba_content = read_file(ba_path)
    
    # Khởi tạo các Agent
    ui_agent = UIAgent()
    test_agent = TestAgent()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # 2. Sinh code UI
        task_ui = progress.add_task(description="[yellow]UI Agent đang phân tích BA và viết code UI...[/yellow]", total=1)
        start_time = time.time()
        ui_result = ui_agent.generate_ui(ba_content)
        progress.update(task_ui, completed=1, description="[green]UI Agent đã viết xong code UI![/green]")
        
        # Lưu code UI ra thư mục outputs
        write_output_file(ui_result.file_path, ui_result.code_content)
        console.print(f"   [dim]✔ Đã lưu file UI vào: outputs/{ui_result.file_path}[/dim]")
        
        # 3. Sinh code Test
        task_test = progress.add_task(description="[yellow]Test Agent đang viết Widget Test...[/yellow]", total=1)
        test_result = test_agent.generate_tests(ba_content, ui_result.code_content)
        progress.update(task_test, completed=1, description="[green]Test Agent đã viết xong Widget Test![/green]")
        
        # Lưu code Test ra thư mục outputs
        write_output_file(test_result.file_path, test_result.test_code_content)
        console.print(f"   [dim]✔ Đã lưu file Test vào: outputs/{test_result.file_path}[/dim]")
        
    # 4. Hiển thị tổng kết
    elapsed_time = time.time() - start_time
    console.print("\n[bold green]=== TỔNG KẾT TIẾN TRÌNH ===[/bold green]")
    console.print(f"⏱  Thời gian thực thi: [cyan]{elapsed_time:.2f} giây[/cyan]")
    console.print(f"\n[bold]1. Kết quả từ UI Agent ({ui_result.file_path}):[/bold]")
    console.print(Panel(ui_result.explanation, title="Giải thích của UI Agent", border_style="blue"))
    
    console.print(f"\n[bold]2. Kết quả từ Test Agent ({test_result.file_path}):[/bold]")
    console.print(f"Các kịch bản kiểm thử đã bao phủ:")
    for idx, scenario in enumerate(test_result.test_scenarios_covered, 1):
        console.print(f"   [green]▶[/green] {scenario}")

    console.print(
        "\n[bold yellow]LƯU Ý:[/bold yellow] Các file đã được xuất ra thư mục [bold]outputs/[/bold].\n"
        "Bạn có thể sao chép chúng trực tiếp vào dự án Flutter thực tế của mình hoặc kết nối thêm "
        "MCP Server để hệ thống tự động ghi thẳng vào thư mục dự án và chạy 'flutter test'."
    )

if __name__ == "__main__":
    main()
