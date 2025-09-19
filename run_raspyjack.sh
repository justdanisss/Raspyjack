#!/usr/bin/env bash
set -e

export SDL_VIDEODRIVER=kmsdrm
export SDL_AUDIODRIVER=alsa

cd /root/Raspyjack
source /root/raspyjack-venv/bin/activate

# chvt 2   # opcional

exec python3 raspyjack.py
