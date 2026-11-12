"""Entry point for ``python -m blink``"""

import signal

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .app import Blink


def main() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Blink()
    Gtk.main()


if __name__ == "__main__":
    main()
