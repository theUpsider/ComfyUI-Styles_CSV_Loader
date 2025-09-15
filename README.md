[![Publish to Comfy registry](https://github.com/theUpsider/ComfyUI-Styles_CSV_Loader/actions/workflows/publish.yml/badge.svg)](https://github.com/theUpsider/ComfyUI-Styles_CSV_Loader/actions/workflows/publish.yml)
[![Tests](https://github.com/theUpsider/ComfyUI-Styles_CSV_Loader/actions/workflows/test.yml/badge.svg)](https://github.com/theUpsider/ComfyUI-Styles_CSV_Loader/actions/workflows/test.yml)
# Styles CSV Loader Extension for ComfyUI
Extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that loads styles from a CSV file.

## Description
This extension allows users to load styles from a CSV file (styles.csv), primarily for migration purposes from the [automatic1111 Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui). 

## Installation
- Clone this repository into the `custom_nodes` folder of ComfyUI. Restart ComfyUI and the extension should be loaded.
- OR: Use the [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager) to install this extension.

**Important**: The `styles.csv` file must be located in the root of `ComfyUI` where `main.py` resides.

## Nodes Description
Each style is represented as a dictionary with the keys being `style_name` and the values being a list containing `positive_prompt` and `negative_prompt`. The prompts are outputs of this Node.

### Custom CSV Files
The extension now supports loading styles from custom CSV files in addition to the default `styles.csv`. You can specify a custom CSV file path using the optional `csv_file_path` parameter:

- **Relative paths**: Relative to the ComfyUI root directory (e.g., `"my_styles/portrait_styles.csv"`)
- **Absolute paths**: Full file system paths (e.g., `"/path/to/my/custom_styles.csv"`)
- **Default behavior**: When no custom path is specified, it uses `styles.csv` from the ComfyUI root directory

If a selected style is not found in the custom CSV file, the node will fall back to the default styles loaded from `styles.csv`.

## CSV Format
The CSV file should have the following format:
```csv
name,prompt,negative_prompt
"Style Name","positive prompt text","negative prompt text"
"Another Style","more positive text","more negative text"
```

### Examples
You can organize your styles in multiple CSV files for different purposes:

**portraits.csv**:
```csv
name,prompt,negative_prompt
"Professional Portrait","portrait photography, professional lighting, sharp focus","ugly, deformed, extra limbs"
"Vintage Portrait","vintage portrait, sepia tone, classical","modern, digital, colorful"
```

**landscapes.csv**:
```csv
name,prompt,negative_prompt
"Golden Hour","landscape photography, golden hour, wide angle","people, buildings, urban"
"Mountain Vista","mountain landscape, dramatic clouds, epic view","flat, boring, low quality"
```

## Development

### Setting up the development environment
1. Clone the repository
2. Install test dependencies:
   ```bash
   pip install pytest pytest-cov
   ```

### Running tests
Run all tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Test Structure
- `tests/test_styles_csv_loader.py` - Main test file for the StylesCSVLoader class
- `tests/fixtures/` - Example CSV files for testing:
  - `valid_styles.csv` - Properly formatted CSV with valid styles
  - `invalid_styles.csv` - CSV with missing columns to test error handling
  - `complex_styles.csv` - CSV with complex content (quotes, special characters)

### Continuous Integration
The project uses GitHub Actions for CI/CD. Tests are automatically run on:
- Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Every push to main branch
- Every pull request

### Code Coverage
The project maintains 100% test coverage. Coverage reports are generated during CI runs.

## Author
- David Fischer
- GitHub: [theUpsider](https://github.com/theUpsider)
- Support me on [BuyMeACoffee](https://www.buymeacoffee.com/theupsider)
