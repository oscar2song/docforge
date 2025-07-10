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
    print("  python main.py merge -i input_folder -o merged.pdf --page-numbers")
    print("  python main.py pdf-to-word -i input.pdf -o output.docx --method simple")
    print("  python main.py split-pdf -i input.pdf -o output_folder --pages '1-5,10-15'")
    print("  python main.py batch-ocr -i input_folder -o output_folder")
    print("  python main.py batch-optimize -i input_folder -o output_folder --type scanned")
    print("  python main.py batch-pdf-to-word -i input_folder -o output_folder --method ocr")
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
    print("\n📄 PDF to Word Conversion Methods:")
    print("  simple - Fast text extraction (for native PDFs)")
    print("  ocr    - OCR-based conversion (for scanned PDFs)")
    print("\n✂️ PDF Split Types:")
    print("  pages     - Split by page ranges or fixed page count")
    print("  size      - Split by maximum file size")
    print("  bookmarks - Split at bookmark boundaries")
    print("\n🔥 Interactive Mode:")
    print("  python main.py                    # Interactive menu")
    print("\n💡 Examples:")
    print("  # OCR with precise layout")
    print("  python main.py ocr -i scan.pdf -o searchable.pdf --layout-mode precise")
    print()
    print("  # Aggressive optimization with custom quality")
    print("  python main.py optimize -i large.pdf -o small.pdf --type aggressive --quality 60")
    print()
    print("  # Merge PDFs with page numbers")
    print("  python main.py merge -i 'file1.pdf,file2.pdf' -o merged.pdf --page-numbers")
    print()
    print("  # Convert PDF to Word using OCR")
    print("  python main.py pdf-to-word -i document.pdf -o document.docx --method ocr")
    print()
    print("  # Split PDF by page ranges")
    print("  python main.py split-pdf -i document.pdf -o splits/ --pages '1-10,20-30'")
    print()
    print("  # Split PDF by file size")
    print("  python main.py split-pdf -i large.pdf -o splits/ --split-type size --max-size-mb 5")
    print()
    print("  # Batch convert PDFs to Word")
    print("  python main.py batch-pdf-to-word -i ./pdfs -o ./word_docs --method simple")
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

  # Convert PDF to Word (simple method)
  python main.py pdf-to-word -i document.pdf -o document.docx --method simple

  # Convert PDF to Word (OCR method for scanned PDFs)
  python main.py pdf-to-word -i scanned.pdf -o document.docx --method ocr

  # Split PDF by page ranges
  python main.py split-pdf -i document.pdf -o output/ --pages "1-5,10-15"

  # Split PDF every 3 pages
  python main.py split-pdf -i document.pdf -o output/ --pages-per-file 3

  # Split PDF by file size
  python main.py split-pdf -i large.pdf -o output/ --split-type size --max-size-mb 5

  # Split PDF by bookmarks
  python main.py split-pdf -i document.pdf -o output/ --split-type bookmarks

  # Batch optimize scanned PDFs
  python main.py batch-optimize -i ./input -o ./output --type scanned

  # Batch convert PDFs to Word
  python main.py batch-pdf-to-word -i ./pdfs -o ./word_docs --method ocr

  # Advanced interactive optimization
  python main.py advanced-optimize -i input.pdf -o output.pdf

  # Advanced interactive merge
  python main.py advanced-merge -i ./folder -o merged.pdf

  # Advanced interactive PDF to Word conversion
  python main.py advanced-pdf-to-word -i input.pdf -o output.docx

  # Advanced interactive PDF splitting
  python main.py advanced-split-pdf -i input.pdf -o output/

  # Analyze PDF for OCR
  python main.py analyze -i input.pdf --type ocr

Optimization Types:
  standard, aggressive, scanned, scale_only, high_quality

OCR Layout Modes:
  standard, precise, text_only

PDF to Word Methods:
  simple (fast text extraction), ocr (OCR-based for scanned PDFs)

PDF Split Types:
  pages (by page ranges/count), size (by file size), bookmarks (by bookmarks)

Merge Options:
  --page-numbers (add page numbers)
  --no-page-numbers (merge without page numbers)
  --preserve-signatures (use signature-preserving method)

New Commands:
  pdf-to-word          Convert PDF to Word document
  split-pdf            Split PDF into multiple files
  batch-pdf-to-word    Batch convert PDFs to Word documents
  advanced-pdf-to-word Advanced PDF to Word with full options
  advanced-split-pdf   Advanced PDF splitting with full options
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