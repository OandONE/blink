"""Main application: tray icon, menu, and reminder loop"""

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
gi.require_version("Notify", "0.7")

from gi.repository import Gtk, GLib, Notify
from gi.repository import AppIndicator3 as AppIndicator

from .config import load_config, save_config
from .scheduler import Event, Scheduler


class Blink:
    def __init__(self):
        self.config = load_config()
        Notify.init("Blink")

        self.scheduler = Scheduler(
            blink_interval=self.config["blink_interval"],
            look_away_interval=self.config["look_away_interval"],
            look_away_duration=self.config["look_away_duration"],
            rest_duration=self.config["rest_duration"],
            enabled=self.config["enabled"],
        )

        self.indicator = AppIndicator.Indicator.new(
            "blink-indicator",
            "eye-open",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

        status_item = Gtk.MenuItem(label="Blink is running")
        status_item.set_sensitive(False)
        self.menu.append(status_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        self.toggle_item = Gtk.MenuItem(
            label="⏸ Pause" if self.scheduler.enabled else "▶ Resume"
        )
        self.toggle_item.connect("activate", self.toggle)
        self.menu.append(self.toggle_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="✕ Quit")
        quit_item.connect("activate", self.quit)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        # Timer runs unconditionally; the scheduler decides when to emit
        GLib.timeout_add(1000, self._tick)

    def _tick(self) -> bool:
        for event in self.scheduler.tick():
            self._handle_event(event)
        return True

    def _handle_event(self, event: Event) -> None:
        if event is Event.BLINK:
            self._notify("👁 Blink!", "Remember to blink your eyes.")
        elif event is Event.LOOK_AWAY:
            self._notify(
                "👀 20-20-20 Rule",
                f"Look at something 20 feet away "
                f"for {self.scheduler.look_away_duration} seconds.",
            )
        elif event is Event.REST:
            self._notify(
                "😌 Rest Your Eyes",
                f"Close your eyes for {self.scheduler.rest_duration} seconds.",
            )

    def _notify(self, title: str, message: str) -> None:
        notification = Notify.Notification.new(title, message, "dialog-information")
        notification.set_timeout(5000)
        notification.show()

    def toggle(self, widget) -> None:
        if self.scheduler.enabled:
            self.scheduler.pause()
            self.toggle_item.set_label("▶ Resume")
        else:
            self.scheduler.resume()
            self.toggle_item.set_label("⏸ Pause")
        self.config["enabled"] = self.scheduler.enabled
        save_config(self.config)

    def quit(self, widget) -> None:
        # Do NOT touch `enabled` here — the user's pause preference is
        # persisted by `toggle` and should survive restarts
        Notify.uninit()
        Gtk.main_quit()
