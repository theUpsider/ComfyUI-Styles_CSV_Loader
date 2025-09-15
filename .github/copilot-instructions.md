# ComfyUI Styles CSV Loader Extension

This is a Python extension/plugin for ComfyUI that loads style prompts from CSV files, primarily for migration from Automatic1111 Stable Diffusion WebUI.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Repository Structure
- **`styles_csv_loader.py`** - Main extension code containing the StylesCSVLoader class
- **`__init__.py`** - Module initialization that imports the main class
- **`pyproject.toml`** - Project metadata for Comfy Registry publishing
- **`README.md`** - User documentation
- **`.github/workflows/publish.yml`** - Automated publishing to Comfy Registry

### Prerequisites and Dependencies
- This extension requires ComfyUI to be installed and running
- No additional Python packages need to be installed beyond ComfyUI's dependencies
- The extension depends on ComfyUI's `folder_paths` module for file path resolution
- Python 3.6+ is required (follows ComfyUI requirements)

### Development Workflow
- **No build process required** - This is a pure Python plugin that loads directly into ComfyUI
- **No automated tests exist** - Validation is done through manual testing and syntax checking
- **No linting configuration** - Follow Python PEP 8 standards manually
- Always validate Python syntax after making changes: `python3 -c "import ast; ast.parse(open('styles_csv_loader.py').read())"`
- Always validate init file syntax: `python3 -c "import ast; ast.parse(open('__init__.py').read())"`

### Testing and Validation
- **CSV Parsing Testing**: Create test CSV files and validate parsing logic standalone:
  ```bash
  # Create test CSV in /tmp
  echo 'style_name,positive_prompt,negative_prompt
  cinematic,cinematic lighting professional photography,low quality blurry
  vintage,"old photo sepia tone, vintage style",modern digital' > /tmp/test_styles.csv
  
  # Test parsing logic (takes <5 seconds)
  python3 -c "
  import os, re
  def load_styles_csv(path):
      with open(path, 'r', encoding='utf-8') as f:
          styles = [[x.replace('\"', '').replace('\n', '') for x in re.split(',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)', line)] for line in f.readlines()[1:]]
          return {x[0]: [x[1], x[2]] for x in styles}
  result = load_styles_csv('/tmp/test_styles.csv')
  print(f'Loaded {len(result)} styles successfully')
  "
  ```

- **Syntax Validation**: Always run before committing changes:
  ```bash
  python3 -c "import ast; ast.parse(open('styles_csv_loader.py').read()); print('styles_csv_loader.py syntax valid')"
  python3 -c "import ast; ast.parse(open('__init__.py').read()); print('__init__.py syntax valid')"
  ```

- **Full Integration Testing**: Requires ComfyUI environment:
  1. Install ComfyUI
  2. Copy this extension to `ComfyUI/custom_nodes/ComfyUI-Styles_CSV_Loader/`
  3. Create a test `styles.csv` in ComfyUI root directory
  4. Restart ComfyUI
  5. Verify "Load Styles CSV" node appears in loaders category
  6. Test loading different styles and verify positive/negative prompts output correctly

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
3. Test CSV parsing with sample data (see Testing section above)
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
- Check that `styles.csv` exists in ComfyUI root directory
- Validate CSV format with test parsing script
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
└── styles_csv_loader.py
```

### Key Code Patterns
- CSV parsing regex: `,(?=(?:[^"]*"[^"]*")*[^"]*$)` - handles quoted fields with commas
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
- [ ] Test CSV parsing with sample data
- [ ] Verify no new dependencies introduced
- [ ] Update version in pyproject.toml if needed
- [ ] Test in actual ComfyUI environment if possible