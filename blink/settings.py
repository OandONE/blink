"""GTK3 settings dialog for editing config.json

Uses only standard GTK3 widgets so it works on any Linux desktop
(GNOME, KDE, XFCE, MATE, Cinnamon, Budgie, ...) with no GNOME-specific
dependencies
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

from .config import load_config, save_config


# (key, label, min, max, step)
FIELDS = (
    ("blink_interval", "Blink interval (seconds)", 1, 3600, 1),
    ("look_away_interval", "Look-away interval (seconds)", 30, 7200, 10),
    ("look_away_duration", "Look-away duration (seconds)", 1, 300, 1),
    ("rest_duration", "Rest duration (seconds)", 1, 300, 1),
)


class SettingsWindow(Gtk.Window):
    """Edit Blink settings and save them to config.json

    ``on_save`` is called with the updated config dict after a successful
    save, so the caller can apply the changes to a running scheduler
    """

    def __init__(self, on_save):
        super().__init__(title="Blink Settings")
        self._on_save = on_save
        self._config = load_config()
        self._spins = {}

        self.set_border_width(12)
        self.set_default_size(360, -1)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        grid = Gtk.Grid(column_spacing=12, row_spacing=10)
        self.add(grid)

        row = 0
        for key, label, lo, hi, step in FIELDS:
            lbl = Gtk.Label(label=label, xalign=0)
            spin = Gtk.SpinButton.new_with_range(lo, hi, step)
            spin.set_value(self._config[key])
            grid.attach(lbl, 0, row, 1, 1)
            grid.attach(spin, 1, row, 1, 1)
            self._spins[key] = spin
            row += 1

        hint = Gtk.Label(label="Changes apply immediately.", xalign=0)
        grid.attach(hint, 0, row, 2, 1)
        row += 1

        buttons = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        buttons.set_layout(Gtk.ButtonBoxStyle.END)
        buttons.set_spacing(6)

        cancel = Gtk.Button(label="Cancel")
        cancel.connect("clicked", lambda _b: self.destroy())
        buttons.add(cancel)

        save = Gtk.Button(label="Save")
        save.connect("clicked", self._on_save_clicked)
        buttons.add(save)

        grid.attach(buttons, 0, row, 2, 1)

        self.connect("key-press-event", self._on_key)
        self.show()
        grid.show_all()

    def _on_key(self, _widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()
            return True
        return False

    def _on_save_clicked(self, _widget):
        for key, spin in self._spins.items():
            self._config[key] = int(spin.get_value())
        save_config(self._config)
        self._on_save(self._config)
        self.destroy()
