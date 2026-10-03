#!/usr/bin/env python3
"""Generate decks/07-manual-therapy slides (EN + FR) in the shared inline-style grammar."""
import json, pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
PROJ = ROOT / "decks/07-manual-therapy/project"
DISPLAY = "font-family:Outfit, Helvetica, Arial, sans-serif"
INK, PAPER = "#16202b", "#f7f4ee"

def sec(sid, dark, inner, footer=None, note="", gap=40, bg=None, transition="fade"):
    bg = bg or (INK if dark else PAPER)
    color = "#f7f4ee" if dark else "#1f2630"
    if bg == "#c0392b": color = "#fff6f3"
    fcol = "#8794a2" if dark else "#5c6672"
    out = [f'<section id="{sid}" data-transition="{transition}" style="background:{bg}; color:{color}; font-family:Inter, Helvetica, Arial, sans-serif; padding:128px 128px 160px; display:flex; flex-direction:column; gap:{gap}px">']
    out.append(inner)
    if footer:
        out.append(f'  <p style="position:absolute; left:128px; bottom:64px; width:1600px; font-size:22px; color:{fcol}">{footer}</p>')
    out.append(f"  <aside>{note}</aside>")
    out.append("</section>\n")
    return "\n".join(out)

def h2(t, size=64):
    return f'  <h2 style="{DISPLAY}; font-size:{size}px; font-weight:600; line-height:1.12">{t}</h2>'

def lede(t, dark, size=30, width=1600):
    return f'  <p style="width:{width}px; font-size:{size}px; line-height:1.5; color:{"#c3ccd6" if dark else "#37414d"}">{t}</p>'

TONES = {
    "teal": ("background:#1f7a6b; color:#f2fbf8", "", ""),
    "red": ("background:#c0392b; color:#fff6f3", "", ""),
    "panel": ("background:#243141", "color:#f0a08c", "color:#c3ccd6"),
    "ink": ("background:#16202b; color:#f7f4ee", "color:#f0a08c", "color:#c3ccd6"),
    "white": ("background:#ffffff; border:1px solid #e2ddd2", "", "color:#4b5560"),
}

def card(tone, title, body, h=32, p=27, pad=40, gap=14, flex="flex:1", big=None):
    box, hc, pc = TONES[tone]
    parts = [f'    <div style="{flex}; display:flex; flex-direction:column; gap:{gap}px; {box}; padding:{pad}px; border-radius:20px">']
    if big:
        parts.append(f'      <p style="{DISPLAY}; font-size:92px; font-weight:600; line-height:1">{big}</p>')
    if title:
        parts.append(f'      <h3 style="{DISPLAY}; font-size:{h}px; font-weight:600; {hc}">{title}</h3>')
    for b in body:
        if isinstance(b, list):
            items = "".join(f"<li>{i}</li>" for i in b)
            parts.append(f'      <ul style="font-size:{p}px; line-height:1.5; padding-left:32px; {pc}">{items}</ul>')
        elif b.startswith("~small~"):
            parts.append(f'      <p style="font-size:{p-4}px; line-height:1.45; {pc}">{b[7:]}</p>')
        else:
            parts.append(f'      <p style="font-size:{p}px; line-height:1.5; {pc}">{b}</p>')
    parts.append("    </div>")
    return "\n".join(parts)

def row(cards, gap=28):
    return f'  <div style="display:flex; gap:{gap}px; flex:1">\n' + "\n".join(cards) + "\n  </div>"

def build(L):
    S = {}
    c = L["cover"]
    S["cover"] = sec("cover", True, f'''  <p style="font-size:28px; font-weight:500; letter-spacing:2px; color:#f0a08c">{c["eyebrow"]}</p>
  <div style="display:flex; flex-direction:column; gap:36px">
    <h1 style="{DISPLAY}; font-size:108px; font-weight:600; line-height:1.02">{c["title"]}</h1>
    <p style="width:1300px; font-size:38px; line-height:1.4; color:#c3ccd6">{c["sub"]}</p>
  </div>''', c["footer"], c["note"]).replace("gap:40px\">", "justify-content:space-between\">", 1).replace("display:flex; flex-direction:column; gap:40px", "display:flex; flex-direction:column; justify-content:space-between", 1)

    w = L["who"]
    S["who"] = sec("who", False, "\n".join([h2(w["h"]), lede(w["lede"], False), row([
        card(t, ti, [b], h=30, p=24, pad=36) for (t, ti, b) in w["cards"]], gap=24)]), w["footer"], w["note"])

    y = L["why"]
    side = "\n".join(f'''      <div style="display:flex; flex-direction:column; gap:6px; background:#243141; padding:26px 34px; border-radius:18px">
        <h3 style="{DISPLAY}; font-size:27px; font-weight:600; color:#f0a08c">{a}</h3>
        <p style="font-size:23px; line-height:1.45; color:#c3ccd6">{b}</p>
      </div>''' for a, b in y["side"])
    S["why"] = sec("why", True, "\n".join([h2(y["h"]), f'''  <div style="display:flex; gap:40px; flex:1">
    <div style="width:620px; display:flex; flex-direction:column; justify-content:center; gap:20px; background:#1f7a6b; color:#f2fbf8; padding:52px; border-radius:20px">
      <p style="{DISPLAY}; font-size:110px; font-weight:600; line-height:1">{y.get("num", "66%")}</p>
      <p style="font-size:26px; line-height:1.5">{y["big"]}</p>
      <p style="font-size:22px; line-height:1.45">{y["bigsmall"]}</p>
    </div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center; gap:18px">
{side}
    </div>
  </div>''']), y["footer"], y["note"])

    hn = L["honest"]
    S["honest"] = sec("honest", False, "\n".join([h2(hn["h"]), row([
        card(t, ti, bs, h=34, p=27, pad=40, gap=18) for (t, ti, bs) in hn["cards"]], gap=28)]), hn["footer"], hn["note"])

    ins = L["insulin"]
    S["insulin"] = sec("insulin", False, "\n".join([h2(ins["h"]), lede(ins["lede"], False, size=28), row([
        card("red", None, [ins["big"], "~small~" + ins["bigsmall"]], p=25, pad=40, flex="width:440px", big="~6&times;"),
        card("white", ins["c2"][0], [ins["c2"][1]], h=32, p=27, pad=36),
        card("white", ins["c3"][0], [ins["c3"][1]], h=32, p=27, pad=36),
        card("teal", ins["c4"][0], [ins["c4"][1]], h=32, p=27, pad=36)], gap=24)]), ins["footer"], ins["note"])

    lo = L["lows"]
    S["lows"] = sec("lows", True, "\n".join([h2(lo["h"]), lede(lo["lede"], True, size=29), row([
        card(t, ti, [b], h=32, p=27, pad=36) for (t, ti, b) in lo["cards"]], gap=24)]), lo["footer"], lo["note"])

    se = L["sensors"]
    S["sensors"] = sec("sensors", False, "\n".join([h2(se["h"]), row([
        card(t, ti, [b], h=32, p=27, pad=38) for (t, ti, b) in se["cards"]], gap=24)]), se["footer"], se["note"])

    nt = L["notoday"]
    S["notoday"] = sec("notoday", False, "\n".join([h2(nt["h"]), row([
        card("ink", ti, [b], h=32, p=27, pad=38) for (ti, b) in nt["cards"]], gap=24),
        f'  <p style="font-size:31px; line-height:1.45; font-weight:600; width:1600px">{nt["statement"]}</p>']),
        nt["footer"], nt["note"], bg="#c0392b", transition="push").replace("color:#5c6672", "color:#ffd9d2")

    ne = L["nerves"]
    S["nerves"] = sec("nerves", True, "\n".join([h2(ne["h"]), lede(ne["lede"], True, size=29), row([
        card(t, ti, [b], h=32, p=27, pad=36) for (t, ti, b) in ne["cards"]], gap=24)]), ne["footer"], ne["note"])

    jo = L["joints"]
    S["joints"] = sec("joints", False, "\n".join([h2(jo["h"]), row([
        card(t, ti, [b], h=32, p=27, pad=38) for (t, ti, b) in jo["cards"]], gap=24)]), jo["footer"], jo["note"])

    sk = L["skin"]
    S["skin"] = sec("skin", True, "\n".join([h2(sk["h"]), row([
        card(t, ti, [b], h=32, p=27, pad=38) for (t, ti, b) in sk["cards"]], gap=24)]), sk["footer"], sk["note"])

    te = L["tell"]
    S["tell"] = sec("tell", False, "\n".join([h2(te["h"]), row([
        card("white", te["left"][0], [te["left"][1]], h=36, p=29, pad=48, gap=18, flex="flex:1.6"),
        card("teal", te["right"][0], te["right"][1], h=36, p=29, pad=48, gap=18)], gap=32)]), te["footer"], te["note"], gap=36)

    th = L["therapists"]
    S["therapists"] = sec("therapists", True, "\n".join([h2(th["h"]), row([
        card(t, ti, [b] if isinstance(b, str) else b, h=34, p=28, pad=44, gap=16) for (t, ti, b) in th["cards"]], gap=28)]), th["footer"], th["note"])

    ch = L["choosing"]
    S["choosing"] = sec("choosing", False, "\n".join([h2(ch["h"]), row([
        card(t, ti, [b], h=32, p=27, pad=36) for (t, ti, b) in ch["cards"]], gap=24)]), ch["footer"], ch["note"])

    he = L["help"]
    tiles = "\n".join(f'''    <div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; padding:32px; border-radius:16px">
      <h3 style="{DISPLAY}; font-size:26px; font-weight:600">{a}</h3>
      <p style="font-size:{fs}px; line-height:1.4">{b}</p>
    </div>''' for (bg, a, b, fs) in he["tiles"])
    S["help"] = sec("help", True, "\n".join([h2(he["h"]), f'  <div style="display:flex; gap:20px">\n{tiles}\n  </div>',
        f'  <p style="font-size:30px; line-height:1.5; width:1600px; color:#c3ccd6">{he["close"]}</p>']), he["footer"], he["note"], gap=36)
    return S

ORDER = ["cover", "who", "why", "honest", "insulin", "lows", "sensors", "notoday", "nerves", "joints", "skin", "tell", "therapists", "choosing", "help"]

if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    from slide_text import EN, FR
    for lang, L, d in (("en", EN, "slides"), ("fr", FR, "slides-fr")):
        out = PROJ / d
        out.mkdir(parents=True, exist_ok=True)
        S = build(L)
        for k in ORDER:
            (out / f"{k}.html").write_text(S[k])
    deck = {
        "v": 4, "createdOnFiles": {"v": 1, "at": "2026-10-03T12:00:00Z"},
        "title": "Massage, Orthotherapy and Type 1 Diabetes",
        "order": ORDER,
        "sections": {
            "s1": {"description": "Who does what in Québec, why people with type 1 book, and what massage can honestly claim", "start": "cover"},
            "s2": {"description": "Glucose on the table: insulin sites, lows, sensors and pumps, and when to reschedule", "start": "insulin"},
            "s3": {"description": "Bodies with complications: numb feet, stiff shoulders and hands, skin and getting up", "start": "nerves"},
            "s4": {"description": "What to tell the therapist, what therapists need, choosing one in Québec, and help", "start": "tell"},
        },
        "faces": {
            "outfit": {"family": "Outfit", "href": "https://fonts.googleapis.com/css2?family=Outfit:wght@300..700&display=swap"},
            "inter": {"family": "Inter", "href": "https://fonts.googleapis.com/css2?family=Inter:wght@300..700&display=swap"},
        },
        "designSystems": [],
    }
    (PROJ / "deck.json").write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n")
    print("wrote", len(ORDER), "slides x 2 languages")
