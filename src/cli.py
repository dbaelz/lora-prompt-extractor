import argparse

_PROGRAM_NAME = "Binaural Mixer"
_VERSION = "0.0.1"
_DESCRITION = "Extract positive prompts from ComfyUI images for LoRA training."

def parse_args():
    parser = argparse.ArgumentParser(
        description=_DESCRITION
    )
    parser.add_argument("--version", action="version", version=f"{_PROGRAM_NAME} - version {_VERSION}")

    parser.add_argument("image_folder", help="Directory containing the images")
    parser.add_argument(
        "word_to_remove", nargs="?", default=None, help="Word to remove from prompt (optional)"
    )
    return parser.parse_args()
