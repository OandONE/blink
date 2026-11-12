"""System tray backends and platform-aware factory"""

import sys

from .base import Tray

__all__ = ["Tray", "create_tray"]


def create_tray() -> Tray:
    """Return the tray backend for the current platform."""
    if sys.platform.startswith("linux"):
        from .linux import GtkTray
        return GtkTray()
    raise NotImplementedError(
        f"Blink does not yet support tray icons on {sys.platform!r}. "
        "A Windows backend is planned."
    )
