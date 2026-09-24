#!/usr/bin/env python3
"""Flatten each deck's slides into plain structured JSON for content writing.

For every slide: heading, body as light Markdown (cards become ### blocks with a
tone hint), the absolutely-positioned footer line (sources/caveats), and the
<aside> speaker note. Output: build/slides/<deck>.json
"""
import json
import pathlib
import re

from bs4 import BeautifulSoup, NavigableString

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECKS = ["00-master", "01-food", "02-movement", "03-medications", "04-drugs-alcohol", "05-complications"]
TONES = {"#c0392b": "warning", "#1f7a6b": "do", "#16202b": "dark", "#243141": "dark"}


def inline(el):
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            out.append(str(c))
        elif c.name in ("b", "strong"):
            out.append(f"**{inline(c).strip()}**")
        elif c.name in ("i", "em"):
            out.append(f"*{inline(c).strip()}*")
        elif c.name == "br":
            out.append(" ")
        else:
            out.append(inline(c))
    return re.sub(r"\s+", " ", "".join(out))


def tone(el):
    style = (el.get("style") or "").lower()
    m = re.search(r"background:\s*(#[0-9a-f]{6})", style)
    return TONES.get(m.group(1)) if m else None


def blocks(el, depth=0):
    lines = []
    for c in el.find_all(recursive=False):
        if c.name == "aside":
            continue
        style = c.get("style") or ""
        if c.name == "p" and "position:absolute" in style.replace(" ", ""):
            continue
        if c.name in ("h1", "h2"):
            continue
        if c.name in ("h3", "h4"):
            lines.append(f"### {inline(c).strip()}")
        elif c.name == "p":
            t = inline(c).strip()
            if t:
                lines.append(t)
        elif c.name in ("ul", "ol"):
            for i, li in enumerate(c.find_all("li", recursive=False), 1):
                lines.append(f"{'-' if c.name == 'ul' else f'{i}.'} {inline(li).strip()}")
        elif c.name in ("table",):
            for tr in c.find_all("tr"):
                lines.append("| " + " | ".join(inline(td).strip() for td in tr.find_all(["td", "th"])) + " |")
        else:
            inner = blocks(c, depth + 1)
            t = tone(c)
            if inner and t:
                lines.append(f"[card:{t}]")
                lines.extend(inner)
                lines.append("[/card]")
            else:
                lines.extend(inner)
    return lines


def slide(path, sid):
    soup = BeautifulSoup(path.read_text(), "lxml")
    sec = soup.find("section")
    h = sec.find(["h1", "h2"])
    footer = [inline(p).strip() for p in sec.find_all("p") if "position:absolute" in (p.get("style") or "").replace(" ", "")]
    aside = sec.find("aside")
    return {
        "id": sid,
        "heading": inline(h).strip() if h else "",
        "body": "\n\n".join(blocks(sec)),
        "footer": " ".join(footer),
        "note": inline(aside).strip() if aside else "",
    }


def main():
    out = ROOT / "build" / "slides"
    out.mkdir(parents=True, exist_ok=True)
    for deck in DECKS:
        proj = ROOT / "decks" / deck / "project"
        meta = json.loads((proj / "deck.json").read_text())
        starts = {s["start"]: s["description"] for s in meta["sections"].values()}
        section, slides = None, []
        for sid in meta["order"]:
            section = starts.get(sid, section)
            s = slide(proj / "slides" / f"{sid}.html", sid)
            s["section"] = section
            slides.append(s)
        (out / f"{deck}.json").write_text(json.dumps({"deck": deck, "title": meta["title"], "slides": slides}, ensure_ascii=False, indent=1))
        print(deck, len(slides))


if __name__ == "__main__":
    main()
