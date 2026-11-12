#!/usr/bin/env bash
#
# Blink installer — installs to /opt/blink, sets up a `blink` command,
# registers icons + .desktop entry, and enables autostart.
#
# Usage:
#   sudo ./install.sh          # system-wide install (recommended)
#   ./install.sh --uninstall   # remove everything
#
set -euo pipefail

APP_NAME="blink"
INSTALL_DIR="/opt/blink"
BIN_PATH="/usr/local/bin/blink"
DESKTOP_PATH="/usr/share/applications/blink.desktop"
ICON_DIR="/usr/share/icons/hicolor"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---- helpers ---------------------------------------------------------------

info()  { printf '\033[1;34m[blink]\033[0m %s\n' "$*"; }
warn()  { printf '\033[1;33m[blink]\033[0m %s\n' "$*"; }
die()   { printf '\033[1;31m[blink]\033[0m %s\n' "$*" >&2; exit 1; }

require_root() {
    if [[ $EUID -ne 0 ]]; then
        die "This script must be run with sudo (it writes to /opt and /usr)."
    fi
}

check_python_deps() {
    info "Checking Python GTK3 dependencies…"
    local missing=()
    python3 - <<'PY' || missing+=("python3-gi")
import gi
gi.require_version("Gtk", "3.0")
PY
    python3 -c "import gi; gi.require_version('Notify', '0.7')" 2>/dev/null \
        || missing+=("gir1.2-notify-0.7")
    python3 -c "
import gi
for ns in ('AyatanaAppIndicator3','AppIndicator3'):
    try:
        gi.require_version(ns, '0.1'); break
    except ValueError: pass
else:
    raise SystemExit(1)
" 2>/dev/null || missing+=("gir1.2-ayatanaappindicator3-0.1")

    if (( ${#missing[@]} )); then
        warn "Missing packages: ${missing[*]}"
        warn "Install them with your package manager, e.g.:"
        warn "  sudo apt install python3-gi gir1.2-notify-0.7 gir1.2-ayatanaappindicator3-0.1"
        warn "Continuing anyway — Blink will fall back to stderr notifications."
    else
        info "All GTK dependencies found."
    fi
}

# ---- install ---------------------------------------------------------------

do_install() {
    require_root
    check_python_deps

    info "Installing to ${INSTALL_DIR}…"
    rm -rf "${INSTALL_DIR}"
    mkdir -p "${INSTALL_DIR}"
    cp -r "${SCRIPT_DIR}/blink"        "${INSTALL_DIR}/blink"
    cp    "${SCRIPT_DIR}/config.json"  "${INSTALL_DIR}/config.json"
    cp    "${SCRIPT_DIR}/LICENSE"      "${INSTALL_DIR}/LICENSE" 2>/dev/null || true
    cp    "${SCRIPT_DIR}/README.md"    "${INSTALL_DIR}/README.md" 2>/dev/null || true
    find "${INSTALL_DIR}" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

    info "Creating ${BIN_PATH}…"
    cat > "${BIN_PATH}" <<EOF
#!/usr/bin/env bash
cd ${INSTALL_DIR} && exec python3 -m blink "\$@"
EOF
    chmod 755 "${BIN_PATH}"

    info "Installing icons…"
    install -Dm644 "${INSTALL_DIR}/blink/assets/icon.svg" \
        "${ICON_DIR}/scalable/apps/blink.svg"
    for size in 22 48 256; do
        src="${INSTALL_DIR}/blink/assets/icon-${size}.png"
        [[ $size -eq 22 ]] && src="${INSTALL_DIR}/blink/assets/icon.png"
        if [[ -f "$src" ]]; then
            install -Dm644 "$src" "${ICON_DIR}/${size}x${size}/apps/blink.png"
        fi
    done
    gtk-update-icon-cache -f -t "${ICON_DIR}" 2>/dev/null || true

    info "Installing .desktop entry…"
    install -Dm644 "${SCRIPT_DIR}/blink.desktop" "${DESKTOP_PATH}"
    update-desktop-database /usr/share/applications 2>/dev/null || true

    # Autostart for the invoking user (sudo sets SUDO_USER)
    local real_user="${SUDO_USER:-$USER}"
    local real_home
    real_home="$(getent passwd "${real_user}" | cut -d: -f6)"
    if [[ -n "${real_home}" && -d "${real_home}" ]]; then
        local autostart_dir="${real_home}/.config/autostart"
        info "Enabling autostart for ${real_user}…"
        install -d -o "${real_user}" -g "$(id -gn "${real_user}")" "${autostart_dir}"
        cat > "${autostart_dir}/blink.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Blink
Comment=Eye care reminder
Exec=/usr/local/bin/blink
StartupNotify=false
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
        chown "${real_user}:$(id -gn "${real_user}")" "${autostart_dir}/blink.desktop"
    fi

    info "Done."
    echo
    info "Run it now:"
    echo "    blink                    # from any terminal"
    echo "    or find “Blink” in your app menu / dash"
    echo
    info "Autostart will kick in on next login."
    info "To start it immediately without logging out:"
    echo "    blink &"
}

# ---- uninstall -------------------------------------------------------------

do_uninstall() {
    require_root
    info "Removing ${INSTALL_DIR}…"
    rm -rf "${INSTALL_DIR}"

    info "Removing ${BIN_PATH}…"
    rm -f "${BIN_PATH}"

    info "Removing icons…"
    rm -f "${ICON_DIR}/scalable/apps/blink.svg"
    for size in 22 48 256; do
        rm -f "${ICON_DIR}/${size}x${size}/apps/blink.png"
    done
    gtk-update-icon-cache -f -t "${ICON_DIR}" 2>/dev/null || true

    info "Removing .desktop entry…"
    rm -f "${DESKTOP_PATH}"
    update-desktop-database /usr/share/applications 2>/dev/null || true

    local real_user="${SUDO_USER:-$USER}"
    local real_home
    real_home="$(getent passwd "${real_user}" | cut -d: -f6)"
    if [[ -n "${real_home}" ]]; then
        rm -f "${real_home}/.config/autostart/blink.desktop"
        info "Removed autostart entry (user config in ~/.config/blink left in place)."
    fi

    info "Done."
}

# ---- main ------------------------------------------------------------------

case "${1:-install}" in
    --uninstall|uninstall) do_uninstall ;;
    install|"")            do_install ;;
    *) die "Unknown argument: $1 (use --uninstall to remove)" ;;
esac