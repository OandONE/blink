"""Linux system tray backend (AppIndicator3 with Gtk.StatusIcon fallback)"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

try:
    gi.require_version("AppIndicator3", "0.1")
    from gi.repository import AppIndicator3
    _HAS_APPINDICATOR = True
except (ValueError, ImportError):
    _HAS_APPINDICATOR = False

from .base import Tray


class GtkTray(Tray):
    """Tray for Linux desktops

    Uses AppIndicator when available (KDE Plasma, XFCE with
    statusnotifier plugin, Budgie, MATE, Cinnamon, and GNOME with the
    AppIndicator shell extension). Falls back to Gtk.StatusIcon, which
    ships with every GTK3 install, for desktops without AppIndicator
    """

    def __init__(self):
        self._toggle_label = "⏸ Pause"
        self._on_toggle = lambda: None
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

        quit_item = Gtk.MenuItem(label="✕ Quit")
        quit_item.connect("activate", lambda _w: self._on_quit())
        menu.append(quit_item)

        menu.show_all()
        return menu

    # Tray interface

    def set_on_toggle(self, callback):
        self._on_toggle = callback

    def set_on_quit(self, callback):
        self._on_quit = callback

    def set_toggle_label(self, label):
        self._toggle_label = label
        self._toggle_item.set_label(label)

    def show(self):
        if _HAS_APPINDICATOR:
            self._indicator = AppIndicator3.Indicator.new(
                "blink-indicator",
                "eye-open",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            )
            self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self._indicator.set_menu(self._menu)
        else:
            self._status_icon = Gtk.StatusIcon.new_from_icon_name("eye-open")
            self._status_icon.set_tooltip_text("Blink — eye care reminder")
            self._status_icon.connect("popup-menu", self._on_popup)
            self._status_icon.connect(
                "activate", lambda _icon: self._on_toggle()
            )
            self._status_icon.set_visible(True)

    def _on_popup(self, icon, button, time):
        self._menu.popup(
            None, None, Gtk.StatusIcon.position_menu, icon, button, time
        )
