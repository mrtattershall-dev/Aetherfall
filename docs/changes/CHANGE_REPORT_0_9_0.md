# Aetherfall — change report, 0.8.1 → 0.9.0

Pacing, and the merchant actually talking. Minor bump: a new module, a changed
speech contract, and a changed interaction flow.

```
Files / sections changed:
  aetherfall-0.9.0.html
    · AF.build         — 0.8.1 -> 0.9.0 (save schema unchanged at 4)
    · AF.ease          — NEW MODULE: one home for every curve
    · AF.transition    — 320ms linear -> 560ms smoothstep
    · AF.speech        — fade in/out, a 6px rise, and a typewriter reveal
    · AF.conversation  — NEW MODULE: a line at a time, then whatever follows
    · AF.content       — merchant prose is a sequence; NPC entries take textIds
    · AF.interact      — a conversation or open shop owns the confirm button
    · AF.render        — nineSlice clamps its corners to the box it is given
    · AF.shopInterior  — the merchant talks first, then opens his shop
    · AF.selftest      — 296 -> 302

Rules touched (AF-R-###):
  AF-R-1011  every id in a sequence is validated, not just the first
  AF-R-801   which line is spoken stays AF.content's job; the runner walks a list
  AF-R-203   the merchant's five new lines ship as [placeholder] prose
  AF-R-405   nothing here scales fractionally; the clamp keeps frames integer

FLEXIBLE choices made (AF-R-802 requires stating these):
  1. Fade is 560ms, smoothstepped. Long enough to read as deliberate, short
     enough that a player crossing a doorway repeatedly does not resent it.
  2. Speech types at 42 characters a second and fades over 180ms either end.
  3. A press COMPLETES a typing line before it advances one — the JRPG
     convention, and the reason a player mashing A cannot skip a line.
  4. Cancel leaves a conversation WITHOUT running what follows it. Backing out
     of a chat must not open the shop you were backing out of.
  5. A vendor zone naming an NPC talks first; one with no NPC opens straight
     away, so nothing else using a vendor zone had to change.
  6. The merchant's greeting still appears in the shop log as well. The panel
     is where a shopkeeper's patter belongs once the shop is up.

Assumptions made:
  None.

Self-test: 302/302, four consecutive runs, identical
Regression checks:
  boots ✓ (0 faults) / five scenes clean ✓ / arrivals ✓ / credits ✓ /
  cited-but-unindexed 0 ✓ / atlas rects in bounds ✓
Verified how: headless jsdom + offline renders of the bubble mid-type,
  complete, and the shop. NOT device-verified.
```

## What "snappy" actually was

Measured rather than guessed, because it could have been five systems:

| System | Before | Now |
|---|---|---|
| Scene fade | 320ms, **linear** | 560ms, smoothstep |
| Speech in | appeared whole, one frame | fades up over 180ms, rises 6px |
| Speech out | vanished, one frame | fades down over its last 180ms |
| Speech text | all at once | types at 42 cps, A completes it |
| Camera | already eased | unchanged — it was fine |

The camera was already frame-rate-independent and smooth, so it was left
alone. Worth saying: a linear fade is what made the transition read as a
flicker rather than a fade — it spends as long in the barely-dark range as the
visibly-dark one. Smoothstep holds the extremes and moves quickly through the
middle, which is what the eye expects from something physical.

`AF.ease` exists so those curves live in one place. A curve copied into three
modules becomes three slightly different curves, and that difference is the
kind nobody can name but everybody feels.

## The merchant talks

Three lines before the shop, two after the barrow gate is cleared:

> *Careful past the forge, it spits.*
> *Everything on the counter is for sale. Everything behind it is not.*
> *Go on then. Have a look.*

`AF.conversation` walks a list and runs a `then` when it ends — opening the
shop, in his case. It owns no prose and no conditions: **which** lines are
spoken is still `AF.content.npcLine`'s decision, first match against world
state. A second copy of that logic in the runner is exactly the drift AF-R-801
is about.

NPC entries now take `textIds` (a sequence) as well as `textId` (one line), so
this works for every future NPC rather than for him specifically. A sequence
with any missing id is skipped **whole** rather than played with a hole in it,
and the install-time validator checks every id in the sequence — a run that
validates on its opening line and dies three lines in is the silent failure
AF-R-1011 exists to prevent.

## The loop that would have trapped the player

A press advanced the dialogue **and** re-probed the zone the speaker stands
in, restarting from line one. Forever.

It could not appear while talking took a single press, which is why nothing
caught it until now. `AF.interact` now ignores confirm while a conversation or
a shop is open: an overlay that claims input has to claim it *there*, not just
draw over the top.

Removing that guard fails three tests, including
*the conversation restarted itself — A is both advancing and re-triggering*.

## Two tests changed, and why that is not weakening them

Both merchant walk-up tests asserted "press A → shop opens", which is no longer
the flow. They now press A and **walk the conversation through** to the shop.

The property each guards is unchanged: stand where a player can stand, face
the counter, press the real button, and end in *this* shop. Only the number of
presses moved, and the press count comes from the data, so adding a fourth line
will not break them — only a broken flow will.

## Three bugs the render caught

None would have failed a test:

1. **The speaker's name rendered as a missing text id.** `nameOf("npc_merchant")`
   resolved nothing because he had no entry — he had never needed a name until
   he spoke. He is `Shopkeeper`, provisional like every other name.
2. **The bubble was a squashed strip.** `ui_panel_slate` has 48px corners on
   screen and the bubble was 72px tall, so top and bottom overlapped by 24.
   `nineSlice` now clamps its corner to half the box, so any caller smaller
   than twice the corner degrades instead of rendering broken — and the bubble
   is 108 tall regardless.
3. **The text sat under the border.** Third surface in this build to hit the
   same thing, so the inset is derived from the frame here too rather than
   written as a number.

## Left for you

- **All five merchant lines are `[placeholder]`**, and so is his name. Canon.
- **No portrait, no name plate art.** The bubble shows a name and a line; the
  Franuka UI pack has banners and frames that could dress it.
- **Nothing wraps yet.** A line longer than the bubble will run off it — the
  vendor log trims, the bubble does not. Worth doing when real prose lands,
  since wrapping against `[placeholder] ` prefixes measures the wrong string.
- **Still not device-verified.** The typewriter and fades are timing-based, and
  timing is the one thing an offline replay models least well.
