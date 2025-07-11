# DocForge Testing Guide

## 🧪 Test Suite Overview

DocForge includes comprehensive testing with **47/47 tests passing**:

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end functionality  
- **Performance Tests**: Speed and efficiency
- **Rich UI Tests**: Interface component validation

## 🚀 Running Tests

### All Tests
```bash
pytest tests/ -v
```

### Specific Test Categories
```bash
pytest tests/test_exceptions.py -v      # Error handling
pytest tests/test_validators.py -v      # Smart validation
pytest tests/test_rich_interface.py -v  # Rich UI components
pytest tests/test_integration.py -v     # End-to-end tests
```

### Coverage Report
```bash
pytest tests/ --cov=docforge --cov-report=html -v
```

## 📊 Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_exceptions.py       # Error handling tests
├── test_validators.py       # Validation system tests  
├── test_rich_interface.py   # Rich UI tests
├── test_cli_interface.py    # CLI logic tests
├── test_integration.py      # End-to-end tests
└── test_performance.py     # Performance benchmarks
```

## ✅ Test Requirements

For contributions, ensure:
- All 47 tests pass
- New features include tests
- Coverage remains high
- Performance benchmarks met
```
