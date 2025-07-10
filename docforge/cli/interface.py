"""
Command line interface for DocForge.
"""

import argparse
from pathlib import Path
import sys

from ..core.processor import DocumentProcessor


class CLIInterface:
    """Command line interface for DocForge."""

    def __init__(self):
        self.processor = DocumentProcessor()

    @staticmethod
    def setup_parsers(subparsers):
        """Setup CLI argument parsers."""

        # OCR command
        ocr_parser = subparsers.add_parser('ocr', help='Add OCR to PDF')
        ocr_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        ocr_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
        ocr_parser.add_argument('--language', default='eng', help='OCR language (default: eng)')
        ocr_parser.add_argument('--dpi', type=int, default=300, help='DPI for processing (default: 300)')
        ocr_parser.add_argument('--layout-mode', choices=['standard', 'precise', 'text_only'],
                                default='standard', help='Layout preservation mode (default: standard)')
        ocr_parser.add_argument('--preserve-images', action='store_true', default=True,
                                help='Preserve original images (default: True)')

        # Optimize command - Enhanced with all options
        optimize_parser = subparsers.add_parser('optimize', help='Optimize PDF file')
        optimize_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        optimize_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
        optimize_parser.add_argument('--type',
                                     choices=['standard', 'aggressive', 'scanned', 'scale_only', 'high_quality'],
                                     default='standard', help='Optimization type (default: standard)')
        optimize_parser.add_argument('--dpi', type=int, default=150, help='Target DPI (default: 150)')
        optimize_parser.add_argument('--quality', type=int, default=70, help='JPEG quality 1-100 (default: 70)')

        # Merge command - NEW
        merge_parser = subparsers.add_parser('merge', help='Merge PDF files')
        merge_parser.add_argument('-i', '--input', required=True,
                                  help='Input folder or comma-separated file list')
        merge_parser.add_argument('-o', '--output', required=True, help='Output merged PDF file')
        merge_parser.add_argument('--page-numbers', action='store_true', default=True,
                                  help='Add page numbers (default: True)')
        merge_parser.add_argument('--no-page-numbers', action='store_true',
                                  help='Do not add page numbers')
        merge_parser.add_argument('--preserve-signatures', action='store_true', default=True,
                                  help='Use signature-preserving merge (default: True)')
        merge_parser.add_argument('--font-size', type=int, default=12,
                                  help='Page number font size (default: 12)')

        # Merge folder command - NEW
        merge_folder_parser = subparsers.add_parser('merge-folder', help='Merge all PDFs in a folder')
        merge_folder_parser.add_argument('-i', '--input', required=True, help='Input folder')
        merge_folder_parser.add_argument('-o', '--output', required=True, help='Output merged PDF file')
        merge_folder_parser.add_argument('--page-numbers', action='store_true', default=True,
                                         help='Add page numbers (default: True)')
        merge_folder_parser.add_argument('--no-page-numbers', action='store_true',
                                         help='Do not add page numbers')
        merge_folder_parser.add_argument('--preserve-signatures', action='store_true', default=True,
                                         help='Use signature-preserving merge (default: True)')

        # PDF to Word command - NEW
        pdf_to_word_parser = subparsers.add_parser('pdf-to-word', help='Convert PDF to Word document')
        pdf_to_word_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        pdf_to_word_parser.add_argument('-o', '--output', required=True, help='Output Word file (.docx)')
        pdf_to_word_parser.add_argument('--method', choices=['simple', 'ocr'], default='simple',
                                        help='Conversion method (default: simple)')
        pdf_to_word_parser.add_argument('--language', default='eng',
                                        help='OCR language if using OCR method (default: eng)')

        # Split PDF command - NEW
        split_pdf_parser = subparsers.add_parser('split-pdf', help='Split PDF into multiple files')
        split_pdf_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        split_pdf_parser.add_argument('-o', '--output', required=True, help='Output directory')
        split_pdf_parser.add_argument('--pages', help='Page ranges to extract (e.g., "1-5,10-15" or "all")')
        split_pdf_parser.add_argument('--split-type', choices=['pages', 'size', 'bookmarks'], default='pages',
                                      help='Split type: by pages, file size, or bookmarks (default: pages)')
        split_pdf_parser.add_argument('--pages-per-file', type=int, default=1,
                                      help='Pages per output file when using pages split type (default: 1)')
        split_pdf_parser.add_argument('--max-size-mb', type=float, default=10.0,
                                      help='Maximum file size in MB when using size split type (default: 10.0)')

        # Batch OCR command - Enhanced
        batch_ocr_parser = subparsers.add_parser('batch-ocr', help='Batch OCR PDFs')
        batch_ocr_parser.add_argument('-i', '--input', required=True, help='Input folder')
        batch_ocr_parser.add_argument('-o', '--output', required=True, help='Output folder')
        batch_ocr_parser.add_argument('--language', default='eng', help='OCR language (default: eng)')
        batch_ocr_parser.add_argument('--layout-mode', choices=['standard', 'precise', 'text_only'],
                                      default='standard', help='Layout preservation mode (default: standard)')
        batch_ocr_parser.add_argument('--dpi', type=int, default=300, help='DPI for processing (default: 300)')

        # Batch optimize command - Enhanced with all options
        batch_opt_parser = subparsers.add_parser('batch-optimize', help='Batch optimize PDFs')
        batch_opt_parser.add_argument('-i', '--input', required=True, help='Input folder')
        batch_opt_parser.add_argument('-o', '--output', required=True, help='Output folder')
        batch_opt_parser.add_argument('--type',
                                      choices=['standard', 'aggressive', 'scanned', 'scale_only', 'high_quality'],
                                      default='standard', help='Optimization type (default: standard)')
        batch_opt_parser.add_argument('--dpi', type=int, default=150, help='Target DPI (default: 150)')
        batch_opt_parser.add_argument('--quality', type=int, default=70, help='JPEG quality 1-100 (default: 70)')
        batch_opt_parser.add_argument('--max-size', type=int, default=100,
                                      help='Max file size MB to process (default: 100)')

        # Batch PDF to Word command - NEW
        batch_pdf_to_word_parser = subparsers.add_parser('batch-pdf-to-word',
                                                         help='Batch convert PDFs to Word documents')
        batch_pdf_to_word_parser.add_argument('-i', '--input', required=True, help='Input folder')
        batch_pdf_to_word_parser.add_argument('-o', '--output', required=True, help='Output folder')
        batch_pdf_to_word_parser.add_argument('--method', choices=['simple', 'ocr'], default='simple',
                                              help='Conversion method (default: simple)')
        batch_pdf_to_word_parser.add_argument('--language', default='eng',
                                              help='OCR language if using OCR method (default: eng)')

        # Advanced optimize command
        advanced_opt_parser = subparsers.add_parser('advanced-optimize',
                                                    help='Advanced PDF optimization with full options')
        advanced_opt_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        advanced_opt_parser.add_argument('-o', '--output', required=True, help='Output PDF file')

        # Advanced merge command - NEW
        advanced_merge_parser = subparsers.add_parser('advanced-merge', help='Advanced PDF merging with full options')
        advanced_merge_parser.add_argument('-i', '--input', required=True,
                                           help='Input folder or comma-separated file list')
        advanced_merge_parser.add_argument('-o', '--output', required=True, help='Output merged PDF file')

        # Advanced PDF to Word command - NEW
        advanced_pdf_to_word_parser = subparsers.add_parser('advanced-pdf-to-word',
                                                            help='Advanced PDF to Word conversion with full options')
        advanced_pdf_to_word_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        advanced_pdf_to_word_parser.add_argument('-o', '--output', required=True, help='Output Word file')

        # Advanced split PDF command - NEW
        advanced_split_parser = subparsers.add_parser('advanced-split-pdf',
                                                      help='Advanced PDF splitting with full options')
        advanced_split_parser.add_argument('-i', '--input', required=True, help='Input PDF file')
        advanced_split_parser.add_argument('-o', '--output', required=True, help='Output directory')

        # Analysis command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze PDF for optimization/OCR/merge recommendations')
        analyze_parser.add_argument('-i', '--input', required=True, help='Input PDF file or folder')
        analyze_parser.add_argument('--type', choices=['ocr', 'optimization', 'merge'], default='ocr',
                                    help='Analysis type (default: ocr)')

    def execute_command(self, args):
        """Execute CLI command."""
        try:
            if args.command == 'ocr':
                result = self.processor.ocr_pdf(
                    args.input, args.output,
                    language=args.language,
                    dpi=args.dpi,
                    layout_mode=args.layout_mode,
                    preserve_images=args.preserve_images
                )
                print(f"✅ OCR completed: {result['pages_processed']} pages processed")
                print(f"📏 Size: {result['original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")

            elif args.command == 'optimize':
                result = self.processor.optimize_pdf(
                    args.input, args.output,
                    optimization_type=args.type,
                    target_dpi=args.dpi,
                    jpeg_quality=args.quality
                )
                print(f"✅ Optimized: {result['compression_ratio']:.1f}% size reduction")
                print(f"📏 Size: {result['original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
                print(f"🔧 Method: {result['optimization_type']}")

            elif args.command == 'merge':
                # Determine if input is folder or file list
                if ',' in args.input:
                    input_files = [f.strip() for f in args.input.split(',')]
                else:
                    input_files = args.input

                add_page_numbers = args.page_numbers and not args.no_page_numbers

                result = self.processor.merge_pdfs(
                    input_files, args.output,
                    add_page_numbers=add_page_numbers,
                    preserve_signatures=args.preserve_signatures,
                    font_size=args.font_size
                )
                print(f"✅ Merged: {result['files_merged']} files")
                print(f"📏 Size: {result['total_original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
                print(f"📄 Page numbers: {'Yes' if result['add_page_numbers'] else 'No'}")

            elif args.command == 'merge-folder':
                add_page_numbers = args.page_numbers and not args.no_page_numbers

                result = self.processor.merge_folder(
                    args.input, args.output,
                    add_page_numbers=add_page_numbers,
                    preserve_signatures=args.preserve_signatures
                )
                print(f"✅ Merged folder: {result['files_merged']} files")
                print(f"📏 Size: {result['total_original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
                print(f"📄 Page numbers: {'Yes' if result['add_page_numbers'] else 'No'}")

            elif args.command == 'pdf-to-word':
                result = self.processor.pdf_to_word(
                    args.input, args.output,
                    method=args.method,
                    language=args.language
                )
                print(f"✅ PDF to Word conversion completed")
                print(f"📄 Input: {args.input}")
                print(f"📄 Output: {args.output}")
                print(f"🔧 Method: {args.method}")

            elif args.command == 'split-pdf':
                if args.split_type == 'pages' and args.pages:
                    result = self.processor.split_pdf_by_pages(
                        args.input, args.output,
                        page_ranges=args.pages
                    )
                elif args.split_type == 'size':
                    result = self.processor.split_pdf_by_size(
                        args.input, args.output,
                        max_size_mb=args.max_size_mb
                    )
                elif args.split_type == 'bookmarks':
                    result = self.processor.split_pdf_by_bookmarks(
                        args.input, args.output
                    )
                else:
                    # Default pages split
                    result = self.processor.split_pdf(
                        args.input, args.output,
                        pages_per_file=args.pages_per_file
                    )

                if 'output_files' in result:
                    print(f"✅ PDF split completed: {len(result['output_files'])} files created")
                    print(f"📁 Output directory: {args.output}")
                    print(f"🔧 Split type: {args.split_type}")

            elif args.command == 'batch-pdf-to-word':
                result = self.processor.batch_pdf_to_word(
                    args.input, args.output,
                    method=args.method,
                    language=args.language
                )
                if 'processed' in result:
                    print(
                        f"✅ Batch PDF to Word: {result['processed']} files processed, {result.get('failed', 0)} failed")
                    print(f"🔧 Method: {args.method}")

            elif args.command == 'advanced-optimize':
                self._interactive_advanced_optimize()

            elif args.command == 'advanced-merge':
                self._interactive_advanced_merge()

            elif args.command == 'advanced-pdf-to-word':
                self._interactive_advanced_pdf_to_word()

            elif args.command == 'advanced-split-pdf':
                self._interactive_advanced_split_pdf()

            elif args.command == 'batch-ocr':
                result = self.processor.batch_ocr_pdfs(
                    args.input, args.output,
                    language=args.language,
                    layout_mode=args.layout_mode,
                    dpi=args.dpi
                )
                print(f"✅ Batch OCR: {result['processed']} files processed, {result['failed']} failed")
                if result['processed'] > 0:
                    print(
                        f"📏 Total size: {result['total_original_size']:.2f} MB → {result['total_final_size']:.2f} MB")

            elif args.command == 'batch-optimize':
                result = self.processor.batch_optimize_pdfs(
                    args.input, args.output,
                    optimization_type=args.type,
                    target_dpi=args.dpi,
                    jpeg_quality=args.quality,
                    max_file_size_mb=args.max_size
                )
                print(f"✅ Batch optimization: {result['processed']} files processed, {result['failed']} failed")
                if result['processed'] > 0:
                    total_reduction = ((result['total_original_size'] - result['total_final_size']) /
                                       result['total_original_size']) * 100
                    print(f"💾 Total reduction: {total_reduction:.1f}%")
                    print(
                        f"📏 Total size: {result['total_original_size']:.2f} MB → {result['total_final_size']:.2f} MB")

            elif args.command == 'analyze':
                if args.type == 'ocr':
                    self.processor.analyze_pdf_for_ocr(args.input)
                elif args.type == 'merge':
                    self.processor.analyze_merge_candidates(args.input)
                else:
                    # Basic optimization analysis
                    from pathlib import Path
                    file_path = Path(args.input)
                    if file_path.exists():
                        size_mb = file_path.stat().st_size / (1024 * 1024)
                        print(f"📊 PDF Analysis: {file_path.name}")
                        print(f"📏 File size: {size_mb:.2f} MB")

                        if size_mb > 10:
                            print("💡 Recommendation: File is large, try aggressive optimization")
                        elif size_mb > 5:
                            print("💡 Recommendation: Try standard optimization")
                        else:
                            print("💡 Recommendation: File already small, optimization may have minimal effect")
                    else:
                        print(f"❌ File not found: {args.input}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)

    def run_interactive(self):
        """Run interactive CLI mode."""
        print("\n🔨 DocForge Interactive Mode")
        print("=" * 35)

        while True:
            print("\nAvailable operations:")
            print("1. Simple OCR PDF")
            print("2. Advanced OCR PDF (all options)")
            print("3. Simple PDF Optimization (standard/aggressive)")
            print("4. Advanced PDF Optimization (6+ methods)")
            print("5. Interactive PDF Optimization (full menu)")
            print("6. Simple PDF Merge")
            print("7. Advanced PDF Merge (all options)")
            print("8. Interactive PDF Merge (full menu)")
            print("9. PDF to Word Conversion")
            print("10. Advanced PDF to Word (all options)")
            print("11. Split PDF")
            print("12. Advanced Split PDF (all options)")
            print("13. Batch OCR Processing")
            print("14. Batch PDF Optimization")
            print("15. Batch PDF to Word")
            print("16. Analyze PDF")
            print("17. Exit")

            choice = input("\nSelect operation (1-17): ").strip()

            if choice == '1':
                self._interactive_ocr()
            elif choice == '2':
                self._interactive_advanced_ocr()
            elif choice == '3':
                self._interactive_optimize()
            elif choice == '4':
                self._interactive_advanced_optimize()
            elif choice == '5':
                self._interactive_full_optimize()
            elif choice == '6':
                self._interactive_merge()
            elif choice == '7':
                self._interactive_advanced_merge()
            elif choice == '8':
                self._interactive_full_merge()
            elif choice == '9':
                self._interactive_pdf_to_word()
            elif choice == '10':
                self._interactive_advanced_pdf_to_word()
            elif choice == '11':
                self._interactive_split_pdf()
            elif choice == '12':
                self._interactive_advanced_split_pdf()
            elif choice == '13':
                self._interactive_batch_ocr()
            elif choice == '14':
                self._interactive_batch_optimize()
            elif choice == '15':
                self._interactive_batch_pdf_to_word()
            elif choice == '16':
                self._interactive_analyze()
            elif choice == '17':
                print("🔨 Thanks for using DocForge!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def _interactive_ocr(self):
        """Interactive OCR - Simple version."""
        print("\n--- OCR Processing (Simple) ---")
        input_file = input("Input PDF file: ")
        output_file = input("Output PDF file: ")
        language = input("Language [eng]: ") or "eng"

        try:
            result = self.processor.ocr_pdf(input_file, output_file, language=language)
            print(f"✅ OCR completed: {result['pages_processed']} pages processed")
            print(f"📏 Size: {result['original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_advanced_ocr(self):
        """Interactive OCR - Advanced version with all options."""
        print("\n--- OCR Processing (Advanced) ---")
        input_file = input("Input PDF file: ")
        output_file = input("Output PDF file: ")
        language = input("Language [eng]: ") or "eng"

        print("\nLayout mode:")
        print("1. Standard (good balance)")
        print("2. Precise (best layout preservation)")
        print("3. Text only (no images)")
        layout_choice = input("Choose layout mode (1-3) [1]: ") or "1"
        layout_map = {"1": "standard", "2": "precise", "3": "text_only"}
        layout_mode = layout_map.get(layout_choice, "standard")

        preserve_images = layout_mode != "text_only"

        try:
            dpi = int(input("DPI [300]: ") or "300")
        except ValueError:
            dpi = 300

        try:
            result = self.processor.ocr_pdf(
                input_file, output_file,
                language=language,
                dpi=dpi,
                layout_mode=layout_mode,
                preserve_images=preserve_images
            )
            print(f"✅ OCR completed: {result['pages_processed']} pages processed")
            print(f"📏 Size: {result['original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
            print(f"🔧 Method: {layout_mode}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_optimize(self):
        """Interactive optimization - Simple version."""
        print("\n--- PDF Optimization (Simple) ---")
        input_file = input("Input PDF file: ")
        output_file = input("Output PDF file: ")
        print("Optimization type:")
        print("  standard   - Balanced quality/size (recommended)")
        print("  aggressive - Maximum compression")
        opt_type = input("Optimization type (standard/aggressive) [standard]: ") or "standard"

        try:
            result = self.processor.optimize_pdf(input_file, output_file, optimization_type=opt_type)
            print(f"✅ Optimized: {result['compression_ratio']:.1f}% size reduction")
            print(f"📏 Size: {result['original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_advanced_optimize(self):
        """Interactive optimization - Advanced version with all methods."""
        print("\n--- PDF Optimization (Advanced) ---")
        print("\n🔧 Choose your optimization method:")
        print()
        print("1. Standard Optimization")
        print("   - Moderate compression, good balance")
        print("   - Best for: Mixed content PDFs")
        print()
        print("2. Aggressive Optimization")
        print("   - Maximum compression, smaller files")
        print("   - Best for: When file size is priority")
        print()
        print("3. Scanned PDF Optimization")
        print("   - Optimized for scanned documents")
        print("   - Best for: Scanned papers/books")
        print()
        print("4. Page Scaling Optimization")
        print("   - Scale oversized pages to standard sizes")
        print("   - Best for: Oversized pages")
        print()
        print("5. High Quality Optimization")
        print("   - Preserve maximum quality")
        print("   - Best for: Important documents")
        print()
        print("6. Custom Settings")
        print("   - Set your own DPI and quality")
        print()

        choice = input("Choose method (1-6): ").strip()

        input_file = input("📁 Input PDF file: ")
        output_file = input("📁 Output PDF file: ")

        try:
            if choice == "1":
                result = self.processor.optimize_pdf(input_file, output_file, optimization_type='standard')
            elif choice == "2":
                result = self.processor.optimize_pdf(input_file, output_file, optimization_type='aggressive')
            elif choice == "3":
                result = self.processor.optimize_pdf(input_file, output_file, optimization_type='scanned')
            elif choice == "4":
                result = self.processor.optimize_pdf(input_file, output_file, optimization_type='scale_only')
            elif choice == "5":
                result = self.processor.optimize_pdf(input_file, output_file, optimization_type='high_quality')
            elif choice == "6":
                # Custom settings
                try:
                    dpi = int(input("🎯 Target DPI (default 150): ") or "150")
                    quality = int(input("🗜️ JPEG quality % (default 70): ") or "70")

                    print("Optimization type:")
                    print("1. Standard  2. Aggressive  3. Scanned  4. High Quality")
                    type_choice = input("Choose type (1-4): ").strip()
                    type_map = {"1": "standard", "2": "aggressive", "3": "scanned", "4": "high_quality"}
                    opt_type = type_map.get(type_choice, "standard")

                    result = self.processor.optimize_pdf(
                        input_file, output_file,
                        target_dpi=dpi, jpeg_quality=quality,
                        optimization_type=opt_type
                    )
                except ValueError:
                    print("❌ Invalid input, using defaults")
                    result = self.processor.optimize_pdf(input_file, output_file, optimization_type='standard')
            else:
                print("❌ Invalid choice, using standard optimization")
                result = self.processor.optimize_pdf(input_file, output_file, optimization_type='standard')

            print(f"✅ Success!")
            print(f"📏 Size: {result['original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
            print(f"💾 Reduction: {result['compression_ratio']:.1f}%")
            print(f"🔧 Method: {result['optimization_type']}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_full_optimize(self):
        """Interactive optimization - Full menu system."""
        print("\n--- PDF Optimization (Interactive Menu) ---")
        try:
            # This would call the full interactive system from the processor
            result = self.processor.choose_optimization_method()
            if result:
                print(f"✅ Optimization completed via interactive menu!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_merge(self):
        """Interactive merge - Simple version."""
        print("\n--- PDF Merge (Simple) ---")
        input_source = input("Input (folder path or file1.pdf,file2.pdf): ")
        output_file = input("Output merged PDF file: ")

        # Determine if it's a folder or file list
        if ',' in input_source:
            input_files = [f.strip() for f in input_source.split(',')]
        else:
            input_files = input_source

        add_numbers = input("Add page numbers? (y/n) [y]: ").strip().lower()
        add_page_numbers = add_numbers != 'n'

        try:
            result = self.processor.merge_pdfs(input_files, output_file, add_page_numbers=add_page_numbers)
            print(f"✅ Merged: {result['files_merged']} files")
            print(f"📏 Size: {result['total_original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
            print(f"📄 Page numbers: {'Yes' if result['add_page_numbers'] else 'No'}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_advanced_merge(self):
        """Interactive merge - Advanced version with all options."""
        print("\n--- PDF Merge (Advanced) ---")

        print("📄 Choose merge type:")
        print("1. Merge folder (alphabetical order)")
        print("2. Merge specific files (custom order)")
        print("3. Standard merge")
        print("4. Signature-preserving merge")

        merge_choice = input("Choose type (1-4): ").strip()

        if merge_choice == "1":
            folder_path = input("📁 Input folder: ")
            output_file = input("📁 Output PDF file: ")

            add_numbers = input("Add page numbers? (y/n) [y]: ").strip().lower()
            add_page_numbers = add_numbers != 'n'

            preserve_sigs = input("Preserve signatures? (y/n) [y]: ").strip().lower()
            preserve_signatures = preserve_sigs != 'n'

            try:
                result = self.processor.merge_folder(folder_path, output_file,
                                                     add_page_numbers=add_page_numbers,
                                                     preserve_signatures=preserve_signatures)
                print(f"✅ Merged folder: {result['files_merged']} files")
                print(f"📏 Size: {result['total_original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        elif merge_choice == "2":
            print("Enter file paths (one per line, empty line to finish):")
            file_list = []
            while True:
                file_path = input(f"File {len(file_list) + 1}: ").strip()
                if not file_path:
                    break
                file_list.append(file_path)

            if not file_list:
                print("❌ No files specified")
                return

            output_file = input("📁 Output PDF file: ")

            add_numbers = input("Add page numbers? (y/n) [y]: ").strip().lower()
            add_page_numbers = add_numbers != 'n'

            preserve_sigs = input("Preserve signatures? (y/n) [y]: ").strip().lower()
            preserve_signatures = preserve_sigs != 'n'

            try:
                result = self.processor.merge_specific_files(file_list, output_file,
                                                             add_page_numbers=add_page_numbers,
                                                             preserve_signatures=preserve_signatures)
                print(f"✅ Merged files: {result['files_merged']} files")
                print(f"📏 Size: {result['total_original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        else:
            # Standard or signature-preserving merge
            input_source = input("Input (folder path or file1.pdf,file2.pdf): ")
            output_file = input("📁 Output PDF file: ")

            if ',' in input_source:
                input_files = [f.strip() for f in input_source.split(',')]
            else:
                input_files = input_source

            add_numbers = input("Add page numbers? (y/n) [y]: ").strip().lower()
            add_page_numbers = add_numbers != 'n'

            preserve_signatures = merge_choice == "4"

            try:
                result = self.processor.merge_pdfs(input_files, output_file,
                                                   add_page_numbers=add_page_numbers,
                                                   preserve_signatures=preserve_signatures)
                print(f"✅ Merged: {result['files_merged']} files")
                print(f"📏 Size: {result['total_original_size_mb']:.2f} MB → {result['final_size_mb']:.2f} MB")
                print(f"🔧 Method: {'Signature-preserving' if preserve_signatures else 'Standard'}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    def _interactive_full_merge(self):
        """Interactive merge - Full menu system."""
        print("\n--- PDF Merge (Interactive Menu) ---")
        try:
            # This would call the full interactive system from the processor
            result = self.processor.choose_merge_method()
            if result:
                print(f"✅ Merge completed via interactive menu!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_pdf_to_word(self):
        """Interactive PDF to Word conversion - Simple version."""
        print("\n--- PDF to Word Conversion (Simple) ---")
        input_file = input("Input PDF file: ")
        output_file = input("Output Word file (.docx): ")

        if not output_file.endswith('.docx'):
            output_file += '.docx'

        print("\nConversion method:")
        print("1. Simple extraction (fast, good for text PDFs)")
        print("2. OCR-based conversion (slower, good for scanned PDFs)")
        method_choice = input("Choose method (1-2) [1]: ") or "1"
        method = "simple" if method_choice == "1" else "ocr"

        language = "eng"
        if method == "ocr":
            language = input("OCR language [eng]: ") or "eng"

        try:
            result = self.processor.pdf_to_word(input_file, output_file, method=method, language=language)
            print(f"✅ PDF to Word conversion completed")
            print(f"📄 Method: {method}")
            print(f"📁 Output: {output_file}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_advanced_pdf_to_word(self):
        """Interactive PDF to Word - Advanced version with all options."""
        print("\n--- PDF to Word Conversion (Advanced) ---")
        input_file = input("Input PDF file: ")
        output_file = input("Output Word file (.docx): ")

        if not output_file.endswith('.docx'):
            output_file += '.docx'

        print("\n📄 Conversion Methods:")
        print("1. Simple Text Extraction")
        print("   - Fast extraction of existing text")
        print("   - Best for: Native PDFs with selectable text")
        print("   - Preserves: Text content, basic formatting")
        print()
        print("2. OCR-based Conversion")
        print("   - OCR + text extraction")
        print("   - Best for: Scanned PDFs, image-based PDFs")
        print("   - Preserves: All text content via OCR")
        print()

        method_choice = input("Choose conversion method (1-2): ").strip()
        method = "simple" if method_choice == "1" else "ocr"

        language = "eng"
        if method == "ocr":
            language = input("OCR language [eng]: ") or "eng"

        try:
            result = self.processor.pdf_to_word(input_file, output_file, method=method, language=language)
            print(f"✅ Advanced PDF to Word conversion completed")
            print(f"🔧 Method: {method}")
            print(f"📁 Output: {output_file}")
            if language != "eng":
                print(f"🌐 Language: {language}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_split_pdf(self):
        """Interactive PDF splitting - Simple version."""
        print("\n--- Split PDF (Simple) ---")
        input_file = input("Input PDF file: ")
        output_folder = input("Output folder: ")

        print("\nSplit method:")
        print("1. Split by pages (extract specific pages)")
        print("2. Split every N pages")
        print("3. Split by file size")
        split_choice = input("Choose method (1-3) [1]: ") or "1"

        try:
            if split_choice == "1":
                pages = input("Page ranges (e.g., '1-5,10-15') or 'all': ")
                result = self.processor.split_pdf_by_pages(input_file, output_folder, page_ranges=pages)
            elif split_choice == "2":
                pages_per_file = int(input("Pages per file [1]: ") or "1")
                result = self.processor.split_pdf(input_file, output_folder, pages_per_file=pages_per_file)
            elif split_choice == "3":
                max_size = float(input("Maximum file size in MB [10.0]: ") or "10.0")
                result = self.processor.split_pdf_by_size(input_file, output_folder, max_size_mb=max_size)

            if 'output_files' in result:
                print(f"✅ PDF split completed: {len(result['output_files'])} files created")
                print(f"📁 Output folder: {output_folder}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_advanced_split_pdf(self):
        """Interactive PDF splitting - Advanced version with all options."""
        print("\n--- Split PDF (Advanced) ---")
        input_file = input("Input PDF file: ")
        output_folder = input("Output folder: ")

        print("\n📄 Split Methods:")
        print("1. Split by Page Ranges")
        print("   - Extract specific page ranges")
        print("   - Best for: Extracting chapters, sections")
        print()
        print("2. Split by Fixed Page Count")
        print("   - Split into files with N pages each")
        print("   - Best for: Even distribution")
        print()
        print("3. Split by File Size")
        print("   - Split to keep files under size limit")
        print("   - Best for: Size-constrained sharing")
        print()
        print("4. Split by Bookmarks")
        print("   - Split at bookmark boundaries")
        print("   - Best for: Documents with proper bookmarks")
        print()

        split_choice = input("Choose method (1-4): ").strip()

        try:
            if split_choice == "1":
                print("Example page ranges: '1-5,10-15' or '1-3,7,12-20'")
                pages = input("Page ranges: ")
                result = self.processor.split_pdf_by_pages(input_file, output_folder, page_ranges=pages)
            elif split_choice == "2":
                pages_per_file = int(input("Pages per file: "))
                result = self.processor.split_pdf(input_file, output_folder, pages_per_file=pages_per_file)
            elif split_choice == "3":
                max_size = float(input("Maximum file size in MB: "))
                result = self.processor.split_pdf_by_size(input_file, output_folder, max_size_mb=max_size)
            elif split_choice == "4":
                result = self.processor.split_pdf_by_bookmarks(input_file, output_folder)
            else:
                print("❌ Invalid choice, using page ranges")
                pages = input("Page ranges: ")
                result = self.processor.split_pdf_by_pages(input_file, output_folder, page_ranges=pages)

            if 'output_files' in result:
                print(f"✅ Advanced PDF split completed: {len(result['output_files'])} files created")
                print(f"📁 Output folder: {output_folder}")
                print(
                    f"🔧 Method: {['Page ranges', 'Fixed pages', 'File size', 'Bookmarks'][int(split_choice) - 1] if split_choice.isdigit() and 1 <= int(split_choice) <= 4 else 'Page ranges'}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_batch_ocr(self):
        """Interactive batch OCR."""
        print("\n--- Batch OCR ---")
        input_folder = input("Input folder: ")
        output_folder = input("Output folder: ")
        language = input("Language [eng]: ") or "eng"

        print("\nLayout mode:")
        print("1. Standard  2. Precise  3. Text only")
        layout_choice = input("Choose layout mode (1-3) [1]: ") or "1"
        layout_map = {"1": "standard", "2": "precise", "3": "text_only"}
        layout_mode = layout_map.get(layout_choice, "standard")

        try:
            result = self.processor.batch_ocr_pdfs(
                input_folder, output_folder,
                language=language,
                layout_mode=layout_mode
            )
            print(f"✅ Batch OCR: {result['processed']} files processed, {result['failed']} failed")
            if result['processed'] > 0:
                print(f"📏 Total size: {result['total_original_size']:.2f} MB → {result['total_final_size']:.2f} MB")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_batch_optimize(self):
        """Interactive batch optimization."""
        print("\n--- Batch Optimization ---")
        input_folder = input("Input folder: ")
        output_folder = input("Output folder: ")

        print("\nOptimization type:")
        print("1. Standard (balanced)")
        print("2. Aggressive (maximum compression)")
        print("3. Scanned PDF (for scanned documents)")
        print("4. High Quality (preserve quality)")

        choice = input("Choose type (1-4): ").strip()
        type_map = {"1": "standard", "2": "aggressive", "3": "scanned", "4": "high_quality"}
        opt_type = type_map.get(choice, "standard")

        try:
            max_size = int(input("Max file size MB to process [100]: ") or "100")
        except ValueError:
            max_size = 100

        try:
            result = self.processor.batch_optimize_pdfs(
                input_folder, output_folder,
                optimization_type=opt_type,
                max_file_size_mb=max_size
            )
            print(f"✅ Batch optimization: {result['processed']} files processed, {result['failed']} failed")
            if result['processed'] > 0:
                total_reduction = ((result['total_original_size'] - result['total_final_size']) /
                                   result['total_original_size']) * 100
                print(f"💾 Total reduction: {total_reduction:.1f}%")
                print(f"📏 Total size: {result['total_original_size']:.2f} MB → {result['total_final_size']:.2f} MB")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_batch_pdf_to_word(self):
        """Interactive batch PDF to Word conversion."""
        print("\n--- Batch PDF to Word ---")
        input_folder = input("Input folder: ")
        output_folder = input("Output folder: ")

        print("\nConversion method:")
        print("1. Simple extraction (fast)")
        print("2. OCR-based conversion (slower, better for scanned PDFs)")

        method_choice = input("Choose method (1-2) [1]: ") or "1"
        method = "simple" if method_choice == "1" else "ocr"

        language = "eng"
        if method == "ocr":
            language = input("OCR language [eng]: ") or "eng"

        try:
            result = self.processor.batch_pdf_to_word(
                input_folder, output_folder,
                method=method,
                language=language
            )
            if 'processed' in result:
                print(f"✅ Batch PDF to Word: {result['processed']} files processed, {result.get('failed', 0)} failed")
                print(f"🔧 Method: {method}")
                print(f"📁 Output folder: {output_folder}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _interactive_analyze(self):
        """Interactive PDF analysis."""
        print("\n--- PDF Analysis ---")
        input_file = input("PDF file or folder to analyze: ")

        print("\nAnalysis type:")
        print("1. OCR analysis (check if OCR is needed)")
        print("2. Optimization analysis (size and structure)")
        print("3. Merge analysis (folder of PDFs for merging)")

        choice = input("Choose analysis type (1-3): ").strip()

        try:
            if choice == "1":
                self.processor.analyze_pdf_for_ocr(input_file)
            elif choice == "2":
                # Basic file info
                from pathlib import Path
                file_path = Path(input_file)
                if file_path.exists():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"📊 PDF Analysis: {file_path.name}")
                    print(f"📏 File size: {size_mb:.2f} MB")

                    if size_mb > 10:
                        print("💡 Recommendation: File is large, try aggressive optimization")
                    elif size_mb > 5:
                        print("💡 Recommendation: Try standard optimization")
                    else:
                        print("💡 Recommendation: File already small, optimization may have minimal effect")
                else:
                    print(f"❌ File not found: {input_file}")
            elif choice == "3":
                self.processor.analyze_merge_candidates(input_file)
            else:
                print("❌ Invalid choice")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
