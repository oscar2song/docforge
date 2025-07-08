"""Custom exceptions for DocForge processing."""

class DocForgeError(Exception):
    """Base exception for DocForge errors."""
    pass

class PDFProcessingError(DocForgeError):
    """Exception raised during PDF processing."""
    pass

class OCRProcessingError(DocForgeError):
    """Exception raised during OCR processing."""
    pass

class OptimizationError(DocForgeError):
    """Exception raised during optimization."""
    pass