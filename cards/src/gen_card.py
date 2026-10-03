import pathlib, sys
OUT = pathlib.Path(sys.argv[1])
T = {
 "en": dict(lang="en-CA", eyebrow="KRKT:T1DE · FOR MY MASSAGE THERAPIST OR ORTHOTHERAPIST", title="I have type 1 diabetes",
   rows=[("Insulin", "&#9744; pump &nbsp; &#9744; injections &nbsp;·&nbsp; last dose at ______ in my ______________"),
         ("Devices", "Sensor: ______________ &nbsp; Pump site: ______________"),
         ("Glucose now", "______ mmol/L &nbsp; &#9744; steady &nbsp; &#9744; rising &nbsp; &#9744; falling"),
         ("Numb areas", "____________________________________________"),
         ("Also", "&#9744; stiff joints &nbsp; &#9744; wounds &nbsp; &#9744; dizzy when standing &nbsp; &#9744; recent eye surgery")],
   asks_h="Please", asks=["No oil, pressure or stretching within a hand’s width of my sensor or pump site.",
        "Skip my recent injection site and pump site — and no heat there (stones, packs, hot towels).",
        "Broad, gentle pressure and no heat on numb areas.",
        "Keep my fast sugar within my reach. Let me sit a moment before I stand."],
   stop="If I say “SUGAR”, stop — I may be going low.",
   low="Signs of a low: confusion, sweating, shaking, sudden quiet. Stop, help me sit up, sugar first. Unconscious or seizing: call 911, nothing by mouth.",
   foot="Education, not medical advice · t1de.krkt.shop · KRKT Library", cut="cut here"),
 "fr": dict(lang="fr-CA", eyebrow="KRKT:T1DE · POUR MON MASSOTHÉRAPEUTE OU ORTHOTHÉRAPEUTE", title="J’ai le diabète de type&nbsp;1",
   rows=[("Insuline", "&#9744; pompe &nbsp; &#9744; injections &nbsp;·&nbsp; dernière dose à ______ dans ______________"),
         ("Appareils", "Capteur&nbsp;: ______________ &nbsp; Site de pompe&nbsp;: ______________"),
         ("Glycémie", "______ mmol/L &nbsp; &#9744; stable &nbsp; &#9744; en hausse &nbsp; &#9744; en baisse"),
         ("Zones engourdies", "____________________________________________"),
         ("Aussi", "&#9744; articulations raides &nbsp; &#9744; plaies &nbsp; &#9744; étourdissements debout &nbsp; &#9744; chirurgie aux yeux récente")],
   asks_h="S’il vous plaît", asks=["Pas d’huile, de pression ni d’étirement à moins d’une main de largeur de mon capteur ou de ma pompe.",
        "Évitez mon site d’injection récent et le site de ma pompe — et pas de chaleur (pierres, compresses, serviettes chaudes).",
        "Pression large et douce, sans chaleur, sur les zones engourdies.",
        "Gardez mon sucre rapide à ma portée. Laissez-moi m’asseoir un moment avant de me lever."],
   stop="Si je dis «&nbsp;SUCRE&nbsp;», arrêtez — je fais peut-être une hypo.",
   low="Signes d’hypo&nbsp;: confusion, sueurs, tremblements, silence soudain. Arrêtez, aidez-moi à m’asseoir, le sucre d’abord. Perte de conscience ou convulsion&nbsp;: 911, rien par la bouche.",
   foot="De l’éducation, pas un avis médical · t1de.krkt.shop · Bibliothèque KRKT", cut="découper ici"),
}
CSS = """@page{size:Letter;margin:0}*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,Helvetica,Arial,sans-serif;background:#fff;color:#1f2630}
.sheet{width:8.5in;height:11in;padding:.35in .45in;display:flex;flex-direction:column;justify-content:space-between}
.card{height:5.05in;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;border:1px solid #e2ddd2}
.top{background:#16202b;color:#f7f4ee;padding:16px 22px 14px}
.eb{font-size:8.5pt;letter-spacing:1.4px;color:#f0a08c;font-weight:600}
h1{font-family:Outfit,Helvetica,Arial,sans-serif;font-size:22pt;font-weight:600;margin-top:4px}
.body{flex:1;background:#f7f4ee;padding:12px 22px 10px;display:flex;gap:16px}
.l{flex:1.05;display:flex;flex-direction:column;gap:9px}.r{flex:1;display:flex;flex-direction:column;gap:8px}
.row b{display:block;font-family:Outfit,sans-serif;font-size:9pt;color:#1f7a6b;letter-spacing:.5px;text-transform:uppercase}
.row span{font-size:10.5pt;line-height:1.55}
.asks{background:#fff;border:1px solid #e2ddd2;border-radius:10px;padding:10px 12px}
.asks h2{font-family:Outfit,sans-serif;font-size:10.5pt;margin-bottom:4px}
.asks li{font-size:9.6pt;line-height:1.4;margin:0 0 3px 14px}
.stop{background:#1f7a6b;color:#f2fbf8;border-radius:10px;padding:9px 12px;font-family:Outfit,sans-serif;font-weight:600;font-size:12pt;line-height:1.3}
.low{background:#c0392b;color:#fff6f3;border-radius:10px;padding:10px 12px;font-size:9.6pt;line-height:1.4}
.ft{background:#f7f4ee;font-size:7.5pt;color:#5c6672;padding:0 22px 10px}
.cut{text-align:center;font-size:7pt;color:#8794a2;border-top:1px dashed #b9b2a5;padding-top:3px;letter-spacing:1px}"""
def card(t):
    rows = "".join(f'<div class="row"><b>{a}</b><span>{b}</span></div>' for a, b in t["rows"])
    asks = "".join(f"<li>{a}</li>" for a in t["asks"])
    return f'''<div class="card"><div class="top"><div class="eb">{t["eyebrow"]}</div><h1>{t["title"]}</h1></div>
<div class="body"><div class="l">{rows}<div class="stop">{t["stop"]}</div></div>
<div class="r"><div class="asks"><h2>{t["asks_h"]}</h2><ul>{asks}</ul></div><div class="low">{t["low"]}</div></div></div>
<div class="ft">{t["foot"]}</div></div>'''
for k, t in T.items():
    html = f'''<!doctype html><html lang="{t["lang"]}"><head><meta charset="utf-8"><title>{t["title"]}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Outfit:wght@500;600&display=swap">
<style>{CSS}</style></head><body><div class="sheet">{card(t)}<div class="cut">✂ {t["cut"]}</div>{card(t)}</div></body></html>'''
    (OUT / f"therapist-card-{k}.html").write_text(html)
print("ok")
