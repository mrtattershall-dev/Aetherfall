# Aetherfall — change report, 0.37.0 → 0.38.0

The first sound effects. The build has had music since 0.13 and, until now,
silence for everything else.

```
Files / sections changed:
  aetherfall.html
    · AF.build     — 0.37.0 -> 0.38.0 (save schema unchanged at 4)
    · AF.audio     — exposes its AudioContext and unlock state
    · AF.sfx       — NEW MODULE: one-shot effects, 5 embedded footsteps
    · AF.sceneKit  — walk() plays a footstep on the foot-plant frames
    · AF.selftest  — 389 -> 391

Rules touched (AF-R-###):
  AF-R-802   the FLEXIBLE choices below
  AF-R-921   timing measured from the sheet, not assumed
  AF-R-1004  an effect that cannot play returns false; it never throws
  AF-R-1012  the picker does not touch the seeded RNG

FLEXIBLE choices made (AF-R-802 requires stating these):
  1. A separate module from AF.audio, sharing its AudioContext but not its
     gain node.
  2. No media-element fallback for effects. No Web Audio means silence.
  3. Clips decode lazily on first unlock, not at boot.
  4. Footsteps fire on the animation's foot-plant frames, not on a timer or
     on distance walked.
  5. The variant picker uses Math.random, deliberately not the seeded RNG.

Assumptions made:
  None. The foot-plant frames were measured out of the atlas.

Self-test: 391/391, three consecutive runs, identical
Boot faults: 0
Verified how: headless Chromium with a real click — context running, all five
  clips decoded, a step fires through the live walk path. NOT device-verified,
  and nobody has heard this through a phone speaker.
```

## Cost

```
5 footsteps, 64 kbps mono   22 KB embedded
build   4.46 MB -> 4.48 MB
```

Effects are 0.5% of what the music costs. This is the shape the earlier note
predicted: **the pack was never the problem, the pack was the wrong unit.**
Five recordings out of it, compressed, are essentially free.

## Why a separate module

`AF.audio` and `AF.sfx` have opposite lifetimes. Music is one long cue that
must survive a scene change; an effect is fire-and-forget and may overlap
itself. Putting both in one module means one of those behaviours pretending to
be the other.

What **is** shared is the AudioContext, and that is not a tidiness decision —
iOS unlocks a *context*, not a sound. A second context would want its own
gesture and would sit suspended until it got one, which is precisely the class
of bug 0.13.1 and 0.13.2 were spent on. The gain node is deliberately *not*
shared, so the music setting and the effects setting are independent.

## Footsteps land on the frame the foot lands on

Not a timer, and not distance walked — both drift out of sync with what is on
screen. The step fires from the same event that advances the sprite, so it
cannot drift.

**Which frames was measured, not assumed.** Reading the silhouette of every
`citizen_down` frame out of the atlas:

```
frame   0    1    2    3    4    5
height 25   27   26   25   27   26   px
```

The body sits lowest — weight on a planted foot — at frames **0 and 3**, and
the cycle is symmetric, which is what a two-step six-frame walk should look
like. That is where the sound goes.

## Five clips, and the rule that makes them worth five

One clip per step is the sound a game makes when nobody thought about it. The
picker excludes the previous clip rather than merely making it unlikely, so a
back-to-back repeat is impossible rather than rare.

It uses `Math.random`, **not** the seeded RNG. AF-R-1012 keeps dialogue out of
the seeded stream so the same world state always gives the same line; the
argument is stronger for a footstep, which would otherwise let how far you
walked decide what the next encounter roll returns.

## A test that could not stub what it wanted to

The first version of the no-repeat test reassigned `AF.sfx.play` to record
picks. It recorded nothing, because `playVariant` calls the module's own
binding rather than the export — correct encapsulation defeating the test.

Rather than weaken the module, the picker's last choice is exposed as
`lastOf(family)`. A headless suite can never hear a footstep, but it can read
the sequence of decisions, which is the part worth guarding.

Both new tests are revert-proven:

| Reverted | Fails with |
|---|---|
| the no-repeat filter | `clip step_dirt_3 repeated back-to-back at 3` |
| the call in `walk()` | `sceneKit.walk no longer plays a footstep; the footstep is no longer tied to the measured foot-plant frames` |

## Left for you

- **This is one family deep.** No menu, hit, death, door, save or encounter
  cue. `AF.battle.todo()` says so. The channel is built, so each of those is
  now a clip and a call site.
- **Ambience is still unbuilt.** The five forest beds need a second *looping*
  channel, and three of them need weather and a day/night clock that do not
  exist.
- **Nobody has heard any of this on a phone.**
