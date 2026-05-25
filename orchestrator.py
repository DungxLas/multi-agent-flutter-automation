import os
import time
import subprocess
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

def write_project_file(project_path: str, file_path: str, content: str):
    full_path = os.path.join(project_path, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

def run_tests(project_path: str) -> tuple[int, str]:
    """Chạy lệnh flutter test trong thư mục dự án và trả về exit code cùng log output."""
    try:
        result = subprocess.run(
            ["flutter", "test"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return -1, "Lỗi: Quá thời gian chạy thử nghiệm (Timeout 60s)"
    except Exception as e:
        return -1, f"Lỗi thực thi lệnh flutter test: {str(e)}"

def main():
    # Tải cấu hình từ file .env
    load_dotenv()
    
    console.print(Panel.fit(
        "[bold green]HỆ THỐNG ĐIỀU PHỐI MULTI-AGENT CHO DỰ ÁN FLUTTER[/bold green]\n"
        "[dim]Triển khai song song: UI Agent & Test Agent (Tích hợp thực tế & Self-healing)[/dim]",
        border_style="green"
    ))
    
    # 1. Đọc tài liệu BA đầu vào
    ba_path = "inputs/login_feature_ba.md"
    if not os.path.exists(ba_path):
        console.print(f"[bold red]Lỗi:[/bold red] Không tìm thấy tài liệu BA đầu vào tại {ba_path}")
        return
        
    console.print(f"[blue]=> Đang đọc tài liệu BA từ {ba_path}...[/blue]")
    ba_content = read_file(ba_path)
    
    # Đọc cấu hình kết nối dự án Flutter
    project_path = os.getenv("FLUTTER_PROJECT_PATH")
    package_name = os.getenv("FLUTTER_PACKAGE_NAME")
    auto_run = os.getenv("AUTO_RUN_TESTS", "false").lower() == "true"
    max_healing = int(os.getenv("MAX_HEALING_ATTEMPTS", "3"))

    if project_path:
        console.print(f"[cyan]=> Đã cấu hình kết nối dự án Flutter: {project_path}[/cyan]")
        console.print(f"[cyan]=> Package name: {package_name}[/cyan]")
    else:
        console.print("[yellow]=> Chưa cấu hình dự án Flutter trong .env. Chỉ xuất file ra outputs/.[/yellow]")
    
    # Khởi tạo các Agent
    ui_agent = UIAgent()
    test_agent = TestAgent()
    
    current_ui_code = ""
    current_test_code = ""
    ui_file_path = "lib/presentation/pages/login_page.dart"
    test_file_path = "test/presentation/pages/login_page_test.dart"

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # 2. Sinh code UI
        task_ui = progress.add_task(description="[yellow]UI Agent đang phân tích BA và viết code UI...[/yellow]", total=1)
        start_time = time.time()
        ui_result = ui_agent.generate_ui(ba_content)
        current_ui_code = ui_result.code_content
        ui_file_path = ui_result.file_path
        progress.update(task_ui, completed=1, description="[green]UI Agent đã viết xong code UI![/green]")
        
        # Lưu file UI
        write_output_file(ui_file_path, current_ui_code)
        console.print(f"   [dim]✔ Đã lưu file UI vào: outputs/{ui_file_path}[/dim]")
        if project_path:
            write_project_file(project_path, ui_file_path, current_ui_code)
            console.print(f"   [dim]✔ Đã ghi trực tiếp vào dự án: {project_path}/{ui_file_path}[/dim]")
        
        # 3. Sinh code Test
        task_test = progress.add_task(description="[yellow]Test Agent đang viết Widget Test...[/yellow]", total=1)
        test_result = test_agent.generate_tests(ba_content, current_ui_code, package_name=package_name)
        current_test_code = test_result.test_code_content
        test_file_path = test_result.file_path
        progress.update(task_test, completed=1, description="[green]Test Agent đã viết xong Widget Test![/green]")
        
        # Lưu file Test
        write_output_file(test_file_path, current_test_code)
        console.print(f"   [dim]✔ Đã lưu file Test vào: outputs/{test_file_path}[/dim]")
        if project_path:
            write_project_file(project_path, test_file_path, current_test_code)
            console.print(f"   [dim]✔ Đã ghi trực tiếp vào dự án: {project_path}/{test_file_path}[/dim]")
        
        # 4. Tự động chạy test & Vòng lặp tự sửa lỗi (Self-healing Loop)
        if project_path and auto_run:
            task_run_test = progress.add_task(description="[yellow]Đang tự động chạy flutter test...[/yellow]", total=1)
            exit_code, log_output = run_tests(project_path)
            
            if exit_code == 0:
                progress.update(task_run_test, completed=1, description="[green]✔ Tất cả test cases đều PASS ngay lần chạy đầu tiên![/green]")
            else:
                progress.update(task_run_test, completed=1, description="[red]✘ Phát hiện lỗi kiểm thử! Kích hoạt Self-healing...[/red]")
                
                # Bắt đầu vòng lặp sửa lỗi tự động
                healed = False
                for attempt in range(1, max_healing + 1):
                    task_heal = progress.add_task(
                        description=f"[yellow]Self-healing: Đang tự động sửa lỗi (Lần {attempt}/{max_healing})...[/yellow]", 
                        total=1
                    )
                    
                    # Gọi Agent sửa lỗi
                    healed_result = test_agent.heal_code(
                        ba_document=ba_content,
                        ui_code_content=current_ui_code,
                        test_code_content=current_test_code,
                        error_log=log_output,
                        package_name=package_name
                    )
                    
                    # Cập nhật code mới
                    current_ui_code = healed_result.ui_code_content
                    current_test_code = healed_result.test_code_content
                    
                    # Ghi đè vào dự án và outputs
                    write_output_file(ui_file_path, current_ui_code)
                    write_output_file(test_file_path, current_test_code)
                    write_project_file(project_path, ui_file_path, current_ui_code)
                    write_project_file(project_path, test_file_path, current_test_code)
                    
                    # Chạy lại test
                    exit_code, log_output = run_tests(project_path)
                    
                    if exit_code == 0:
                        progress.update(task_heal, completed=1, description=f"[green]✔ Sửa lỗi thành công ở lần thử thứ {attempt}![/green]")
                        console.print(Panel(healed_result.explanation, title=f"AI giải thích cách sửa (Lần {attempt})", border_style="green"))
                        healed = True
                        break
                    else:
                        progress.update(task_heal, completed=1, description=f"[red]✘ Lần {attempt} thất bại. Tiếp tục phân tích lỗi...[/red]")
                
                if not healed:
                    console.print(Panel("[bold red]Self-healing thất bại![/bold red]\nĐã vượt quá số lần thử tối đa nhưng vẫn chưa pass test.", border_style="red"))
                    console.print(f"Log lỗi cuối cùng:\n{log_output}")
        
    # 5. Hiển thị tổng kết
    elapsed_time = time.time() - start_time
    console.print("\n[bold green]=== TỔNG KẾT TIẾN TRÌNH ===[/bold green]")
    console.print(f"⏱  Thời gian thực thi: [cyan]{elapsed_time:.2f} giây[/cyan]")
    console.print(f"\n[bold]1. Kết quả từ UI Agent ({ui_file_path}):[/bold]")
    console.print(Panel(ui_result.explanation, title="Giải thích của UI Agent", border_style="blue"))
    
    console.print(f"\n[bold]2. Kết quả từ Test Agent ({test_file_path}):[/bold]")
    if project_path and auto_run:
        if exit_code == 0:
            console.print("   [green]▶[/green] Trạng thái chạy test: [bold green]TẤT CẢ ĐỀU PASS[/bold green]")
        else:
            console.print("   [red]▶[/red] Trạng thái chạy test: [bold red]CÓ TEST CASE THẤT BẠI[/bold red]")
    else:
        console.print(f"Các kịch bản kiểm thử đã bao phủ:")
        for idx, scenario in enumerate(test_result.test_scenarios_covered, 1):
            console.print(f"   [green]▶[/green] {scenario}")

if __name__ == "__main__":
    main()
