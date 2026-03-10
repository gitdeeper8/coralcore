# 🪸 CORAL-CORE Test Suite

## 📋 Overview

This directory contains the test suite for the CORAL-CORE framework.

## 📁 Structure

```

tests/
├── init.py           # Test package initialization
├── conftest.py           # Pytest fixtures and configuration
├── README.md             # This file
├── data/                 # Test data files
│   └── sample_parameters.csv  # Sample parameter data
├── unit/                 # Unit tests
│   ├── parameters/       # Parameter module tests
│   │   └── test_calcification.py
│   ├── rhi/              # RHI module tests
│   │   ├── test_composite.py
│   │   └── test_alert.py
│   └── utils/            # Utilities tests
│       ├── test_chemistry.py
│       └── test_acoustics.py
├── integration/          # Integration tests
│   └── test_pipeline.py
└── field/                # Field data validation
└── test_field_data.py

```

## 🚀 Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=coralcore --cov-report=html
```

Run specific test file:

```bash
pytest tests/unit/parameters/test_calcification.py -v
```

Run tests by marker:

```bash
# Unit tests only
pytest tests/ -m unit

# Integration tests only
pytest tests/ -m integration

# Field validation tests only
pytest tests/ -m field

# Slow tests
pytest tests/ -m slow
```

Run with parallel execution:

```bash
pytest tests/ -n auto
```

📊 Test Coverage Goals

· Unit tests: >90% coverage
· Integration tests: Critical paths covered
· Field validation: All 14 reef systems validated

🔧 Adding New Tests

1. Create test file in appropriate directory
2. Use fixtures from conftest.py
3. Follow naming convention: test_*.py
4. Add appropriate markers
5. Update this README if adding new categories

📝 Test Data

Sample data is provided in data/sample_parameters.csv for testing.
For full field datasets, refer to the main data repository.

✅ Continuous Integration

Tests are automatically run on:

· Push to main/develop branches
· Pull requests
· Release tags

See .github/workflows/ci.yml for details.
