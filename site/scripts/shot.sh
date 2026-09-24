#!/usr/bin/env bash
# Screenshot a URL of the locally served site: shot.sh <out.png> <width> <height> <url>
exec google-chrome-stable --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=3000 \
  --window-size="$2,$3" --screenshot="$1" "$4" 2>/dev/null
