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
        - style_name: string
        - positive_prompt: string (comma-separated prompts, optionally in quotes)
        - negative_prompt: string (comma-separated prompts, optionally in quotes)

        Returns:
            dict: Dictionary of styles, where each key is style_name and value is [positive_prompt, negative_prompt]
        """
        styles = {"Error loading styles.csv, check the console": ["", ""]}

        if not os.path.exists(styles_path):
            print(f"""Error. No styles.csv found. Put your styles.csv in the root directory of ComfyUI. Then press "Refresh".
Your current root directory is: {folder_paths.base_path}
""")
            return styles

        try:
            with open(styles_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            styles = {}
            for i, line in enumerate(lines[1:], start=2):  # Skip header row
                try:
                    # Split using regex that respects quoted fields
                    parts = [x.replace('"', '').replace('\n', '') for x in re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)]
                    
                    if len(parts) != 3:
                        raise ValueError(f"Expected 3 columns, got {len(parts)}")

                    style_name, positive_prompt, negative_prompt = parts
                    styles[style_name] = [positive_prompt, negative_prompt]

                except Exception as e:
                    print(f"Error parsing line {i}: {line.strip()} -> {e}")

        except Exception as e:
            print(f"""Error loading styles.csv. Make sure it is in the root directory of ComfyUI. Then press "Refresh".
Your current root directory is: {folder_paths.base_path}
Error: {e}
""")

        return styles

    @classmethod
    def INPUT_TYPES(cls):
        cls.styles_csv = cls.load_styles_csv(os.path.join(folder_paths.base_path, "styles.csv"))
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
