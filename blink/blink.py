import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GLib, Notify
from gi.repository import AppIndicator3 as AppIndicator
import yaml
import os
import signal

CONFIG_PATH = os.path.expanduser("~/.config/blink/config.yaml")
DEFAULT_CONFIG = {
    'blink_interval': 30,
    'look_away_interval': 1200,
    'look_away_duration': 20,
    'rest_duration': 20,
    'enabled': True
}

class Blink:
    def __init__(self):
        self.config = self.load_config()
        Notify.init("Blink")
        
        # System Tray
        self.indicator = AppIndicator.Indicator.new(
            "blink-indicator",
            "eye-open",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        
        # Menu
        self.menu = Gtk.Menu()
        
        status_item = Gtk.MenuItem(label="Blink is running")
        status_item.set_sensitive(False)
        self.menu.append(status_item)
        
        self.menu.append(Gtk.SeparatorMenuItem())
        
        self.toggle_item = Gtk.MenuItem(label="⏸ Pause" if self.config['enabled'] else "▶ Resume")
        self.toggle_item.connect("activate", self.toggle)
        self.menu.append(self.toggle_item)
        
        self.menu.append(Gtk.SeparatorMenuItem())
        
        quit_item = Gtk.MenuItem(label="✕ Quit")
        quit_item.connect("activate", self.quit)
        self.menu.append(quit_item)
        
        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        
        self.blink_counter = 0
        self.look_counter = 0
        self.rest_counter = 0
        
        if self.config['enabled']:
            GLib.timeout_add(1000, self._tick)
    
    def load_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'w') as f:
                yaml.dump(DEFAULT_CONFIG, f)
            return DEFAULT_CONFIG.copy()
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    
    def save_config(self):
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(self.config, f)
    
    def _tick(self):
        if not self.config['enabled']:
            return True
        
        self.blink_counter += 1
        self.look_counter += 1
        self.rest_counter += 1
        
        # remember
        if self.blink_counter >= self.config['blink_interval']:
            self.blink_counter = 0
            self._notify("👁 Blink!", "Remember to blink your eyes.")
        
        # 20-20-20
        if self.look_counter >= self.config['look_away_interval']:
            self.look_counter = 0
            self.rest_counter = 0
            self._notify("👀 20-20-20 Rule", 
                        f"Look at something 20 feet away for {self.config['look_away_duration']} seconds.")
        
        # rest
        if self.rest_counter >= self.config['look_away_duration'] and self.rest_counter == self.config['look_away_duration']:
            self._notify("😌 Rest Your Eyes", 
                        f"Close your eyes for {self.config['rest_duration']} seconds.")
        
        return True
    
    def _notify(self, title, message):
        notification = Notify.Notification.new(title, message, "dialog-information")
        notification.set_timeout(5000)
        notification.show()
    
    def toggle(self, widget):
        self.config['enabled'] = not self.config['enabled']
        self.save_config()
        
        if self.config['enabled']:
            self.toggle_item.set_label("⏸ Pause")
            self.blink_counter = 0
            self.look_counter = 0
            self.rest_counter = 0
        else:
            self.toggle_item.set_label("▶ Resume")
    
    def quit(self, widget):
        self.config['enabled'] = False
        self.save_config()
        Notify.uninit()
        Gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Blink()
    Gtk.main()
