# 👁️ Blink — Eye care reminder for developers who forget to blink.

![logo](blink/assets/icon.svg)

A lightweight system tray app that reminds you to blink, look away, and rest
your eyes. Built with GTK3 and AppIndicator, it works on any Linux desktop
(GNOME, KDE, XFCE, MATE, Cinnamon, Budgie, ...).

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 👁 **Blink Reminder** | Reminds you to blink every 30 seconds |
| 👀 **20-20-20 Rule** | Every 20 minutes, look 20 feet away for 20 seconds |
| 😌 **Eye Rest** | Close your eyes and rest after looking away |
| ⏸ **Pause/Resume** | Toggle reminders from the system tray menu |
| ⚙ **Settings Window** | Edit all intervals from the tray menu |
| 🚀 **Autostart** | Starts automatically on login (optional, on by default) |
| 🐧 **Native Linux** | Built with GTK3 and AppIndicator |

---

## 📦 Installation

### Recommended: system-wide install

```bash
git clone https://github.com/OandONE/blink.git
cd blink
sudo ./install.sh
```

This installs Blink to `/opt/blink`, adds a `blink` command to
`/usr/local/bin`, registers the icon and menu entry, and enables autostart
for your user. Log out and back in (or run `blink &`) and you're set.

### Requirements

Blink depends on system libraries, so they must come from your distro's
package manager, not `pip`:

**Debian / Ubuntu 24.04+:**
```bash
sudo apt install python3-gi gir1.2-notify-0.7 gir1.2-ayatanaappindicator3-0.1
```

**Debian / Ubuntu 22.04 and older:**
```bash
sudo apt install python3-gi gir1.2-notify-0.7 gir1.2-appindicator3-0.1
```

**Fedora / RHEL:**
```bash
sudo dnf install python3-gobject libnotify libayatana-appindicator-gtk3
```

**Arch / Manjaro:**
```bash
sudo pacman -S python-gobject libnotify libayatana-appindicator
```

> If AppIndicator isn't available, Blink falls back to `Gtk.StatusIcon`,
> which ships with every GTK3 install. On stock GNOME Shell, install the
> AppIndicator extension (`gnome-shell-extension-appindicator` or
> `gnome-shell-ubuntu-extensions` on Ubuntu).

### Development (run from source)

```bash
git clone https://github.com/OandONE/blink.git
cd blink
python3 -m blink
```

> **Using a virtualenv?** Create it with `--system-site-packages` so
> PyGObject (installed via the system package manager) is visible:
>
> ```bash
> python3 -m venv --system-site-packages venv
> source venv/bin/activate
> python3 -m blink
> ```

---

## 🗑️ Uninstall

```bash
cd blink
sudo ./install.sh --uninstall
```

Removes `/opt/blink`, the `blink` command, the icon, the menu entry, and
the autostart file. Your personal settings in `~/.config/blink/config.json`
are **kept** — delete them manually if you want a clean slate.

---

## 🎨 Configuration

### Via the Settings window (recommended)

Right-click the tray icon → **Settings…** → edit intervals → **Save**.
Changes are applied immediately; no restart needed.

### Via `config.json`

Blink reads settings from two places, in this order:

1. **User overrides:** `~/.config/blink/config.json` (created when you
   save from the Settings window — safe to edit by hand)
2. **Shipped defaults:** `config.json` at the project root (or
   `/opt/blink/config.json` after install — read-only, do not edit)

The file format is JSON:

```json
{
  "blink_interval": 30,
  "look_away_interval": 1200,
  "look_away_duration": 20,
  "rest_duration": 20,
  "enabled": true
}
```

| Key | Description |
|-----|-------------|
| `blink_interval` | Seconds between blink reminders |
| `look_away_interval` | Seconds between 20-20-20 reminders (default 20 min) |
| `look_away_duration` | How long to look away (seconds) |
| `rest_duration` | How long to close your eyes (seconds) |
| `enabled` | Start the app enabled (pause/resume toggles are per-session) |

Changes take effect on the next launch (except when saved via the Settings
window, which applies them live). Pause/Resume from the tray only affects
the current session — the `enabled` flag in `config.json` stays untouched.

---

## 🐧 Desktop integration

After `sudo ./install.sh`, Blink appears in your application menu / dash
with its own icon. If the icon doesn't show up right away, log out and
back in, or refresh the icon cache:

```bash
sudo gtk-update-icon-cache -f /usr/share/icons/hicolor
sudo update-desktop-database /usr/share/applications
```

### Autostart

`install.sh` creates `~/.config/autostart/blink.desktop` so Blink starts
on login. To disable it:

```bash
rm ~/.config/autostart/blink.desktop
```

To re-enable it, re-run `sudo ./install.sh` (or recreate the file
yourself — see the script for its contents).

---

## 🚧 Roadmap

- [x] ⚙️ Settings GUI
- [x] 🚀 Autostart option
- [ ] 🎨 Custom notification sounds
- [ ] 🪟 Windows support

---

## 📄 License

MIT © OandONE (2026)
