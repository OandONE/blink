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

```bash
sudo apt install python3-gi python3-yaml gir1.2-notify-0.7 -y
git clone https://github.com/OandONE/blink.git && cd blink/blink
python3 blink.py
```

---

## 🚀 Autostart (run on boot)

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/blink.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Blink
Comment=Eye care reminder
Exec=python3 /home/YOUR_USERNAME/blink/blink/blink.py
StartupNotify=false
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
```

> Replace `YOUR_USERNAME` with your Linux username.

---

## 🎨 Configuration

Edit `~/.config/blink/config.yaml`:

```yaml
blink_interval: 30        # seconds between blink reminders
look_away_interval: 1200  # seconds between 20-20-20 reminders (20 min)
look_away_duration: 20    # how long to look away
rest_duration: 20         # how long to close your eyes
enabled: true
```

---

## 🚧 Roadmap

- [ ] ⚙️ Settings GUI
- [ ] 🚀 Autostart option
- [ ] 🎨 Custom notification sounds
- [ ] 🪟 Windows support

---

## 📄 License

MIT © OandONE (2026)
