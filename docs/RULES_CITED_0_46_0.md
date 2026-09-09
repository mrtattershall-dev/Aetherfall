# Rules cited in the source — derived census at 0.46.0

> **This is NOT the rules index.** `docs/RULES_INDEX.md` has never existed
> in this repository, and two addendum files amend an index that is not
> here. This document is *derived from the build*: every `AF-R-###` the
> code actually cites, with where and how. It cannot say what a rule
> MEANS, or whether it is LOCKED or FLEXIBLE — only the Bible can, and
> the Bible is not in the repo.
>
> Its one job is to make the gap measurable. Until now, "cited but not
> indexed" and "indexed but not cited" were both unanswerable. Half of
> that is answered below; supply the index and the other half follows.

**89 distinct rules**, **839 citations**, **21 machine-enforced** — those appear in an
`AF.rules.refuse/require/forbid` call, so breaking them stops the build or
refuses the action. The other 68 are cited in reasoning only: nothing fails
when the code drifts from them, which makes them the ones worth reading
against the Bible first.

## Enforced — a refusal fires

| rule | cites | what the refusal says |
|---|---|---|
| `AF-R-102` | 19 | Cannot register unknown mode "${name}". |
| `AF-R-203` | 19 | ${id}" is both approved and provisional |
| `AF-R-311` | 3 | AF.const.TILE === before && AF.const.TILE === 64, |
| `AF-R-401` | 4 | canvas.width === V.W && canvas.height === V.H, |
| `AF-R-402` | 5 | ctx.imageSmoothingEnabled === false, |
| `AF-R-605` | 7 | Every interactable needs a string id. |
| `AF-R-611` | 5 | NPC "${id}" declares no lines |
| `AF-R-622` | 12 | unknown authored encounter "${id} |
| `AF-R-702` | 5 | unknown command "${o?.type}". Grammar: ${COMMANDS.join(" / ")} |
| `AF-R-707` | 8 | problems.join("; ") |
| `AF-R-711` | 57 | enemy "${def.id}" has no base stats — numbers must be data |
| `AF-R-803` | 36 | Item "${it.id}" has kind "${it.kind}". Kinds: ${KINDS.join(", ")}. |
| `AF-R-812` | 14 | AF.state.integrity === AF.state.integrity, |
| `AF-R-821` | 7 | Quest "${q.id}" needs at least one step. |
| `AF-R-903` | 28 | unknown element "${element}" — define it before using it |
| `AF-R-904` | 63 | stat "${def.id}" already defined |
| `AF-R-905` | 34 | stat id "${def.id}" is not snake_case |
| `AF-R-922` | 3 | Animation "${def.id}" has no frame rectangles. |
| `AF-R-1001` | 11 | ascension node "${n.id}" names icon "${n.icon}", which has no atlas rect |
| `AF-R-1010` | 10 | A story flag needs a non-empty string id. |
| `AF-R-1011` | 12 | Text "${id}" must be a string, got ${typeof line}. |

## Cited in reasoning only — no machine check

| rule | cites | where it is first invoked |
|---|---|---|
| `AF-R-201` | 6 | L613: …06 · REGISTRY — stable IDs and canon control (AF-R-201, AF-R-905)… |
| `AF-R-202` | 2 | L637: …// AF-R-202: canon:true requires a named human approval. No approval, no canon.… |
| `AF-R-301` | 1 | L3531: …NIGHT GRADE (AF-R-301)… |
| `AF-R-302` | 1 | L19164: …0.16.0 — BIRDS (AF-R-302, AF-R-611 spirit: a place that is alive).… |
| `AF-R-303` | 10 | L2074: …AF-R-303 marks biome palettes FLEXIBLE and packs bind to regions.… |
| `AF-R-312` | 1 | L480: …// AF-R-312: 64x64 is a placement standard, not a universal asset size.… |
| `AF-R-313` | 1 | L481: …// AF-R-313: 40px/56px art is valid; only the world GRID is fixed.… |
| `AF-R-314` | 3 | L573: …asset, and AF-R-314 then demanded it be a multiple of the 32px… |
| `AF-R-315` | 1 | L458: …HALF_GRID: 32, // AF-R-315 — permitted placement increment… |
| `AF-R-321` | 2 | L537: …// AF-R-321 / AF-R-323 — art bounds are separate from the cell and smaller… |
| `AF-R-322` | 5 | L3051: …Footprint convention (AF-R-322 / AF-R-341): a prop's ground footprint is… |
| `AF-R-323` | 3 | L462: …// AF-R-323 — visible humanoid body inside that cell, not the cell itself… |
| `AF-R-331` | 24 | L546: …// AF-R-331 — collision is never the sprite rectangle… |
| `AF-R-332` | 3 | L465: …// AF-R-332 — foot collision, deliberately much smaller than the cell… |
| `AF-R-341` | 7 | L1923: …(AF-R-341 — art extends beyond footprint). Collision is authored per asset,… |
| `AF-R-342` | 1 | L3384: …13 · DEPTH (AF-R-342)… |
| `AF-R-403` | 1 | L3403: …14 · CAMERA (AF-R-401, AF-R-402, AF-R-403)… |
| `AF-R-404` | 2 | L468: …// AF-R-404 FLEXIBLE — logical viewport. 960x540 = 15 x 8.44 tiles.… |
| `AF-R-405` | 21 | L1298: …ATLAS — measured, embedded, verified (AF-R-911, AF-R-1001, AF-R-405)… |
| `AF-R-503` | 2 | L3101: …// --- AF-R-521: an authored road must stay walkable (AF-R-503) -----------… |
| `AF-R-505` | 5 | L674: …// AF-R-505 — the one settlement the Bible already establishes as canon.… |
| `AF-R-511` | 2 | L2947: …11 · AUTHORING — Rowan's Hold constraints (AF-R-511 … AF-R-518)… |
| `AF-R-512` | 7 | L2981: …spawnClearance: 4, // AF-R-512… |
| `AF-R-513` | 4 | L3003: …/* AF-R-513 / AF-R-514 / AF-R-517 / AF-R-822.… |
| `AF-R-514` | 2 | L3003: …/* AF-R-513 / AF-R-514 / AF-R-517 / AF-R-822.… |
| `AF-R-515` | 2 | L3035: …// AF-R-515 — one landmark per region… |
| `AF-R-516` | 2 | L2982: …npcMinDegree: 3, // AF-R-516… |
| `AF-R-517` | 1 | L3003: …/* AF-R-513 / AF-R-514 / AF-R-517 / AF-R-822.… |
| `AF-R-518` | 4 | L2947: …11 · AUTHORING — Rowan's Hold constraints (AF-R-511 … AF-R-518)… |
| `AF-R-519` | 9 | L3044: …PLACEMENT VALIDATION — AF-R-519 … AF-R-522 (ADOPTED 2026-09-03)… |
| `AF-R-520` | 3 | L3081: …// --- AF-R-520: a thing must stand somewhere that exists -----------------… |
| `AF-R-521` | 22 | L2798: …questions, as with ROAD_UNDER and AF-R-521, `placement` vs `drawSize`,… |
| `AF-R-522` | 6 | L3044: …PLACEMENT VALIDATION — AF-R-519 … AF-R-522 (ADOPTED 2026-09-03)… |
| `AF-R-524` | 15 | L3199: …Adopted as AF-R-524 (2026-09-03). Shadowing is reported as a note, not a… |
| `AF-R-602` | 1 | L485: …MOVEMENT_MODEL: "free", // AF-R-602 FLEXIBLE: 'free' \| 'grid' \| 'hybrid'… |
| `AF-R-612` | 1 | L460: …CELL: Object.freeze({ W: 64, H: 64 }), // AF-R-612 default actor cell… |
| `AF-R-613` | 1 | L2295: …08 · ANIMATION (AF-R-613, AF-R-921 … AF-R-924)… |
| `AF-R-621` | 2 | L3831: …17 · MODE (AF-R-102, AF-R-621, AF-R-701)… |
| `AF-R-701` | 2 | L3831: …17 · MODE (AF-R-102, AF-R-621, AF-R-701)… |
| `AF-R-703` | 2 | L5267: …/* FLEXIBLE (AF-R-703, stated per AF-R-802): initiative is a single AGI-sorted… |
| `AF-R-704` | 2 | L5163: …· AF-R-704 / AF-R-705 — both named a battle draw path and an effect layer… |
| `AF-R-705` | 2 | L5163: …· AF-R-704 / AF-R-705 — both named a battle draw path and an effect layer… |
| `AF-R-706` | 2 | L958: …ipment: def.equipment \|\| {}, // slot -> item id; slots are open (AF-R-706 spirit)… |
| `AF-R-708` | 4 | L5880: …"AF-R-708 combat readability was unverifiable until 0.43.0; the device then reported that with a full party the… |
| `AF-R-709` | 5 | L4121: …already tracks for exactly this purpose (AF-R-709). */… |
| `AF-R-710` | 9 | L5168: …· AF-R-710 — defeat is handled explicitly, not implied by a party of… |
| `AF-R-801` | 43 | L37: …07b STATS the only home for a stat formula (AF-R-801)… |
| `AF-R-802` | 54 | L782: …FLEXIBLE choices made here, stated as AF-R-802 requires:… |
| `AF-R-811` | 5 | L2872: …integrity: 100, // AF-R-811 shard / seal integrity… |
| `AF-R-813` | 3 | L2865: …flags: { // AF-R-813: boss flags are the act model… |
| `AF-R-814` | 2 | L680: …// AF-R-814 — areas the Bible marks UNDEFINED. Listed so they stay visible as… |
| `AF-R-822` | 1 | L3003: …/* AF-R-513 / AF-R-514 / AF-R-517 / AF-R-822.… |
| `AF-R-911` | 13 | L572: …/* 0.13.8 — AF-R-911 demanded a WORLD placement from every declared… |
| `AF-R-912` | 1 | L725: …07 · ASSETS (AF-R-911, AF-R-912, AF-R-1001, AF-R-1006)… |
| `AF-R-921` | 18 | L1944: …measured 6-frame swing (AF-R-921). place/collision measured against the new… |
| `AF-R-923` | 16 | L1247: …AF-R-923 asks for instead of a look at the picture.… |
| `AF-R-924` | 3 | L2295: …08 · ANIMATION (AF-R-613, AF-R-921 … AF-R-924)… |
| `AF-R-931` | 11 | L3980: …18 · SAVE (AF-R-931, AF-R-932)… |
| `AF-R-932` | 14 | L3919: …silently defaulting, matching AF-R-932's spirit for the field it… |
| `AF-R-941` | 6 | L2703: …an undeclared rect is invisible to "used" (AF-R-941).… |
| `AF-R-942` | 1 | L12280: …t("a seeded roll reproduces exactly (AF-R-942 spirit / determinism)", () => {… |
| `AF-R-1002` | 3 | L2250: …keeps reporting the gap rather than letting it disappear (AF-R-1002).… |
| `AF-R-1003` | 2 | L3884: …AF-R-1003 exists to prevent.… |
| `AF-R-1004` | 6 | L5144: …19 · SELFTEST (AF-R-1004, AF-R-1005)… |
| `AF-R-1005` | 7 | L371: …be the thing that breaks the build (AF-R-1005). */… |
| `AF-R-1006` | 28 | L15: …unverified draws as a labelled placeholder box, on purpose (AF-R-1006).… |
| `AF-R-1007` | 18 | L2805: …seal_custodian -> knight is the user's call (AF-R-1007), taken on the… |
| `AF-R-1012` | 8 | L4333: …/* 0.6.18 — AF-P-001..004 were ADOPTED as AF-R-1010, AF-R-1011, AF-R-1012 and… |

---

Generated by `tools/rules-census.py` from `aetherfall.html` at 0.46.0.
