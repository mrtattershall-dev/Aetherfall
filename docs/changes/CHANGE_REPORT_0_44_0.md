# Change report — 0.44.0

**Build** `Aetherfall 0.44.0 · rowans-hold · save v4`
**Self-test** 396 / 396 (one new), two runs, 0 boot faults, no page errors
**Size** 5,941,222 bytes (unchanged — no assets added)
**Branch** `claude/newest-build-nv7xsl`

Two defects reported from the device. Both made the fight unplayable, both had
been shipping for fourteen versions, and neither could be seen from a desk.

---

## 1. There was no d-pad in a fight

0.30.3 added this, with a reason:

```css
/*  THE PAD IS FOR WALKING, and there is no walking in a fight.  */
body.battle .pad{display:none}
```

The reason is true and it is not the whole truth. **The battle menu is a
vertical list.** Every command, every skill, every item and every target is
chosen with up and down. Hiding the pad left a touch-only player able to press
A on whatever row the cursor happened to start on and nothing else — Attack,
and only ever Attack, at the first enemy, forever.

It survived because a keyboard has arrow keys. On a desktop the fight plays
correctly, and no test in the suite can press a button that is not drawn.

Left and right genuinely do nothing here — the battle UI reads
`AF.input.axis().y` and nothing else — so they hide, exactly as the title
screen has hidden them for the same reason since 0.14.3:

```css
body.battle .pad .l,body.battle .pad .r{display:none}
```

Verified against the real listener, not the axis: a `pointerdown` on ▼ moves
the cursor 0 → 1 and `pointerup` releases it. The pad binds Pointer Events
with per-`pointerId` tracking and capture, which is the same path that already
walks the overworld on the reporting device.

## 2. The enemies were behind the command panel

Not always — **only with a party of four**, which is why every screenshot this
project has ever taken missed it.

The battle screen was laid out bottom-up from a fixed 960 and never checked
that the pieces fit:

| | |
|---|---|
| `partyPoint` | `V.H − CONTROL_BAND − n·66 − 24` |
| with n = 4 | party strip top **552** |
| panel bottom | 534, panel height 240 → **panel top 294** |
| `GROUND_Y` 386, enemy 128 tall | enemy occupies **258 → 386** |

The panel is opaque and drawn last. With four members it covered the enemy
from 294 down — which is all of it.

### What changed

**The control band is measured, not assumed.** `CONTROL_BAND = 96` was
hard-coded from reading the stylesheet, while 0.31.0 had already built
`AF.controls` to answer exactly this question by asking the DOM. Two answers
to one question (AF-R-801), and the battle used the one that cannot be right
on more than one device. Both errors are measured:

- canvas letterboxed top and bottom → A/B fall **below** it; true band **19**,
  and 96 threw away 77 canvas pixels
- canvas filling the viewport, the reporting device, pad shown → **229**, and
  96 draws the party strip underneath the buttons

**The party strip is two columns above two members.** One column of four rows
is 180px of a 960px screen; the same four in two columns is 90. That 90px is
what buys the log back — see below. Row height 22·S → 15·S, since 22·S held a
name line, a 22px bar and 30px of air.

**The command panel scrolls.** It was sized to `options().length`, so a
character's spellbook decided the whole screen's budget. `PANEL_ROWS = 5` is a
window that follows the cursor, never scrolls past either end, and marks more
above or below with ▲▼. Twelve skills now draw in the same box five commands
do.

**`GROUND_Y` 386 → 210**, putting the enemy band above every arrangement the
budget can produce. The backdrop still draws its full 448; the panel simply
covers its lower part, which is what an opaque panel is for.

**The log moved under the enemies.** It was anchored at `BAND + 6` = 454,
below all of the drawn backdrop — which only worked while the panel started
lower than that. It no longer does, so a log at 454 had negative room and drew
nothing. It measures the space between the enemies' feet and the panel now,
and carries its own scrim, because it draws over grass and grey text on green
is not readable.

### Before and after, at the reporting device's geometry (414×736, band 229, four members)

| | 0.43.0 | 0.44.0 |
|---|---|---|
| enemy | 258 → 386, **entirely behind the panel** | 82 → 210, **fully visible** |
| panel top | 294 | 359 |
| log | 0 lines | header + 3 |
| party strip | 4 rows, 552 → 816, **under the buttons** | 2 rows, 617 → 707, clear |
| d-pad | hidden | ▲▼ shown |

---

## The test that should have existed since 0.30.3

**396 tests passed on the broken build.** Every draw path runs clean whether
or not the panel is on top of the monster — AUDIT_0_9_3's open finding 6 — and
the only way to catch it is to assert the *budget* rather than the drawing.

`the battle screen fits: nothing covers the enemies and nothing hides under a
button` drives the real layout resolvers across **every party size 1–4, five
menu lengths (1, 3, 5, 8, 14 options) and six control bands**, and asserts
five properties:

1. the panel never reaches the enemy band
2. the panel stays under the `PANEL_ROWS` height cap
3. the party strip clears the controls
4. the log has room for the round header **and at least one message** — a log
   that can only print "round 1" tells the player nothing
5. every member sits inside their own cell and on screen

The control band is measured from the DOM at runtime, so the test substitutes
it through a `defineProperty` getter and restores the descriptor in a
`finally`. And it checks the control itself, by putting the body in `battle`
and reading computed styles: up and down must be visible, left and right must
not.

`AF.battle` now exposes `layout`, `GROUND_Y`, `PARTY_ROW`, `PANEL_ROWS`,
`BAND_CEILING` and `controlBand` for this. The suite could not previously ask
where anything was drawn.

## The test found something I had not been told about

At a band of 420 the budget does not fit. **420 is landscape**: the canvas
keeps its 540×960 aspect, becomes a short strip, and a d-pad fixed at 150 CSS
pixels then covers 413 of the 960 canvas pixels.

That is not a regression — it was worse before, with the strip drawn straight
under the buttons — but it is real, and it is now named rather than hidden.
`BAND_CEILING = 292` is *derived*: solving the four rules above for the band
with a full party gives 292. The test asserts the portrait range up to it, and
separately asserts that **40px past the ceiling the budget actually fails** —
so a `BAND_CEILING` that no longer binds cannot let the range above it quietly
stop testing anything.

`AF.battle.todo()` now carries the gap: the battle screen is laid out for
portrait, there is no orientation gate and no landscape layout, and 292 is the
number to design against when someone builds one.

## Revert-proof

Every fix re-broken, one at a time, and the test observed to catch it:

| Reverted | Caught as |
|---|---|
| `GROUND_Y` back to 386 | `log has room for 1 line(s); it needs the header and a message` |
| `controlBand()` back to a constant 96 | `party strip ends at 840, under the controls at 822` |
| `PARTY_ROW` back to 22·S | `log has room for 0 line(s)` |
| panel window removed | `panel is 483 tall, over the 240 cap` |
| `body.battle .pad{display:none}` | `the whole d-pad is hidden in battle` |
| up/down hidden instead of left/right | `up/down are hidden in battle — a touch-only player could press A on one row and nothing else` |
| left/right left visible | `left/right are shown in battle and the battle UI reads only axis().y` |
| single-column strip | `band 229, party 4: log has room for 1 line(s)` |

## Verification

Screenshotted at 414×736 with `deviceScaleFactor: 2` — the reporting device's
geometry, band measuring **229**, matching the estimate exactly.

- **four members**: enemy fully visible, "Husk appears." readable in the log,
  four HP readouts complete (`54/54`, `66/66`, `42/42`, `46/46`), selection
  outline around Aren's cell, ▲▼ pad and A/B present
- **one member**: single full-width row, unchanged in character
- **twelve skills**: five drawn in the same box the five commands use, `▲▼` on
  the header, cursor centred on Jolt, ability icons intact, enemy still clear
- **touch**: `pointerdown` on ▼ moves the cursor, `pointerup` releases

## A defect I introduced and caught in the same pass

The first two-column attempt scaled every width by `COL_W/540`. The `54/54`
readout came out 48px wide and clipped to **`54/…`** — the one number in the
row a player actually reads. The cell is laid out in *fractions of itself*
now, which holds at both widths where scaled constants do not.

## Files touched

- `aetherfall.html` — version, the `body.battle` pad rule, `GROUND_Y`,
  `controlBand()`, `PANEL_ROWS`, `BAND_CEILING`, `PARTY_ROW`,
  `layout.partyGrid`/`partyPoint`/`panelBox`, the log block, the party strip,
  the panel window, six new exports, one new self-test, two `todo()` lines

## Not verified

- Nothing on a device. This is the second consecutive version whose whole
  point is a device report, and the fixes are measured against a browser at
  the device's geometry rather than against the device.
- The Custodian fight has still never been played end to end — but for the
  first time it plausibly *can* be, on a phone, with a full party.
