# Finding — the Barrow Downs leaked out of the world

Found while siting the Custodian encounter at the deepest point of
`barrow_downs`. **Fixed and revert-proven in 0.35.0.**

## What was wrong

`AF.barrowDowns`'s edge guards were copied from `AF.forestRoute`, whose south
edge really does open onto this scene. Three things came with the copy, and all
three are wrong here:

1. **A two-tile gap in the south wall at columns 8-9.**
2. **An `EXIT_SOUTH` constant** — declared, and never used by anything in the
   module.
3. **The comment explaining them:** *"the south end opens onto the barrow
   downs. The trail leaves at columns 8-9 (see PATH's last segment)."*

Neither half of that comment is true in this scene. Its south end opens onto
nothing — `deep_barrow` has no map, which the module header states plainly —
and its trail leaves at **columns 13-14**: `PATH`'s last segment is
`seg(13, 12, 14, 33)`.

So the wall had a hole where no trail runs, opening onto a scene that does not
exist, with nothing watching it.

## Why nothing stopped the player

`AF.collision.move` tests the blocker list and **never clamps to the world
box**. The camera clamps; the player does not. Edge containment in this engine
is entirely the outer guard blockers, so a gap in a wall is not a scenic edge —
it is a way out of the map.

No `edgeExit` watched that gap either, so there was not even a refusal to hit.

## Measured, before the fix

Driven through the real `AF.collision.move` step in headless Chromium:

| Walk | Result |
|---|---|
| Down columns 8-9 (the hole) | crossed the world's bottom edge and kept going — **1,472px out and still moving** when the probe stopped |
| Down columns 13-14 (the trail) | **stopped at the wall**, correctly |

That contrast is why this survived: a player walking the map the way the map is
laid out follows the trail, hits the wall, and turns around. The hole is two
tiles to the west of anywhere the trail goes.

## The fix

The south wall is one span. `sGapX0`/`sGapX1` and the unused `EXIT_SOUTH` are
gone, and the comment now says what is actually true, including the condition
for the gap's return:

> When `deep_barrow` is built the gap comes back at the TRAIL's columns and an
> edgeExit comes back with it — both together, or neither.

## The test

`no column of the barrow lets the player walk out of the world` drives the real
collision step from inside the map, down **every** column and out to both sides.
It guards the class, not the instance: a hole cut anywhere in any of the four
walls fails it.

Revert-proven. Restoring the gap fails it with:

```
south@col8 reached y=3008 of 2176; south@col9 reached y=3008 of 2176
```

## Where it sits in the pattern

This is handoff §6 — *geometry is not logic* — with a twist worth keeping. §6's
examples are all zones that were **correct as data and wrong as geometry**. This
is the inverse: geometry that was correct for the module it was written in and
wrong for the module it was pasted into, carrying its own explanation with it so
that reading the code confirmed the mistake.

**A comment copied with the code it explains will lie in the new file with
exactly the authority it had in the old one.**
