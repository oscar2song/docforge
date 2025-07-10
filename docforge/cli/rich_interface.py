# cli/rich_interface.py
"""
Rich CLI interface for DocForge - Beautiful terminal output with progress bars,
tables, and professional formatting.
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.tree import Tree
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich import box
from typing import List, Dict, Any, Optional
import time
import os
from pathlib import Path

# Initialize Rich console
console = Console()


class DocForgeUI:
    """Rich UI manager for DocForge operations."""

    def __init__(self):
        self.console = console

    def print_banner(self):
        """Display DocForge banner."""
        banner = """
[bold blue]
╔══════════════════════════════════════════════════════════════╗
║                          DocForge 🔨                         ║
║        Forge perfect documents with precision & power        ║
╚══════════════════════════════════════════════════════════════╝
[/bold blue]
        """
        self.console.print(Panel(banner.strip(), border_style="blue"))

    def print_success(self, message: str):
        """Print success message."""
        self.console.print(f"✅ [bold green]{message}[/bold green]")

    def print_error(self, message: str):
        """Print error message."""
        self.console.print(f"❌ [bold red]Error:[/bold red] {message}")

    def print_warning(self, message: str):
        """Print warning message."""
        self.console.print(f"⚠️  [bold yellow]Warning:[/bold yellow] {message}")

    def print_info(self, message: str):
        """Print info message."""
        self.console.print(f"ℹ️  [bold blue]Info:[/bold blue] {message}")

    def create_progress_bar(self, description: str = "Processing..."):
        """Create a rich progress bar."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console
        )

    def display_file_tree(self, directory: str, title: str = "Files"):
        """Display a file tree."""
        tree = Tree(f"📁 {title}")

        def add_files_to_tree(path: Path, tree_node):
            try:
                for item in sorted(path.iterdir()):
                    if item.is_dir():
                        folder_node = tree_node.add(f"📁 {item.name}")
                        add_files_to_tree(item, folder_node)
                    else:
                        # Add file with appropriate icon
                        icon = self._get_file_icon(item.suffix.lower())
                        tree_node.add(f"{icon} {item.name}")
            except PermissionError:
                tree_node.add("❌ Permission denied")

        add_files_to_tree(Path(directory), tree)
        self.console.print(tree)

    def _get_file_icon(self, extension: str) -> str:
        """Get appropriate icon for file type."""
        icons = {
            '.pdf': '📄',
            '.docx': '📝',
            '.doc': '📝',
            '.txt': '📄',
            '.png': '🖼️',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
        }
        return icons.get(extension, '📄')

    def display_results_table(self, results: List[Dict[str, Any]], title: str = "Processing Results"):
        """Display processing results in a formatted table."""
        table = Table(title=title, box=box.ROUNDED)
        table.add_column("File", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Size", justify="right", style="magenta")
        table.add_column("Time", justify="right", style="blue")
        table.add_column("Output", style="green")

        for result in results:
            # Status with appropriate styling
            if result.get('success', False):
                status = "[green]✅ Success[/green]"
            else:
                status = "[red]❌ Failed[/red]"

            # File size formatting
            size = self._format_file_size(result.get('file_size', 0))

            # Processing time
            proc_time = f"{result.get('processing_time', 0):.2f}s"

            table.add_row(
                result.get('input_file', 'Unknown'),
                status,
                size,
                proc_time,
                result.get('output_file', 'N/A')
            )

        self.console.print(table)

    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024.0 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f} {size_names[i]}"


    def display_operation_summary(self, operation: str, input_files: int,
                                  success_count: int, total_time: float):
        """Display operation summary."""
        if input_files == 0:
            input_files = 1  # Prevent division by zero

        success_rate = (success_count / input_files * 100)
        avg_time = total_time / input_files

        summary_text = f"""[bold cyan]{operation} Complete![/bold cyan]

    📊 Summary:
    • Files processed: [bold]{success_count}/{input_files}[/bold]
    • Success rate: [bold green]{success_rate:.1f}%[/bold green]
    • Total time: [bold blue]{total_time:.2f}s[/bold blue]
    • Average per file: [bold yellow]{avg_time:.2f}s[/bold yellow]"""

        summary_panel = Panel(
            summary_text,
            title="🎉 Operation Summary",
            border_style="green"
        )
        self.console.print(summary_panel)

    def prompt_user_choice(self, question: str, choices: List[str]) -> str:
        """Prompt user for choice with rich formatting."""
        choice_text = " / ".join([f"[bold cyan]{choice}[/bold cyan]" for choice in choices])
        return Prompt.ask(f"{question} ({choice_text})")

    def confirm_action(self, message: str) -> bool:
        """Confirm user action."""
        return Confirm.ask(f"⚠️  {message}")

    def display_config_panel(self, config: Dict[str, Any]):
        """Display current configuration."""
        config_text = "\n".join([f"• [bold]{key}:[/bold] [cyan]{value}[/cyan]"
                                 for key, value in config.items()])

        panel = Panel(
            config_text,
            title="⚙️ Current Configuration",
            border_style="blue"
        )
        self.console.print(panel)


class BatchProgressTracker:
    """Track progress for batch operations with rich display."""

    def __init__(self, ui: DocForgeUI):
        self.ui = ui
        self.progress = None
        self.task_id = None
        self.results = []

    def start_batch(self, total_files: int, operation: str):
        """Start batch processing with progress tracking."""
        self.progress = self.ui.create_progress_bar()
        self.progress.start()
        self.task_id = self.progress.add_task(
            f"[cyan]{operation}...", total=total_files
        )
        self.results = []

    def update_progress(self, file_name: str, success: bool, **kwargs):
        """Update progress for a single file."""
        # Store result
        result = {
            'input_file': file_name,
            'success': success,
            **kwargs
        }
        self.results.append(result)

        # Update progress bar
        if self.progress and self.task_id is not None:
            self.progress.update(
                self.task_id,
                advance=1,
                description=f"[cyan]Processing: {os.path.basename(file_name)}..."
            )

    def finish_batch(self, operation: str):
        """Finish batch processing and show results."""
        if self.progress:
            self.progress.stop()

        # Display results
        success_count = sum(1 for r in self.results if r['success'])
        total_time = sum(r.get('processing_time', 0) for r in self.results)

        self.ui.display_results_table(self.results, f"{operation} Results")
        self.ui.display_operation_summary(
            operation, len(self.results), success_count, total_time
        )


def demonstrate_rich_ui():
    """Demonstrate the rich UI capabilities."""
    ui = DocForgeUI()

    # Banner
    ui.print_banner()

    # Various message types
    ui.print_info("Starting DocForge demonstration...")
    ui.print_success("Rich UI loaded successfully!")
    ui.print_warning("This is a demonstration mode")

    # Configuration display
    sample_config = {
        "OCR Language": "eng",
        "Optimization Level": "moderate",
        "Output Format": "PDF",
        "Batch Size": 10
    }
    ui.display_config_panel(sample_config)

    # Simulate batch processing
    tracker = BatchProgressTracker(ui)
    tracker.start_batch(5, "PDF Processing")

    # Simulate processing files
    for i in range(5):
        time.sleep(0.5)  # Simulate processing time
        tracker.update_progress(
            f"document_{i + 1}.pdf",
            success=True,
            file_size=1024 * (i + 1) * 100,
            processing_time=0.5,
            output_file=f"output_{i + 1}.pdf"
        )

    tracker.finish_batch("PDF Processing")


if __name__ == "__main__":
    demonstrate_rich_ui()
