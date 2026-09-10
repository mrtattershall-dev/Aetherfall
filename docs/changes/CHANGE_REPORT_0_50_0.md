# Change report — 0.50.0

**Build** `Aetherfall 0.50.0 · rowans-hold · save v5`
**Self-test** 407 / 407 (one new) at **five geometries**, boot and re-run — 15
suite runs, 0 boot faults, no page errors
**Branch** `claude/newest-build-nv7xsl`

A full audit pass. Findings and method in `docs/audits/AUDIT_0_50_0_FULL.md`;
this is what changed.

---

## The suite was green at one screen size

Every "402/402", "405/405" and "406/406" reported in this project came from a
harness fixed at **540 × 960**. Run at the sizes the game meets, 0.49.1 was red:
404/406 on an iPhone, 403/406 in landscape, 404/406 on an SE.

Three tests were calibrated to portrait — a wrap fixture measured against the
portrait bubble width, a row count of "three" that is two when the bubble is
wider, and a row filter reaching 120px past the panel that in landscape
swallowed the diagnostic band and called it dialogue. All three are now derived
from the viewport and **run both orientations**; the harness runs five
geometries.

**One of them was hiding a live bug.**

## Six live defects

| | |
|---|---|
| **The battle log collapsed to one line on an iPhone SE.** At 320 × 568 the control band measures 294 — two past the layout's declared ceiling of 292 — and the panel took its five rows regardless. A player saw `round 1` and nothing else about the fight. | The panel now spends a **scrolling menu row** before it spends the log. Measured new ceiling: **346**. The band sweep gained 294 explicitly. |
| **The diagnostic band's last line was clipped 3px** off the bottom in both orientations — visible in the device screenshots all along. | The three lines step up from `V.H - 12`. |
| **`X is acting…` was drawn under the landscape d-pad.** 0.48.0 moved the log past the left thumb; the line that stands in the same place kept a bare `10 * S`. | `layout.zone().x + 10 * S`, like the log. |
| **The title wordmark's first letter sat behind the left thumb** in landscape. | The left column is nudged by the measured thumb width. Portrait untouched. |
| **The suite left two actors in the player's registry** — `heal_probe_a`/`heal_probe_b`, since 0.45.0. `snapshotSession` never watched the registry, and the only stray check was keyed on a `t_` prefix these two politely did not use. | The test forgets them, and a new check asks the question **absolutely**. |
| **A save with negative money loaded straight through**, after which every shop row reads "can't afford" forever. | Clamped on load, like the shape and schema checks beside it. |

## Two tests, and why the first version of each was wrong

**`no actor outlives the suite that the game did not declare`** — asked
absolutely, not as a diff against a snapshot taken at the start of `run()`. The
diff was the first version and was worthless: the harness runs the suite twice,
so on the second run the actors leaked by the first are already in the baseline.
It passed on exactly the build it was written to fail.

**`the engine's own text stays on the canvas and out of the thumbs`** — the
generalisation of two of the defects above. It measures real glyph boxes, since
the HUD band and the battle screen use different faces and guessing a line
height is how the probe that found these produced false positives of its own.

> Its first version guarded the HUD half with
> `if (typeof sc.drawHud === "function")`. The active scene during the suite is
> the guild hall, which does not expose it — so it measured nothing and **went
> green over a reverted fix**. A skip that reads as a pass is the same failure
> as the geometry problem, one layer in. It now reports a missing HUD as a
> failure and asks `rowans_hold` by id.

**Revert-proof** — eight reverts, eight catches:

| Reverted | Caught as |
|---|---|
| the panel takes fixed rows again | `portrait, band 294, party 2, 5 options: log has room for 1 line(s)` |
| the diag band back at `V.H - 6` | `portrait/hud "2 assets still unverif" ends at 962, past the canvas bottom (960)` |
| `is acting` back to a bare `10 * S` | `landscape/battle "Cairn Hound is acting…" starts at 30, behind the left thumb (114)` |
| the heal test stops forgetting its probes | `left in AF.actors: heal_probe_a, heal_probe_b (new this run: none)` |
| the bubble never wraps | `portrait: a line 1071px wide was drawn on one line in a 540px view` + the same in landscape |
| the scene draws its own second bubble (the 0.47.0 bug) | `a row is drawn at 758, inside the panel's top frame (776)` |
| `wide()` always false | `landscape: member 0 is behind the left thumb` |
| the board never transposes | `landscape, board: "«icon»" at y 444..492 is outside the panel interior` |

## Verified sound, not changed

300 battles with a flat heap and no registry or listener growth; storage refused
entirely (iOS private browsing) — boots, plays, saves to memory, 407/407;
corrupt saves of seven shapes all refused or absorbed; audio blocked — 407/407;
4,000 random inputs with live rotations — 0 throws; a full playthrough of 52,000
real ticks — 0 faults; determinism holds; no profitable buy-sell loop; NEW GAME
is already disabled in the pause menu so it cannot destroy a save.

Four things this audit nearly reported and did not, because they are not bugs,
are listed in the audit document with the reason each looked like one.

---

## Open

**The vitals readout exists in one scene of six.** `drawHud` lives inside
`rowans_hold` and nothing else calls it: HP, MP and SEAL are shown in the
village and nowhere else — not the forest, not the barrow, not any interior. The
barrow is where the seal band matters and where a party gets worn down, and it
is the one place the bar is invisible.

No stated rule requires a HUD, so this is a **design call and not a defect**
(AF-R-1007). It is in `todo()` with the measurement rather than answered here.
The repair, if wanted, is one line: hoist the call out of the scene and into the
overworld mode.

**Still true:** nothing device-verified since 0.48.0, and balance remains
simulated rather than played.
