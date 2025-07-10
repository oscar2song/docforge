#!/usr/bin/env python3
"""
DocForge PDF Splitter Module
Follows DocForge architecture with BaseProcessor inheritance
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Union, Tuple

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("PyPDF2 is required. Install it with: pip install PyPDF2")
    sys.exit(1)

# Import BaseProcessor from your existing architecture
try:
    from ..core.base_processor import BaseProcessor
except ImportError:
    try:
        from core.base_processor import BaseProcessor
    except ImportError:
        # Fallback if BaseProcessor doesn't exist yet
        class BaseProcessor:
            def __init__(self, verbose=True):
                self.verbose = verbose

            def log(self, message):
                if self.verbose:
                    print(message)


class PDFSplitter(BaseProcessor):
    """
    DocForge PDF Splitter

    Split PDF files into multiple documents based on page ranges, bookmarks,
    or custom splitting criteria. Supports batch processing and various output formats.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the PDF splitter.

        Args:
            verbose (bool): Enable verbose logging
        """
        super().__init__(verbose=verbose)

    def process(self, input_path: str, method: str = 'pages', **kwargs) -> List[str]:
        """
        Main processing method - split PDF using specified method.

        Args:
            input_path (str): Path to input PDF file
            method (str): Split method ('pages', 'size', 'bookmarks')
            **kwargs: Additional options based on method

        Returns:
            List[str]: List of created output file paths
        """
        if method == 'pages':
            start_pages = kwargs.get('start_pages', [1])
            output_dir = kwargs.get('output_dir')
            naming_template = kwargs.get('naming_template', "{base}_part{num}_pages{start}-{end}")
            return self.split_by_pages(input_path, start_pages, output_dir, naming_template)

        elif method == 'size':
            max_pages_per_file = kwargs.get('max_pages_per_file', 10)
            output_dir = kwargs.get('output_dir')
            return self.split_by_size(input_path, max_pages_per_file, output_dir)

        elif method == 'bookmarks':
            output_dir = kwargs.get('output_dir')
            return self.split_by_bookmarks(input_path, output_dir)

        else:
            raise ValueError(f"Unknown split method: {method}")

    def split_by_pages(self, input_path: str, start_pages: Union[str, List[int]],
                       output_dir: Optional[str] = None,
                       naming_template: str = "{base}_part{num}_pages{start}-{end}") -> List[str]:
        """
        Split PDF by start page numbers.

        Args:
            input_path (str): Path to input PDF
            start_pages (Union[str, List[int]]): Start page numbers
            output_dir (str, optional): Output directory
            naming_template (str): Filename template

        Returns:
            List[str]: Created file paths
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Parse start pages if string provided
        if isinstance(start_pages, str):
            start_pages = self._parse_start_pages(start_pages)

        # Set output directory
        if output_dir is None:
            output_dir = input_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        # Read the input PDF
        self.log(f"Reading PDF: {input_path}")
        reader = PdfReader(str(input_path))
        total_pages = len(reader.pages)
        self.log(f"Total pages: {total_pages}")

        # Validate start pages
        start_pages = sorted(set(start_pages))
        if start_pages[0] < 1:
            raise ValueError("Page numbers must start from 1")
        if start_pages[-1] > total_pages:
            raise ValueError(f"Start page {start_pages[-1]} exceeds total pages {total_pages}")

        # Calculate page ranges
        page_ranges = self._calculate_page_ranges(start_pages, total_pages)

        self.log(f"Will create {len(page_ranges)} files:")
        for i, (start, end) in enumerate(page_ranges):
            self.log(f"  Part {i + 1}: pages {start}-{end}")

        # Create output files
        output_files = []
        base_name = input_path.stem

        for i, (start_page, end_page) in enumerate(page_ranges):
            # Create output filename using template
            output_filename = naming_template.format(
                base=base_name,
                num=i + 1,
                start=start_page,
                end=end_page
            ) + ".pdf"
            output_path = output_dir / output_filename

            # Create new PDF with specified pages
            writer = PdfWriter()

            # Add pages (convert from 1-indexed to 0-indexed)
            for page_num in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page_num])

            # Write to file
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            output_files.append(str(output_path))
            self.log(f"Created: {output_path}")

        return output_files

    def split_by_size(self, input_path: str, max_pages_per_file: int,
                      output_dir: Optional[str] = None) -> List[str]:
        """
        Split PDF by maximum pages per file.

        Args:
            input_path (str): Path to input PDF
            max_pages_per_file (int): Maximum pages per output file
            output_dir (str, optional): Output directory

        Returns:
            List[str]: Created file paths
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        reader = PdfReader(str(input_path))
        total_pages = len(reader.pages)

        # Calculate start pages based on size limit
        start_pages = list(range(1, total_pages + 1, max_pages_per_file))

        self.log(f"Splitting {total_pages} pages into files of max {max_pages_per_file} pages each")

        return self.split_by_pages(input_path, start_pages, output_dir,
                                   "{base}_part{num}_{start}-{end}")

    def split_by_bookmarks(self, input_path: str, output_dir: Optional[str] = None) -> List[str]:
        """
        Split PDF based on bookmarks.

        Args:
            input_path (str): Path to input PDF
            output_dir (str, optional): Output directory

        Returns:
            List[str]: Created file paths
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        reader = PdfReader(str(input_path))

        if not reader.outline:
            raise ValueError("PDF has no bookmarks/outline to split by")

        # Extract bookmark page numbers
        bookmark_pages = self._extract_bookmark_pages(reader)

        if not bookmark_pages:
            raise ValueError("Could not extract valid bookmark page numbers")

        self.log(f"Found {len(bookmark_pages)} bookmarks")
        for title, page_num in bookmark_pages:
            self.log(f"  '{title}' at page {page_num}")

        # Use only the page numbers for splitting
        start_pages = [page for _, page in bookmark_pages]

        return self.split_by_pages(input_path, start_pages, output_dir,
                                   "{base}_{num}_{start}-{end}")

    def extract_pages(self, input_path: str, page_range: str, output_path: str) -> bool:
        """
        Extract specific pages from PDF.

        Args:
            input_path (str): Path to input PDF
            page_range (str): Page range specification (e.g., "1-5,10,15-20")
            output_path (str): Path for output PDF

        Returns:
            bool: True if extraction successful
        """
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)

            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

            # Parse page range
            pages_to_extract = self._parse_page_range(page_range)

            reader = PdfReader(str(input_path))
            total_pages = len(reader.pages)

            # Validate page numbers
            invalid_pages = [p for p in pages_to_extract if p < 1 or p > total_pages]
            if invalid_pages:
                raise ValueError(f"Invalid page numbers: {invalid_pages}")

            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create new PDF with specified pages
            writer = PdfWriter()

            for page_num in sorted(pages_to_extract):
                writer.add_page(reader.pages[page_num - 1])  # Convert to 0-indexed

            # Write to file
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            self.log(f"Extracted {len(pages_to_extract)} pages to: {output_path}")
            return True

        except Exception as e:
            self.log(f"Error extracting pages: {e}")
            return False

    def get_pdf_info(self, input_path: str) -> Dict:
        """
        Get information about a PDF file.

        Args:
            input_path (str): Path to PDF file

        Returns:
            Dict: PDF information including page count, bookmarks, etc.
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")

        reader = PdfReader(str(input_path))

        info = {
            'path': str(input_path),
            'page_count': len(reader.pages),
            'has_bookmarks': bool(reader.outline),
            'bookmarks': [],
            'metadata': {}
        }

        # Extract metadata
        if reader.metadata:
            info['metadata'] = {
                'title': reader.metadata.get('/Title', ''),
                'author': reader.metadata.get('/Author', ''),
                'subject': reader.metadata.get('/Subject', ''),
                'creator': reader.metadata.get('/Creator', ''),
                'producer': reader.metadata.get('/Producer', ''),
                'creation_date': reader.metadata.get('/CreationDate', ''),
                'modification_date': reader.metadata.get('/ModDate', '')
            }

        # Extract bookmarks
        if reader.outline:
            try:
                bookmark_pages = self._extract_bookmark_pages(reader)
                info['bookmarks'] = [{'title': title, 'page': page}
                                     for title, page in bookmark_pages]
            except:
                pass

        return info

    def batch_split(self, input_patterns: List[str], split_config: Dict,
                    output_dir: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Batch split multiple PDF files.

        Args:
            input_patterns (List[str]): List of file paths or glob patterns
            split_config (Dict): Configuration for splitting (method, parameters)
            output_dir (str, optional): Base output directory

        Returns:
            Dict[str, List[str]]: Mapping of input files to output files
        """
        results = {}

        # Collect all input files
        input_files = []
        for pattern in input_patterns:
            if '*' in pattern or '?' in pattern:
                from glob import glob
                input_files.extend(glob(pattern))
            else:
                input_files.append(pattern)

        method = split_config.get('method', 'pages')

        for input_file in input_files:
            try:
                self.log(f"Processing: {input_file}")

                # Create output subdirectory for each input file
                file_output_dir = output_dir
                if output_dir:
                    file_stem = Path(input_file).stem
                    file_output_dir = Path(output_dir) / file_stem

                # Process based on method
                if method == 'pages':
                    start_pages = split_config.get('start_pages', [1])
                    output_files = self.split_by_pages(input_file, start_pages, file_output_dir)
                elif method == 'size':
                    max_pages = split_config.get('max_pages_per_file', 10)
                    output_files = self.split_by_size(input_file, max_pages, file_output_dir)
                elif method == 'bookmarks':
                    output_files = self.split_by_bookmarks(input_file, file_output_dir)
                else:
                    raise ValueError(f"Unknown split method: {method}")

                results[input_file] = output_files

            except Exception as e:
                self.log(f"Error processing {input_file}: {e}")
                results[input_file] = []

        return results

    def _parse_start_pages(self, start_pages_str: str) -> List[int]:
        """Parse comma-separated start page numbers."""
        try:
            pages = [int(p.strip()) for p in start_pages_str.split(',')]
            return pages
        except ValueError as e:
            raise ValueError(f"Invalid page numbers format: {start_pages_str}. Use format: 1,89,150")

    def _parse_page_range(self, page_range: str) -> List[int]:
        """
        Parse page range specification like "1-5,10,15-20".

        Args:
            page_range (str): Page range specification

        Returns:
            List[int]: List of page numbers
        """
        pages = []

        for part in page_range.split(','):
            part = part.strip()

            if '-' in part:
                start, end = part.split('-', 1)
                start_page = int(start.strip())
                end_page = int(end.strip())
                pages.extend(range(start_page, end_page + 1))
            else:
                pages.append(int(part))

        return sorted(set(pages))

    def _calculate_page_ranges(self, start_pages: List[int], total_pages: int) -> List[Tuple[int, int]]:
        """Calculate page ranges from start pages."""
        page_ranges = []

        for i, start in enumerate(start_pages):
            if i == len(start_pages) - 1:
                end = total_pages
            else:
                end = start_pages[i + 1] - 1
            page_ranges.append((start, end))

        return page_ranges

    def _extract_bookmark_pages(self, reader: PdfReader) -> List[Tuple[str, int]]:
        """Extract bookmark titles and page numbers."""
        bookmarks = []

        def extract_from_outline(outline, level=0):
            for item in outline:
                if isinstance(item, list):
                    extract_from_outline(item, level + 1)
                else:
                    try:
                        title = item.title if hasattr(item, 'title') else str(item)
                        page = reader.get_destination_page_number(item) + 1
                        bookmarks.append((title, page))
                    except:
                        continue

        extract_from_outline(reader.outline)

        # Remove duplicates and sort by page number
        seen_pages = set()
        unique_bookmarks = []

        for title, page in sorted(bookmarks, key=lambda x: x[1]):
            if page not in seen_pages:
                unique_bookmarks.append((title, page))
                seen_pages.add(page)

        return unique_bookmarks


# Backward compatibility functions
def parse_start_pages(start_pages_str):
    """Parse comma-separated start page numbers."""
    try:
        pages = [int(p.strip()) for p in start_pages_str.split(',')]
        return pages
    except ValueError as e:
        raise ValueError(f"Invalid page numbers format: {start_pages_str}. Use format: 1,89,150")


def split_pdf(input_path, start_pages, output_dir=None):
    """
    Split a PDF file into multiple files based on start page numbers.
    Original function preserved for backward compatibility.

    Args:
        input_path (str): Path to the input PDF file
        start_pages (list): List of start page numbers (1-indexed)
        output_dir (str, optional): Directory to save output files

    Returns:
        list: List of created output file paths
    """
    splitter = PDFSplitter(verbose=True)
    return splitter.split_by_pages(input_path, start_pages, output_dir)


def split_pdf_simple(input_file, start_pages, output_dir=None):
    """
    Simplified function for use in other scripts.
    Original function preserved for backward compatibility.

    Args:
        input_file (str): Path to input PDF
        start_pages (str or list): Either "1,89" or [1, 89]
        output_dir (str, optional): Output directory

    Returns:
        list: Created file paths
    """
    if isinstance(start_pages, str):
        start_pages = parse_start_pages(start_pages)

    return split_pdf(input_file, start_pages, output_dir)


# Command line interface for standalone usage
def main():
    """Command line interface - preserved from original."""
    if len(sys.argv) != 3:
        print("Usage: python pdf_splitter.py <input_pdf> <start_pages>")
        print("Example: python pdf_splitter.py document.pdf 1,89")
        print("This will split a PDF into parts starting at pages 1 and 89")
        sys.exit(1)

    input_pdf = sys.argv[1]
    start_pages_str = sys.argv[2]

    try:
        # Parse start pages
        start_pages = parse_start_pages(start_pages_str)
        print(f"Start pages: {start_pages}")

        # Split the PDF using original function
        output_files = split_pdf(input_pdf, start_pages)

        print(f"\nSuccessfully created {len(output_files)} files:")
        for file_path in output_files:
            print(f"  {file_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
