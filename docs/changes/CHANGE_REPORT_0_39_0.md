# Aetherfall — change report, 0.38.0 → 0.39.0

Doors and fire. Five more clips, two more call sites, and a correction I owe
you about the effect layer.

```
Files / sections changed:
  aetherfall.html
    · AF.build       — 0.38.0 -> 0.39.0 (save schema unchanged at 4)
    · AF.sfx         — +5 clips, +3 families, ELEMENT map, plays() counter
    · AF.transition  — to() takes opts.sfx
    · AF.demo / interiors — the six door call sites say which cue they are
    · AF.selftest    — 391 -> 392

Rules touched (AF-R-###):
  AF-R-802   the FLEXIBLE choices below
  AF-R-1006  an element with no cue is silent, never borrowed

FLEXIBLE choices made (AF-R-802 requires stating these):
  1. The cue lives on AF.transition.to as `opts.sfx`, not on each door.
  2. Entering plays door_open; leaving plays door_close.
  3. ELEMENT is a mapping only. An element with no entry is SILENT.
  4. AF.sfx listens for battle:hit itself, beside AF.battleVfx's listener
     rather than inside it.

Assumptions made:
  None.

Self-test: 392/392, three consecutive runs, identical
Boot faults: 0
Verified how: headless Chromium with a real click — 10 clips decoded, a fire
  hit sounds, a physical hit does not, a door sounds, a wilderness edge does
  not. NOT device-verified.
```

## Cost

```
5 clips, 64 kbps mono   64 KB base64
build   4.50 MB -> 4.56 MB
```

## A correction: combat was never visually inert

I told you twice that the effect layer was missing and that it was the biggest
polish gap, on the strength of `AF-R-705` / `AF.effects` being listed as a
phantom symbol. **That was wrong.**

`AF.battleVfx` shipped at 0.30.0. It is live — updated in the battle loop,
drawn, screen-shake included, and covered by self-tests. It carries a per-element
`LOOK` table with a distinct tint, glow, spark and shape for physical, fire,
ice, lightning, shadow and radiant, and it uses a hashed spread rather than the
seeded RNG so a cosmetic spark cannot change a fight.

The rule index says `AF.effects` does not exist, and it does not. The
*capability* does, under another name. That is the phantom-symbol trap running
backwards: I trusted the index over the build, in a project whose own handoff
says to measure the build. The right fix is an index amendment re-pointing
AF-R-705 at `AF.battleVfx`, which is a §31 call and yours (AF-R-1007).

## Why the cue lives on the transition

`AF.transition.to` is shared: the six doors use it, and so do the wilderness
edge exits. A sound attached to transitions in general would fire walking from
the Outwood into the barrow, which is not a door.

So `to()` takes `opts.sfx` and plays nothing without it. Every existing caller
is unchanged and silent; the six doors each declare what they are. The
transition is the one thing that knows a journey happened, so the cue belongs
there rather than copied into six handlers.

## The element map is a mapping, not a fallback

`ELEMENT = { fire: "fire" }`. Ice, lightning, shadow and radiant hits are
**silent**, deliberately — the same rule `AF.battleVfx`'s `LOOK` table follows
in reverse. A wrong sound reads as a bug; no sound reads as a gap, and the gap
stays honest until the recordings exist. Send four more clips and it is four
lines.

`AF.sfx` listens for `battle:hit` beside `AF.battleVfx`'s listener rather than
inside it. Picture and sound are different concerns with different failure
modes, and a missing clip must not be able to take a frame of animation with it.

## A counter, because `lastOf` could not see it

The first verification asked "did the last pick change" and reported the doors
silent. They were not. `door_open` is a one-clip family, so its pick repeats by
definition and the previous value was already set by the boot suite.

`plays()` counts calls instead, and counts them **before** `play()` — the count
answers *was this asked for*, not *was it audible*. An effect asked for before
the first gesture is correctly silent and still happened.

Both halves of the new test are revert-proven:

| Reverted | Fails with |
|---|---|
| the cue in `to()` | `a transition asked for a door cue and none was played` |
| mapping physical to fire's sound | `an unmapped element borrowed a sound instead of staying silent` |

## Left for you

- **Interior ambience is still unbuilt** — five more beds arrived, and like the
  forest set they need a second *looping* channel, plus the weather and
  day/night systems three of them assume.
- **Silent still:** menus, non-fire elements, death, save, encounter start, the
  vendor, and every refusal.
- **Nobody has heard any of it on a phone.**
