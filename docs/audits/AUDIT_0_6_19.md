# Aetherfall — deep audit, 0.6.19

Run against the running build, not the documents. Fourteen areas. One real bug
found and fixed; several honest gaps recorded rather than papered over.

**Headline: `AF.save.read()` accepted a save with no resolvable player.** Fixed,
tested, and the test proven to fail without the fix.

---

## A. Build identity
```
Aetherfall 0.6.19 · rowans-hold · save v3
self-tests   163/163, repeatable x3, state restored between runs
walkthrough  16/16 (door -> interior -> save -> reload -> exit, via input:confirm)
baseline     0.6.17 through the same harness: 139/139
file         546 KB (atlas base64 is 207 KB of it)
```

## B. Atlas integrity — clean
167 rects in a 512x1131 atlas. **No rect out of bounds, none zero-sized, none
sharing identical coordinates.** (Duplicate coords would mean two ids silently
pointing at the same art.)

## C. Asset declarations — clean
No asset claims `verified` without a measured rect (AF-R-1001). No atlas asset
missing its RECTS entry. **No uncredited pack** (AF-R-941, self-tested).
`AF.assets.todo()` is down to the two known unsliceable reference sheets —
`sheet_master` and `sheet_rowans_world` — which are declared `verified:false`
on purpose so diagnostics keeps reporting them.

## D. Rule index vs code — the gap is closed in one direction
```
cited in code            77
present in the index    103
cited in code but NOT indexed    0   <- was 4 before 0.6.19
indexed but never cited         26
machine-enforced (refuse/require/forbid)  17
leftover AF-P ids                1   (a comment recording the adoption)
```
The dangerous direction — rules the build enforces that the index does not
contain — is now **zero**. The 26 uncited rows are mostly `review`-grade by
nature (Bible policy, reporting duties) plus the battle rules for a mode that
does not exist.

**AF-R-524 is not in the enforced count**, and that is correct: it is checked by
`AF.authoring.validateInteractables()` plus a self-test, not by a `refuse` call.
The index says so.

## E. Phantom enforcement symbols — 4 remain, all marked
| Rule | Symbol | Status |
|---|---|---|
| AF-R-622 | `AF.encounter` | **missing** — ⚠ in index |
| AF-R-601 | `AF.player` | **missing** — ⚠ in index |
| AF-R-704/705 | battle draw path / effect layer | **missing** — ⚠ in index |
| AF-R-942 | `AF.perf` | **missing** — downgraded to `review` |
| AF-R-803 | `AF.data` | exists |
| AF-R-524 / 203 / 931 | validators | exist |

None is new; all are recorded in the addendum. AF-R-622 is the one worth closing
first, since encounters are the next real feature.

## F. Scene registry — consistent
```
rowans_hold          2176x1664  blockers 21  arrivals [from_guildhall]  interactables 5
guild_hall_interior  1344x896   blockers 42  arrivals [from_hold]       interactables 2
```
Every scene declares an arrival point. **Every interactable in every scene passes
the AF-R-524 walk-up check with zero problems and zero shadowing notes.**

## G. Save migrations — ONE REAL BUG, FIXED

| Case | Result |
|---|---|
| v1 → v3 chain | ok — `actorId` recovered at 1→2, scene renamed at 2→3 |
| v2 with old scene id | ok — becomes `rowans_hold` |
| v3 round trip | ok |
| unknown scene id | refused (AF-R-931) |
| **v1 with no party** | **ACCEPTED — AF-R-932 / AF-R-904 breach** |

The 1→2 migration leaves `actorId` undefined when a v1 save has no party, and
its own comment claimed "the AF-R-904 boot check refuses it". **It does not.**
Boot runs once at startup; loading such a save mid-session applied it and left
the game with no protagonist — the blank HUD and party-less overworld that
AF-R-904 exists to prevent.

Nothing caught this because no test had ever exercised *load* with an empty
party — only *boot*.

**Fixed:** `AF.save.read()` now resolves the player link against the save's own
party before touching any state, so a refused load leaves the running game
intact. It also rejects an `actorId` matching nobody, not just an empty party.

Removing the fix fails the new test with `a save with an empty party was
accepted` — **and takes two unrelated tests down with it** (`Cannot read
properties of null`), which is a fair measure of how far the corruption spreads.

## H. Collision vs world bounds
| Scene | In-world blockers | Solid area | SPAWN |
|---|---|---|---|
| rowans_hold | 17 | 5.7% | free |
| guild_hall_interior | 38 | 71.3% | free |

The interior's 71% is expected: the room is an irregular shape inside a 21x14
rectangle, so most of that rectangle is wall or outside the room. Four
out-of-world blockers per scene are the deliberate outer tunnelling guards.

Neither spawn sits inside a blocker.

## I. Character draw maths — consistent across all four sheets
| Animation | Draw size | Centre | Foot |
|---|---|---|---|
| citizen_walk | 128x128 | on x | on y |
| herbalist_walk | 128x128 | on x | on y |
| host_idle | 128x128 | on x | on y |
| guildmaster_idle | 192x128 | on x | on y+24 (footInset 6) |

All routed through `AF.render.character()`. The 32px off-centre bug cannot recur
per-scene because there is only one call site's worth of arithmetic left.

## J. Animation integrity — clean
Five real animations, all `verified:true`, **no frame rect outside the atlas**.
`citizen_walk` and `herbalist_walk` are 4-direction (24 frames); `host_idle`,
`guildmaster_idle` and `door_guildhall` are single-row flat lists — correct,
since none of those sheets has verified directional rows (AF-R-923).

Test fixtures `fake_walk` / `fake2` are absent after a run, confirming the
self-test sandbox tears itself down.

## K. Placeholder canon — contained
9 text entries, **exactly one placeholder**: `placeholder.guildmaster.idle`, and
it renders visibly prefixed `[placeholder]`. No unapproved canon is hiding in
the script (AF-R-203).

## L. Determinism — clean
Seeded RNG reproduces identically from the same state. Ground scatter is
positional, not random — `scatterAt(3,4)` returns the same variant every call,
so the map looks identical every boot.

## M. Performance shape — comfortable
2000 collision moves against the interior's 42 blockers: **7ms**. The
sprite-derived collision costs nothing measurable at this size. File is 546 KB,
of which the atlas is 207 KB.

## N. Debug overlay — works, defaults off
`AF.debug.toggle()` draws grid, blockers, interact zones and a coordinate
readout in both scenes without throwing. Off by default.

---

## Open findings, not fixed

1. **Rowan's Hold collision is still grid-derived.** Its 17 blockers come from
   each prop's `collision:[w,h]` box centred on placement, not from the art's
   alpha. The Guild Hall interior now uses sprite-derived rectangles at quarter-
   tile precision; the same generator would work on Rowan's Hold props. Not done
   because it changes collision under a scene that is currently correct enough,
   and should be a deliberate pass with screenshots.
2. **AF-R-622 / `AF.encounter` still absent** — the last phantom that blocks a
   real feature.
3. **`x500.png`** still missing from the pack, so the interior floor is a
   placeholder and the second floor cannot be built.
4. **26 indexed-but-uncited rules** have never been reviewed one by one. Most are
   legitimately `review`-grade; nobody has confirmed that for each.
5. **Nothing tests rendering.** Every check here is logic or geometry. The
   double-size and off-centre sprite bugs both passed a full green suite and were
   caught only by device screenshots. `AF.debug` narrows this, but a screenshot
   per scene after any draw change remains the only real defence.
