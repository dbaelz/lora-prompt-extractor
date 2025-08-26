import argparse


_PROGRAM_NAME = "LoRA Prompt Extractor"
_VERSION = "0.1.0"
_DESCRIPTION = "Extract positive prompts from ComfyUI images and create .txt files for LoRA training. Optionally remove specified words from prompts."

def parse_args():
    parser = argparse.ArgumentParser(
        description=_DESCRIPTION
    )
    parser.add_argument("--version", action="version", version=f"{_PROGRAM_NAME} - version {_VERSION}")
    parser.add_argument("image_folder", help="Directory containing the images")
    parser.add_argument(
        "--words-to-remove", "-w",
        nargs="*",
        default=[],
        metavar="WORD",
        help="Words to remove from prompt (optional, space separated)"
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Export a summary.csv with the filenames and the .txt file descriptions"
    )
    return parser.parse_args()
