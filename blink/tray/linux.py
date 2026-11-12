"""Linux system tray backend (Ayatana/AppIndicator3 with Gtk.StatusIcon fallback)"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Ubuntu 24.04+ ships AyatanaAppIndicator3 instead of the legacy
# AppIndicator3. Try Ayatana first, then fall back to the old name, then
# fall back to Gtk.StatusIcon
_APPINDICATOR = None
try:
    gi.require_version("AyatanaAppIndicator3", "0.1")
    from gi.repository import AyatanaAppIndicator3 as _APPINDICATOR
except (ValueError, ImportError):
    try:
        gi.require_version("AppIndicator3", "0.1")
        from gi.repository import AppIndicator3 as _APPINDICATOR
    except (ValueError, ImportError):
        _APPINDICATOR = None

_HAS_APPINDICATOR = _APPINDICATOR is not None

from .base import Tray


class GtkTray(Tray):
    def __init__(self):
        self._toggle_label = "⏸ Pause"
        self._on_toggle = lambda: None
        self._on_settings = lambda: None
        self._on_quit = lambda: None
        self._indicator = None
        self._status_icon = None
        self._menu = self._build_menu()

    def _build_menu(self) -> Gtk.Menu:
        menu = Gtk.Menu()

        status = Gtk.MenuItem(label="Blink is running")
        status.set_sensitive(False)
        menu.append(status)
        menu.append(Gtk.SeparatorMenuItem())

        self._toggle_item = Gtk.MenuItem(label=self._toggle_label)
        self._toggle_item.connect("activate", lambda _w: self._on_toggle())
        menu.append(self._toggle_item)

        menu.append(Gtk.SeparatorMenuItem())

        self._settings_item = Gtk.MenuItem(label="⚙ Settings…")
        self._settings_item.connect("activate", lambda _w: self._on_settings())
        menu.append(self._settings_item)

        menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="✕ Quit")
        quit_item.connect("activate", lambda _w: self._on_quit())
        menu.append(quit_item)

        menu.show_all()
        return menu

    def set_on_toggle(self, callback):
        self._on_toggle = callback

    def set_on_settings(self, callback):
        self._on_settings = callback

    def set_on_quit(self, callback):
        self._on_quit = callback

    def set_toggle_label(self, label):
        self._toggle_label = label
        self._toggle_item.set_label(label)

    def show(self):
        if _HAS_APPINDICATOR:
            self._indicator = _APPINDICATOR.Indicator.new(
                "blink-indicator",
                "dialog-information",
                _APPINDICATOR.IndicatorCategory.APPLICATION_STATUS,
            )
            self._indicator.set_status(_APPINDICATOR.IndicatorStatus.ACTIVE)
            self._indicator.set_menu(self._menu)
        else:
            self._status_icon = Gtk.StatusIcon.new_from_icon_name(
                "dialog-information"
            )
            self._status_icon.set_tooltip_text("Blink - eye care reminder")
            self._status_icon.connect("popup-menu", self._on_popup)
            self._status_icon.connect("activate", lambda _i: self._on_toggle())
            self._status_icon.set_visible(True)

    def _on_popup(self, icon, button, time):
        self._menu.popup(
            None, None, Gtk.StatusIcon.position_menu, icon, button, time
        )
