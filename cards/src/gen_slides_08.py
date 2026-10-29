#!/usr/bin/env python3
"""Generate decks/08-fast-carbs slides (EN + FR). Reuses the deck 07 layout helpers.

    python3 cards/src/gen_slides_08.py <repo root>
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen_slides import sec, h2, lede, card, row, DISPLAY  # noqa: E402
from slide_text_08 import EN, FR  # noqa: E402

ROOT = pathlib.Path(sys.argv[1])
PROJ = ROOT / "decks/08-fast-carbs/project"
ORDER = ["cover", "rule", "speed", "pantry", "candy", "canada", "label", "notfirst", "amounts", "medicine", "kits", "help"]


def table(head, rows, size=29, pad=13):
    """Three-column chart in the BT1 style: food · amount · carbs, alternating rows."""
    th = "".join(f'<th style="text-align:left; padding:0 28px 14px; {DISPLAY}; font-size:24px; font-weight:600; letter-spacing:2px; color:#5c6672">{h}</th>' for h in head)
    body = []
    for i, (food, amt, g, tag) in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else "#efe9df"
        tagh = f' <span style="font-size:20px; font-weight:600; color:#c0392b; margin-left:10px">{tag}</span>' if tag else ""
        body.append(
            f'<tr style="background:{bg}"><td style="padding:{pad}px 28px; font-weight:600">{food}{tagh}</td>'
            f'<td style="padding:{pad}px 28px; color:#37414d">{amt}</td>'
            f'<td style="padding:{pad}px 28px; {DISPLAY}; font-weight:600; color:#1f7a6b; white-space:nowrap">{g}</td></tr>')
    return (f'  <table style="width:1664px; border-collapse:collapse; font-size:{size}px; line-height:1.3; border:2px solid #16202b">'
            f'<thead style="background:#f7f4ee"><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>')


def build(L):
    S = {}
    c = L["cover"]
    S["cover"] = sec("cover", True, f'''  <p style="font-size:28px; font-weight:500; letter-spacing:2px; color:#f0a08c">{c["eyebrow"]}</p>
  <div style="display:flex; flex-direction:column; gap:36px">
    <h1 style="{DISPLAY}; font-size:108px; font-weight:600; line-height:1.02">{c["title"]}</h1>
    <p style="width:1300px; font-size:38px; line-height:1.4; color:#c3ccd6">{c["sub"]}</p>
  </div>''', c["footer"], c["note"]).replace("display:flex; flex-direction:column; gap:40px", "display:flex; flex-direction:column; justify-content:space-between", 1)

    r = L["rule"]
    S["rule"] = sec("rule", False, "\n".join([h2(r["h"]), lede(r["lede"], False), row([
        card(t, ti, [b], h=32, p=27, pad=36, big=big) for (t, big, ti, b) in r["cards"]], gap=24)]), r["footer"], r["note"])

    s = L["speed"]
    side = "\n".join(f'''      <div style="display:flex; flex-direction:column; gap:6px; background:#243141; padding:24px 34px; border-radius:18px">
        <h3 style="{DISPLAY}; font-size:28px; font-weight:600; color:#f0a08c">{a}</h3>
        <p style="font-size:24px; line-height:1.45; color:#c3ccd6">{b}</p>
      </div>''' for a, b in s["side"])
    S["speed"] = sec("speed", True, "\n".join([h2(s["h"]), f'''  <div style="display:flex; gap:40px; flex:1">
    <div style="width:620px; display:flex; flex-direction:column; justify-content:center; gap:20px; background:#1f7a6b; color:#f2fbf8; padding:52px; border-radius:20px">
      <p style="{DISPLAY}; font-size:100px; font-weight:600; line-height:1">{s["num"]}</p>
      <p style="font-size:27px; line-height:1.5">{s["big"]}</p>
      <p style="font-size:23px; line-height:1.45">{s["bigsmall"]}</p>
    </div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center; gap:16px">
{side}
    </div>
  </div>''']), s["footer"], s["note"])

    for k in ("pantry", "candy"):
        t = L[k]
        S[k] = sec(k, False, "\n".join([h2(t["h"]), table(L["head"], t["rows"], *((33, 17) if k == "pantry" else (37, 24)))]), t["footer"], t["note"], gap=36)

    ca = L["canada"]
    S["canada"] = sec("canada", True, "\n".join([h2(ca["h"]), lede(ca["lede"], True, size=29), row([
        card(t, ti, [b], h=32, p=26, pad=36) for (t, ti, b) in ca["cards"]], gap=24)]), ca["footer"], ca["note"])

    lb = L["label"]
    S["label"] = sec("label", False, "\n".join([h2(lb["h"]), lede(lb["lede"], False), row([
        card(t, ti, [b], h=32, p=27, pad=40, big=big) for (t, big, ti, b) in lb["cards"]], gap=24)]), lb["footer"], lb["note"])

    nf = L["notfirst"]
    S["notfirst"] = sec("notfirst", False, "\n".join([h2(nf["h"]), row([
        card("ink", ti, [b], h=32, p=26, pad=36) for (ti, b) in nf["cards"]], gap=24),
        f'  <p style="font-size:31px; line-height:1.45; font-weight:600; width:1600px">{nf["statement"]}</p>']),
        nf["footer"], nf["note"], bg="#c0392b", transition="push").replace("color:#5c6672", "color:#ffd9d2")

    am = L["amounts"]
    S["amounts"] = sec("amounts", False, "\n".join([h2(am["h"]), row([
        card(t, ti, [b] if isinstance(b, str) else b, h=32, p=26, pad=36) for (t, ti, b) in am["cards"]], gap=24)]), am["footer"], am["note"])

    me = L["medicine"]
    S["medicine"] = sec("medicine", True, "\n".join([h2(me["h"]), lede(me["lede"], True, size=29), row([
        card(t, ti, [b], h=32, p=27, pad=38) for (t, ti, b) in me["cards"]], gap=24)]), me["footer"], me["note"])

    ki = L["kits"]
    S["kits"] = sec("kits", False, "\n".join([h2(ki["h"]), row([
        card(t, ti, [b], h=32, p=27, pad=38) for (t, ti, b) in ki["cards"]], gap=24)]), ki["footer"], ki["note"])

    he = L["help"]
    tiles = "\n".join(f'''    <div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; padding:32px; border-radius:16px">
      <h3 style="{DISPLAY}; font-size:26px; font-weight:600">{a}</h3>
      <p style="font-size:{fs}px; line-height:1.4">{b}</p>
    </div>''' for (bg, a, b, fs) in he["tiles"])
    S["help"] = sec("help", True, "\n".join([h2(he["h"]), f'  <div style="display:flex; gap:20px">\n{tiles}\n  </div>',
        f'  <p style="font-size:30px; line-height:1.5; width:1600px; color:#c3ccd6">{he["close"]}</p>']), he["footer"], he["note"], gap=36)
    return S


if __name__ == "__main__":
    for L, d in ((EN, "slides"), (FR, "slides-fr")):
        out = PROJ / d
        out.mkdir(parents=True, exist_ok=True)
        S = build(L)
        for k in ORDER:
            (out / f"{k}.html").write_text(S[k])
    deck = {
        "v": 4, "createdOnFiles": {"v": 1, "at": "2026-10-04T12:00:00Z"},
        "title": "Fast-Acting Carbs: What Treats a Low",
        "order": ORDER,
        "sections": {
            "s1": {"description": "The 15-15 rule and why some sugars work faster than others", "start": "cover"},
            "s2": {"description": "The chart: pantry and candy amounts for Canada, and making your own row from a label", "start": "pantry"},
            "s3": {"description": "What isn't a first choice, and who needs a different amount", "start": "notfirst"},
            "s4": {"description": "Treating it like medicine, where to keep it, and help", "start": "medicine"},
        },
        "faces": {
            "outfit": {"family": "Outfit", "href": "https://fonts.googleapis.com/css2?family=Outfit:wght@300..700&display=swap"},
            "inter": {"family": "Inter", "href": "https://fonts.googleapis.com/css2?family=Inter:wght@300..700&display=swap"},
        },
        "designSystems": [],
    }
    (PROJ / "deck.json").write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n")
    print("wrote", len(ORDER), "slides x 2 languages")
