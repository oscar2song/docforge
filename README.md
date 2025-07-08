# 🔨 DocForge - Document Processing Toolkit

**Forge perfect documents from any format with precision, power, and simplicity.**

DocForge is a comprehensive document processing toolkit built on proven implementations with a modern modular architecture. Born from real-world needs and battle-tested algorithms, DocForge transforms how you work with documents.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### 🔍 **OCR Processing**
- **Convert scanned PDFs** to searchable documents with precision
- **Multiple layout modes**: Standard, Precise, and Text-only
- **Language support**: 100+ languages via Tesseract
- **Batch processing**: Handle hundreds of documents efficiently
- **Memory optimized**: Smart processing for large files

### 🗜️ **Smart PDF Optimization**
- **6+ optimization methods**: Standard, Aggressive, Scanned, Scale-only, High-quality, Custom
- **Advanced compression**: Reduce file sizes by up to 90% without quality loss
- **Page scaling**: Normalize oversized pages to standard formats
- **Signature preservation**: Maintain document integrity for legal files
- **Batch optimization**: Process entire folders with custom settings

### 📄 **PDF Merging** *(NEW!)*
- **Flexible input**: Merge folders or specific file lists
- **Custom ordering**: Alphabetical or user-defined sequence
- **Page numbering**: Optional with customizable positioning and fonts
- **Signature preservation**: Specialized mode for legal documents
- **Analysis tools**: Preview merge operations before execution

### ⚙️ **Additional Capabilities**
- **Document analysis**: Extract insights and metadata
- **Batch processing**: Handle hundreds of documents efficiently
- **Memory efficient**: Optimized for large-scale operations
- **Cross-platform**: Windows, macOS, and Linux support

## 🏗️ **Architecture**

DocForge is built with a clean, modular architecture:

```
docforge/
├── core/          # Core processing engine and exceptions
├── pdf/           # PDF operations (proven implementations)
│   ├── optimizer.py    # PDF optimization with 6+ methods
│   ├── ocr.py         # OCR processing with layout preservation
│   └── pdf_merger.py  # PDF merging with signature support
├── cli/           # Command-line interface
└── utils/         # Shared utilities and logging
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/oscar2song/docforge.git
cd docforge

# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies
# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# macOS
brew install tesseract poppler

# Windows: Download Tesseract from
# https://github.com/tesseract-ocr/tesseract
```

### Requirements

Create `requirements.txt`:
```txt
PyMuPDF>=1.23.0
pytesseract>=0.3.10
Pillow>=10.0.0
pdf2image>=3.1.0
reportlab>=4.0.0
PyPDF2>=3.0.0
```

## 📖 Usage

### Interactive Mode
```bash
# Start interactive mode with 12 options
python main.py
```

### Command Line Interface

#### OCR Processing
```bash
# Basic OCR
python main.py ocr -i scanned.pdf -o searchable.pdf --language eng

# Precise layout preservation
python main.py ocr -i document.pdf -o searchable.pdf --layout-mode precise --dpi 400

# Batch OCR with text-only output
python main.py batch-ocr -i ./scanned_docs -o ./searchable_docs --layout-mode text_only
```

#### PDF Optimization
```bash
# Standard optimization
python main.py optimize -i large.pdf -o optimized.pdf --type standard

# Aggressive compression
python main.py optimize -i huge.pdf -o compressed.pdf --type aggressive --quality 60

# Optimize scanned documents
python main.py optimize -i scan.pdf -o optimized.pdf --type scanned --dpi 150

# High-quality optimization
python main.py optimize -i important.pdf -o optimized.pdf --type high_quality

# Batch optimization
python main.py batch-optimize -i ./large_files -o ./optimized --type aggressive --max-size 50
```

#### PDF Merging *(NEW!)*
```bash
# Merge all PDFs in folder with page numbers
python main.py merge -i ./contracts -o merged_contracts.pdf --page-numbers

# Merge specific files in custom order
python main.py merge -i "intro.pdf,chapter1.pdf,chapter2.pdf" -o book.pdf --preserve-signatures

# Merge folder without page numbers
python main.py merge-folder -i ./documents -o combined.pdf --no-page-numbers

# Advanced interactive merging
python main.py advanced-merge -i ./legal_docs -o final_contract.pdf
```

#### Analysis and Planning
```bash
# Analyze PDF for OCR needs
python main.py analyze -i document.pdf --type ocr

# Analyze folder for merge planning
python main.py analyze -i ./documents --type merge

# Optimization analysis
python main.py analyze -i large.pdf --type optimization
```

### Programmatic API

```python
from docforge import DocumentProcessor

# Initialize the processor
processor = DocumentProcessor(verbose=True)

# OCR processing with precise layout
result = processor.ocr_pdf(
    "scanned_document.pdf",
    "searchable_document.pdf",
    language='eng',
    layout_mode='precise',
    dpi=300
)

# PDF optimization with custom settings
result = processor.optimize_pdf(
    "large_document.pdf",
    "optimized_document.pdf",
    optimization_type="aggressive",
    target_dpi=150,
    jpeg_quality=60
)

# PDF merging with page numbers
result = processor.merge_pdfs(
    ["file1.pdf", "file2.pdf", "file3.pdf"],
    "merged_document.pdf",
    add_page_numbers=True,
    preserve_signatures=True,
    font_size=12
)

# Batch processing
result = processor.batch_optimize_pdfs(
    "input_folder/",
    "output_folder/",
    optimization_type="scanned",
    max_file_size_mb=100
)
```

## 🎯 Optimization Types

| Type | Best For | Compression | Quality | Speed |
|------|----------|-------------|---------|-------|
| **Standard** | Mixed content PDFs | Moderate | Good | Fast |
| **Aggressive** | Maximum file size reduction | High | Moderate | Fast |
| **Scanned** | Scanned documents/books | High | Good | Medium |
| **Scale-only** | Oversized pages | Low | Excellent | Fast |
| **High-quality** | Important documents | Low | Excellent | Medium |
| **Custom** | Specific requirements | Variable | Variable | Variable |

## 🌐 OCR Language Support

DocForge supports 100+ languages through Tesseract:

```bash
# Common languages
eng (English), fra (French), deu (German), spa (Spanish), ita (Italian)
por (Portuguese), rus (Russian), chi_sim (Chinese Simplified), jpn (Japanese), kor (Korean)

# Multiple languages
python main.py ocr -i multilingual.pdf -o searchable.pdf --language "eng+fra+deu"
```

## 📄 PDF Merge Options

### Input Methods
- **Folder**: Merge all PDFs alphabetically
- **File list**: Custom order with comma separation
- **Interactive**: Choose files one by one

### Merge Modes
- **Standard**: Fast merging for most documents
- **Signature-preserving**: Maximum preservation for legal documents

### Customization
- **Page numbering**: Optional with custom font and position
- **File analysis**: Preview before merging
- **Batch operations**: Process multiple merge jobs

## 🛠️ Advanced Features

### Interactive Menus
DocForge provides comprehensive interactive menus:

1. **Simple OCR PDF** - Quick OCR processing
2. **Advanced OCR PDF** - All layout and quality options
3. **Simple PDF Optimization** - Standard/Aggressive choice
4. **Advanced PDF Optimization** - 6+ methods with custom settings
5. **Interactive PDF Optimization** - Guided optimization experience
6. **Simple PDF Merge** - Basic merging with page numbers
7. **Advanced PDF Merge** - All merge options and signature preservation
8. **Interactive PDF Merge** - Complete guided merge experience
9. **Batch OCR Processing** - Process multiple files
10. **Batch PDF Optimization** - Optimize entire folders
11. **Analyze PDF** - Document analysis and recommendations
12. **Exit**

### Analysis Tools
```python
# Analyze PDF for OCR potential
processor.analyze_pdf_for_ocr("document.pdf")

# Analyze folder for merge planning
processor.analyze_merge_candidates("./documents")

# Get optimization recommendations
# Automatic analysis based on file size and content
```

### Memory Management
- **Batch processing**: Handle large files without memory issues
- **Smart chunking**: Process documents in memory-efficient batches
- **Cleanup optimization**: Automatic garbage collection on Windows
- **Progress tracking**: Real-time feedback for long operations

## 📊 Performance Examples

### File Size Reductions
- **Standard PDFs**: 20-50% reduction
- **Scanned documents**: 60-90% reduction
- **Oversized pages**: 70-95% reduction
- **Image-heavy files**: 40-80% reduction

### Processing Speed
- **OCR**: ~2-5 pages/second (depending on content)
- **Optimization**: ~10-50 pages/second
- **Merging**: ~100+ pages/second

## 🗺️ Roadmap

### ✅ **Completed**
- ✅ Core PDF processing with proven implementations
- ✅ OCR with multiple layout modes and batch processing
- ✅ 6+ PDF optimization methods with custom settings
- ✅ PDF merging with signature preservation
- ✅ Comprehensive CLI interface with 12 interactive options
- ✅ Document analysis and recommendations
- ✅ Memory-efficient batch processing

### 🔄 **In Progress**
- 📄 Word document processing (Word ↔ PDF conversion)
- 📊 Excel and PowerPoint support
- 🎨 Modern GUI interface

### 🚀 **Planned**
- 🤖 AI-powered document analysis
- 🌐 Web interface for cloud processing
- 📱 Mobile app integration
- 🔌 Plugin system for custom processors
- 📈 Advanced analytics and reporting
- 🔗 Integration with cloud storage providers

## 🤝 Contributing

We welcome contributions! The modular architecture makes it easy to add new features:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Add your processor** to the appropriate folder
4. **Update the CLI interface** if needed
5. **Add tests and documentation**
6. **Submit a pull request**

### Development Setup
```bash
# Clone for development
git clone https://github.com/oscar2song/docforge.git
cd docforge

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Check examples
python examples/basic_usage.py
```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended for large batches
- **Storage**: 1GB free space for temporary files
- **OS**: Windows 10+, macOS 10.14+, or Linux

### Dependencies
- **PyMuPDF**: PDF processing and rendering
- **Tesseract**: OCR text recognition
- **Poppler**: PDF to image conversion
- **Pillow**: Image processing
- **ReportLab**: PDF generation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with proven implementations and enhanced with modern architecture
- Powered by PyMuPDF, Tesseract, and other excellent open source libraries
- Inspired by real-world document processing needs
- Community-driven development for maximum utility

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/oscar2song/docforge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/oscar2song/docforge/discussions)
- **Documentation**: Coming soon!

---

**Built by craftsmen, for craftsmen.** 🔨

⭐ **If DocForge helped you, please give it a star!** ⭐

*Transform your document processing workflow with DocForge - where precision meets power.*