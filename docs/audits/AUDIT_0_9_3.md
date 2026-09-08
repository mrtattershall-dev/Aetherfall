# Aetherfall — deep audit, 0.9.3

Run against the running build, not the documents. Fifteen areas. **No new
crashing bug found; four honest gaps recorded, one test added for a draw path
nothing had ever reached.**

Context: 0.9.3 exists because the first device screenshots in twelve versions
found three bugs that 322 tests had passed. This audit was aimed squarely at
that class — code that is never executed — rather than at logic that is.

---

## A. Build identity
```
Aetherfall 0.9.3 · rowans-hold · save v4
self-tests   321/323, repeatable ×3, identical
boot faults  0
file         1068 KB (atlas base64 is ~305 KB of it)
```
The two failures are the harness's multi-pointer touch model, confirmed against
an untouched 0.9.1 at 303/305 before any result here was believed.

## B. Atlas integrity — clean
`512×1755`, **295 rects. No rect out of bounds, none zero-sized, and no two
rects share identical coordinates.** The last matters more than it used to: 88
icons were added this pass at 16×16, and duplicate coordinates would mean two
items silently drawing the same picture. There are none.

## C. Asset declarations — clean
`AF.assets.todo()` is down to the two known unsliceable reference sheets
(`sheet_master`, `sheet_rowans_world`), declared `verified:false` on purpose so
diagnostics keeps reporting them. **No uncredited pack** (AF-R-941).

## D. Rule index vs code — the dangerous direction is closed
```
cited in code                    88
present in the index            103
cited in code but NOT indexed      0
indexed but never cited           15
machine-enforced                  23
```
Re-measured after the 0.9.2 restoration of the twelve missing rows. This is the
third version in a row the diff has been run and the first where it was run
against the file actually on disk.

## E. Phantom enforcement symbols — 3 remain, all known
| Rule | Symbol | Reality |
|---|---|---|
| AF-R-622 | `AF.encounter` | exists |
| AF-R-803 | `AF.data` | exists |
| AF-R-704 | `AF.battle.draw` | exists |
| AF-R-601 | `AF.player` | **missing** — movement is `AF.sceneKit.walk`. Six versions recorded, still a §31 amendment and still the user's call. |
| AF-R-705 | `AF.effects` | **missing** — no effect layer |
| AF-R-942 | `AF.perf` | **missing** |

## F. Scene registry — consistent
| Scene | World | Blockers | Arrivals |
|---|---|---|---|
| `rowans_hold` | 2176×1664 | 22 | from_guildhall, from_shop, from_forest, defeat |
| `guild_hall_interior` | 1344×896 | 42 | from_hold |
| `shop_interior` | 1152×1216 | 78 | from_hold |
| `forest_route` | 1408×2560 | 29 | from_hold, from_barrow |
| `barrow_downs` | 1280×2176 | 17 | from_forest |

Every scene declares at least one arrival. **No arrival and no spawn sits
inside a blocker** in any scene.

---

## G. Draw paths — THE FINDING

This is the area the shop bug came from, so it was audited first and hardest.

Every draw path was executed against a recording context:

| Path | Result |
|---|---|
| all five scene `draw()` | run clean |
| `AF.vendor.draw` buy / sell | run clean, 28 / 22 text draws |
| `AF.speech.draw` | runs, wraps to 2 lines |
| `AF.battle.draw` | runs |
| `AF.transition.draw` | runs |
| debug overlay | runs, default off |

**But reaching them is harder than it looks, and that is the real finding.**

Two traps caught in the writing of this audit:

1. **`AF.scene.enter(id)` with no arrival throws** `AF-R-905 refused: no
   arrival point "undefined"`. Correct behaviour, but it means a naive draw
   test never gets as far as the draw.
2. **`AF.battle.ui` exposes only `{options, choose, back, state}`.** Setting
   `ui.level = "skill"` creates a dead property; the internal level never
   changes and the draw stays on the command menu. `choose()` takes no
   argument either — it reads the internal cursor. **A test written the
   obvious way silently exercises the command menu forever and reports
   success.**

The skill menu is exactly where 0.9.2's icon alignment bug lived. It is only
reachable by driving the real path: hold a direction, let `update()` read
`AF.input.axis()` edge-triggered, then emit `input:confirm`. A test that does
this is now in the suite, and it asserts every offered skill is actually drawn.

That is the drawing-side restatement of 0.6.18's lesson. **Testing that a
system responds is not testing that a player can reach it** — and it applies to
menus as much as to doors.

## H. Save integrity — sound, one gap
| Case | Result |
|---|---|
| v4 round trip through a scene change | ok |
| unknown scene id | refused (AF-R-931) |
| empty party | refused (AF-R-904) with a full reason |
| schema 99 (from the future) | refused |
| v1 → v4 chain | migrated |
| **`money: -50`** | **accepted — balance becomes −50** |

Negative money loads without complaint. It is not exploitable (you cannot buy
anything with it) and the vendor's own refusals hold, but it is the shape this
project refuses elsewhere: `AF.integrity.spend()` will not go below its floor,
and `AF.save.migrate()` refuses rather than silently reinterpreting. **Recorded,
not fixed** — clamping versus refusing is a design call (AF-R-1007), and the
same question applies to every other numeric field in the save envelope, which
is the more useful version of the question.

## I. Collision vs world bounds
| Scene | In-world blockers | Solid |
|---|---|---|
| rowans_hold | 17 | 5.5% |
| guild_hall_interior | 38 | 71.3% |
| shop_interior | 74 | 90.4% |
| forest_route | 23 | 1.4% |
| barrow_downs | 11 | 7.9% |

`shop_interior` at **90.4%** is the outlier and is expected: it is a two-room
interior with sprite-derived collision at quarter-tile precision inside a
rectangle that is mostly wall. Worth knowing rather than worth fixing — but if
a third room is ever added there, that number is the one to watch.

## J. Determinism — clean
The seeded RNG reproduces identically from the same seed.

## K. Placeholder canon — contained
**140 placeholder text ids.** Every one renders a visible `[placeholder]`
marker (AF-R-203). No unapproved canon is hiding in the script.

## L. Authoring validators — clean
| Scene | Placement problems | Interactable problems | Notes |
|---|---|---|---|
| rowans_hold | 0 | 0 | 3 |
| guild_hall_interior | 0 | 0 | 0 |
| shop_interior | 0 | 0 | 0 |
| forest_route | 0 | 0 | 0 |
| barrow_downs | 0 | 0 | 0 |

The three notes in Rowan's Hold are partial-shadowing reports — an NPC
answering first on some approaches — which is legitimate authoring.

## M. Performance — comfortable
2000 collision moves against `shop_interior`'s 78 blockers: **6 ms**. The
sprite-derived collision still costs nothing measurable at this size.

## N. Debug overlay — works, defaults off

## O. AF-R-512 spawn clearance — the rule is not what it looks like

The warning on the device screenshot is real, and measuring it turned up two
problems the warning does not say:

| Scene | Nearest blocker to spawn | Warns? |
|---|---|---|
| rowans_hold | 4.03 tiles | yes |
| guild_hall_interior | 0.75 tiles | **no** |
| shop_interior | 0.06 tiles | **no** |
| forest_route | 2.93 tiles | **no** |
| barrow_downs | 2.93 tiles | **no** |

1. **The check only looks at `props`.** It iterates placement-declared props
   with a `block`, and only Rowan's Hold has them — the interiors and the
   wilderness build blockers by other routes. So AF-R-512 is measured in **one
   scene out of five** while the index lists it as `code`-enforced.
2. **The threshold is geometrically impossible where it is not measured.**
   `guild_hall_interior` is 21×14 tiles; a 10-tile clearance around a spawn
   cannot exist in it. `shop_interior` spawns 0.06 tiles from a wall, which is
   what walking in through a door means.

So the rule as written suits an outdoor spawn and cannot suit an interior one.
Either it needs a per-scene-kind limit, or interiors need an explicit
exemption. **A rule nobody can satisfy is a rule that gets ignored**, which is
the failure mode the addendum exists to catch. Changing a LOCKED number is
AF-R-1007, so this is recorded, not changed.

---

---

# Asset library re-audit

Run over all 36 uploaded archives and the live atlas.

## Inventory
**36 uploads, 34 distinct packs.** Two were uploaded twice, byte-identical:
HP/Mana/Scroll Bars (573594) and Fishing Village (885927).

**Every pack ships a terms file except `rpg-ultimate.zip`** — checked across
the whole library, not one spot. Those 579 files stay blocked under AF-R-1001.
Note that Raven's `Special Note to the Dev.txt` is a thank-you note from the
artist, not a licence; its terms live only on the itch page.

## Icon integrity — 88/88 exact
Every item and ability icon was cropped out of the **live build's base64 atlas**
and compared pixel-for-pixel against its source file in the Franuka archive,
using the `ICON_INDEX` / `ABILITY_ICON_INDEX` provenance tables.

```
checked      88
mismatches    0
```

This is the check that would have caught the spritesheet mis-cut in one step.
**It cannot become a self-test** — it needs the source archives, which the
build does not ship. It belongs in an audit, run whenever icons are re-cut.

## THE FINDING — 88 icons were drawn but undeclared

`AF.credits.inUse()` derives the credited-pack list from **declared** assets
and animations. The 88 icons existed only as atlas rects, so:

- `AF.credits.declaredUnused()` reported **`franuka_icons` as unused** while
  its art was on screen in the shop and the battle menu.
- `AF.credits.requiredLinks()` listed only `franuka_ui`.

The Fantasy RPG Icon Pack is **CC BY 4.0 with a mandatory credit link**. The
build was drawing 88 of its icons while its own credits screen carried no
obligation to link it.

AF-R-941 did not catch it, and correctly so: it checks that no *used* pack is
uncredited, and an undeclared rect is invisible to "used". **Provenance has to
live on the asset, not in a comment beside it.**

**Fixed.** Both `defineItem` and `defineAbility` now `AF.assets.declare()`
their icon with `pack: "franuka_icons"`, a `source` string naming the pack's
own file, and the measured rect. Two guards were added and revert-proven:
art that is drawn must be a declared asset with a credited pack, and a pack
whose licence demands a link must appear in `requiredLinks()`.

```
before: inUse 8   declaredUnused: craftpix_chapel, franuka_icons
after : inUse 9   declaredUnused: craftpix_chapel
        requiredLinks: franuka_icons, franuka_ui
```

## Dead weight in the atlas — 4.6%
18 rects are never drawn, totalling 23,148 of 503,884 packed pixels.

| Rect | Size | Why |
|---|---|---|
| `bld_chapel` | 127×159 | **20,193 px — 87% of all dead weight.** The chapel was removed by AF-C-003 in 0.6.21; its building art stayed. `craftpix_chapel` is still credited for it, and is the only entry `declaredUnused()` still reports. |
| 16 × `ui_*` | small | pressed/selected button states, cursors, arrows, triangles — unused but plausibly intended, not defects |
| `icon_node` | 16×16 | ascension board |

Removing `bld_chapel` means repacking and re-encoding the base64, so it is
recorded for the next atlas pass rather than done here.

## Still unmeasured / unused
- **Six packs** measured at 0.9.2 and used by nothing: Mage Tower, Blacksmith,
  Noble's Manor, Training Arena, Camp, Raven Fantasy Icons.
- **The three enemy sprite packs** (Ent 166, Skeletons 214, Ghost 209 PNGs)
  declare **zero** assets. Still blocked on the battle draw scale, which is
  still the single decision gating the most work.
- **The full RPG UI pack**: 631 unique assets, one now in use (`ui_nameplate`).
  Item slots and Spellbook/Tabs remain the party screen's furniture.

## Open findings, not fixed

1. **`AF-R-512` is measured in one scene of five and its threshold is
   impossible in the other four.** The most substantive finding here.
2. **Negative money loads silently.** The only numeric save field probed; the
   others have not been.
3. **`AF-R-601` still names `AF.player.step`.** Seventh version.
4. **`AF-R-705` / `AF-R-942`** remain phantom symbols for features that do not
   exist. Legitimate, but the index should keep saying `review`.
5. **15 indexed-but-uncited rules** have still never been reviewed one at a
   time. Most are legitimately `review`-grade; nobody has confirmed that for
   each.
6. **Rendering is still only checked by execution, not by appearance.** The new
   guards prove a panel runs and draws the right number of rows. They cannot
   tell you an icon is 32px too high — that took a phone. The three bugs in
   0.9.3 were all of that kind.
7. **`shop_interior` is 90.4% solid.** Fine now, fragile if extended.
