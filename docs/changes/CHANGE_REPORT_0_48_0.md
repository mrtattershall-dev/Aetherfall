# Change report — 0.48.0

**Build** `Aetherfall 0.48.0 · rowans-hold · save v5`
**Self-test** 402 / 402, two runs, 0 boot faults, no page errors
**Size** 5,998,712 bytes
**Branch** `claude/newest-build-nv7xsl`

**Both orientations, on the user's call.** I argued for picking one — supporting
both doubles the layout surface permanently, and every bug this session found
was a layout bug. The decision was to keep both (AF-R-1007), so that is what
this builds, and the cost is paid where it lands: the suite now checks both.

---

## The model: each axis pays for its own scarcity

Portrait is 540×960 and **height** is scarce. Landscape is 960×540 and **width**
is abundant. The controls have to be spent out of whichever axis can afford
them, and until now they were always spent out of height:

| | portrait | landscape, before | landscape, now |
|---|---|---|---|
| controls cost | 229px of height (24%) | **229px of 540 (42%)** | 10px of height |
| | | | 114px of width, per side |
| battle panel top | 290 | **−61 — off the top** | 290 |
| log room | 4 lines | **0** | 4 lines |

`AF.controls` no longer answers one question. **A control reserves the edge it
actually sits on**: it counts against the bottom band only if its lower edge is
in the last quarter of the canvas, otherwise against whichever side it is on.
One rule, and it needs no knowledge of the orientation — the CSS moves the
buttons and the numbers follow.

```css
body.landscape .pad     { top:50%; bottom:auto; transform:translateY(-50%); left:10px }
body.landscape #actions { top:50%; bottom:auto; transform:translateY(-50%);
                          right:12px; flex-direction:column-reverse }
```

## `AF.view` — which way the phone is held

Two authored viewports, picked at boot and on every rotation. The swap
**mutates `AF.const.VIEW` in place** rather than replacing it, because 89 places
read that object; every one reads `.W`/`.H` at draw time rather than
destructuring at definition (checked before relying on it), so the whole build
sees the new size on the next frame without a single call site changing.

Replacing the object would have silently stranded the one module that caches
it — `AF.title`, `const V = AF.const.VIEW` — on the old size.

Both viewports are 16:9-family, so `WORLD_SCALE` 4 and `UI_SCALE` 3 hold in
either orientation and no asset is resampled (AF-R-405).

## What changed per screen

**The battle screen** was the redesign. In landscape the bottom of the screen is
not a stack of bands, it is **two columns**: command panel in the left of the
free centre, party strip in the right, one column instead of two. The feet line
moves 210 → 150 to keep the same proportion of a shorter screen, and the log
and the strip get scrims because in landscape they sit over grass rather than
over the black band under the backdrop.

**The title** separated along the abundant axis: wordmark and subtitle on the
left, the button block centred on the right. Before, `BOTTOM` landed at 258,
four buttons and their gaps are 192, and the block started at **−39** — the
wordmark was drawn through the tagline and New Game was off the top.

**The speech bubble** insets past the thumbs. In portrait `AF.controls` reports
no side band and it is the 10px it always was; in landscape a bubble starting
at x=10 put its first word under a d-pad. It also reads *better* wide — Wren's
line wraps to two rows instead of three.

**The overworld needed nothing.** It is camera-based, so it simply shows more
world — which is the point: four of six maps are wider than they are tall.

## Tests

`the battle screen fits` now runs **both orientations**: portrait across six
control bands, landscape across three, every party size and five menu lengths.
It gained two assertions that only mean anything wide — the panel and every
party member must clear the thumbs.

Testing only portrait is how the landscape panel came to be laid out at −61.

**Revert-proof**

| Reverted | Caught as |
|---|---|
| `wide()` always false (portrait layout everywhere) | `landscape: member 0 is behind the left thumb; the command panel starts behind the left thumb` |
| feet line fixed at the portrait 210 | `landscape: log has room for 1 line(s); it needs the header and a message` |

> The first run of the widened test failed *two* tests, not one. A leftover
> `desc` reference threw **inside a `finally`**, which meant `AF.controls.band`
> was left stubbed at `BAND_CEILING + 40` for every test after it — and the
> speech test, which positions a bubble off that number, failed as collateral.
> A throw in a cleanup block does not just lose the cleanup; it poisons
> everything downstream.

## Verified

- 402/402 × 2, 0 boot faults, no page errors
- **Portrait is unchanged** — battle screenshot at 414×736 is identical in
  layout to 0.46.0
- Landscape at 896×414, screenshotted: overworld, battle, dialogue, title

---

## Not finished

**The board and party screen overflows in landscape.** Its node tree is laid out
as a vertical column and 540px cannot hold eleven nodes; the lower ones are
drawn off the bottom. It needs the same treatment the battle screen got — the
tree spread along the abundant axis. Portrait is unaffected. This is the next
piece.

**The vendor screen is unverified** in landscape.

**The key art is portrait-shaped.** The title's illustration is a tall image
centred in a wide frame, so landscape shows it with dark margins either side.
That is an asset, not a layout: it needs a wide crop or a wide painting.

**The corridor question is still open**, as agreed. `forest_route` (2560 tall)
and `barrow_downs` (2176) are north–south corridors, and landscape shows 540px
of what is ahead instead of 960 — 44% less on the axis you are travelling.
Worth judging now that there is something to look at.
