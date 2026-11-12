# 👁️ Blink — Eye care reminder for developers who forget to blink.

A lightweight system tray app that reminds you to blink, look away, and rest your eyes.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 👁 **Blink Reminder** | Reminds you to blink every 30 seconds |
| 👀 **20-20-20 Rule** | Every 20 minutes, look 20 feet away for 20 seconds |
| 😌 **Eye Rest** | Close your eyes and rest after looking away |
| ⏸ **Pause/Resume** | Toggle reminders from the system tray menu |
| 🐧 **Native Linux** | Built with GTK3 and AppIndicator |

---

## 📦 Installation

Blink depends on system-level libraries (GTK3, libnotify), so the recommended
way to run it is against your system Python — not inside a plain venv.

```bash
# Required
sudo apt install python3-gi gir1.2-notify-0.7 -y
# Recommended (better tray integration on most desktops)
sudo apt install gir1.2-appindicator3-0.1 -y

git clone https://github.com/OandONE/blink.git && cd blink
python3 -m blink
```

> **Using a virtualenv?** Create it with `--system-site-packages` so PyGObject
> (which is installed via the system package manager) is visible:
>
> ```bash
> python3 -m venv --system-site-packages venv
> source venv/bin/activate
> python3 -m blink
> ```

---

## 🚀 Autostart (run on boot)

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/blink.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Blink
Comment=Eye care reminder
Exec=sh -c "cd /home/YOUR_USERNAME/blink && python3 -m blink"
StartupNotify=false
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
```

> Replace `YOUR_USERNAME` with your Linux username.

---

## 🎨 Configuration

Edit `config.json` at the project root:

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
| `enabled` | Start the app enabled (toggle is per-session) |

Changes take effect on the next launch. Pause/Resume from the tray only
affects the current session — the `enabled` flag in `config.json` stays
untouched.

---

## 🚧 Roadmap

- [ ] ⚙️ Settings GUI
- [ ] 🚀 Autostart option
- [ ] 🎨 Custom notification sounds
- [ ] 🪟 Windows support

---

## 📄 License

MIT © OandONE (2026)
