#!/usr/bin/env python3
"""
🔨 DocForge - Document Processing Toolkit
Entry point for the application
"""

import argparse
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

try:
    from docforge.core.processor import DocumentProcessor
    from docforge.cli.interface import CLIInterface
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the correct directory and dependencies are installed")
    sys.exit(1)


def print_help():
    """Print usage help."""
    print("\n📖 DocForge Usage:")
    print("=" * 30)
    print("\n🔧 Command Line Usage:")
    print("  python main.py ocr -i input.pdf -o output.pdf")
    print("  python main.py optimize -i input.pdf -o output.pdf --type aggressive")
    print("  python main.py batch-ocr -i input_folder -o output_folder")
    print("  python main.py batch-optimize -i input_folder -o output_folder --type scanned")
    print("  python main.py advanced-optimize -i input.pdf -o output.pdf")
    print("  python main.py analyze -i input.pdf --type ocr")
    print("\n🎯 Available Optimization Types:")
    print("  standard     - Balanced quality/size (recommended)")
    print("  aggressive   - Maximum compression")
    print("  scanned      - Optimized for scanned documents")
    print("  scale_only   - Scale oversized pages")
    print("  high_quality - Preserve maximum quality")
    print("\n🌐 OCR Layout Modes:")
    print("  standard - Good balance (default)")
    print("  precise  - Best layout preservation")
    print("  text_only - Text without images")
    print("\n🔥 Interactive Mode:")
    print("  python main.py                    # Interactive menu")
    print("\n💡 Examples:")
    print("  # OCR with precise layout")
    print("  python main.py ocr -i scan.pdf -o searchable.pdf --layout-mode precise")
    print()
    print("  # Aggressive optimization with custom quality")
    print("  python main.py optimize -i large.pdf -o small.pdf --type aggressive --quality 60")
    print()
    print("  # Batch optimize scanned PDFs")
    print("  python main.py batch-optimize -i ./scans -o ./optimized --type scanned")
    print()


def main():
    """Main entry point for DocForge."""
    print("🔨 DocForge - Document Processing Toolkit")
    print("Forge perfect documents with precision and power")
    print("=" * 50)

    parser = argparse.ArgumentParser(
        description="DocForge Document Processing Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python main.py

  # OCR a PDF
  python main.py ocr -i input.pdf -o output.pdf --language eng

  # Optimize with aggressive compression
  python main.py optimize -i input.pdf -o output.pdf --type aggressive

  # Merge PDFs from folder
  python main.py merge -i ./folder -o merged.pdf --page-numbers

  # Merge specific files
  python main.py merge -i "file1.pdf,file2.pdf" -o merged.pdf --preserve-signatures

  # Batch optimize scanned PDFs
  python main.py batch-optimize -i ./input -o ./output --type scanned

  # Advanced interactive optimization
  python main.py advanced-optimize -i input.pdf -o output.pdf

  # Advanced interactive merge
  python main.py advanced-merge -i ./folder -o merged.pdf

  # Analyze PDF for OCR
  python main.py analyze -i input.pdf --type ocr

Optimization Types:
  standard, aggressive, scanned, scale_only, high_quality

OCR Layout Modes:
  standard, precise, text_only

Merge Options:
  --page-numbers (add page numbers)
  --no-page-numbers (merge without page numbers)
  --preserve-signatures (use signature-preserving method)
        """
    )

    parser.add_argument('--help-extended', action='store_true',
                        help='Show extended help with examples')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add subcommands
    CLIInterface.setup_parsers(subparsers)

    # Parse arguments
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        print("🚀 Starting Interactive Mode...")
        print("Use --help to see command line options")
        cli = CLIInterface()
        cli.run_interactive()
        return

    args = parser.parse_args()

    if args.help_extended:
        print_help()
        return

    if not args.command:
        # Interactive mode
        print("🚀 Starting Interactive Mode...")
        cli = CLIInterface()
        cli.run_interactive()
    else:
        # Command line mode
        print(f"🔧 Executing: {args.command}")
        cli = CLIInterface()
        cli.execute_command(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 DocForge interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        print("Use --help for usage information")
        sys.exit(1)
