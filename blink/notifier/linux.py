"""Linux notification backend (libnotify with stderr fallback)"""

import sys

import gi
gi.require_version("Gtk", "3.0")

try:
    gi.require_version("Notify", "0.7")
    from gi.repository import Notify
    _HAS_NOTIFY = True
except (ValueError, ImportError):
    _HAS_NOTIFY = False

from .base import Notifier


class LinuxNotifier(Notifier):
    """Linux notification backend

    Prefers libnotify (works on GNOME, KDE, XFCE, Budgie, and any desktop
    running a freedesktop notification daemon like dunst or mako). Falls back
    to stderr if libnotify or the daemon is unavailable, so reminders are
    never silently dropped
    """

    def __init__(self, app_name: str = "Blink"):
        self._app_name = app_name
        self._available = False
        if _HAS_NOTIFY:
            try:
                Notify.init(app_name)
                self._available = True
            except Exception:
                self._available = False

    def notify(self, title: str, message: str) -> None:
        if self._available:
            try:
                n = Notify.Notification.new(title, message, "dialog-information")
                n.set_timeout(5000)
                n.show()
                return
            except Exception:
                # Daemon went away mid-session; drop to stderr
                self._available = False
        print(f"[{self._app_name}] {title} — {message}", file=sys.stderr)

    def close(self) -> None:
        if self._available:
            try:
                Notify.uninit()
            except Exception:
                pass
            self._available = False
    