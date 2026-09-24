# KRKT:T1DE — content spec

Site: **KRKT's Type 1 Diabetes Education**, from the KRKT Library (alias `KRKT:T1DE`).
French name: **L'éducation sur le diabète de type 1 de KRKT**, de la Bibliothèque KRKT.
Bilingual: English (`en`) and Québec French (`fr`). Québec context throughout.

Source material: `build/slides/<deck>.json` (extracted from `decks/<deck>/project/slides/*.html`).
Each slide has `heading`, `body` (light Markdown; `[card:warning|do|dark]` … `[/card]` marks a
coloured card on the slide), `footer` (sources and caveats), `note` (speaker note), `section`.

## Where pages go

```
site/src/content/pages/en/<topic>/<slug>.md
site/src/content/pages/fr/<topic>/<slug-fr>.md
```

Every topic folder has an `index.md` (the topic's landing page: a short intro, 80–200 words,
that sets up the pages below it; the site lists the child pages automatically — do not
hand-write a list of links).

| Topic key | EN folder | FR folder | Written from |
|---|---|---|---|
| start | `start` | `commencer` | 00-master (overview sections) |
| emergencies | `emergencies` | `urgences` | 00-master (`two`, `hypo`, `glucagon`, `dka`, `sick`) |
| food | `food` | `alimentation` | 01-food |
| movement | `movement` | `activite-physique` | 02-movement |
| medications | `medications` | `medicaments` | 03-medications |
| drugs-alcohol | `drugs-alcohol` | `drogues-alcool` | 04-drugs-alcohol |
| complications | `complications` | `complications` | 05-complications |
| people | `people` | `entourage` | 00-master (`people`, `language`, `distress`, `notfailure`) |
| help | `help` | `aide` | 00-master `help`, `library` + every deck's `help` slide |

## Frontmatter (all fields required unless marked optional)

```yaml
---
title: "Reading a Canadian Nutrition Facts table"
description: "One sentence, ≤155 characters, plain language — used for search results and cards."
topic: food               # topic key from the table above (same in both languages)
order: 4                  # position within the topic; index.md is 0
translationKey: food/labels   # identical in the EN and FR file — this is how the pair is linked
sources:
  - "Canadian Food Inspection Agency"
  - "Diabète Québec"
reviewed: 2026-09-24
---
```

Slugs: EN kebab-case English, FR kebab-case French without accents (`lire-une-etiquette`).
`translationKey` is `<topic>/<english-slug>` in **both** files.

## Page shape

- One page per deck section, or per 3–6 closely related slides. 350–1200 words. Slides that
  are only a cover or a "how to use this deck" become part of the topic `index.md`.
- Write for the web: an opening paragraph that says what the page answers, then `##` headings.
  No `#` H1 in the body (the title is rendered from frontmatter).
- The speaker notes are the best material in the decks — fold them into the prose.
- Footers carry caveats as well as sources: caveats go into the text, source names go into `sources`.
- Keep every number exactly as the slide gives it. Do not add new clinical numbers, doses or
  claims that are not in the source slides. If a transition sentence needs a fact, leave it out.
- Units: mmol/L. EN uses decimal point (3.9); **FR uses decimal comma (3,9 mmol/L)** and a
  non-breaking space before units and %: `3,9 mmol/L`, `70 %`.

## Callouts and stat cards (remark directives)

```md
:::warning[Never add the sugars line]
Sugars are already counted inside Carbohydrate…
:::

:::do[Subtract fibre in full]
…
:::

:::note
A neutral aside, or where bodies disagree.
:::

:::emergency[Call 911 if]
- they can't swallow safely
- …
:::

:::stats
- **>70%** time in range, 3.9 to 10.0 — about 17 hours a day
- **<4%** below 3.9 — about an hour
:::
```

Map slide cards: `[card:warning]` → `:::warning`, `[card:do]` → `:::do`, `[card:dark]` → `:::note`
(or plain prose if it reads better). Use `:::emergency` only for "act now" instructions
(hypo treatment, glucagon, DKA signs, when to call 911). Use `:::stats` for big-number slides.
Don't overuse callouts — at most ~3 per page besides stats.

## Editorial rules (from the README — non-negotiable)

1. Risk language, never certainty: "lowers the risk of", never "will cause".
2. No fear-based messaging and no graphic descriptions.
3. Never "control", "compliant/non-compliant", "good/bad blood sugar", "diabetic" as a noun.
   Use "manage", "in/outside target range", the actual numbers, "person with diabetes".
4. Every historical rate is paired with its trend.
5. Disagreements are shown, not hidden — name both positions.
6. State evidence grades where a recommendation rests on weak evidence.
7. Complications are never a verdict on effort.
8. Education, not medical advice: doses, ratios and targets belong with the person's own team.

## Québec French (FR-QC)

Translate for a Québec reader, not a France reader. Natural, warm, plain-language Québécois
professional register (the tone of Diabète Québec), tutoiement **no** — use *vous*.
Inclusive but light: prefer epicene wording ("les personnes", "l'entourage") over "·e".

Glossary (use consistently):

| EN | FR-QC |
|---|---|
| blood sugar / blood glucose | glycémie |
| low / hypo | hypoglycémie (« hypo ») |
| high | hyperglycémie |
| DKA | acidocétose diabétique (ACD) |
| time in range | temps dans la cible |
| target range | cible glycémique / zone cible |
| CGM | capteur de glucose en continu (CGM / surveillance du glucose en continu) |
| A1C | A1C (hémoglobine glyquée) |
| carbohydrate(s) | glucides |
| Nutrition Facts table | tableau de la valeur nutritive |
| sick days | jours de maladie |
| diabetes team | équipe de soins en diabète |
| insulin-to-carb ratio | ratio insuline:glucides |
| rapid-acting / long-acting insulin | insuline à action rapide / à action prolongée |
| person with type 1 | personne vivant avec le diabète de type 1 |
| pharmacist | pharmacien ou pharmacienne |
| coach | entraîneur ou entraîneuse |
| harm reduction | réduction des méfaits |

Keep proper names in their official form: Diabète Québec, Diabetes Canada → **Diabète Canada**,
Santé Canada, Agence canadienne d'inspection des aliments, Info-Santé 811, 911, RAMQ.
Québec typography: « guillemets » with non-breaking spaces, a space before `:`,
no space before `; ! ?`.

## French slides (for the FR PowerPoint download)

For each slide `decks/<deck>/project/slides/<id>.html`, write
`decks/<deck>/project/slides-fr/<id>.html`: identical markup, attributes and inline styles —
translate only the text nodes and the `<aside>` note. If French runs longer, you may shorten the
wording, but do not change styles or layout. Keep the 1920×1080 design intact.
