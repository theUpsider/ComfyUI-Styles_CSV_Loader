# ComfyUI Styles CSV Loader Extension

This is a Python extension/plugin for ComfyUI that loads style prompts from CSV files, primarily for migration from Automatic1111 Stable Diffusion WebUI.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Repository Structure
- **`styles_csv_loader.py`** - Main extension code containing the StylesCSVLoader class
- **`__init__.py`** - Module initialization that imports the main class
- **`pyproject.toml`** - Project metadata for Comfy Registry publishing
- **`README.md`** - User documentation
- **`run_tests.py`** - Test runner script using pytest framework
- **`tests/`** - Comprehensive test suite with fixtures and unit tests
- **`.github/workflows/publish.yml`** - Automated publishing to Comfy Registry

### Prerequisites and Dependencies
- This extension requires ComfyUI to be installed and running
- No additional Python packages need to be installed beyond ComfyUI's dependencies
- The extension depends on ComfyUI's `folder_paths` module for file path resolution
- Python 3.6+ is required (follows ComfyUI requirements)

### Development Workflow
- **No build process required** - This is a pure Python plugin that loads directly into ComfyUI
- **Automated testing framework** - Uses pytest with comprehensive test coverage
- **No linting configuration** - Follow Python PEP 8 standards manually
- Always validate Python syntax after making changes: `python3 -c "import ast; ast.parse(open('styles_csv_loader.py').read())"`
- Always validate init file syntax: `python3 -c "import ast; ast.parse(open('__init__.py').read())"`

### Testing and Validation
- **Run the test suite**: Use the automated testing framework for comprehensive validation:
  ```bash
  # Run all tests
  python run_tests.py
  
  # Run tests with coverage reporting
  python run_tests.py --coverage
  ```

- **Test Structure**: The test suite includes:
  - Unit tests for CSV parsing logic
  - Tests for various CSV formats (valid, invalid, complex)
  - Integration tests for ComfyUI node functionality
  - Test fixtures with sample CSV files

- **Syntax Validation**: Always run before committing changes:
  ```bash
  python3 -c "import ast; ast.parse(open('styles_csv_loader.py').read()); print('styles_csv_loader.py syntax valid')"
  python3 -c "import ast; ast.parse(open('__init__.py').read()); print('__init__.py syntax valid')"
  ```

### CSV File Format Requirements
- Must be named `styles.csv` and located in ComfyUI root directory (where `main.py` is)
- Format: `style_name,positive_prompt,negative_prompt`
- First row is header (ignored)
- Supports quoted fields with commas inside quotes
- Example valid CSV:
  ```csv
  style_name,positive_prompt,negative_prompt
  cinematic,cinematic lighting professional photography,low quality blurry
  vintage,"old photo sepia tone, vintage style",modern digital
  ```

## Common Tasks

### Making Code Changes
1. Edit `styles_csv_loader.py` for core functionality changes
2. Run syntax validation: `python3 -c "import ast; ast.parse(open('styles_csv_loader.py').read())"`
3. Run the test suite to validate changes: `python run_tests.py`
4. If changing module structure, also validate `__init__.py`

### Adding New Features
- All new functionality should be added to the `StylesCSVLoader` class
- Follow ComfyUI node conventions:
  - `INPUT_TYPES()` classmethod for defining inputs
  - `RETURN_TYPES` and `RETURN_NAMES` class attributes
  - `execute()` method for main functionality
  - `FUNCTION` attribute pointing to execute method
  - `CATEGORY` for node organization

### Debugging CSV Issues
- Run the test suite to identify issues: `python run_tests.py`
- Check test fixtures in `tests/fixtures/` for valid CSV examples
- Common issues:
  - Unescaped quotes in CSV fields
  - Wrong number of columns
  - File encoding problems (use UTF-8)

### Release Process
- Update version in `pyproject.toml`
- Commit changes to main branch
- GitHub workflow automatically publishes to Comfy Registry

## File Contents Reference

### Repository Root Structure
```
.
├── .git/
├── .github/
│   └── workflows/
│       └── publish.yml
├── .gitignore
├── LICENSE
├── README.md
├── __init__.py
├── pyproject.toml
├── run_tests.py
├── styles_csv_loader.py
└── tests/
    ├── __init__.py
    ├── fixtures/
    │   ├── complex_styles.csv
    │   ├── invalid_styles.csv
    │   └── valid_styles.csv
    └── test_styles_csv_loader.py
```

### Key Code Patterns
- CSV parsing regex: `,(?=(?:[^"]*"[^"]*")*[^"]*$)` - handles quoted fields with commas (matches literal double quotes)
- Error handling: Always return default error style on exceptions
- ComfyUI integration: Uses `folder_paths.base_path` for CSV location
- Node registration: `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`

### Common Error Messages
- "Error loading styles.csv, check the console" - Default fallback style
- "No styles.csv found" - File missing from ComfyUI root
- CSV parsing errors - Usually due to malformed CSV format

## Validation Checklist
Before committing any changes:
- [ ] Run Python syntax validation on all modified .py files
- [ ] Run the test suite: `python run_tests.py`
- [ ] Verify no new dependencies introduced
- [ ] Update version in pyproject.toml if needed
- [ ] Ensure all tests pass