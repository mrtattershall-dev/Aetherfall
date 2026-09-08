# Where the paperwork stands at 0.34.0

The five documents in this repo describe builds 0.6.19, 0.7.0, 0.7.3, 0.9.0 and
0.9.3. The build on disk is **0.34.0**. That is a gap of roughly twenty-five
versions, so this file records what was re-measured against `aetherfall.html`
itself rather than what the documents assert.

Method: static measurement of the file (grep/awk over the source). Anything
needing a running canvas — self-test tallies, `AF.text.placeholders()`,
`AF.credits.inUse()`, collision solidity — is marked **not re-measured** and
still carries its 0.9.3 figure.

---

## Re-measured, and changed since 0.9.3

| Thing | 0.9.3 | 0.34.0 |
|---|---|---|
| Atlas | 512×1755, 295 rects | **512×2764, 730 rects** |
| Scenes registered | 5 | **7** (`inn_interior`, `inn_interior_room` added) |
| Arrival ids | 4 kinds | 7 — `from_barrow from_chapel from_forest from_guildhall from_hold from_inn from_shop` |
| Distinct `AF-R-###` cited in code | 88 | **89** |
| `AF.rules.refuse` call sites | — | 141 |
| `AF.rules.require` call sites | — | 10 |
| `AF.rules.forbid` call sites | — | 2 |
| `t("…")` test declarations in source | — | 381 |
| File | 1068 KB | 2771 KB (base64 atlas ≈ 1055 KB of it) |

Atlas integrity re-checked and **clean**: no zero-sized rect, no rect out of
bounds, no two rects sharing identical coordinates, and the maximum extent of
all 730 rects is exactly 512×2764 — the declared atlas size to the pixel, so no
packed row is wasted.

> **Correction.** This table first read *546 rects*. That came from a
> line-anchored `grep`, which silently missed the 184 rects that share a line
> with another. The figure above is a real parse of the `RECTS` table
> (`tools/atlas-report.py`), cross-checked against the decoded atlas image.
> The other atlas figures were unaffected.

## Closed since the audits were written

- **`bld_chapel` is gone.** The 0.9.3 audit called it 87% of all dead atlas
  weight, deferred to "the next atlas pass". That pass happened — zero
  occurrences remain.
- **AF-R-512's impossible threshold.** The audit's most substantive finding was
  that spawn clearance asked for 10 tiles, which no interior can satisfy.
  `spawnClearance` is now **4**, and the check is explicitly `report-only`.
  The rule was made satisfiable rather than ignored.
- **AF-R-622 / `AF.encounter`** — real since 0.7.0, 26 references now.
- **`AF.data`** (AF-R-803) — 78 references.
- **`AF.battle.draw`** (AF-R-704) — present.

## Still open, carried across every version

| Finding | First recorded | State at 0.34.0 |
|---|---|---|
| **`AF-R-601` names `AF.player.step`; movement is `AF.sceneKit.walk`** | 0.6.19 | **still true.** `AF.player` has **zero** occurrences; `AF.sceneKit.walk` has 7. Recorded in seven consecutive versions up to 0.9.3, and unaddressed in every version since. It is a §31 index amendment and remains the user's call. |
| **`AF-R-705` / `AF.effects`** — no effect layer | 0.6.19 | **zero occurrences.** Phantom. |
| **`AF-R-942` / `AF.perf`** | 0.6.19 | **zero occurrences.** Phantom. |
| **Negative money loads silently** | 0.9.3 | not re-measured; no clamp or refusal on `money` found in the save path by inspection. The wider question — every other numeric field in the save envelope — was never opened. |
| **Rendering is checked by execution, not appearance** | 0.6.19, restated 0.9.3 | unchanged by anything static. The three bugs 0.9.3 existed to chase were all of this kind, and only a phone caught them. |
| **15 indexed-but-uncited rules never reviewed one at a time** | 0.6.19 (as 26) | **cannot be checked here** — see below. |

## The document that is missing, and why it matters most

**`docs/RULES_INDEX.md` is not in this repo.** The build's own header comment
points at it (`Rule IDs (AF-R-###) refer to docs/RULES_INDEX.md`), all five
uploaded documents measure against it, and it is the one file none of them is.

Its absence blocks the single check the 0.7.0 addendum is most emphatic about.
That addendum records twelve rules marked "adopted, nothing left pending" that
**nobody had actually added to the index**, undetected for four versions, one of
them (`AF-R-711`) the most-cited rule in the build at 52 references. The fix was
step 0 of the handoff: *diff the ids cited in code against the ids in
`RULES_INDEX.md`.*

Half of that diff is now mechanical here — 89 cited ids, extractable in one
command. The other half does not exist in the repo, so the dangerous direction
(rules the build enforces that the index does not contain) **cannot currently be
measured at all**. It has not been measured since 0.9.3.

Also absent, in rough order of usefulness:

1. `docs/RULES_INDEX_ADDENDUM.md` — the pre-0.7.0 body. The file here is
   explicitly *a section to append*, and says so in its first paragraph; it
   names but does not reproduce the AF-R-524 discussion and the pre-0.7.0
   FLEXIBLE choices, "all of which remain in force".
2. `PASS_PLAN.pdf` — cited by the scene registry and the placeholder inventory;
   open question 1 (the forest's name) is tracked against it.
3. Change reports for 0.9.1 → 0.34.0. Twenty-five versions with no record of
   what changed or which FLEXIBLE choices were made, which AF-R-802 requires be
   stated.
4. Any audit after 0.9.3.

## The battle draw scale is decided

`PLACEHOLDER_INVENTORY` calls this "the one technical decision blocking the
most", gating every enemy sprite declaration and the atlas budget. **It was
settled at 0.10.0** and the reasoning is in the source, under `18 · BATTLE`:

> Enemies draw at WORLD_SCALE, not UI_SCALE, because they stand on world art.
> … The sprites are pixel-block 1 with content boxes of 24x21 (skeleton),
> 20x30 (ghost) and 39x50 (ent) against the party's 16x24 — the same pixel
> density as the world, so there is no density break to record.
> The 64 and 128 in the source files are frame canvas, not art.

That last line is the answer to the arithmetic the inventory posed: the packs'
64px and 128px are padding around small art, so neither number was ever the
draw size. Seven enemy families are declared and 177 enemy frames are packed.

## What the placeholder inventory is worth now

It was measured against 0.7.3 at 134 text ids; 0.9.3 counted 140. Neither number
survives to 0.34.0 — placeholder ids are generated at runtime
(`AF.text.define("placeholder.name."+id, …)`), so only a running build can
count them.

What does survive is its structure, and it is still the most actionable document
of the five: the bottleneck is **about nine decisions**, not engine work. Whether
the tone sentence was ever given, the forest ever named, or the battle draw scale
ever chosen is not answerable from the file alone — but each is checkable in one
question, and each unblocks a named pile of work.
