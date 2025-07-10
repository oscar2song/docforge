# DocForge 🔨

> Forge perfect documents from any format with precision, power, and simplicity.

DocForge is a comprehensive document processing toolkit built on proven implementations with a modern modular architecture. Born from real-world needs and battle-tested algorithms, DocForge transforms how you work with documents.

## ✨ Features

- 🔍 **OCR Processing**: Convert scanned PDFs to searchable documents with precision
- 📄 **PDF to Word**: Convert PDF documents to Word format (.docx) seamlessly
- ✂️ **PDF Splitting**: Split large PDFs into smaller files or extract specific pages
- 🗜️ **Smart Optimization**: Reduce file sizes without compromising quality
- ⚙️ **Batch Processing**: Handle hundreds of documents efficiently
- 🔧 **Document Analysis**: Extract insights and metadata
- 🎯 **Modular Design**: Use only what you need, extend easily

## 🚀 Why DocForge?

- Battle-tested OCR algorithms with Windows compatibility
- Advanced optimization techniques from real-world usage
- Memory-efficient batch processing for large-scale operations
- Clean, modular codebase that's easy to understand and extend
- Comprehensive error handling and logging
- Both programmatic API and command-line interface

## 📦 Installation

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

## 🔥 Quick Start

### Programmatic Usage

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

# Convert PDF to Word
result = processor.pdf_to_word(
    "document.pdf",
    "document.docx"
)

# Split PDF into multiple files
result = processor.split_pdf(
    "large_document.pdf",
    "output_folder/",
    pages_per_split=10
)

# Extract specific pages
result = processor.extract_pdf_pages(
    "source.pdf",
    "pages_1_to_5.pdf",
    start_page=1,
    end_page=5
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

### Command Line Usage

```bash
# Interactive mode
python main.py

# OCR processing
python main.py ocr -i scanned.pdf -o searchable.pdf --language eng

# PDF to Word conversion
python main.py pdf-to-word -i document.pdf -o document.docx

# Split PDF
python main.py split-pdf -i large.pdf -o output_folder/ --pages-per-split 5

# Extract specific pages
python main.py extract-pages -i source.pdf -o extracted.pdf --start 1 --end 10

# Batch optimization
python main.py batch-optimize -i input_folder/ -o output_folder/ --type aggressive
```

## 🏗️ Architecture

DocForge is built with a clean, modular architecture:

```
docforge/
├── core/          # Core processing engine
├── pdf/           # PDF operations (proven implementations)
│   ├── ocr.py              # OCR processing and text extraction
│   ├── optimizer.py        # PDF optimization and compression
│   ├── pdf_merger.py       # PDF merging and combining
│   ├── pdf_splitter.py     # PDF splitting and page extraction
│   └── pdf_to_word.py      # PDF to Word conversion
├── cli/           # Command-line interface
└── utils/         # Shared utilities
```

## 📚 Examples

```python
# Run the examples
python examples/basic_usage.py
```

## 🤝 Contributing

We welcome contributions! The modular architecture makes it easy to add new features.

## 🗺️ Roadmap

- ✅ Core PDF processing with proven implementations
- ✅ OCR and optimization capabilities
- ✅ PDF splitting and page extraction
- ✅ PDF to Word conversion
- ✅ Command-line interface
- ✅ Comprehensive documentation
- 🎨 Modern GUI interface
- 🚀 Performance optimizations
- 📊 Excel and PowerPoint support
- 📄 Word to PDF conversion
- 🤖 AI-powered document analysis
- 🌐 Web interface

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with proven implementations and enhanced with modern architecture for the open source community.

---

⭐ **If DocForge helped you, please give it a star!** ⭐

*Built by craftsmen, for craftsmen.* 🔨