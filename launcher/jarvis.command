#!/bin/zsh

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

cd "$HOME/Desktop/Jarvis"

source .venv/bin/activate

exec python main.py

