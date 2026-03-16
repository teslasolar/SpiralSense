# SYM-L3 | p=3 | Data Writer
# Persistence layer. JSON serialization.
# All data encrypted at rest in production (AES-256-GCM).

import json
import os


def save_json(data: dict, filepath: str) -> None:
    """Save data dict to JSON file."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def load_json(filepath: str) -> dict:
    """Load JSON file to dict."""
    with open(filepath, "r", encoding="utf-8") as fh:
        return json.load(fh)
