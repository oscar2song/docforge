# docforge/cli/interface.py - Enhanced version with Rich CLI
"""
Enhanced CLIInterface that integrates Rich UI with your existing functionality
This preserves all your existing commands while adding beautiful Rich output
"""

import argparse
import sys
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any

# Import Rich components
try:
    from .rich_interface import DocForgeUI, BatchProgressTracker

    RICH_AVAILABLE = True
except ImportError:
    # Fallback if Rich is not available
    RICH_AVAILABLE = False
    print("⚠️  Rich not available. Using basic CLI interface.")

from ..core.processor import DocumentProcessor


class CLIInterface:
    """Enhanced CLI Interface with Rich UI support."""

    def __init__(self, use_rich: bool = True):
        """Initialize CLI interface with optional Rich UI."""
        self.use_rich = use_rich and RICH_AVAILABLE

        if self.use_rich:
            self.ui = DocForgeUI()
        else:
            self.ui = None

        self.processor = DocumentProcessor(verbose=True)

    def print_message(self, message: str, msg_type: str = "info"):
        """Print message with Rich if available, otherwise use basic print."""
        if self.ui:
            if msg_type == "success":
                self.ui.print_success(message)
            elif msg_type == "error":
                self.ui.print_error(message)
            elif msg_type == "warning":
                self.ui.print_warning(message)
            else:
                self.ui.print_info(message)
        else:
            # Fallback to basic print
            icons = {
                "success": "✅",
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️"
            }
            icon = icons.get(msg_type, "ℹ️")
            print(f"{icon} {message}")

    def show_banner(self):
        """Show DocForge banner."""
        if self.ui:
            self.ui.print_banner()
        else:
            print("🔨 DocForge - Document Processing Toolkit")
            print("Forge perfect documents with precision and power")
            print("=" * 50)

    def create_progress_context(self, description: str = "Processing..."):
        """Create progress context (Rich or basic)."""
        if self.ui:
            return self.ui.create_progress_bar()
        else:
            # Fallback: basic progress indication
            return BasicProgressContext(description)

    def display_config(self, config: Dict[str, Any]):
        """Display configuration panel."""
        if self.ui:
            self.ui.display_config_panel(config)
        else:
            print("\n⚙️ Configuration:")
            for key, value in config.items():
                print(f"  • {key}: {value}")
            print()

    def confirm_action(self, message: str) -> bool:
        """Confirm user action."""
        if self.ui:
            return self.ui.confirm_action(message)
        else:
            response = input(f"⚠️  {message} (y/N): ").lower().strip()
            return response in ['y', 'yes']

    @staticmethod
    def setup_parsers(subparsers):
        """Set up all command parsers - keep your existing implementation."""

        # OCR command
        ocr_parser = subparsers.add_parser('ocr', help='OCR processing')
        ocr_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        ocr_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
        ocr_parser.add_argument('--language', default='eng', help='OCR language (default: eng)')
        ocr_parser.add_argument('--layout-mode', choices=['standard', 'precise', 'text_only'],
                                default='standard', help='OCR layout mode')

        # Optimize command
        optimize_parser = subparsers.add_parser('optimize', help='Optimize PDF')
        optimize_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        optimize_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
        optimize_parser.add_argument('--type',
                                     choices=['standard', 'aggressive', 'scanned', 'scale_only', 'high_quality'],
                                     default='standard', help='Optimization type')
        optimize_parser.add_argument('--quality', type=int, default=85, help='Image quality (1-100)')

        # Merge command
        merge_parser = subparsers.add_parser('merge', help='Merge PDFs')
        merge_parser.add_argument('-i', '--input', required=True, help='Input files or folder')
        merge_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
        merge_parser.add_argument('--page-numbers', action='store_true', help='Add page numbers')
        merge_parser.add_argument('--no-page-numbers', action='store_true', help='No page numbers')
        merge_parser.add_argument('--preserve-signatures', action='store_true', help='Preserve signatures')

        # PDF to Word command
        pdf2word_parser = subparsers.add_parser('pdf-to-word', help='Convert PDF to Word')
        pdf2word_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        pdf2word_parser.add_argument('-o', '--output', required=True, help='Output DOCX file')
        pdf2word_parser.add_argument('--method', choices=['simple', 'ocr'], default='simple',
                                     help='Conversion method')

        # Split PDF command
        split_parser = subparsers.add_parser('split-pdf', help='Split PDF')
        split_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        split_parser.add_argument('-o', '--output', required=True, help='Output directory')
        split_parser.add_argument('--pages', help='Page ranges (e.g., "1-5,10-15")')
        split_parser.add_argument('--pages-per-file', type=int, help='Pages per output file')
        split_parser.add_argument('--split-type', choices=['pages', 'size', 'bookmarks'],
                                  default='pages', help='Split method')
        split_parser.add_argument('--max-size-mb', type=float, help='Maximum file size in MB')

        # Batch commands
        batch_ocr_parser = subparsers.add_parser('batch-ocr', help='Batch OCR processing')
        batch_ocr_parser.add_argument('-i', '--input', required=True, help='Input directory')
        batch_ocr_parser.add_argument('-o', '--output', required=True, help='Output directory')
        batch_ocr_parser.add_argument('--language', default='eng', help='OCR language')

        batch_optimize_parser = subparsers.add_parser('batch-optimize', help='Batch optimization')
        batch_optimize_parser.add_argument('-i', '--input', required=True, help='Input directory')
        batch_optimize_parser.add_argument('-o', '--output', required=True, help='Output directory')
        batch_optimize_parser.add_argument('--type', choices=['standard', 'aggressive', 'scanned'],
                                           default='standard', help='Optimization type')

        batch_pdf2word_parser = subparsers.add_parser('batch-pdf-to-word', help='Batch PDF to Word conversion')
        batch_pdf2word_parser.add_argument('-i', '--input', required=True, help='Input directory')
        batch_pdf2word_parser.add_argument('-o', '--output', required=True, help='Output directory')
        batch_pdf2word_parser.add_argument('--method', choices=['simple', 'ocr'], default='simple')

        # Advanced commands
        adv_optimize_parser = subparsers.add_parser('advanced-optimize', help='Advanced optimization')
        adv_optimize_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        adv_optimize_parser.add_argument('-o', '--output', required=True, help='Output PDF file')

        adv_merge_parser = subparsers.add_parser('advanced-merge', help='Advanced merge')
        adv_merge_parser.add_argument('-i', '--input', required=True, help='Input folder')
        adv_merge_parser.add_argument('-o', '--output', required=True, help='Output PDF file')

        adv_pdf2word_parser = subparsers.add_parser('advanced-pdf-to-word', help='Advanced PDF to Word')
        adv_pdf2word_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        adv_pdf2word_parser.add_argument('-o', '--output', required=True, help='Output DOCX file')

        adv_split_parser = subparsers.add_parser('advanced-split-pdf', help='Advanced PDF splitting')
        adv_split_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        adv_split_parser.add_argument('-o', '--output', required=True, help='Output directory')

        # Analyze command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze PDF')
        analyze_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        analyze_parser.add_argument('--type', choices=['ocr', 'structure', 'metadata'],
                                    default='ocr', help='Analysis type')

        # Test command (for Rich CLI testing)
        test_parser = subparsers.add_parser('test-rich', help='Test Rich CLI interface')

    def execute_command(self, args):
        """Execute the specified command with Rich UI enhancements."""
        command_map = {
            'ocr': self.handle_ocr,
            'optimize': self.handle_optimize,
            'merge': self.handle_merge,
            'pdf-to-word': self.handle_pdf_to_word,
            'split-pdf': self.handle_split_pdf,
            'batch-ocr': self.handle_batch_ocr,
            'batch-optimize': self.handle_batch_optimize,
            'batch-pdf-to-word': self.handle_batch_pdf_to_word,
            'advanced-optimize': self.handle_advanced_optimize,
            'advanced-merge': self.handle_advanced_merge,
            'advanced-pdf-to-word': self.handle_advanced_pdf_to_word,
            'advanced-split-pdf': self.handle_advanced_split_pdf,
            'analyze': self.handle_analyze,
            'test-rich': self.handle_test_rich,
        }

        handler = command_map.get(args.command)
        if handler:
            try:
                handler(args)
            except Exception as e:
                self.print_message(f"Command failed: {str(e)}", "error")
                sys.exit(1)
        else:
            self.print_message(f"Unknown command: {args.command}", "error")
            sys.exit(1)

    def handle_ocr(self, args):
        """Handle OCR command with Rich UI."""
        self.print_message(f"Starting OCR processing: {args.input}")

        # Display configuration
        config = {
            "Input File": args.input,
            "Output File": args.output,
            "Language": args.language,
            "Layout Mode": args.layout_mode
        }
        self.display_config(config)

        # Check if output exists
        if os.path.exists(args.output):
            if not self.confirm_action(f"Output file '{args.output}' exists. Overwrite?"):
                self.print_message("Operation cancelled", "warning")
                return

        start_time = time.time()

        # Process with progress indication
        with self.create_progress_context() as progress:
            if self.ui:
                task = progress.add_task("[cyan]OCR Processing...", total=100)

            # Call your existing OCR method
            result = self.processor.ocr_pdf(
                args.input,
                args.output,
                language=args.language
            )

            if self.ui:
                progress.update(task, completed=100)

        processing_time = time.time() - start_time

        if result and result.get('success', True):
            self.print_message(f"OCR completed successfully in {processing_time:.2f}s", "success")
            self.print_message(f"Output saved to: {args.output}")
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Processing failed'
            self.print_message(f"OCR failed: {error_msg}", "error")

    def handle_pdf_to_word(self, args):
        """Handle PDF to Word conversion with Rich UI."""
        self.print_message(f"Converting PDF to Word: {args.input}")

        config = {
            "Input File": args.input,
            "Output File": args.output,
            "Method": args.method
        }
        self.display_config(config)

        start_time = time.time()

        with self.create_progress_context() as progress:
            if self.ui:
                task = progress.add_task("[cyan]Converting PDF to Word...", total=100)

            # Call your existing PDF to Word method
            result = self.processor.pdf_to_word(args.input, args.output, method=args.method)

            if self.ui:
                progress.update(task, completed=100)

        processing_time = time.time() - start_time

        if result and result.get('success', True):
            self.print_message(f"Conversion completed in {processing_time:.2f}s", "success")
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Conversion failed'
            self.print_message(f"Conversion failed: {error_msg}", "error")

    def handle_batch_ocr(self, args):
        """Handle batch OCR with Rich progress tracking."""
        self.print_message(f"Starting batch OCR: {args.input} -> {args.output}")

        # Find PDF files
        input_path = Path(args.input)
        pdf_files = list(input_path.glob("*.pdf"))

        if not pdf_files:
            self.print_message(f"No PDF files found in {args.input}", "warning")
            return

        self.print_message(f"Found {len(pdf_files)} PDF files for processing")

        if not self.confirm_action(f"Process {len(pdf_files)} files?"):
            self.print_message("Batch operation cancelled", "warning")
            return

        # Create output directory
        output_path = Path(args.output)
        output_path.mkdir(parents=True, exist_ok=True)

        # Use Rich batch tracker if available
        if self.ui:
            tracker = BatchProgressTracker(self.ui)
            tracker.start_batch(len(pdf_files), "Batch OCR")

            for pdf_file in pdf_files:
                file_start_time = time.time()
                output_file = output_path / f"{pdf_file.stem}_ocr{pdf_file.suffix}"

                try:
                    result = self.processor.ocr_pdf(str(pdf_file), str(output_file), language=args.language)
                    success = result and result.get('success', True)

                    tracker.update_progress(
                        str(pdf_file),
                        success=success,
                        file_size=pdf_file.stat().st_size,
                        processing_time=time.time() - file_start_time,
                        output_file=str(output_file)
                    )
                except Exception as e:
                    tracker.update_progress(
                        str(pdf_file),
                        success=False,
                        file_size=pdf_file.stat().st_size,
                        processing_time=time.time() - file_start_time,
                        error=str(e)
                    )

            tracker.finish_batch("Batch OCR")
        else:
            # Fallback: basic progress indication
            for i, pdf_file in enumerate(pdf_files, 1):
                print(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
                output_file = output_path / f"{pdf_file.stem}_ocr{pdf_file.suffix}"

                try:
                    result = self.processor.ocr_pdf(str(pdf_file), str(output_file), language=args.language)
                    if result and result.get('success', True):
                        print(f"  ✅ Success: {output_file.name}")
                    else:
                        print(f"  ❌ Failed: {pdf_file.name}")
                except Exception as e:
                    print(f"  ❌ Error: {str(e)}")

    def handle_test_rich(self, args):
        """Test the Rich interface."""
        if not self.ui:
            self.print_message("Rich interface not available", "error")
            return

        self.print_message("Testing Rich CLI interface...")

        # Test all message types
        self.print_message("This is a success message!", "success")
        self.print_message("This is a warning message!", "warning")
        self.print_message("This is an error message!", "error")

        # Test configuration display
        config = {
            "Rich Version": "13.0+",
            "Status": "Working",
            "Features": "Progress bars, tables, colors"
        }
        self.display_config(config)

        # Test batch processing simulation
        tracker = BatchProgressTracker(self.ui)
        tracker.start_batch(3, "Test Processing")

        for i in range(3):
            time.sleep(1)
            tracker.update_progress(
                f"test_file_{i + 1}.pdf",
                success=True,
                file_size=1024 * (i + 1) * 100,
                processing_time=1.0,
                output_file=f"output_{i + 1}.pdf"
            )

        tracker.finish_batch("Test Processing")
        self.print_message("Rich CLI test completed!", "success")

    # Add placeholder methods for other commands
    def handle_optimize(self, args):
        """Handle optimize command - implement with your existing logic."""
        self.print_message(f"Optimizing: {args.input} -> {args.output}")
        # Add your existing optimization logic here with Rich UI enhancements

    def handle_merge(self, args):
        """Handle merge command - implement with your existing logic."""
        self.print_message(f"Merging: {args.input} -> {args.output}")
        # Add your existing merge logic here with Rich UI enhancements

    def handle_split_pdf(self, args):
        """Handle split PDF command - implement with your existing logic."""
        self.print_message(f"Splitting: {args.input} -> {args.output}")
        # Add your existing split logic here with Rich UI enhancements

    # Add other command handlers following the same pattern...
    def handle_batch_optimize(self, args):
        """Handle batch optimize - implement with your existing logic."""
        pass

    def handle_batch_pdf_to_word(self, args):
        """Handle batch PDF to Word - implement with your existing logic."""
        pass

    def handle_advanced_optimize(self, args):
        """Handle advanced optimize - implement with your existing logic."""
        pass

    def handle_advanced_merge(self, args):
        """Handle advanced merge - implement with your existing logic."""
        pass

    def handle_advanced_pdf_to_word(self, args):
        """Handle advanced PDF to Word - implement with your existing logic."""
        pass

    def handle_advanced_split_pdf(self, args):
        """Handle advanced split PDF - implement with your existing logic."""
        pass

    def handle_analyze(self, args):
        """Handle analyze command - implement with your existing logic."""
        pass

    def run_interactive(self):
        """Run interactive mode with Rich UI."""
        if self.ui:
            self.ui.print_info("Starting DocForge Interactive Mode...")
            # Add your existing interactive mode logic here with Rich enhancements
        else:
            print("🚀 Starting Interactive Mode...")
            # Your existing interactive mode logic


class BasicProgressContext:
    """Fallback progress context when Rich is not available."""

    def __init__(self, description: str):
        self.description = description

    def __enter__(self):
        print(f"🔄 {self.description}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("✅ Completed")
        else:
            print("❌ Failed")

    def add_task(self, description: str, total: int = 100):
        return None

    def update(self, task_id, **kwargs):
        pass
