# Styles CSV Loader Extension for ComfyUI
Extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that loads styles from a CSV file.
## Description
This extension allows users to load styles from a CSV file, primarily for migration purposes from the [automatic1111 Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui). 

## Installation
Clone this repository into the `custom_nodes` folder of ComfyUI. Restart ComfyUI and the extension should be loaded.

**Important**: The `styles.csv` file must be located in the root of `ComfyUI` where `main.py` resides.
## Nodes Description
Each style is represented as a dictionary with the keys being `style_name` and the values being a list containing `positive_prompt` and `negative_prompt`. The prompts are outputs of this Node.

## Author
- David Fischer
- GitHub: [theUpsider](https://github.com/theUpsider)
- Support me on [BuyMeACoffee](https://www.buymeacoffee.com/theupsider)