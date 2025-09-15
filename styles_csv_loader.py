import os
import re
import folder_paths


class StylesCSVLoader:
    """
    Loads csv file with styles. For migration purposes from automatic11111 webui.
    """

    @staticmethod
    def load_styles_csv(styles_path: str):
        """Loads csv file with styles. It has only one column.
        Ignore the first row (header).
        positive_prompt are strings separated by comma. Each string is a prompt.
        negative_prompt are strings separated by comma. Each string is a prompt.

        Returns:
            list: List of styles. Each style is a dict with keys: style_name and value: [positive_prompt, negative_prompt]
        """
        styles = {"Error loading styles.csv, check the console": ["", ""]}
        if not os.path.exists(styles_path):
            # Normalize path for cross-platform display
            normalized_base_path = os.path.normpath(folder_paths.base_path)
            print(f"""Error. No styles.csv found. Put your styles.csv in the root directory of ComfyUI. Then press "Refresh".
                  Your current root directory is: {normalized_base_path}
            """)
            return styles
        try:
            with open(styles_path, "r", encoding="utf-8") as f:
                styles = [[x.replace('"', '').replace('\n', '') for x in re.split(
                    ',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)] for line in f.readlines()[1:]]
                styles = {x[0]: [x[1], x[2]] for x in styles}
        except Exception as e:
            # Normalize path for cross-platform display
            normalized_base_path = os.path.normpath(folder_paths.base_path)
            print(f"""Error loading styles.csv. Make sure it is in the root directory of ComfyUI. Then press "Refresh".
                    Your current root directory is: {normalized_base_path}
                    Error: {e}
            """)
        return styles

    @classmethod
    def INPUT_TYPES(cls):
        # Use os.path.normpath to ensure cross-platform compatibility
        styles_path = os.path.normpath(os.path.join(folder_paths.base_path, "styles.csv"))
        cls.styles_csv = cls.load_styles_csv(styles_path)
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
        return (self.styles_csv[styles][0], self.styles_csv[styles][1])


NODE_CLASS_MAPPINGS = {
    "Load Styles CSV": StylesCSVLoader
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "StylesCSVLoader": "Load Styles CSV Node"
}
