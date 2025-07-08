"""
Main DocForge processor that coordinates all operations.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from .exceptions import DocForgeError
from ..pdf.ocr import PDFOCRProcessor
from ..pdf.optimizer import PDFOptimizer
from ..utils.logger import setup_logger

class DocumentProcessor:
    """Main DocForge processor that coordinates all operations."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = setup_logger(__name__, verbose)
        
        # Initialize operation modules
        self.ocr_processor = PDFOCRProcessor(verbose)
        self.optimizer = PDFOptimizer(verbose)
        
        if verbose:
            print("🔨 DocForge DocumentProcessor initialized")
            print(f"   OCR available: {self.ocr_processor.has_dependencies}")
            print(f"   PDF processing available: {self.optimizer.has_dependencies}")
    
    # OCR methods
    def ocr_pdf(self, input_path: str, output_path: str, **kwargs) -> Dict[str, Any]:
        """Add OCR text layer to PDF using proven implementation."""
        return self.ocr_processor.ocr_pdf(input_path, output_path, **kwargs)
    
    def batch_ocr_pdfs(self, input_folder: str, output_folder: str, **kwargs) -> Dict[str, Any]:
        """Batch OCR PDF files."""
        return self.ocr_processor.batch_ocr_pdfs(input_folder, output_folder, **kwargs)
    
    # Optimization methods
    def optimize_pdf(self, input_path: str, output_path: str, **kwargs) -> Dict[str, Any]:
        """Optimize a single PDF file."""
        return self.optimizer.optimize_pdf(input_path, output_path, **kwargs)
    
    def batch_optimize_pdfs(self, input_folder: str, output_folder: str, **kwargs) -> Dict[str, Any]:
        """Batch optimize PDF files."""
        return self.optimizer.batch_optimize_pdfs(input_folder, output_folder, **kwargs)