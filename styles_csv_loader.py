import re

class StylesCSVLoader:
    """
    Loads csv file with styles. For migration purposes from automatic11111 webui.
    """
    def __init__(self):
        if not hasattr(self, "styles_csv"):
            self.styles_csv = self.load_styles_csv("styles.csv")
    
    def load_styles_csv(styles_path):
        """Loads csv file with styles. It has only one column.
        Ignore the first row (header).
        positive_prompt are strings separated by comma. Each string is a prompt.
        negative_prompt are strings separated by comma. Each string is a prompt.

        Returns:
            list: List of styles. Each style is a dict with keys: style_name and value: [positive_prompt, negative_prompt]
        """
        
        with open(styles_path, "r", encoding="utf-8") as f:    
            styles = [[x.replace('"', '').replace('\n','') for x in re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)] for line in f.readlines()[1:]]
            styles = {x[0]: [x[1],x[2]] for x in styles}
        return styles
        
    @classmethod
    def INPUT_TYPES(s):
        if not hasattr(s, "styles_csv"):
            s.styles_csv = s.load_styles_csv("styles.csv")
        return {
            "required": {
                "styles": (list(s.styles_csv.keys()),),
            },
                                
        }
    
    RETURN_TYPES = ("STRING","STRING")
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
