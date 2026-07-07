#!/usr/bin/env bash
set -euo pipefail
export HOME=/home/galyarder
export PATH=/home/galyarder/.local/bin:/home/galyarder/.cargo/bin:$PATH
printf 'computer-use-linux: '
command -v computer-use-linux || true
printf 'computer-use-linux-cosmic: '
command -v computer-use-linux-cosmic || true
printf 'ydotool: '
command -v ydotool || true
printf 'ydotoold: '
command -v ydotoold || true
printf 'ydotoold active: '
systemctl --user is-active ydotoold.service 2>/dev/null || true
printf 'ydotool socket: '
ls -l "${XDG_RUNTIME_DIR:-/run/user/$UID}/.ydotool_socket" 2>/dev/null || true
printf 'uinput: '
ls -l /dev/uinput 2>/dev/null || true
computer-use-linux doctor | jq .readiness
