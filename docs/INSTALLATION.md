# DocForge Installation Guide

## 📋 Prerequisites

### Python Requirements
- Python 3.8 or higher
- pip package manager
- Virtual environment support

### System Dependencies

#### Windows
1. Download Tesseract from [GitHub Releases](https://github.com/tesseract-ocr/tesseract)
2. Install to `C:\Program Files\Tesseract-OCR\`
3. Add to PATH environment variable

#### macOS
```bash
brew install tesseract poppler
Ubuntu/Debian
bashsudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
🚀 Installation Steps
1. Clone Repository
bashgit clone https://github.com/oscar2song/docforge.git
cd docforge
2. Create Virtual Environment
bashpython -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install Dependencies
bashpip install -r requirements.txt
4. Verify Installation
bashpython main.py test-rich
🔧 Troubleshooting
Common Issues
"Tesseract not found"

Ensure Tesseract is in PATH
Restart terminal after installation

"Rich interface not available"

Run: pip install rich
Verify: python -c "import rich; print('Rich OK')"

"Tests failing"

Install test dependencies: pip install -r requirements-test.txt
Run: pytest tests/ -v
