# docforge/cli/interface.py - Enhanced with comprehensive error handling

"""
Enhanced CLIInterface with integrated error handling system
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
    RICH_AVAILABLE = False

# Import error handling system
from ..core.exceptions import (
    DocForgeException, ProcessingResult, FileNotFoundError,
    InvalidFileFormatError, ValidationError, OCRError, safe_execute
)

from ..core.validators import FileValidator, ParameterValidator

from ..core.processor import DocumentProcessor


class CLIInterface:
    """Enhanced CLI Interface with comprehensive error handling."""

    def __init__(self, use_rich: bool = True):
        """Initialize CLI interface with error handling."""
        self.use_rich = use_rich and RICH_AVAILABLE

        if self.use_rich:
            self.ui = DocForgeUI()
        else:
            self.ui = None

        if self.ui:
            self.console = self.ui.console  # Add this line
        else:
            self.console = None  # Add this line for fallback

        self.processor = DocumentProcessor(verbose=True)
        self.validator = FileValidator()
        self.param_validator = ParameterValidator()

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

    def display_result(self, result: ProcessingResult):
        """Display processing result with appropriate UI."""
        if self.ui:
            self.ui.display_processing_result(result)
        else:
            # Fallback display
            if result.success:
                self.print_message(result.message, "success")
                if result.processing_time:
                    self.print_message(f"Completed in {result.processing_time:.2f}s")
            else:
                self.print_message(result.message, "error")
                if result.error and result.error.suggestions:
                    print("\n💡 Suggestions:")
                    for i, suggestion in enumerate(result.error.suggestions, 1):
                        print(f"  {i}. {suggestion}")

    def validate_common_args(self, args) -> bool:
        """Validate common arguments and display errors if invalid."""
        try:
            # Validate input file if present
            if hasattr(args, 'input') and args.input:
                expected_ext = ['.pdf'] if 'pdf' in getattr(args, 'command', '') else None
                self.validator.validate_input_file(args.input, expected_ext)

            # Validate output path if present
            if hasattr(args, 'output') and args.output:
                self.validator.validate_output_path(args.output)

            # Validate language if present
            if hasattr(args, 'language') and args.language:
                self.param_validator.validate_language_code(args.language)

            # Validate optimization type if present
            if hasattr(args, 'type') and args.type:
                self.param_validator.validate_optimization_type(args.type)

            # Validate quality if present
            if hasattr(args, 'quality') and args.quality:
                self.param_validator.validate_quality(args.quality)

            # Validate page ranges if present
            if hasattr(args, 'pages') and args.pages:
                self.param_validator.validate_page_range(args.pages)

            return True

        except DocForgeException as e:
            if self.ui:
                self.ui.display_error_details(e)
            else:
                self.print_message(e.message, "error")
                if e.suggestions:
                    print("\n💡 Suggestions:")
                    for i, suggestion in enumerate(e.suggestions, 1):
                        print(f"  {i}. {suggestion}")
            return False

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
        """Set up all command parsers - enhanced with better help."""

        # OCR command
        ocr_parser = subparsers.add_parser('ocr', help='OCR processing with validation')
        ocr_parser.add_argument('-i', '--input', required=True,
                                help='Input PDF file (must exist and be readable)')
        ocr_parser.add_argument('-o', '--output', required=True,
                                help='Output PDF file (directory will be created if needed)')
        ocr_parser.add_argument('--language', default='eng',
                                help='OCR language code (eng, fra, deu, spa, etc.)')
        ocr_parser.add_argument('--layout-mode', choices=['standard', 'precise', 'text_only'],
                                default='standard', help='OCR layout preservation mode')

        # Optimize command
        optimize_parser = subparsers.add_parser('optimize', help='Optimize PDF with validation')
        optimize_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        optimize_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
        optimize_parser.add_argument('--type',
                                     choices=['standard', 'aggressive', 'scanned', 'scale_only', 'high_quality'],
                                     default='standard', help='Optimization type')
        optimize_parser.add_argument('--quality', type=int, default=85,
                                     help='Image quality (1-100, default: 85)')

        # PDF to Word command
        pdf2word_parser = subparsers.add_parser('pdf-to-word', help='Convert PDF to Word with validation')
        pdf2word_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        pdf2word_parser.add_argument('-o', '--output', required=True, help='Output DOCX file')
        pdf2word_parser.add_argument('--method', choices=['simple', 'ocr'], default='simple',
                                     help='Conversion method (simple for text PDFs, ocr for scanned)')

        # Split PDF command
        split_parser = subparsers.add_parser('split-pdf', help='Split PDF with validation')
        split_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        split_parser.add_argument('-o', '--output', required=True, help='Output directory')
        split_parser.add_argument('--pages', help='Page ranges (e.g., "1-5,10-15") or single pages')
        split_parser.add_argument('--pages-per-file', type=int, help='Pages per output file')
        split_parser.add_argument('--split-type', choices=['pages', 'size', 'bookmarks'],
                                  default='pages', help='Split method')
        split_parser.add_argument('--max-size-mb', type=float, help='Maximum file size in MB')

        # Batch commands with validation
        batch_ocr_parser = subparsers.add_parser('batch-ocr', help='Batch OCR with error handling')
        batch_ocr_parser.add_argument('-i', '--input', required=True, help='Input directory')
        batch_ocr_parser.add_argument('-o', '--output', required=True, help='Output directory')
        batch_ocr_parser.add_argument('--language', default='eng', help='OCR language')

        # Test command for error handling
        test_parser = subparsers.add_parser('test-rich', help='Test Rich CLI interface')
        test_errors_parser = subparsers.add_parser('test-errors', help='Test error handling system')

        # Add other parsers as before...
        # (keeping the rest of your existing parsers)

        # Add this to your setup_parsers method in CLIInterface
        test_validation_parser = subparsers.add_parser('test-validation',
                                                       help='Test enhanced validation system')

    def execute_command(self, args):
        """Execute command with comprehensive error handling."""

        # Validate common arguments first
        if not self.validate_common_args(args):
            sys.exit(1)

        command_map = {
            'ocr': self.handle_ocr,
            'optimize': self.handle_optimize,
            'pdf-to-word': self.handle_pdf_to_word,
            'split-pdf': self.handle_split_pdf,
            'batch-ocr': self.handle_batch_ocr,
            'test-rich': self.handle_test_rich,
            'test-errors': self.handle_test_errors,
            # Add this to your command_map in execute_command method
            'test-validation': self.handle_test_validation,
            # Add other commands...
        }

        handler = command_map.get(args.command)
        if handler:
            try:
                result = handler(args)
                if isinstance(result, ProcessingResult):
                    self.display_result(result)
                    if not result.success:
                        sys.exit(1)
            except Exception as e:
                # This should rarely happen now with proper error handling
                self.print_message(f"Unexpected error: {str(e)}", "error")
                sys.exit(1)
        else:
            self.print_message(f"Unknown command: {args.command}", "error")
            sys.exit(1)

    def handle_ocr(self, args) -> ProcessingResult:
        """Handle OCR command with comprehensive error handling."""

        def _ocr_operation():
            self.print_message(f"Starting OCR processing: {args.input}")

            # Display configuration
            config = {
                "Input File": args.input,
                "Output File": args.output,
                "Language": args.language,
                "Layout Mode": getattr(args, 'layout_mode', 'standard')
            }
            self.display_config(config)

            # Check if output exists
            if os.path.exists(args.output):
                if not self.confirm_action(f"Output file '{args.output}' exists. Overwrite?"):
                    raise ValidationError(
                        'user_choice',
                        'cancelled',
                        'user confirmation to proceed',
                        ['Choose a different output file', 'Confirm the overwrite operation']
                    )

            # Process with progress indication
            with self.create_progress_context() as progress:
                if self.ui:
                    task = progress.add_task("[cyan]OCR Processing...", total=100)

                # Call your existing OCR method
                result = self.processor.ocr_pdf(
                    args.input,
                    args.output,
                    language=args.language,
                    layout_mode=getattr(args, 'layout_mode', 'standard')
                )

                if self.ui:
                    progress.update(task, completed=100)

            # Return structured result
            if result and result.get('success', True):
                return ProcessingResult.success_result(
                    message="OCR processing completed successfully",
                    operation="OCR",
                    input_file=args.input,
                    output_file=args.output,
                    metadata=result if isinstance(result, dict) else {}
                )
            else:
                error_msg = result.get('error', 'OCR processing failed') if result else 'OCR processing failed'
                from ..core.exceptions import OCRError
                raise OCRError(args.input, error_msg)

        # Execute with error handling
        return safe_execute(_ocr_operation, _operation_name="OCR")

    def handle_pdf_to_word(self, args) -> ProcessingResult:
        """Handle PDF to Word conversion with error handling."""

        def _pdf_to_word_operation():
            self.print_message(f"Converting PDF to Word: {args.input}")

            config = {
                "Input File": args.input,
                "Output File": args.output,
                "Method": args.method
            }
            self.display_config(config)

            with self.create_progress_context() as progress:
                if self.ui:
                    task = progress.add_task("[cyan]Converting PDF to Word...", total=100)

                # Call your existing PDF to Word method
                result = self.processor.pdf_to_word(args.input, args.output, method=args.method)

                if self.ui:
                    progress.update(task, completed=100)

            if result and result.get('success', True):
                return ProcessingResult.success_result(
                    message="PDF to Word conversion completed successfully",
                    operation="PDF to Word",
                    input_file=args.input,
                    output_file=args.output,
                    metadata=result if isinstance(result, dict) else {}
                )
            else:
                error_msg = result.get('error', 'Conversion failed') if result else 'Conversion failed'
                raise DocForgeException(
                    message=f"PDF to Word conversion failed: {error_msg}",
                    error_code='CONVERSION_FAILED',
                    context={'input_file': args.input, 'method': args.method},
                    suggestions=[
                        'Try a different conversion method (simple vs ocr)',
                        'Ensure the PDF is not password-protected',
                        'Check if the PDF contains convertible content',
                        'Verify sufficient disk space for output'
                    ]
                )

        return safe_execute(_pdf_to_word_operation, _operation_name="PDF to Word")

    def handle_batch_ocr(self, args) -> ProcessingResult:
        """Handle batch OCR with comprehensive error tracking."""

        def _batch_ocr_operation():
            self.print_message(f"Starting batch OCR: {args.input} -> {args.output}")

            # Validate directories
            input_path = self.validator.validate_directory(args.input, must_exist=True)
            output_path = self.validator.validate_output_path(args.output)

            # Find PDF files
            pdf_files = list(input_path.glob("*.pdf"))

            if not pdf_files:
                raise ValidationError(
                    'input_directory',
                    str(input_path),
                    'directory containing PDF files',
                    [f"No PDF files found in {input_path}",
                     'Check if the directory contains .pdf files',
                     'Verify the directory path is correct']
                )

            self.print_message(f"Found {len(pdf_files)} PDF files for processing")

            if not self.confirm_action(f"Process {len(pdf_files)} files?"):
                raise ValidationError(
                    'user_choice',
                    'cancelled',
                    'user confirmation to proceed',
                    ['Confirm the batch operation to continue']
                )

            # Create output directory
            output_path.mkdir(parents=True, exist_ok=True)

            # Process with Rich batch tracker if available
            if self.ui:
                tracker = BatchProgressTracker(self.ui)
                tracker.start_batch(len(pdf_files), "Batch OCR")

                for pdf_file in pdf_files:
                    output_file = output_path / f"{pdf_file.stem}_ocr{pdf_file.suffix}"

                    # Process individual file with error handling
                    file_result = safe_execute(
                        self.processor.ocr_pdf,
                        str(pdf_file),
                        str(output_file),
                        language=args.language,
                        _operation_name=f"OCR {pdf_file.name}"
                    )

                    # Set file-specific metadata
                    file_result.input_file = str(pdf_file)
                    file_result.output_file = str(output_file) if file_result.success else None
                    if file_result.success:
                        file_result.metadata['file_size'] = pdf_file.stat().st_size

                    tracker.update_progress(file_result)

                tracker.finish_batch("Batch OCR")

                # Calculate overall success
                success_count = sum(1 for r in tracker.results if r.success)

                return ProcessingResult.success_result(
                    message=f"Batch OCR completed: {success_count}/{len(pdf_files)} files processed successfully",
                    operation="Batch OCR",
                    input_file=str(input_path),
                    output_file=str(output_path),
                    metadata={
                        'total_files': len(pdf_files),
                        'successful_files': success_count,
                        'failed_files': len(pdf_files) - success_count
                    }
                )
            else:
                # Fallback for non-Rich processing
                success_count = 0
                for i, pdf_file in enumerate(pdf_files, 1):
                    print(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
                    output_file = output_path / f"{pdf_file.stem}_ocr{pdf_file.suffix}"

                    try:
                        result = self.processor.ocr_pdf(str(pdf_file), str(output_file), language=args.language)
                        if result and result.get('success', True):
                            success_count += 1
                            print(f"  ✅ Success: {output_file.name}")
                        else:
                            print(f"  ❌ Failed: {pdf_file.name}")
                    except Exception as e:
                        print(f"  ❌ Error: {str(e)}")

                return ProcessingResult.success_result(
                    message=f"Batch OCR completed: {success_count}/{len(pdf_files)} files processed",
                    operation="Batch OCR",
                    metadata={'success_count': success_count, 'total_files': len(pdf_files)}
                )

        return safe_execute(_batch_ocr_operation, _operation_name="Batch OCR")

    def handle_test_errors(self, args) -> ProcessingResult:
        """Test the error handling system with various error scenarios."""

        if not self.ui:
            self.print_message("Error testing requires Rich interface", "error")
            return ProcessingResult.error_result(
                error=DocForgeException("Rich interface not available"),
                operation="Test Errors"
            )

        self.print_message("Testing error handling system...")

        # Test different error types
        error_tests = [
            ("File Not Found", lambda: FileNotFoundError("nonexistent_file.pdf")),
            ("Invalid Format", lambda: InvalidFileFormatError("document.txt", ".pdf", ".txt")),
            ("Validation Error", lambda: ValidationError("quality", 150, "1-100")),
            ("OCR Error", lambda: OCRError("sample.pdf", "Tesseract not found"))
        ]

        for test_name, error_creator in error_tests:
            self.ui.console.print(f"\n[bold cyan]Testing: {test_name}[/bold cyan]")
            try:
                raise error_creator()
            except DocForgeException as e:
                self.ui.display_error_details(e)

            time.sleep(1)  # Brief pause between tests

        self.print_message("Error handling test completed!", "success")
        return ProcessingResult.success_result(
            message="All error types tested successfully",
            operation="Test Errors"
        )

    def handle_test_rich(self, args) -> ProcessingResult:
        """Test the Rich interface - enhanced version."""
        if not self.ui:
            self.print_message("Rich interface not available", "error")
            return ProcessingResult.error_result(
                error=DocForgeException("Rich interface not available"),
                operation="Test Rich"
            )

        self.print_message("Testing Rich CLI interface...")

        # Test all message types
        self.print_message("This is a success message!", "success")
        self.print_message("This is a warning message!", "warning")
        self.print_message("This is an error message!", "error")

        # Test configuration display
        config = {
            "Rich Version": "13.0+",
            "Error Handling": "Enhanced",
            "Features": "Progress bars, tables, colors, error panels"
        }
        self.display_config(config)

        # Test batch processing simulation
        tracker = BatchProgressTracker(self.ui)
        tracker.start_batch(3, "Test Processing")

        for i in range(3):
            time.sleep(1)
            result = ProcessingResult.success_result(
                message=f"Test file {i + 1} processed",
                operation="Test",
                input_file=f"test_file_{i + 1}.pdf",
                output_file=f"output_{i + 1}.pdf",
                processing_time=1.0,
                metadata={'file_size': 1024 * (i + 1) * 100}
            )
            tracker.update_progress(result)

        tracker.finish_batch("Test Processing")
        self.print_message("Rich CLI test completed!", "success")

        return ProcessingResult.success_result(
            message="Rich CLI interface test completed successfully",
            operation="Test Rich",
            metadata={'tests_passed': 'all'}
        )

    # Placeholder methods for other commands - implement with error handling
    def handle_optimize(self, args) -> ProcessingResult:
        """Handle optimize command - add your existing logic with error handling."""
        return safe_execute(
            lambda: self._optimize_implementation(args),
            _operation_name="PDF Optimization"
        )

    def _optimize_implementation(self, args):
        """Your existing optimization logic wrapped with error handling."""
        # Add your existing optimization code here
        # This is just a placeholder
        raise DocForgeException(
            "Optimization not yet implemented with error handling",
            error_code="NOT_IMPLEMENTED",
            suggestions=["Implement optimization logic in _optimize_implementation method"]
        )

    def handle_split_pdf(self, args) -> ProcessingResult:
        """Handle split PDF - add your existing logic with error handling."""
        return safe_execute(
            lambda: self._split_pdf_implementation(args),
            _operation_name="PDF Splitting"
        )

    def _split_pdf_implementation(self, args):
        """Your existing split PDF logic wrapped with error handling."""
        # Add your existing split PDF code here
        # This is just a placeholder
        raise DocForgeException(
            "PDF splitting not yet implemented with error handling",
            error_code="NOT_IMPLEMENTED",
            suggestions=["Implement split PDF logic in _split_pdf_implementation method"]
        )

    def run_interactive(self):
        """Run interactive mode with enhanced error handling."""
        if self.ui:
            self.ui.print_info("Starting DocForge Interactive Mode with Enhanced Error Handling...")
            # Add your existing interactive mode logic here
        else:
            print("🚀 Starting Interactive Mode...")
            # Your existing interactive mode logic

    def handle_test_validation(self, args):
        """Test the enhanced validation system."""

        if not self.ui:
            self.print_message("Enhanced validation testing requires Rich interface", "error")
            return

        self.print_message("Testing enhanced validation system...")

        # Test Parameter Validation
        if self.console:  # Check if console is available
            self.console.print(f"\n[bold cyan]Testing Parameter Validation:[/bold cyan]")
        else:
            print("\nTesting Parameter Validation:")

        test_cases = [
            ("language", "en", "Should auto-correct to 'eng'"),
            ("language", "french", "Should auto-correct to 'fra'"),
            ("quality", 150, "Should show validation error"),
        ]

        for param, value, description in test_cases:
            if self.console:
                self.console.print(f"\n[yellow]Test: {description}[/yellow]")
            else:
                print(f"\nTest: {description}")

            try:
                if param == "language":
                    from ..core.validators import SmartParameterValidator
                    result, suggestions = SmartParameterValidator.validate_and_suggest_language(value)
                    if result != value:
                        self.print_message(f"✨ Auto-corrected {param}: '{value}' → '{result}'", "success")
                elif param == "quality":
                    from ..core.validators import ParameterValidator
                    ParameterValidator.validate_quality(value)

            except ValidationError as e:
                if self.ui:
                    self.ui.display_error_details(e)
                else:
                    self.print_message(f"Validation Error: {e.message}", "error")
            except Exception as e:
                self.print_message(f"Test failed: {str(e)}", "warning")

        self.print_message("Enhanced validation test completed!", "success")


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
