import pathlib, sys, json
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
N = " "
CARDS = {
"en": [
 ("THE NUMBERS", "Six figures behind the advice, without the hype.", [
  ("66%", "of adults with ~31 years of type 1 had a hand or shoulder condition — DCCT/EDIC, Diabetes Care 2014"),
  ("31%", "had frozen shoulder, about five times more likely with diabetes than without"),
  ("~6×", "faster insulin absorption when an injection site was massaged for 30 minutes — Linde 1986"),
  ("+110%", "insulin absorption after two sauna sessions; glucose 3.0–3.3 mmol/L lower — Koivisto 1980"),
  ("~1 in 3", "people with type 1 have lumps at insulin sites (lipohypertrophy) a therapist may spot first"),
  ("0", "professional orders for massage therapy or orthotherapy in Québec — titles aren't protected")]),
 ("HONEST CLAIMS", "What massage can promise someone with type 1 — and what it can't.", [
  ("Supported", "Feeling calmer: single sessions lowered anxiety, blood pressure and heart rate (37 trials)"),
  ("Low-quality support", "Joint mobilisation + exercise for frozen shoulder in diabetes (8 trials)"),
  ("Disputed", "“Lowers cortisol.” A stricter meta-analysis found the effect indistinguishable from zero"),
  ("Not shown", "Treating diabetes. Glucose drops after massage are likely just faster insulin absorption"),
  ("Not shown", "Preventing complications by “improving circulation.” No guideline lists it"),
  ("The honest pitch", "Go because it feels good and helps you move — not to treat diabetes")]),
 ("INSULIN & HEAT", "A working hand, a hot stone and a busy muscle all speed up a recent dose.", [
  ("Massage", "Rubbing a recent injection site sends insulin into the blood faster"),
  ("Heat", "Sauna, hot stones, heat packs, hot tubs: same direction, measurable effect"),
  ("Muscle", "Leg exercise after a leg injection: +135% absorption in ten minutes"),
  ("Do", "Don't inject where you're about to be worked on. Skip recent sites and the pump site"),
  ("Check", "Glucose before and after — at least the first two or three sessions (FQM)"),
  ("Treat", "15 g fast sugar, recheck in 15 minutes. Unconscious: 911, nothing by mouth")]),
 ("SENSORS & PUMPS", "An hour of someone else's hands near your devices.", [
  ("Compression lows", "Pressure on a CGM can show a sudden low that isn't real. Confirm with a finger prick"),
  ("Don't dismiss it", "A real low can look like compression. When in doubt, prick"),
  ("No oil", "Dexcom and Abbott warn lotion stops adhesive holding. Keep a hand's width clear"),
  ("Show them", "Point out the sensor and infusion set before you lie down"),
  ("Pump in reach", "If you disconnect, agree with your team how long — and reconnect before you leave"),
  ("Alarms", "A sensor alarm mid-session is not an interruption to apologise for")]),
 ("TELL YOUR THERAPIST", "Two minutes before you lie down does most of the safety work.", [
  ("1 · Insulin", "Pump or injections — last dose, when and where"),
  ("2 · Devices", "Sensor here, pump site here. No oil, pressure or stretching on them"),
  ("3 · Glucose", "The number right now, and whether it's steady, rising or falling"),
  ("4 · The word", "If I say “sugar”, stop — I may be going low"),
  ("5 · Numb areas", "Broad pressure, no heat — stones and hot towels can burn skin that can't feel"),
  ("6 · Getting up", "Let me sit on the edge of the table before I stand")]),
 ("CHOOSING IN QUÉBEC", "Where the patient does the checking an order would do elsewhere.", [
  ("Unregulated", "Massage therapy and orthotherapy have no professional order in Québec"),
  ("Check membership", "FQM, Mon Réseau Plus and RITMA publish member directories"),
  ("Receipts", "Insurers want a member of an association they recognise. Check their list first"),
  ("RAMQ", "Doesn't cover massage or orthotherapy"),
  ("Taxes", "Massage doesn't count for the federal medical expense credit in Québec. Physio does"),
  ("Ask", "“Have you worked with clients who use insulin, a pump or a sensor?”")]),
],
"fr": [
 ("LES CHIFFRES", "Six chiffres derrière les conseils, sans le battage.", [
  (f"66{N}%", f"des adultes avec ~31{N}ans de type{N}1 avaient un problème à la main ou à l'épaule — DCCT/EDIC, Diabetes Care 2014"),
  (f"31{N}%", "avaient une capsulite, environ cinq fois plus probable avec le diabète"),
  ("~6×", f"absorption plus rapide de l'insuline après 30{N}minutes de massage du site — Linde 1986"),
  (f"+110{N}%", f"d'absorption après deux séances de sauna; glycémie 3,0 à 3,3{N}mmol/L plus basse — Koivisto 1980"),
  ("~1 sur 3", f"personnes avec le type{N}1 ont des bosses aux sites d'insuline (lipohypertrophie)"),
  ("0", "ordre professionnel pour la massothérapie ou l'orthothérapie au Québec — titres non protégés")]),
 ("PROMESSES HONNÊTES", f"Ce que le massage peut promettre avec le type{N}1 — et ce qu'il ne peut pas.", [
  ("Appuyé", f"Se sentir plus calme{N}: anxiété, tension et fréquence cardiaque réduites (37{N}essais)"),
  ("Appui faible", f"Mobilisation + exercice pour la capsulite avec le diabète (8{N}essais)"),
  ("Contesté", f"«{N}Baisse le cortisol.{N}» Une méta-analyse rigoureuse ne trouve aucun effet mesurable"),
  ("Non démontré", "Traiter le diabète. La baisse de glycémie vient sans doute d'une insuline absorbée plus vite"),
  ("Non démontré", f"Prévenir les complications en «{N}améliorant la circulation{N}»"),
  ("L'argument honnête", "On y va parce que ça fait du bien et que ça aide à bouger — pas pour traiter le diabète")]),
 ("INSULINE ET CHALEUR", "Une main qui travaille, une pierre chaude et un muscle actif accélèrent une dose récente.", [
  ("Massage", "Frotter un site d'injection récent fait passer l'insuline plus vite dans le sang"),
  ("Chaleur", "Sauna, pierres chaudes, compresses, spa : même effet, mesurable"),
  ("Muscle", f"Exercice des jambes après une injection dans la cuisse{N}: +135{N}% en dix minutes"),
  ("À faire", "N'injectez pas là où on va travailler. Évitez les sites récents et celui de la pompe"),
  ("Vérifier", "Glycémie avant et après — au moins les deux ou trois premières séances (FQM)"),
  ("Traiter", f"15{N}g de sucre rapide, revérifier après 15{N}minutes. Inconscient{N}: 911"),]),
 ("CAPTEURS ET POMPES", "Une heure de mains étrangères près de vos appareils.", [
  ("Fausses hypos", "Une pression sur le capteur peut afficher une baisse irréelle. Confirmez au glucomètre"),
  ("Sans balayer", "Une vraie hypo peut ressembler à une compression. Dans le doute, piquez"),
  ("Pas d'huile", "Dexcom et Abbott : la lotion empêche l'adhésif de tenir. Une main de largeur libre"),
  ("Montrez-les", "Montrez le capteur et le cathéter avant de vous allonger"),
  ("Pompe à portée", "Si vous la débranchez, convenez de la durée avec votre équipe — et rebranchez"),
  ("Alarmes", "Une alarme pendant la séance n'est pas une interruption dont il faut s'excuser")]),
 ("QUOI DIRE AU THÉRAPEUTE", "Deux minutes avant de vous allonger font l'essentiel du travail de sécurité.", [
  ("1 · Insuline", "Pompe ou injections — dernière dose, quand et où"),
  ("2 · Appareils", "Capteur ici, pompe ici. Pas d'huile, de pression ni d'étirement"),
  ("3 · Glycémie", "Le chiffre actuel, et s'il est stable, en hausse ou en baisse"),
  ("4 · Le mot", f"Si je dis «{N}sucre{N}», arrêtez — je fais peut-être une hypo"),
  ("5 · Zones engourdies", "Pression large, pas de chaleur — une peau qui ne sent rien peut brûler"),
  ("6 · Se relever", "Laissez-moi m'asseoir au bord de la table avant de me lever")]),
 ("CHOISIR AU QUÉBEC", "Le patient fait les vérifications qu'un ordre ferait ailleurs.", [
  ("Non réglementé", "Ni la massothérapie ni l'orthothérapie n'ont d'ordre professionnel au Québec"),
  ("Vérifiez", "La FQM, Mon Réseau Plus et RITMA publient des répertoires de membres"),
  ("Reçus", "Les assureurs exigent un membre d'une association reconnue. Vérifiez leur liste"),
  ("RAMQ", "Ne couvre ni la massothérapie ni l'orthothérapie"),
  ("Impôts", "Au Québec, pas de crédit fédéral pour frais médicaux pour le massage. La physio, oui"),
  ("Demandez", f"«{N}Avez-vous déjà traité des clients avec une pompe, un capteur ou de l'insuline?{N}»")]),
]}
CSS = """*{margin:0;padding:0;box-sizing:border-box}html,body{width:1280px;height:1152px;background:#000}
body{font-family:Inter,Helvetica,Arial,sans-serif;color:#f4efe8;padding:88px 84px 0;position:relative}
.eb{font-size:17px;letter-spacing:5px;font-weight:600;color:#b9b4ad}
h1{font-size:50px;font-weight:800;letter-spacing:-1px;margin-top:14px;line-height:1.05}
.bar{width:120px;height:6px;background:#e0306f;margin-top:10px}
.sub{font-size:21px;color:#cfcac3;margin-top:36px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:64px}
.t{background:#0c0c0c;border:1px solid #262626;padding:26px 28px;min-height:150px}
.t b{display:block;font-size:34px;font-weight:800;color:#e0306f;letter-spacing:-.5px;line-height:1.1}
.t b.w{font-size:24px}
.t p{font-size:18px;line-height:1.45;color:#cfcac3;font-weight:600;margin-top:10px}
.ft{position:absolute;left:84px;right:84px;bottom:150px;border-top:1px solid #222;padding-top:30px;text-align:center}
.ft .a{font-size:17px;letter-spacing:6px;font-weight:700;color:#8d8882}
.ft .b{font-size:14px;letter-spacing:2px;color:#5f5b56;margin-top:16px}"""
names = []
for lang, cards in CARDS.items():
    for i, (title, sub, tiles) in enumerate(cards, 1):
        lib = "KRKT LIBRARY" if lang == "en" else "BIBLIOTHÈQUE KRKT"
        cls = "" if all(len(h) < 9 for h, _ in tiles) else "w"
        tl = "".join(f'<div class="t"><b class="{cls}">{h}</b><p>{p}</p></div>' for h, p in tiles)
        html = f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"><style>{CSS}</style></head>
<body><div class="eb">{lib} — DETAIL 0{i}/06 — T1DE-07</div><h1>{title}</h1><div class="bar"></div><p class="sub">{sub}</p>
<div class="grid">{tl}</div><div class="ft"><div class="a">KRKT, PHR0ZT, MANJARO, ARCH, CLAUDE</div>
<div class="b">krkt.shop · t1de.krkt.shop · {lib} — T1DE-07</div></div></body></html>'''
        slug = title.lower().replace(" & ", "-").replace(" ", "-").replace("é", "e").replace("ê", "e")
        name = f"KRKT-T1DE-07_{lang.upper()}_Card-0{i}_{slug}"
        (OUT / f"{name}.html").write_text(html); names.append(name)
json.dump(names, open(OUT / "index.json", "w"))
print(len(names), "cards")
