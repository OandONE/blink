"""Configuration loading and persistence for Blink

A read-only default config ships with the code (``config.json`` next to the
package). User overrides — including changes saved from the Settings window -
go to the standard XDG location (``~/.config/blink/config.json``) so Blink
works when installed to ``/opt/blink`` without needing root to save settings
"""

import json
import os
from pathlib import Path


DEFAULT_CONFIG = {
    "blink_interval": 30,
    "look_away_interval": 1200,
    "look_away_duration": 20,
    "rest_duration": 20,
    "enabled": True,
}


def _user_config_path() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(xdg) / "blink" / "config.json"


def _shipped_config_path() -> Path:
    # config.json sits next to the package: project root in dev,
    # /opt/blink/ after install
    return Path(__file__).resolve().parent.parent / "config.json"


def load_config() -> dict:
    """Load user config if present, else shipped default, else built-ins."""
    for path in (_user_config_path(), _shipped_config_path()):
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(data)
            return merged
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """Write user overrides to XDG config home (never to /opt)."""
    path = _user_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    tmp.replace(path)
