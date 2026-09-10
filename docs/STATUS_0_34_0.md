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

The enforcement census, which the 0.12.5 addendum lists as PENDING and stale at
23, is re-measured in `docs/audits/GAPS_0_12_5_RECHECK.md`: **89 cited, 24
machine-enforced** at 0.34.0. Three ids gained a check since 0.7.0 — AF-R-203,
AF-R-331 and AF-R-1001.

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
2. `PASS_PLAN.pdf` — cited by the scene registry and the placeholder inventory.
3. Change reports for 0.12.6 → 0.34.0. Twenty-two versions with no record of
   what changed or which FLEXIBLE choices were made, which AF-R-802 requires be
   stated. (0.9.0 and 0.12.5 are here.) The addenda and handoff patches stop at
   0.12.5 too — both are explicitly *sections and patches*, never merged into
   the base documents they amend.
4. Any audit after 0.9.3.

`docs/AI_HANDOFF.md` is now in the repo, and it is the document that makes the
index gap matter: its §2 step 0 is the diff, and its header tells every session
to treat `RULES_INDEX.md` as the authority. Note the handoff's own header is
stale — it names `aetherfall-0.6.19.html`, branch `rowans-hold-undead`, save
schema 3, against a build stamping **0.34.0 · rowans-hold · save v4**.
`AI_HANDOFF_0_7_0_PATCH.md` fixes the first two of those and is explicitly a
patch, not a replacement; the two have never been merged.

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

## Most of the inventory's nine decisions are already answered

All of these were closed in the build without the inventory being updated:

- **The tone sentence, and all 118 names.** `CHANGE_REPORT_0_12_5` records the
  118 mechanical names drafted, approved, and moved into a new `NAMES` table
  registered as `name.<id>` and drawn without a marker. Measured in the 0.34.0
  source: **135 approved, 6 provisional.** The inventory's step 1 — "88% of the
  placeholder count cleared in one exchange" — happened.
- **The forest's name** (its open question 1, "still open across five
  versions"): **The Outwood**. The party is **Aren, Bulwark, Zephyr, Cass**.
- **The battle draw scale** — settled at 0.10.0 (above).
- **The Guild Hall floor / `x500.png`** — settled at 0.7.4, and not by either
  answer the inventory offered. The file genuinely is not in the pack, but the
  pack's `Interior_1st_floor.tmx` declares it and **no tile on either floor
  uses it**; the floor comes from `Walls_interior.png`, which ships. Verified
  against the archive in `docs/audits/ASSET_VERIFY_0_34_0.md`.
- **The barrow art** — `craftpix_undead` supplies it, 54 rects verified.

What is left of that document is six provisional names — `barrow_downs`,
`deep_barrow`, `ashen_reach`, `hold_supplies`, `guild_quartermaster`,
`rowans_smithy` — and the RPG Ultimate licence, which only you can find.

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
