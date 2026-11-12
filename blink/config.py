"""Configuration loading and persistence for Blink

Settings live in ``config.json`` at the project root so users can edit them
directly. The file is created with defaults on first run and merged with
defaults on load, so partial or outdated configs still work
"""

import json
from pathlib import Path


# config.json lives at the project root, one level above the package
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"

DEFAULT_CONFIG = {
    "blink_interval": 30,
    "look_away_interval": 1200,
    "look_away_duration": 20,
    "rest_duration": 20,
    "enabled": True,
}


def load_config() -> dict:
    """Load config from disk, merged with defaults"""
    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    merged = DEFAULT_CONFIG.copy()
    merged.update(data)
    return merged


def save_config(config: dict) -> None:
    """Write config atomically (write to temp, then rename)"""
    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    tmp.replace(CONFIG_PATH)
