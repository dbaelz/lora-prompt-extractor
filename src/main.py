import os
import json
from PIL import Image

from cli import parse_args

def extract_positive_prompt_from_prompt_json(prompt_json):
    try:
        data = json.loads(prompt_json)
    except Exception:
        return None
    # Find the node with 'positive' in its inputs
    for node in data.values():
        if "positive" in node.get("inputs", {}):
            pos_ref = node["inputs"]["positive"][0]
            pos_node = data.get(pos_ref)
            if pos_node and "text" in pos_node.get("inputs", {}):
                return pos_node["inputs"]["text"]
    return None

if __name__ == "__main__":
    args = parse_args()
    image_folder = args.image_folder
    words_to_remove = args.words_to_remove

    # Split each item on commas, strip whitespace, and flatten
    phrases_to_remove = []
    for item in words_to_remove:
        phrases = [phrase.strip() for phrase in item.split(",") if phrase.strip()]
        phrases_to_remove.extend(phrases)

    if not os.path.isdir(image_folder):
        print(f"Error: '{image_folder}' is not a valid directory.")
        exit(1)

    import re
    for file in os.listdir(image_folder):
        if file.lower().endswith(".png"):
            img_path = os.path.join(image_folder, file)
            img = Image.open(img_path)
            meta = img.info
            prompt_json = meta.get("prompt")
            if prompt_json:
                prompt = extract_positive_prompt_from_prompt_json(prompt_json)
                if prompt:
                    for phrase in phrases_to_remove:
                        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                        prompt = pattern.sub('', prompt)
                    prompt = re.sub(r'\s*,\s*', ', ', prompt)
                    prompt = re.sub(r'\s+', ' ', prompt).strip(' ,')
                    prompt = prompt.strip()
                    txt_path = os.path.join(image_folder, os.path.splitext(file)[0] + ".txt")
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(prompt)
    print("✅ Positive prompts extracted to .txt files.")