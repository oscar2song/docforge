# 🔨 DocForge - Document Processing Toolkit

*Forge perfect documents from any format with precision, power, and simplicity.*

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/oscar2song/docforge?style=social)](https://github.com/oscar2song/docforge)

## 🚀 What is DocForge?

DocForge is a comprehensive document processing toolkit built on **proven implementations** with a **modern modular architecture**. Born from real-world needs and battle-tested algorithms, DocForge transforms how you work with documents.

### ⚡ **Core Capabilities**

- **🔍 OCR Processing**: Convert scanned PDFs to searchable documents with precision
- **🗜️ Smart Optimization**: Reduce file sizes without compromising quality  
- **⚙️ Batch Processing**: Handle hundreds of documents efficiently
- **🔧 Document Analysis**: Extract insights and metadata
- **🎯 Modular Design**: Use only what you need, extend easily

## 🎯 **Why DocForge?**

### **Built on Proven Implementations**
- Battle-tested OCR algorithms with Windows compatibility
- Advanced optimization techniques from real-world usage
- Memory-efficient batch processing for large-scale operations

### **Developer-Friendly Architecture**
- Clean, modular codebase that's easy to understand and extend
- Comprehensive error handling and logging
- Both programmatic API and command-line interface

## 🚀 **Quick Start**

### Installation

```bash
git clone https://github.com/oscar2song/docforge.git
cd docforge
pip install -r requirements.txt
```

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# macOS  
brew install tesseract poppler

# Windows: Download Tesseract from
# https://github.com/tesseract-ocr/tesseract
```

### Basic Usage

```python
from docforge import DocumentProcessor

# Initialize the processor
processor = DocumentProcessor(verbose=True)

# OCR a scanned PDF
result = processor.ocr_pdf(
    "scanned_document.pdf",
    "searchable_document.pdf", 
    language='eng'
)

# Optimize PDF size
result = processor.optimize_pdf(
    "large_document.pdf",
    "optimized_document.pdf",
    optimization_type="aggressive"
)

# Batch processing
result = processor.batch_ocr_pdfs(
    "scanned_folder/",
    "searchable_folder/"
)
```

### Command Line Interface

```bash
# Interactive mode
python main.py

# OCR processing
python main.py ocr -i scanned.pdf -o searchable.pdf --language eng

# Batch optimization
python main.py batch-optimize -i input_folder/ -o output_folder/ --type aggressive
```

## 🏗️ **Architecture**

DocForge is built with a clean, modular architecture:

```
docforge/
├── core/           # Core processing engine
├── pdf/            # PDF operations (proven implementations)
├── cli/            # Command-line interface  
└── utils/          # Shared utilities
```

## 🛠️ **Development**

### Running Examples
```bash
python examples/basic_usage.py
```

### Contributing
We welcome contributions! The modular architecture makes it easy to add new features.

## 🗺️ **Roadmap**

### **Version 1.0** (Current)
- ✅ Core PDF processing with proven implementations
- ✅ OCR and optimization capabilities
- ✅ Command-line interface
- ✅ Comprehensive documentation

### **Version 2.0** (Coming Soon)
- 📄 Word document processing (Word ↔ PDF conversion)
- 🎨 Modern GUI interface
- 🚀 Performance optimizations

### **Version 3.0** (Future)
- 📊 Excel and PowerPoint support
- 🤖 AI-powered document analysis
- 🌐 Web interface

## 📄 **License**

This project is licensed under the MIT License.

## 🙏 **Acknowledgments**

Built with proven implementations and enhanced with modern architecture for the open source community.

---

⭐ **If DocForge helped you, please give it a star!** ⭐

*Built by craftsmen, for craftsmen.* 🔨