# 🔨 DocForge - Professional Document Processing Toolkit

[![Tests](https://img.shields.io/badge/tests-47%2F47%20passing-brightgreen.svg)](https://github.com/oscar2song/docforge)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/oscar2song/docforge/blob/main/LICENSE)
[![Rich CLI](https://img.shields.io/badge/CLI-Rich%20Interface-purple.svg)](https://github.com/Textualize/rich)
[![Type Hints](https://img.shields.io/badge/code-type%20safe-blue.svg)](https://github.com/oscar2song/docforge)

> **Forge perfect documents with precision, power, and professional-grade user experience.**

DocForge is a **professional document processing toolkit** that combines proven implementations with modern architecture and enterprise-grade user experience. Built for both developers and end-users, featuring an intuitive Rich CLI interface, intelligent error handling, and comprehensive validation.

## ✨ **Professional Features**

### 🎨 **Beautiful Rich CLI Interface**
- **Stunning visual design** with professional branding
- **Interactive progress bars** with real-time updates  
- **Color-coded status messages** and formatted tables
- **Professional error displays** with bordered panels

### 🛡️ **Enterprise-Grade Error Handling**
- **Intelligent error detection** with contextual information
- **Actionable suggestions** for every error type
- **Beautiful error panels** with Rich formatting
- **Graceful recovery** and user guidance

### 🧠 **Smart Input Validation**
- **Auto-parameter correction** (en→eng, french→fra)
- **File similarity detection** for typos
- **PDF content analysis** with metadata extraction
- **Proactive error prevention** with helpful warnings

### 🧪 **Comprehensive Testing**
- **47/47 tests passing** with full automation
- **Performance benchmarks** and quality assurance
- **Integration testing** across all components
- **Professional development workflow**

### 🎯 **Core Document Processing**
- 🔍 **Advanced OCR** with layout preservation options
- 🗜️ **Smart Optimization** with content-aware compression
- ⚙️ **Intelligent Batch Processing** with progress tracking
- 📄 **PDF to Word Conversion** with multiple methods
- ✂️ **Flexible PDF Splitting** by pages, size, or bookmarks
- 🔧 **Document Analysis** with detailed metadata

## 🚀 **Quick Start**

### Installation

```bash
# Clone the repository
git clone https://github.com/oscar2song/docforge.git
cd docforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies
# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# macOS
brew install tesseract poppler

# Windows: Download Tesseract from
# https://github.com/tesseract-ocr/tesseract
```

### Professional CLI Experience

```bash
# Launch with beautiful Rich interface
python main.py

# OCR with smart validation and progress tracking
python main.py ocr -i document.pdf -o searchable.pdf --language eng

# Batch processing with comprehensive progress display
python main.py batch-ocr -i input_folder/ -o output_folder/

# Smart optimization with content analysis
python main.py optimize -i large.pdf -o optimized.pdf --type aggressive

# PDF to Word conversion with method selection
python main.py pdf-to-word -i document.pdf -o document.docx --method ocr

# Flexible PDF splitting with validation
python main.py split-pdf -i document.pdf -o output/ --pages "1-10,20-30"
```

### Test the Rich Interface

```bash
# Test the beautiful error handling system
python main.py test-errors

# Test smart validation features  
python main.py test-validation

# Test the Rich CLI interface
python main.py test-rich
```

## 💻 **Programmatic API**

```python
from docforge import DocumentProcessor

# Initialize with verbose Rich output
processor = DocumentProcessor(verbose=True)

# OCR with smart validation
result = processor.ocr_pdf(
    "scanned_document.pdf",
    "searchable_document.pdf", 
    language='eng'
)

# Handle results with professional error management
if result.success:
    print(f"✅ OCR completed in {result.processing_time:.2f}s")
    print(f"📄 Output: {result.output_file}")
else:
    print(f"❌ Error: {result.error.message}")
    for suggestion in result.error.suggestions:
        print(f"💡 {suggestion}")
```

## 🏗️ **Professional Architecture**

```
docforge/
├── core/                  # Core processing engine
│   ├── processor.py       # Main document processor
│   ├── exceptions.py      # Comprehensive error handling
│   └── validators.py      # Smart input validation
├── cli/                   # Rich CLI interface
│   ├── rich_interface.py  # Beautiful UI components
│   └── interface.py       # Enhanced CLI logic
├── pdf/                   # PDF operations (proven implementations)
├── utils/                 # Shared utilities
└── tests/                 # Comprehensive test suite (47/47 passing)
    ├── test_exceptions.py    # Error handling tests
    ├── test_validators.py    # Validation system tests
    ├── test_rich_interface.py # Rich UI tests
    └── test_integration.py   # End-to-end tests
```

## 🧪 **Quality Assurance**

### Run the Professional Test Suite

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run all tests (47/47 passing)
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=docforge --cov-report=html -v

# Test specific components
pytest tests/test_rich_interface.py -v     # Test Rich UI
pytest tests/test_exceptions.py -v        # Test error handling
pytest tests/test_validators.py -v        # Test smart validation
```

### Performance Benchmarks

- ⚡ **Parameter validation**: < 1ms per check
- 🎨 **Rich UI rendering**: < 100ms initialization  
- 🧠 **Smart validation**: < 10ms with auto-correction
- 🔍 **File analysis**: < 2s per PDF with metadata

## 📚 **Enhanced Usage Examples**

### Smart Error Handling in Action

```bash
# Try an invalid language - see auto-correction
python main.py ocr -i document.pdf -o output.pdf --language en
# ✨ Auto-corrected language: 'en' → 'eng'

# Try a nonexistent file - see helpful suggestions  
python main.py ocr -i documnet.pdf -o output.pdf
# 📁 Similar files found: document.pdf, Document.pdf
```

### Batch Processing with Intelligence

```bash
# Batch process with comprehensive analysis
python main.py batch-ocr -i pdf_folder/ -o processed/
# 📊 Found 25 PDF files for processing
# ⏱️ Estimated processing time: 8.5 minutes  
# 💾 Total size: 157.3 MB
# 🎯 Success rate: 96% (24/25 files)
```

### Professional Validation

```bash
# Smart quality validation
python main.py optimize -i document.pdf -o output.pdf --quality 150
# ❌ Validation Error: Quality must be between 1-100
# 💡 Use 85 for good balance of quality and size
# 💡 Use 95+ for high quality, 60- for small file size
```

## 🎯 **Command Reference**

| Command | Description | Key Features |
|---------|-------------|--------------|
| `ocr` | OCR processing | Smart validation, layout modes, progress tracking |
| `optimize` | PDF optimization | Content-aware compression, size estimation |
| `pdf-to-word` | PDF to Word conversion | Multiple methods, format detection |
| `split-pdf` | PDF splitting | Flexible splitting, validation, preview |
| `batch-*` | Batch operations | Progress tracking, error recovery, statistics |
| `test-*` | Interface testing | Rich UI validation, error handling demos |

## 🌟 **What Makes DocForge Special**

### 🏢 **Enterprise-Grade Quality**
- **Professional user experience** rivaling commercial software
- **Intelligent error prevention** with contextual guidance  
- **Comprehensive testing** ensuring reliability (47/47 tests)
- **Type-safe codebase** with full annotation coverage

### 🎨 **User-Centered Design**
- **Beautiful Rich CLI** with progress bars and formatting
- **Smart auto-correction** prevents common user mistakes
- **Actionable error messages** that actually help users
- **Interactive confirmation** for destructive operations

### 🛡️ **Robust & Reliable**
- **Graceful error handling** with recovery suggestions
- **Input validation** preventing bad operations
- **Memory-efficient** batch processing for large datasets
- **Cross-platform** compatibility (Windows, macOS, Linux)

## 🤝 **Contributing**

We welcome contributions! The modular architecture makes it easy to add features:

```bash
# Set up development environment
git clone https://github.com/oscar2song/docforge.git
cd docforge
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt

# Run the test suite
pytest tests/ -v

# Test your changes
python main.py test-validation
```

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch  
3. **Add tests** for new functionality
4. **Ensure** all 47 tests pass
5. **Submit** a pull request

## 📈 **Roadmap**

### ✅ **Completed (v1.0)**
- ✅ Professional Rich CLI interface
- ✅ Enterprise-grade error handling
- ✅ Smart input validation and auto-correction  
- ✅ Comprehensive testing suite (47/47 tests)
- ✅ Type-safe codebase

### 🚀 **Coming Soon (v1.1)**
- 📄 Enhanced Word document processing
- 🎨 Optional GUI interface
- 📊 Excel and PowerPoint support
- 🤖 AI-powered document analysis
- 🌐 Web interface option

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

Built with modern architecture and professional development practices:
- **Rich** for beautiful CLI interfaces
- **pytest** for comprehensive testing
- **Type hints** for code safety
- **Modular design** for maintainability

---

<div align="center">

**⭐ If DocForge helped you, please give it a star! ⭐**

*Built by craftsmen, for craftsmen.* 🔨

[Report Bug](https://github.com/oscar2song/docforge/issues) · [Request Feature](https://github.com/oscar2song/docforge/issues) · [Documentation](https://github.com/oscar2song/docforge/wiki)

</div>
