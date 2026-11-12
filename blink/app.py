"""Main application: wires scheduler, notifier, and tray together"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

from .config import load_config, save_config
from .notifier import create_notifier
from .scheduler import Event, Scheduler
from .tray import create_tray


class Blink:
    def __init__(self):
        self.config = load_config()

        self.scheduler = Scheduler(
            blink_interval=self.config["blink_interval"],
            look_away_interval=self.config["look_away_interval"],
            look_away_duration=self.config["look_away_duration"],
            rest_duration=self.config["rest_duration"],
            enabled=self.config["enabled"],
        )

        self.notifier = create_notifier()
        self.tray = create_tray()
        self.tray.set_on_toggle(self._on_toggle)
        self.tray.set_on_quit(self._on_quit)
        self.tray.set_toggle_label(
            "⏸ Pause" if self.scheduler.enabled else "▶ Resume"
        )
        self.tray.show()

        GLib.timeout_add(1000, self._tick)

    def _tick(self) -> bool:
        for event in self.scheduler.tick():
            self._handle_event(event)
        return True

    def _handle_event(self, event: Event) -> None:
        if event is Event.BLINK:
            self.notifier.notify("👁 Blink!", "Remember to blink your eyes.")
        elif event is Event.LOOK_AWAY:
            self.notifier.notify(
                "👀 20-20-20 Rule",
                f"Look at something 20 feet away "
                f"for {self.scheduler.look_away_duration} seconds.",
            )
        elif event is Event.REST:
            self.notifier.notify(
                "😌 Rest Your Eyes",
                f"Close your eyes for {self.scheduler.rest_duration} seconds.",
            )

    def _on_toggle(self) -> None:
        if self.scheduler.enabled:
            self.scheduler.pause()
            self.tray.set_toggle_label("▶ Resume")
        else:
            self.scheduler.resume()
            self.tray.set_toggle_label("⏸ Pause")

    def _on_quit(self) -> None:
        self.notifier.close()
        Gtk.main_quit()
