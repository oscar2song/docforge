# DocForge API Documentation

## 🔧 Core Classes

### DocumentProcessor

The main class for all document processing operations.

```python
from docforge import DocumentProcessor

processor = DocumentProcessor(verbose=True)
```

#### Methods

##### `ocr_pdf(input_file, output_file, language='eng')`
Perform OCR on a PDF file with smart validation.

**Parameters:**
- `input_file` (str): Path to input PDF
- `output_file` (str): Path for output PDF  
- `language` (str): OCR language code (auto-corrected)

**Returns:**
- `ProcessingResult`: Structured result with success/error info

**Example:**
```python
result = processor.ocr_pdf("scan.pdf", "searchable.pdf", language="en")
if result.success:
    print(f"✅ Completed in {result.processing_time:.2f}s")
else:
    print(f"❌ Error: {result.error.message}")
```

## 🎨 Rich UI Classes

### DocForgeUI

Professional Rich CLI interface components.

```python
from docforge.cli.rich_interface import DocForgeUI

ui = DocForgeUI()
ui.print_success("Operation completed!")
ui.display_error_details(error)
```

## 🛡️ Error Handling

### Exception Classes

All errors inherit from `DocForgeException` with rich context:

```python
from docforge.core.exceptions import DocForgeException

try:
    # Process document
    pass
except DocForgeException as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.error_code}")
    for suggestion in e.suggestions:
        print(f"💡 {suggestion}")
```
```
