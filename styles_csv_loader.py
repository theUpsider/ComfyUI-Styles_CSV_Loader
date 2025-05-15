import os
import re
import folder_paths

class StylesCSVLoader:
    """
    Loads csv file with styles. For migration purposes from automatic1111 webui.
    """

    @staticmethod
    def load_styles_csv(styles_path: str):
        """Loads csv file with styles. Each row has three columns:
        - style_name: string (labeled as "name" in the CSV)
        - positive_prompt: string (labeled as "prompt" in the CSV)
        - negative_prompt: string (may be empty or missing)
        Returns:
            dict: Dictionary of styles, where each key is style_name and value is [positive_prompt, negative_prompt]
        """
        error_styles = {
            "Error loading styles.csv, check the console": ["", ""]}

        if not os.path.exists(styles_path):
            print(f"""Error. No styles.csv found. Put your styles.csv in the root directory of ComfyUI. Then press "Refresh".
Your current root directory is: {folder_paths.base_path}
""")
            return error_styles

        try:
            styles = {}
            with open(styles_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row

                # Start counting from 2 (after header)
                for i, row in enumerate(reader, start=2):
                    try:
                        # Initialize variables to avoid "used before assigned" errors
                        style_name = ""
                        positive_prompt = ""
                        negative_prompt = ""

                        # Handle rows with fewer than 3 columns
                        if len(row) == 0:
                            # Skip empty rows
                            continue
                        elif len(row) == 1:
                            print(
                                f"Error parsing line {i}: {','.join(row)} -> Expected at least 2 columns, got {len(row)}")
                            continue
                        elif len(row) == 2:
                            # Missing negative prompt - treat as empty string
                            style_name, positive_prompt = row
                            # negative_prompt already initialized as empty string
                        elif len(row) >= 3:
                            # Normal case or extra columns (ignore extras)
                            style_name, positive_prompt, negative_prompt = row[0], row[1], row[2]

                        styles[style_name] = [positive_prompt, negative_prompt]
                    except Exception as e:
                        # Use a safe version of the row for error reporting
                        row_str = ','.join(row) if isinstance(
                            row, list) else str(row)
                        print(f"Error parsing line {i}: {row_str} -> {e}")

            return styles

        except Exception as e:
            print(f"""Error loading styles.csv. Make sure it is in the root directory of ComfyUI. Then press "Refresh".
Your current root directory is: {folder_paths.base_path}
Error: {e}
""")
            return error_styles

    @classmethod
    def INPUT_TYPES(cls):
        cls.styles_csv = cls.load_styles_csv(
            os.path.join(folder_paths.base_path, "styles.csv"))
        return {
            "required": {
                "styles": (list(cls.styles_csv.keys()),),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive prompt", "negative prompt")
    FUNCTION = "execute"
    CATEGORY = "loaders"

    def execute(self, styles):
        return (
            self.styles_csv[styles][0],
            self.styles_csv[styles][1]
        )


NODE_CLASS_MAPPINGS = {
    "Load Styles CSV": StylesCSVLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StylesCSVLoader": "Load Styles CSV Node"
}
