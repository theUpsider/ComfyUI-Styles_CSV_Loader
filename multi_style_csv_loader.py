import csv
import os
from pathlib import Path
from comfyui import nodes as comfy_nodes  # Adjust if necessary

class MultiStyleCSVLoaderEditable:
    @classmethod
    def INPUT_TYPES(cls):
        style_dir = os.path.join(Path(__file__).parent, "styles")
        os.makedirs(style_dir, exist_ok=True)

        csv_files = [f for f in os.listdir(style_dir) if f.endswith(".csv")]

        return {
            "required": {
                "style_file": (sorted(csv_files),),
                "style_keys": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "Comma-separated keys (e.g. style1, style2)"
                }),
                "manual_edit": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "manual_positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "visible_if": lambda inputs: inputs.get("manual_edit", False)
                }),
                "manual_negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "visible_if": lambda inputs: inputs.get("manual_edit", False)
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "load_styles"
    CATEGORY = "Upsider/Styles"

    def load_styles(self, style_file, style_keys="", manual_edit=False,
                    manual_positive=None, manual_negative=None):
        style_path = os.path.join(Path(__file__).parent, "styles", style_file)
        if not os.path.exists(style_path):
            return ("", "")

        selected_keys = [k.strip() for k in style_keys.split(",") if k.strip()]
        positive_prompt = []
        negative_prompt = []

        with open(style_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                key = row.get("key", "")
                if key in selected_keys:
                    positive_prompt.append(row.get("positive", ""))
                    negative_prompt.append(row.get("negative", ""))

        # Generate final strings
        auto_positive = " ".join(positive_prompt)
        auto_negative = " ".join(negative_prompt)

        if manual_edit:
            # Use manual override if provided
            final_positive = manual_positive or auto_positive
            final_negative = manual_negative or auto_negative
        else:
            final_positive = auto_positive
            final_negative = auto_negative

        return (final_positive, final_negative)


NODE_CLASS_MAPPINGS = {
    "MultiStyleCSVLoaderEditable": MultiStyleCSVLoaderEditable
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiStyleCSVLoaderEditable": "Multi-Style CSV Loader (Editable)"
}
