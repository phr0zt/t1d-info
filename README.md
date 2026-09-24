# t1d-info

Patient-education slide decks about **type 1 diabetes**, written for newly diagnosed
people and for the family, friends, coworkers and coaches around them.

Canadian (Québec) context throughout: mmol/L, Diabetes Canada guidance, 911, and
Québec-specific helplines and coverage rules.

---

## The decks

| # | Deck | Slides | What it covers |
|---|------|--------|----------------|
| 00 | **Master** | 28 | The whole picture in one pass: what type 1 is, the two emergencies, the three daily levers, everything that interferes, the long game, and the people around you. Starts here. |
| 01 | **Food** | 21 | There is no diabetic diet. Food groups by speed, the delayed fat/protein rise, insulin timing, glycemic index, fibre, Canadian Nutrition Facts labels, celiac, hosting, kids' parties. |
| 02 | **Movement** | 22 | Why exercise moves glucose in both directions, starting ranges, insulin reduction, fuelling, the 7–11 hour overnight tail, competition adrenaline, kit, and what coaches need. |
| 03 | **Medications** | 20 | Steroids, beta blockers, SGLT2 inhibitors and euglycemic DKA, sick-day hold lists, CGM interference, glucagon, and the questions to ask before starting anything. |
| 04 | **Drugs and alcohol** | 22 | Harm reduction, not a lecture. Nicotine, cannabis, alcohol, stimulants, MDMA, psychedelics, mixing, travel numbers. |
| 05 | **Complications** | 24 | DCCT/EDIC evidence, each complication plainly, how far the rates have fallen, the Canadian screening schedule, and why outcomes are not a verdict on effort. |
| 06 | **Portable archive** | 143 | All six decks concatenated in order, separated by blank divider slides, for archiving and later builds. |

Total: **137 unique slides**, plus 6 blank dividers in the archive.

---

## Repository layout

Each deck mirrors the layout used by the Claude Slides artifact type, so a deck can be
re-published without any transformation:

```
decks/<nn>-<name>/
  project/
    deck.json           index: title, slide order, section outline, typefaces
    slides/<id>.html    one <section> per slide, 1920×1080, all styles inline
```

`deck.json` fields:

- `order` — slide ids in presentation order
- `sections` — outline; each entry is a one-sentence description and the id it starts at
- `faces` — typefaces (Outfit for display, Inter for text, both from Google Fonts)

In the portable archive every slide id carries a deck prefix so the six decks can
coexist in one index: `m-` master, `f-` food, `mv-` movement, `rx-` medications,
`dg-` drugs, `cx-` complications, plus `blank-1` … `blank-6`.

Speaker notes live in a single `<aside>` as the last child of each `<section>`.

---

## Design system

One palette and one type scale across every deck.

| Token | Hex | Use |
|---|---|---|
| Ink | `#16202b` | Dark backgrounds, headings on light |
| Paper | `#f7f4ee` | Light backgrounds |
| Card | `#ffffff` | Cards on paper |
| Panel | `#243141` | Cards on ink |
| Body on paper | `#4b5560` / `#37414d` | Body text |
| Body on ink | `#c3ccd6` | Body text |
| Accent red | `#c0392b` | Warnings, statement slides |
| Accent teal | `#1f7a6b` | Do-this, positive framing |
| Eyebrow | `#f0a08c` | Labels on ink |
| Muted footer | `#5c6672` / `#8794a2` | Source lines |

Type scale: 120 / 112 / 68 / 44 / 32 / 28 / 24 px.
Display face **Outfit** (600), text face **Inter**.

---

## Editorial rules

These are deliberate and worth keeping if you extend the set.

1. **Risk language, never certainty.** "Lowers the risk of", never "will cause".
   Published guidance (dStigmatize, ADA 2017, Diabetes Canada *Language Matters*)
   is explicit that absolutist framing adds shame and disengagement.
2. **No fear-based messaging and no graphic imagery.** No wound or amputation
   photographs anywhere, by design.
3. **Never "control", "compliant", "good/bad blood sugar".** Use "manage",
   "in/outside target range", and the actual numbers.
4. **Every historical rate is paired with its trend.** Most published complication
   figures come from cohorts diagnosed 1950–1990 and badly mislead on their own.
5. **Disagreements are shown, not hidden.** Where bodies genuinely differ —
   glycemic index, sugar alcohol subtraction, the A1C effect of exercise — the deck
   says so and names both positions.
6. **Evidence grades are stated** where a recommendation rests on weak evidence.
7. **Complications are never framed as a verdict on effort.**

---

## Sources

Diabetes Canada Clinical Practice Guidelines · Diabète Québec · DCCT (NEJM 1993) ·
EDIC (NEJM 2005, JAMA 2015, Diabetes Care 2016) · Battelino et al., Diabetes Care 2019
(time in range) · Riddell et al., Lancet Diabetes & Endocrinology 2017 (exercise
consensus) · ISPAD 2022 · ADA Standards of Care · Wolpert et al., Diabetes Care 2013 ·
Rawshani et al., Diabetes Care 2022 · Canadian Food Inspection Agency · Health Canada ·
NDSS Australia · Breakthrough T1D · dStigmatize · Diabetes Canada *Language Matters*

Per-slide sources appear in the footer of the slide that uses them.

---

## Known gaps

- Diabetes Canada updated its chronic kidney disease chapter in 2025; the screening
  intervals here follow the stable structure but the 2025 full text was not readable
  at build time.
- Time-in-range targets are the adult figures. Children, older adults and pregnancy
  have their own; verify against the primary paper before adding them.
- Periodontal disease is treated qualitatively — the primary sources were not
  reachable at build time.

---

## Licence and use

Patient education, not medical advice. Doses, ratios and targets belong with a
person's own diabetes team. If you reuse this, keep the editorial rules above —
they are the part that makes it safe.
