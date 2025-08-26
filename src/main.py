import csv
import os
import json
import re
from PIL import Image

from cli import parse_args

_SUMMARY_FILENAME = "summary.csv"

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

def clean_prompt(prompt):
    # Remove (tag:weight) or (tag)
    prompt = re.sub(r'\(([^:()]+)(:[^()]+)?\)', r'\1', prompt)
    # Remove [tag]
    prompt = re.sub(r'\[([^\]]+)\]', r'\1', prompt)
    # Remove {tag}
    prompt = re.sub(r'\{([^}]+)\}', r'\1', prompt)
    # Remove extra spaces and commas
    prompt = re.sub(r'\s*,\s*', ', ', prompt)
    prompt = re.sub(r'\s+', ' ', prompt)
    prompt = prompt.strip(' ,')
    return prompt.strip()

if __name__ == "__main__":
    args = parse_args()
    image_folder = args.image_folder
    words_to_remove = args.words_to_remove
    summary_flag = getattr(args, 'summary', False)

    # Split each item on commas, strip whitespace, and flatten
    phrases_to_remove = []
    for item in words_to_remove:
        phrases = [phrase.strip() for phrase in item.split(",") if phrase.strip()]
        phrases_to_remove.extend(phrases)

    if not os.path.isdir(image_folder):
        print(f"Error: '{image_folder}' is not a valid directory.")
        exit(1)
    
    summary_entries = []
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
                    prompt = clean_prompt(prompt)
                    txt_path = os.path.join(image_folder, os.path.splitext(file)[0] + ".txt")
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(prompt)
                    if summary_flag:
                        summary_entries.append((file, prompt))

    if summary_flag and summary_entries:
        summary_path = os.path.join(image_folder, _SUMMARY_FILENAME)
        with open(summary_path, "w", encoding="utf-8", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["filename", "prompt"])
            for entry in summary_entries:
                writer.writerow(entry)
        print(f"✅ Summary written to {summary_path}")

    print("✅ Positive prompts extracted to .txt files.")