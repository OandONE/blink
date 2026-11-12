"""Notification backends and platform-aware factory"""

import sys

from .base import Notifier

__all__ = ["Notifier", "create_notifier"]


def create_notifier() -> Notifier:
    """Return the notification backend for the current platform"""
    if sys.platform.startswith("linux"):
        from .linux import LinuxNotifier
        return LinuxNotifier()
    raise NotImplementedError(
        f"Blink does not yet support notifications on {sys.platform!r}. "
        "A Windows backend is planned."
    )
