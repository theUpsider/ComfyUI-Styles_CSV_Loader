import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the folder_paths module before importing styles_csv_loader
sys.modules['folder_paths'] = MagicMock()

from styles_csv_loader import StylesCSVLoader


class TestStylesCSVLoader(unittest.TestCase):
    """Test cases for StylesCSVLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.fixtures_dir = os.path.join(self.test_dir, 'fixtures')
        self.valid_csv_path = os.path.join(self.fixtures_dir, 'valid_styles.csv')
        self.invalid_csv_path = os.path.join(self.fixtures_dir, 'invalid_styles.csv')
        self.complex_csv_path = os.path.join(self.fixtures_dir, 'complex_styles.csv')
        self.nonexistent_csv_path = os.path.join(self.fixtures_dir, 'nonexistent.csv')
    
    def test_load_valid_csv(self):
        """Test loading a valid CSV file."""
        styles = StylesCSVLoader.load_styles_csv(self.valid_csv_path)
        
        # Check that styles were loaded
        self.assertIsInstance(styles, dict)
        self.assertGreater(len(styles), 0)
        
        # Check specific style exists
        self.assertIn('Cinematic', styles)
        
        # Check structure of a style
        cinematic_style = styles['Cinematic']
        self.assertIsInstance(cinematic_style, list)
        self.assertEqual(len(cinematic_style), 2)  # positive and negative prompt
        
        # Check content
        self.assertEqual(cinematic_style[0], 'cinematic shot, dramatic lighting, film grain')
        self.assertEqual(cinematic_style[1], 'low quality, blurry, amateur')
    
    def test_load_invalid_csv(self):
        """Test loading an invalid CSV file (missing columns). Should return an error dictionary."""
        styles = StylesCSVLoader.load_styles_csv(self.invalid_csv_path)
        
        # The correct behavior: should return a dict with an error message
        self.assertIsInstance(styles, dict)
        error_key = list(styles.keys())[0]
        self.assertIn('Error loading styles.csv', error_key)
        # Style values should always be lists with positive and negative prompts
        self.assertIsInstance(styles[error_key], list)
        self.assertEqual(len(styles[error_key]), 2)

    def test_load_invalid_csv_buggy_behavior(self):
        """[BUG DOCUMENTATION] Current buggy behavior: returns a list instead of error dict for invalid CSV.
        Remove this test once the bug in styles_csv_loader.py is fixed."""
        styles = StylesCSVLoader.load_styles_csv(self.invalid_csv_path)
        # This documents the buggy behavior for regression tracking.
        if isinstance(styles, list):
            self.assertGreater(len(styles), 0)
            self.assertIn('Missing Column', styles[0])
        else:
            # If bug is fixed, this test should be removed.
            self.skipTest("Bug fixed: loader returns error dict instead of list.")
    def test_load_nonexistent_csv(self):
        """Test loading a nonexistent CSV file."""
        styles = StylesCSVLoader.load_styles_csv(self.nonexistent_csv_path)
        
        # Should return error message in styles
        self.assertIsInstance(styles, dict)
        error_key = list(styles.keys())[0]
        self.assertIn('Error loading styles.csv', error_key)
    
    def test_load_complex_csv(self):
        """Test loading a CSV with complex content (quotes, special chars)."""
        styles = StylesCSVLoader.load_styles_csv(self.complex_csv_path)
        
        # Check that styles were loaded
        self.assertIsInstance(styles, dict)
        self.assertGreater(len(styles), 0)
        
        # Check complex quotes handling
        self.assertIn('Complex Quotes', styles)
        complex_style = styles['Complex Quotes']
        self.assertIn('double quotes', complex_style[0])
        
        # Check special characters
        self.assertIn('Special Characters', styles)
        special_style = styles['Special Characters']
        self.assertIn('ñáéíóú', special_style[0])
        
        # Check empty negative prompt
        self.assertIn('Empty Negative', styles)
        empty_neg_style = styles['Empty Negative']
        self.assertEqual(empty_neg_style[1], '')
    
    def test_all_styles_have_correct_structure(self):
        """Test that all loaded styles have the correct structure."""
        styles = StylesCSVLoader.load_styles_csv(self.valid_csv_path)
        
        for style_name, style_data in styles.items():
            # Each style should be a list with exactly 2 elements
            self.assertIsInstance(style_data, list, f"Style '{style_name}' should be a list")
            self.assertEqual(len(style_data), 2, f"Style '{style_name}' should have exactly 2 elements")
            
            # Both elements should be strings
            self.assertIsInstance(style_data[0], str, f"Positive prompt for '{style_name}' should be a string")
            self.assertIsInstance(style_data[1], str, f"Negative prompt for '{style_name}' should be a string")
    
    @patch('styles_csv_loader.folder_paths')
    def test_input_types_with_valid_csv(self, mock_folder_paths):
        """Test INPUT_TYPES method with valid CSV."""
        mock_folder_paths.base_path = self.fixtures_dir
        
        # Create a temporary styles.csv in the fixtures directory
        temp_csv_path = os.path.join(self.fixtures_dir, 'styles.csv')
        with open(temp_csv_path, 'w', encoding='utf-8') as f:
            f.write('name,prompt,negative_prompt\n')
            f.write('"Test Style","test prompt","test negative"\n')
        
        try:
            input_types = StylesCSVLoader.INPUT_TYPES()
            
            # Check structure
            self.assertIn('required', input_types)
            self.assertIn('styles', input_types['required'])
            
            # Check that styles list contains our test style
            styles_list = input_types['required']['styles'][0]
            self.assertIn('Test Style', styles_list)
        
        finally:
            # Clean up
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
    
    def test_execute_method(self):
        """Test the execute method returns correct prompts."""
        loader = StylesCSVLoader()
        
        # Mock the styles_csv attribute
        loader.styles_csv = {
            'Test Style': ['positive prompt here', 'negative prompt here']
        }
        
        positive, negative = loader.execute('Test Style')
        
        self.assertEqual(positive, 'positive prompt here')
        self.assertEqual(negative, 'negative prompt here')


if __name__ == '__main__':
    unittest.main()