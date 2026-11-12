"""Configuration loading and persistence for Blink"""

import json
import os
from pathlib import Path


def _config_dir() -> Path:
    """Respect XDG_CONFIG_HOME when set"""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "blink"
    return Path.home() / ".config" / "blink"


CONFIG_DIR = _config_dir()
CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "blink_interval": 30,
    "look_away_interval": 1200,
    "look_away_duration": 20,
    "rest_duration": 20,
    "enabled": True,
}


def load_config() -> dict:
    """Load config from disk, merged with defaults

    Creates a default config file on first run. Unknown or missing keys
    fall back to defaults, so partial configs are safe to load
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
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
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    tmp.replace(CONFIG_PATH)
