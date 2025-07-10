# docforge/core/validators.py
"""
Input validation system with clear error messages
"""

import os
import re
from pathlib import Path
from typing import Union, List, Optional, Tuple
from .exceptions import ValidationError, FileNotFoundError, InvalidFileFormatError


class FileValidator:
    """Validator for file operations."""

    @staticmethod
    def validate_input_file(file_path: Union[str, Path],
                            expected_extensions: Optional[List[str]] = None) -> Path:
        """
        Validate input file exists and has correct format.

        Args:
            file_path: Path to the input file
            expected_extensions: List of valid file extensions (e.g., ['.pdf', '.PDF'])

        Returns:
            Path object of validated file

        Raises:
            FileNotFoundError: If file doesn't exist
            InvalidFileFormatError: If file has wrong extension
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(str(path))

        # Check if it's a file (not directory)
        if not path.is_file():
            raise ValidationError(
                'input_file',
                str(path),
                'a file (not a directory)',
                [f"'{path}' is a directory, not a file",
                 "Provide the path to a specific file"]
            )

        # Check file extension if specified
        if expected_extensions:
            if path.suffix.lower() not in [ext.lower() for ext in expected_extensions]:
                raise InvalidFileFormatError(
                    str(path),
                    f"one of {expected_extensions}",
                    path.suffix
                )

        return path

    @staticmethod
    def validate_output_path(output_path: Union[str, Path],
                             create_dirs: bool = True) -> Path:
        """
        Validate output path and create directories if needed.

        Args:
            output_path: Path for output file
            create_dirs: Whether to create parent directories

        Returns:
            Path object of validated output path

        Raises:
            PermissionError: If cannot write to output location
        """
        path = Path(output_path)

        # Create parent directories if they don't exist
        if create_dirs and not path.parent.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
            except PermissionError as e:
                raise PermissionError(str(path.parent), "create directory")

        # Check if parent directory exists and is writable
        if not path.parent.exists():
            raise FileNotFoundError(str(path.parent))

        if not os.access(path.parent, os.W_OK):
            raise PermissionError(str(path.parent), "write")

        return path

    @staticmethod
    def validate_directory(dir_path: Union[str, Path],
                           must_exist: bool = True,
                           must_be_readable: bool = True) -> Path:
        """
        Validate directory path.

        Args:
            dir_path: Path to directory
            must_exist: Whether directory must already exist
            must_be_readable: Whether directory must be readable

        Returns:
            Path object of validated directory

        Raises:
            FileNotFoundError: If directory doesn't exist when required
            PermissionError: If directory not accessible
        """
        path = Path(dir_path)

        if must_exist and not path.exists():
            raise FileNotFoundError(str(path))

        if path.exists() and not path.is_dir():
            raise ValidationError(
                'directory_path',
                str(path),
                'a directory (not a file)',
                [f"'{path}' is a file, not a directory",
                 "Provide the path to a directory"]
            )

        if must_be_readable and path.exists() and not os.access(path, os.R_OK):
            raise PermissionError(str(path), "read")

        return path


class ParameterValidator:
    """Validator for command parameters."""

    @staticmethod
    def validate_language_code(language: str) -> str:
        """
        Validate OCR language code.

        Args:
            language: Language code (e.g., 'eng', 'fra', 'deu')

        Returns:
            Validated language code

        Raises:
            ValidationError: If language code is invalid
        """
        # Common language codes
        valid_languages = {
            'eng': 'English',
            'fra': 'French',
            'deu': 'German',
            'spa': 'Spanish',
            'ita': 'Italian',
            'por': 'Portuguese',
            'rus': 'Russian',
            'chi_sim': 'Chinese Simplified',
            'chi_tra': 'Chinese Traditional',
            'jpn': 'Japanese',
            'kor': 'Korean'
        }

        if language not in valid_languages:
            raise ValidationError(
                'language',
                language,
                f"one of {list(valid_languages.keys())}",
                [f"Available languages: {', '.join(valid_languages.keys())}",
                 "Use 'eng' for English (most common)",
                 "Check Tesseract documentation for more language codes"]
            )

        return language

    @staticmethod
    def validate_optimization_type(opt_type: str) -> str:
        """
        Validate optimization type.

        Args:
            opt_type: Optimization type

        Returns:
            Validated optimization type

        Raises:
            ValidationError: If optimization type is invalid
        """
        valid_types = ['standard', 'aggressive', 'scanned', 'scale_only', 'high_quality']

        if opt_type not in valid_types:
            raise ValidationError(
                'optimization_type',
                opt_type,
                f"one of {valid_types}",
                [f"Available types: {', '.join(valid_types)}",
                 "Use 'standard' for balanced quality/size",
                 "Use 'aggressive' for maximum compression"]
            )

        return opt_type

    @staticmethod
    def validate_page_range(page_range: str) -> List[Tuple[int, int]]:
        """
        Validate and parse page range string.

        Args:
            page_range: Page range string (e.g., "1-5,10-15,20")

        Returns:
            List of (start, end) tuples

        Raises:
            ValidationError: If page range format is invalid
        """
        if not page_range.strip():
            raise ValidationError(
                'page_range',
                page_range,
                'non-empty page range (e.g., "1-5,10-15")',
                ['Provide a page range like "1-5" or "1-5,10-15"',
                 'Use single numbers for individual pages',
                 'Use ranges like "1-5" for page ranges']
            )

        try:
            ranges = []
            for part in page_range.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-', 1)
                    start, end = int(start.strip()), int(end.strip())
                    if start > end:
                        raise ValidationError(
                            'page_range',
                            page_range,
                            'start page ≤ end page',
                            [f"In range '{part}', start page ({start}) is greater than end page ({end})",
                             'Use format "start-end" where start ≤ end']
                        )
                    ranges.append((start, end))
                else:
                    page = int(part)
                    ranges.append((page, page))

            return ranges

        except ValueError as e:
            raise ValidationError(
                'page_range',
                page_range,
                'valid page range format (e.g., "1-5,10-15")',
                ['Use numbers only in page ranges',
                 'Separate ranges with commas',
                 'Use hyphens for ranges: "1-5"',
                 'Example: "1-5,10-15,20"']
            )

    @staticmethod
    def validate_quality(quality: int) -> int:
        """
        Validate image quality parameter.

        Args:
            quality: Quality value (1-100)

        Returns:
            Validated quality value

        Raises:
            ValidationError: If quality is out of range
        """
        if not (1 <= quality <= 100):
            raise ValidationError(
                'quality',
                quality,
                'integer between 1 and 100',
                ['Quality must be between 1 (lowest) and 100 (highest)',
                 'Use 85 for good balance of quality and size',
                 'Use 95+ for high quality, 60- for small file size']
            )

        return quality

