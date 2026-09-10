# Change report — 0.49.0

**Build** `Aetherfall 0.49.0 · rowans-hold · save v5`
**Self-test** 403 / 403 (one new), three runs, 0 boot faults, no page errors
**Size** 6,028,809 bytes
**Branch** `claude/newest-build-nv7xsl`

The landscape work 0.48.0 left open, finished — and the screens turned out to
be broken in **portrait** too, for the opposite reason.

---

## The shape of the bug, on three screens

Each of these draws a variable amount of content into a fixed box, and none of
them said so. Landscape ran out of room immediately because the box got
shorter; portrait ran out of it *eventually*, as a character grew.

| | portrait, before | landscape, before |
|---|---|---|
| ascension board | tree fits; readout fits | tree runs **off the bottom**, readout 54px past the edge |
| party sheet, level 1 | equipment + footer **under the d-pad** | EQUIPMENT begins **15px below the canvas**; it and STATUS, 228px, are drawn where nobody can see them |
| party sheet, board bought out | STATUS drawn **through the footer and onto the panel's bottom frame** (last row at y=930) | as above |
| vendor | correct | every row's cursor, icon and first characters **behind the left thumb** |
| overworld HUD | correct | bottom of the SEAL bar **behind the d-pad** |

## The board turns on its side

Every board is three columns by seven rows — 462px tall, which a 540px screen
cannot hold once the banner and the node readout are paid for. Turned ninety
degrees it is 462 **wide**, and width is what landscape has to spare.

```js
const turn = V.W > V.H;
const gx = (n) => turn ? n.y : n.x, gy = (n) => turn ? n.x : n.y;
```

Two lines, because **the graph is untouched**: every prerequisite line is
drawn from the node positions, so rotating the placement rotates the whole
picture and there is no second board layout to keep in step. It reads better
wide than tall — the root sits at the left with its two branches diverging and
rejoining, which is what the board *is*.

The **pitch** also stopped being a constant. `22 * S` was what a 960-tall
screen could afford; once the panel stopped running behind the d-pad there
were 575px of interior, and a seven-row tree at that pitch pushed the
"costs N" readout onto the footer line. It is now derived from the room left,
with a floor of `18 * S` — a node's own box — so icons never touch. The icons
themselves stay `16 * S` whatever happens to the spacing, which is the part
AF-R-405 is about.

## The party sheet is a head and a flow

The screen is a **head** of fixed size (name, vitals, stats) and a run of
**sections** whose length depends on how far the character has grown: a
level-1 Aren lists one ability, a bought-out one lists seven.

- **Landscape** sets the head in a 40% column, because the bars are the one
  part of this screen that wants width, and gives the sections the rest.
- **Portrait** keeps the full width it always had, and goes two-up **only when
  the sections do not fit one column** — so a starting character's sheet is
  laid out as it always was.
- Each section lands in the **first column that can hold it**. That is not the
  same as a cursor that only moves forward: with one cursor, a long ABILITIES
  list pushed EQUIPMENT into the second column and STATUS off the screen while
  the first column still had 92px free.
- The equipment **slot strip wraps**. Four icons at an 18 × S pitch are 216px
  and a portrait column, once the screen went two-up, is 186 — the fourth slot
  was drawn through the panel's right frame. *Found by the new test on its
  first run, not by looking.*

**Nothing goes missing in silence.** A list too long for its column trims with
"+N more"; a section that fits nowhere is named in the footer as `+STATUS`,
the same vocabulary the trimmed lists use. If the note will not fit beside the
hint, **the hint gives way** — up and down are two arrows a player will find,
and a section they cannot see is not.

Three smaller repairs fell out of the same read:

- **`HP` and `MP` were drawn on the bar frame's left cap**, in every
  orientation, because the `8 * S` inset was narrower than the two letters it
  was meant to clear. Measured now, like the readout on the other side.
- **The readout reserved 212px for "8888/8888"**. Four-digit HP does not exist
  in this game, and that reservation is most of a landscape column — which is
  why the bars had nowhere left to be. It is measured against the readouts the
  character can actually show, `max` on both sides so it does not shift as HP
  falls.
- **A narrow column drops the slot prefix** — "Chipped Knife" rather than
  "weapon: Chipped Kni…" — because the icon strip above already names the four
  slots and the name is the half the player does not know. The choice belongs
  to the **list**, not the row: per row it put "Chipped Knife" directly above
  "body: Rag Wrap", which reads as a mistake rather than as a column doing its
  best.

## The vendor and the HUD clear the thumbs

0.31.0 stopped the shop panel running behind the pad at the **bottom**, which
was the whole question in portrait. In landscape the controls move to the left
and right edges, so the same rule now applies to the axis the orientation
actually spends:

```js
const PX = Math.max(8 * S, AF.controls.left);
const PW = Math.min(V.W - 8 * S, V.W - AF.controls.right) - PX;
```

The overworld HUD moved the same way. Its three numbers are the ones a player
checks mid-fight, and the bottom of the SEAL bar was behind a hand.

> **A false positive worth recording.** The first vendor probe reported the
> price "32 (can't afford)" running 99px off the right edge in *both*
> orientations. It does not: the price is drawn with `textAlign = "right"`, so
> it *ends* at the margin. My probe added the string's width to the x it was
> passed. The measurement was wrong, not the game — the same class of mistake
> as the deep audit's three false positives, and caught the same way, by
> checking the claim before writing it up.

## The test

**`the party screen stays inside its panel and above the thumbs`** — asserted
from **what reaches the canvas**, not from the layout helpers, because the
helpers were not the thing that was wrong; the drawing was. It spies on the
context's `fillText` and on `AF.render.blit`, and drives the real path (A on
the sheet is what opens the board).

Across both orientations, both views, four control bands each, and **a
character who has bought their whole board** — the case that overflows — every
mark must be inside the panel's interior, above the footer, and clear of the
left, right and bottom thumbs. Every section must be drawn or named. Every
board node must be visible and its cost readable, because a choice you cannot
price is not a choice.

And one claim about the shipping configuration rather than the general case:
**a starting character's whole sheet must fit**, with nothing hidden at all.

**Revert-proof** — eight, all caught:

| Reverted | Caught as |
|---|---|
| board never transposes | `landscape, board: "«icon»" at y 444..492 is outside the panel interior (60..474)` |
| screen ignores the thumbs | `portrait: "up/down: party  B:" ends at 894, under the controls at 864` |
| icon strip never wraps | `portrait: "«icon»" at x 447..495 is outside the panel interior (66..474)` |
| board pitch fixed at `22 * S` | `portrait, board: "held" at y 624..648 is outside the panel interior` |
| a section that does not fit is dropped in silence | `bought out: the STATUS section is neither drawn nor named as hidden` |
| sections flow forward only | `a starting character's EQUIPMENT section does not fit` |
| head keeps the full width in landscape | `"ABILITIES" at x 835..925 is outside the panel interior (162..826)` |
| the note is never drawn | `bought out: the STATUS section is neither drawn nor named as hidden` |

> The sixth revert **passed on its first attempt**, and the test was wrong, not
> the revert. The footer's `+STATUS` note *contains* the substring `STATUS`, so
> a substring match called a hidden section drawn and waved through a layout
> that had dropped one. Exact matches now. A test that reports the right answer
> for the wrong reason is worse than no test, because it is trusted.

## Verified

- 403/403 × 3 runs, 0 boot faults, no page errors
- **Portrait battle is unchanged** — re-screenshotted at 414×736 against 0.46.0
- Landscape at 896×414: sheet, board, vendor and overworld HUD all
  screenshotted with nothing off-canvas and nothing under a thumb
- Portrait at 414×736: sheet and board at level 1 and with the board bought
  out — the footer hint is legible for the first time

---

## Not finished

**The key art is portrait-shaped.** The title's illustration is a tall image
centred in a wide frame, so landscape shows it with dark margins either side.
An asset, not a layout: it needs a wide crop or a wide painting.

**The corridor question is a judgement now, not a defect.** `forest_route`
(2560 tall) and `barrow_downs` (2176) are north–south corridors, and landscape
shows 540px of what is ahead instead of 960 — 44% less on the axis you are
travelling. Every landscape screen is now worth looking at, so it can be
judged (AF-R-1007).

**A bought-out character's sheet still does not fit portrait** above the
thumbs. The section area is two columns of 212px and the content is roughly
516; the screen shows five abilities, "+2 more", the whole equipment block,
and names STATUS as hidden. That is a labelled shortfall rather than a lie,
and closing it properly means per-column control bands — the pad and the A/B
buttons sit at different heights — which is a bigger change than this pass.

**Still true:** nothing device-verified since 0.43.0, and balance remains
simulated rather than played.
