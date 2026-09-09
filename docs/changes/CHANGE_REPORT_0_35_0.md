# Aetherfall — change report, 0.34.0 → 0.35.0

The first boss anything can reach, and a hole in the map on the way to him.

```
Files / sections changed:
  aetherfall.html
    · AF.build        — 0.34.0 -> 0.35.0 (save schema unchanged at 4)
    · AF.barrowDowns  — south wall sealed; SEAL_BAND; stepCustodian(); banner note
    · AF.content      — the Custodian's warning (canon) + two draft aftermath lines
    · AF.battle       — backdrop props are region-bound, not only the ground
    · AF.battle.todo  — the "triggered by nothing" line is no longer true of him
    · AF.selftest     — 383 -> 387

Rules touched (AF-R-###):
  AF-R-203   his warning draws clean; my aftermath prose draws marked
  AF-R-303   the barrow's fight uses the barrow's own props
  AF-R-622   the fight starts through AF.encounter.trigger, so it is unfleeable
  AF-R-710   defeat leaves custodianDefeated false — he is still there
  AF-R-811   custodianDefeated is the act model's second gate
  AF-R-1006  every rect named is already declared and verified
  AF-R-1007  act structure and the aftermath wording are the user's, not taken

FLEXIBLE choices made (AF-R-802 requires stating these):
  1. He SPEAKS and the fight starts — not an AF.conversation. Cancel would let
     a player decline a boss (0.9.0 choice 4) and standing in the band would
     re-fire it every frame, the loop 0.9.0 fixed. His canon settles it: he
     does not bargain.
  2. He is at the end of the barrow trail, not in `deep_barrow`. The sealed
     south end IS the seal; he is the reason it is sealed. No new region.
  3. The aftermath is narration on the scene's own result banner, not the
     speech bubble — the bubble draws a speaker's name and there is nobody
     left to attribute it to.
  4. The banner note WRAPS, measured against the real font. The vendor log
     trims and the bubble runs off; neither suits a line meant to be read once.
  5. The seal band is the trail's last three rows (31-33), the shape and
     placement of GATE_BAND five rows above it.

Assumptions made:
  None. Every band, flag, rect and frame count came from the build or from a
  pack's own files.

Self-test: 387/387, three consecutive runs, identical
Boot faults: 0
Verified how: HEADLESS CHROMIUM (real canvas, real atlas decode), plus a
  screenshot of the fight. NOT device-verified.
```

## The baseline, and why this harness is worth trusting

Before any change: **383/383, three runs, 0 boot faults**, in headless Chromium
driving the real build. `AI_HANDOFF_0_7_0_PATCH` records three tests failing
under Playwright for an environmental reason — `drawImage` rejecting a stubbed
atlas image. That does not happen here: the atlas is a real embedded data URI
decoded by a real browser, so all 383 pass. The harness is stricter than the one
the handoff describes, not weaker.

## 1 — The south wall was open

Full write-up in `docs/audits/FINDING_barrow_south_leak.md`. In short: the edge
guards were copied from `AF.forestRoute`, whose south edge really does open onto
this scene, and the comment came with them. Here the trail leaves at columns
13-14, not 8-9, and the south opens onto nothing. `AF.collision.move` never
clamps to the world, so the two-tile gap was a way out of the map. Measured
before the fix: a player walking down columns 8-9 was **1,472px past the world's
bottom edge and still moving**.

The wall is one span now. The test drives the real collision step down every
column and out to both sides, so a hole anywhere in any wall fails it.
Revert-proven at columns 8 and 9.

## 2 — The Custodian

`custodian_of_the_seal` has been declared, phased and startable since 0.7.0 and
triggered by nothing, which `AF.battle.todo()` has reported every version since.
That is the fourth instance of this project's most-repeated shape — the door in
0.6.18, the Items backend before 0.10.0, saving before 0.11.0.

He stands at the seal band: the trail's last three rows, against the sealed
south end. The module header has said since 0.7.0 that the way down is closed.
He is the reason it is closed.

**The test that matters is the walk-up.** The gate ambush's own test teleports
into its band, which proves the trigger responds but not that the trail reaches
it — the distinction handoff §6 exists for. This one holds a direction and lets
the real update loop carry the party: 74 frames from the gate band to the fight.
Reverting the wiring reports *"walked 600 frames to y=2175 and met nothing"* —
y=2175 of 2176, the full trail, stopped at the wall that was open this morning.

## 3 — What felling him does, and what it does not

`custodianDefeated` is the flag the AUTHORED table already names, so:

- **Losing does not clear it.** Defeat revives the party at the Hold's gate
  (AF-R-710) with the flag false. He is still standing when they come back.
- **Winning advances the act model** — and *does not move the seal floor*, which
  the test asserts rather than something tidier.

`AF.integrity.gateOf` returns the floor of the next *uncleared* gate, and the
gate ahead of this one is `firstBossDefeated`: declared, first in `FLOORS` at
88, and **set by nothing in the game** — only by self-tests. While it is unmet
it is always the first uncleared gate, so the floor stays 88 however the later
flags fall.

The wiring behind the Custodian is correct and live: with the earlier gate met,
felling him moves the floor 74 → 58, and the test proves that too. The day
something sets `firstBossDefeated`, his consequence arrives with no further
work.

**Not fixed here.** Whether the Custodian *is* the first boss is act structure —
canon, and the user's call (AF-R-1007). Setting a second flag on his death to
make a number move would be answering that quietly. Recorded in
`AF.battle.todo()`.

## 4 — The fight was happening in a wood

Found by screenshotting the battle, not by a test — every draw path "runs clean"
either way, which is `AUDIT_0_9_3`'s open finding 6 exactly.

`backdropRects()` bound the **ground** to the region (`barrow_downs` →
`forest_dirt`) and left the props and scatter hardcoded to the Herbalist pack's
oaks and bushes. So the barrow's boss fight drew barrow dirt and then stood a
forest on it.

0.10.0 wrote the fix down in advance — *"because the region owns its tileset
(AF-R-303) the barrow's fight can look like the barrow by naming different
rects"*. Every rect now named is already declared, verified and in the atlas,
placed by `AF.barrowDowns` itself: `ruin_a`, `ruin_b`, `deadtree_a`, `skulls`,
`grave_b` over `bd_bone_*`, `bd_grit_*`, `bd_crack_3`. No new art, no atlas
change. Screenshot: `docs/audits/custodian_0_35_0.png`.

## Left for you

- ~~**The Custodian is drawn as an ent.**~~ **Done in 0.35.1** — see below.
- **Is he the first boss?** Nothing sets `firstBossDefeated`, so the act model
  cannot advance off 88. See §3.
- **The aftermath prose is my draft**, marked and listed in
  `AF.text.placeholders()`. Your beat, my sentences — approve, rewrite or strike.
- **The sigil is narrated and is not an item.** Canon describes the party
  leaving with it; the bag does not receive it.
- **Balance is still a model, not a player.** He is 230 HP with one phase
  against a level-1 Aren at 54. The todo's line stands: *"no AI_PATTERNS or
  PHASES numbers have been played against a real party."* This is where that
  stops being theoretical.
- **Combat is still visually inert** — AF-R-705 / `AF.effects` remains a
  phantom, so his phase turn and every ability resolve with no animation.


---

# 0.35.1 — the Custodian is a knight

`docs/audits/custodian_0_35_1.png`

## `family` was answering two questions

Mapping him to the `knight` family directly would have **refused the boot**.
`AF.content` validates on `family`: every `"boss"` must declare PHASES and
nothing else may (AF-R-711), so moving him out of the boss family makes him a
non-boss carrying PHASES.

That is the shape this codebase keeps naming — one name serving two questions,
as with `ROAD_UNDER` and AF-R-521, `placement` vs `drawSize`, `spawnClearance`.
The handoff's rule is to split the questions rather than soften the check:

```
family                      stays the TIER — what AF-R-711 refuses on
AF.enemyArt.ART_OF          answers the ART — per enemy, not per family
```

Per-enemy is deliberate: the Ent sheet is right for the Hollow Dragon and wrong
for a rusted knight, and they share a tier. A test asserts both halves, and that
the override has not leaked onto an enemy that declares none.

## Skeleton2, measured

`docs/audits/skeletons_compared.png` — all three idle sets cut from the pack at
`WORLD_SCALE` 4, union-bboxed the way 0.10.0 cuts a non-death state:

| Sheet | Idle union | Drawn | State |
|---|---|---|---|
| Skeleton1 | 25×22 | 100×88 | packed, `husk` |
| **Skeleton2** | **29×23** | **116×92** | **not packed** |
| Skeleton3 | 28×27 | 112×108 | packed, `knight` — the Custodian now |

**Recommendation: keep Skeleton3 for him, and give Skeleton2 to the mob.**

Skeleton3 is full plate with a horned helm, a red cloak and a greatsword — it is
the only one of the three that reads as *a knight*, which is what the canon
says he was. Skeleton2 is lighter, pale, and carries a green gem in its
forehead; it reads as a lesser or arcane undead, and the gem implies a story
nobody has written. As the Custodian it would be a downgrade.

The real problem the comparison exposes is not which skeleton the boss gets:

> **`seal_custodian` and `barrow_knight` are both family `knight`.** The boss and
> a random encounter in the same region are now the same sprite.

Skeleton2 fixes that from the other end — it belongs to `barrow_knight`. That is
an atlas pass, and the atlas has been append-grown since 0.6.18, so it wants to
ride with the repack the 0.12.5 README already asked for rather than adding
another appended block. Recorded in `AF.battle.todo()`, not done here.

Self-test **388/388**, three consecutive runs, 0 boot faults, headless Chromium.

---

# 0.35.2 — the warning is heard while he is alive

`docs/audits/custodian_0_35_2.png`

A quick three-agent audit of the 0.34.0 → 0.35.1 diff (one auditor on the
barrow scene, one on `AF.enemyArt` and the backdrop, one on the new tests).
Two real bugs, one root; one cosmetic note; everything else confirmed fine.

## The bug the screenshot could not see

The Custodian's warning went into `AF.speech` the same frame the fight started.
The speech bubble is neither ticked nor drawn in battle mode, so the line sat
unseen and then played **after he was dead** — over the aftermath note on a win,
or at Rowan's Hold's gate on a loss. And because the walk-up test drove the same
path, the suite left the line parked at boot, so a New Game opened with
*"Custodian of the Seal: Turn back…"* in the starting scene.

The 0.35.0 screenshot was of the battle screen — exactly the surface speech is
not on — which is why looking did not catch it.

**Fix:** `AF.battle.start` takes `opening` lines, printed to the battle log
after *"X appears."*; `AF.encounter.trigger` passes them through (it can never
override enemies or kind). The log is the one surface on screen when he speaks.
The walk-up test now asserts the warning is in the log when the fight opens
**and** that nothing is parked in speech. Revert-proven: without `opening` it
fails *"his warning is not in the battle log when the fight opens"*.

## And then the log clipped him

The fix made a second thing visible: the log trims every entry to one row with
an ellipsis, and his only line became *"Turn back, while I …"*. `clip` was
written for combat notices; his was the first log entry that is a sentence.
The log now wraps a long entry into rows, then takes the newest rows that fit,
so a sentence costs rows rather than being cut and the room budget stays
honest. A single word wider than the panel still clips.

## Confirmed fine by the auditors

- `sGapX0`/`sGapX1`/`EXIT_SOUTH` leave no dangling reference in the barrow.
- `stepCustodian` fires exactly once per band entry: `AF.battle.start` sets
  state synchronously, and on a loss the defeat transition is active until the
  scene changes.
- `SEAL_BAND` (x 800–992, y 1984–2176) brackets trail columns 13–14, rows 31–33.
- `fam` in the battle draw is only ever used for sprite lookups, including
  `deathMs`, which *must* follow the art (knight has 6 death frames, Ent3 12).
- All ten barrow backdrop rect ids exist; `drawBackdrop` assumes no count.
- Both `NAMES` keys exist — `seal_custodian` and `custodian_of_the_seal`.
- No duplicate text ids.

## Cosmetic, not fixed

The treeline loop advances by `p.w × 4 − 52`, and `grave_b` is 13px wide, so it
advances 0 and draws on top of `skulls`. Terminates, overlaps. Swap `grave_b`
for a wider prop in the next art pass.

Self-test **388/388**, three consecutive runs, 0 boot faults, headless Chromium.

---

# 0.36.0 — Skeleton2 packed; the boss stops sharing a sheet

`docs/audits/custodian_0_36_0.png` · `docs/audits/barrow_knight_0_36_0.png`

Your call: **Skeleton3 is the boss, Skeleton1 and Skeleton2 are basic enemies.**
Skeleton1 was already `husk`, so the work was packing Skeleton2 and giving the
Custodian a sheet nothing else uses.

## What moved

```
knight     Skeleton3 -> Skeleton2      barrow_knight, a random encounter
custodian  (new)     -> Skeleton3      seal_custodian, via ART_OF
```

Skeleton3's 23 packed rects were **renamed** `enemy_knight_*` → `enemy_custodian_*`
— same pixels, they were always Skeleton3 — and Skeleton2's 23 frames were cut
and packed as the new `enemy_knight_*`. `barrow_knight` needed no edit: it is
family `knight`, and `knight` now means Skeleton2.

Cut on the rule its sibling families use (0.10.0): union bounding box across
each looping state, per-frame for death, row 0 (front), `Without_shadow`.

```
atlas   512x2764 -> 512x2840   (+76 rows)
rects   730 -> 753
base64  +10,780 chars          file 2,876,607 bytes
```

**Verified byte-exact against the source pack, both ways:**

```
knight     <- Skeleton2   23/23
custodian  <- Skeleton3   23/23
```

Atlas integrity re-checked: 753 rects, none zero-sized, none out of bounds, no
duplicate coordinates, packed extent 512×2839 inside a declared 512×2840.

## The test now guards the property, not the instance

It asserted "his art family is knight", which this change would have made false
while the underlying problem was fixed. It now asserts he has his own sheet and
that **no other enemy resolves to it** — computed over every entry in `ENEMIES`
rather than against `barrow_knight` by name, so a future mob pointed at his
sheet fails too. Both sheet bindings are asserted by name as well.

## One thing worth writing down

The new rect literals went in as `[0, 2764, 29, 23]`. The game parses RECTS as
real JavaScript, so that ran perfectly — but every other entry in the table is
written `[450,1886,28,27]` with no spaces, and `tools/atlas-report.py` matches
`[0-9,]+`. So the tool silently reported **730 rects and a packed extent of
2764**, exactly as if the 23 new frames did not exist, while the game drew them
correctly.

A formatting difference the runtime does not care about made a verification
tool lie in the safe-looking direction. Normalised to the file's convention.

Self-test **388/388**, three consecutive runs, 0 boot faults, headless Chromium.

## Still open

- **Is he the first boss?** Nothing sets `firstBossDefeated`, so felling him
  advances no act gate. Act structure, still yours (AF-R-1007).
- **The aftermath prose is my draft**, marked and listed in `AF.text.placeholders()`.
- **The sigil is narrated and is not an item.**
- **He has never been fought.** 230 HP, one phase, against a level-1 Aren at 54.
