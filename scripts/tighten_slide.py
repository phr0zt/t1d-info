#!/usr/bin/env python3
"""Shrink body text and card padding on one slide so it fits 1920x1080.

Usage: tighten_slide.py <slide.html> [factor]

Scales every font-size below 40px (body copy and card titles, never the slide
heading or big stat numbers) and every 44px card padding by `factor`
(default 0.9), and trims the absolute footer to 20px. Idempotent enough to run
twice when one pass is not enough; the build's overflow check says when to stop.
"""
import re
import sys

path = sys.argv[1]
factor = float(sys.argv[2]) if len(sys.argv) > 2 else 0.9
html = open(path).read()


def font(m):
    size = int(m.group(1))
    return f"font-size:{max(18, round(size * factor)) if size < 40 else size}px"


def footer(m):
    return re.sub(r"font-size:\d+px", "font-size:20px", m.group(0))


html = re.sub(r"font-size:(\d+)px", font, html)
html = re.sub(r"padding:(\d+)px(?=[;\"])", lambda m: f"padding:{round(int(m.group(1)) * factor)}px" if int(m.group(1)) <= 48 else m.group(0), html)
html = re.sub(r'<p style="position:absolute[^"]*"', footer, html)
open(path, "w").write(html)
print("tightened", path)
