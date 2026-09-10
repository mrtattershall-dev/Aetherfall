# Full audit — 0.50.0

**Method.** Everything below was measured by driving the live build in headless
Chromium. Where a claim could be made from source it was made from behaviour
instead — this audit found four of its own false positives that way, and they
are recorded at the end because each is a bug I would otherwise have reported.

**Scope.** Everything, with weight on the three areas `AUDIT_0_45_0_DEEP.md`
listed as never audited: memory over a long session, save-file growth over many
saves, and behaviour after several hundred battles.

---

## The finding that mattered most: the suite was green at one screen size

The self-test suite has been run, this whole project, through a harness fixed at
**540 × 960**. Run at the sizes the game actually meets, 0.49.1 was **red**:

| geometry | boot | re-run |
|---|---|---|
| 540 × 960 (the harness) | 406 / 406 | 406 / 406 |
| 414 × 736 iPhone | **404** / 406 | 406 / 406 |
| 896 × 414 landscape | **403** / 406 | **404** / 406 |
| 320 × 568 iPhone SE | **404** / 406 | 406 / 406 |
| 1024 × 768 tablet | **403** / 406 | **405** / 406 |

Three tests were geometry-dependent, and **one of them was hiding a live bug**.

- **`the speech bubble draws, and wraps instead of running off`** used a fixed
  71-character fixture. The recorder's fake `measureText` is 9px a character, so
  that line is 639px "wide" — wider than a portrait bubble (~480px of text room)
  and *narrower* than a landscape one (~790px). Wide, it legitimately fitted on
  one line and the test called that a wrapping failure. The fixture is derived
  from the viewport now, and the test runs **both orientations**.

- **`a spoken line stays inside its bubble`** asserted "three rows", which is
  what the fixture wraps to in portrait and not in landscape; and it collected
  rows by a y-window reaching **120px past the panel's bottom**, which in
  landscape swallowed the three-line diagnostic band and reported it as dialogue
  drawn outside the bubble. Rows are matched by **content** now. Its message was
  wrong too: it compared against `p.h - FRAME/2` and printed `p.h`, so it read
  *"a row is drawn at 516, past the panel's bottom (522)"*.

- **`the party screen stays inside its panel`** (mine, 0.49.0) counted blitted
  node icons. At **boot** the atlas has not decoded, `drawBoard` skips the blit,
  and it counted 0 of 11. The count is now gated on the atlas being ready — the
  claim is about layout, not about asset loading.

The harness now runs **five geometries × boot + re-runs**. A single-geometry
harness reports on the harness, not on the game.

---

## Live defects found and fixed

### 1 · The battle log collapsed to one line on an iPhone SE · MEDIUM

At 320 × 568 — an SE, or any phone in a small window — `AF.controls` measures a
**294px band**, two past the battle layout's declared `BAND_CEILING` of 292. The
consequence is the exact failure that layout's own budget test names:

| | before | after |
|---|---|---|
| log lines | **1** — "round 1", and nothing else | 2 |
| panel rows | 5, fixed | 4, scrolling |

The panel took `PANEL_ROWS` however little room was left. It now spends a
**menu row** — which scrolls, and whose cursor the window follows — before it
spends the log, which does not. Sweeping the band for the new limit gives a
ceiling of **346**, and 294 is now comfortably inside it. The test's band sweep
gained 294 explicitly.

*This was live on a real device while the suite was green, because the sweep
tested the ceiling and the device measured past it.*

### 2 · The diagnostic band's last line was clipped, in both orientations

Drawn with a top baseline at `V.H - 6`; a 10px face puts its glyph box at
`V.H + 3`. Three pixels off the bottom — and visible in the device screenshots
this whole time as a cut-off *"2 assets still unverified"*. The three lines step
up from `V.H - 12` now.

### 3 · `X is acting…` was drawn under the landscape d-pad

0.48.0 moved the battle log to `layout.zone().x + 10 * S` so it clears the left
thumb. The line that stands in the same place while an enemy takes its turn kept
a bare `10 * S`, and was drawn at x=30 with the pad occupying the first 114.

### 4 · The title wordmark's first letter sat behind the left thumb

`AETHERFALL` spans x 111→468 in landscape with the thumb at 114. The left column
is nudged by the measured thumb width now; portrait has no side band and is
untouched.

### 5 · The suite left two actors in the player's registry · LOW

`heal_probe_a` and `heal_probe_b` — fixtures from the 0.45.0 healing test — have
lived in `AF.actors.byId` for the rest of every session since. The test's own
comment says *"a synthetic actor, never a party member: the suite must leave the
player's game exactly as it found it"*; it got the first half right.

Nothing could see them, for two reasons: `snapshotSession` records the party,
the bag, money and the flags but **never the registry**, and the only guard on
strays was keyed on a **`t_` naming convention** these two politely did not use.

The new check asks the question **absolutely** — is every actor one the game
declares? — rather than diffing against a snapshot. That matters: the diff
version was written first and was worthless, because the harness runs the suite
twice and on the second run the actors leaked by the first are already in the
baseline. It passed on exactly the build it was written to fail.

### 6 · A save with negative money loaded straight through · LOW

`money: -5000` in a hand-edited save loads, and every shop row then reads
"can't afford" forever with nothing saying why. The save layer already refuses
garbage shapes and future schemas; a number outside its own range is the same
kind of claim, and is clamped now.

---

## Verified sound

Most of this audit is this list.

| Area | Result |
|---|---|
| **300 battles** | Heap flat at 29 MB start to finish. 0 faults, 0 errors. |
| **200 two-enemy battles** | Actor registry constant at 4. **Zero** event listeners added after boot. No status-effect accumulation. |
| **Save growth** | 2,431 → 2,679 bytes across 300 battles and 12 saves — level and exp, not a leak. |
| **Storage refused entirely** (iOS private browsing, `setItem` throwing from before boot) | Boots clean, plays, saves to the in-memory adapter, **407/407**, 0 faults. The lazy probe and fallback are correct. |
| **Storage failing mid-session** | `write` throws — and **both** call sites already catch it and report honestly ("Could not save: …"). Not a defect. |
| **Corrupt saves** | Truncated JSON, non-JSON, valid-JSON-wrong-shape, schema 999, null party, unknown actors, a scene that does not exist — all refused or absorbed. No crash, no boot fault. |
| **Audio blocked** (`AudioContext` throwing from before boot) | Boots, plays SFX calls, fights, **407/407**, 0 faults. |
| **4,000 random inputs** across overworld / menu / battle, with live rotations | 0 throws, 0 faults, still playable. |
| **40 rotations mid-transition** | Lands in the right scene, right mode. |
| **Full playthrough** — shop purchase, Hold → forest → barrow, four battles, a defeat, save | 52,000 ticks of real `update` + `draw`. 0 faults, 0 problems. Defeat correctly warped the party home. |
| **Determinism** | Same seed → identical fight. Different seeds → different fights. |
| **Economy** | Buy at 24, sell back at 12. No profitable loop. |
| **DOM menu** | Twelve rows walked with real clicks, into the equipment flow and back. 0 faults. **NEW GAME is disabled in the pause menu**, so it cannot destroy a save by accident. |
| **Every screen, both orientations** | Title, overworld, party sheet, ascension board, vendor buy/sell, battle command and target, speech — all inside the canvas and clear of the thumbs after the fixes above. |

---

## Four false positives, recorded

Each is a bug this audit could have reported that does not exist.

**"The price runs 99px off the right edge."** The vendor's price is drawn with
`textAlign = "right"`, so it *ends* at the margin. My probe added the string's
width to the x it was passed.

**"`AF.save.write` throws instead of reporting."** True, and both call sites
catch it. It only reproduces at all because I replaced `setItem` *after* the
adapter had been probed and cached; a device that refuses storage gets the
memory adapter at the first save.

**"124 things are drawn off-canvas in the overworld."** World tiles and
backdrops, which are camera-anchored and are *meant* to bleed.

**"`RESONANCE` is drawn 141px off the right edge."** A world-anchored labelled
placeholder standing where the resonance stone stands. Off-canvas when the
camera is elsewhere.

**And one near-miss in my own test.** The new engine-text test guarded its HUD
half with `if (typeof sc.drawHud === "function")`. The active scene during the
suite is the guild hall, which does not expose it, so the test measured nothing
and **went green over a reverted fix**. A skip that reads as a pass is the same
failure as the geometry problem above, one layer in. It reports a missing HUD as
a failure now.

---

## Open, and not answered here

**The vitals readout exists in one scene of six.** `drawHud` lives inside the
`rowans_hold` module and nothing else calls it, so HP, MP and SEAL are shown in
the village and nowhere else — not the forest, not the barrow, not any interior.
Measured by drawing all six scenes and looking for the labels:

| scene | vitals shown |
|---|---|
| `rowans_hold` | **yes** |
| `forest_route` | no |
| `barrow_downs` | no |
| `guild_hall_interior` | no |
| `shop_interior` | no |
| `inn_interior` | no |

The barrow is where the seal band matters and where a party gets worn down, and
it is the one place the bar is invisible. No stated rule requires a HUD, so this
is a **design call, not a defect** (AF-R-1007) and it is recorded rather than
answered. The repair, if wanted, is to hoist the call out of the scene and into
the overworld mode — one home instead of six.

**The Custodian is a level gate nothing announces**, unchanged from 0.49.1 and
still in `todo()` with its measured curve.

## Not audited

- Whether any of it is *fun*. No simulation answers that.
- Anything on a device since the 0.48.0 screenshots.
- Audio content — levels and mixes remain unheard.
