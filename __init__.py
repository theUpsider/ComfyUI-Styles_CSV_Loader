import sys
import os

# Add current directory to sys.path to ensure we can import styles_csv_loader
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from styles_csv_loader import StylesCSVLoader