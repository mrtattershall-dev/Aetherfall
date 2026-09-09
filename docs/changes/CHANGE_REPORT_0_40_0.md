# Aetherfall — change report, 0.39.0 → 0.40.0

Swords. The commonest event in the game had no sound.

```
Files / sections changed:
  aetherfall.html
    · AF.build     — 0.39.0 -> 0.40.0 (save schema unchanged at 4)
    · AF.sfx       — +5 clips, +2 families, physical mapped, parry precedence
    · AF.selftest  — the element test now asserts the right property

Rules touched (AF-R-###):
  AF-R-801   `guarded` is read from the hit record, not recomputed
  AF-R-1006  an element with no cue stays silent

FLEXIBLE choices made (AF-R-802 requires stating these):
  1. `physical` maps to the sword swing. It is the default element of every
     basic attack, so this is the change that makes combat audible at all.
  2. A GUARDED hit plays the parry INSTEAD of its element, whatever threw it.
     A parried fireball parries.

Assumptions made:
  None.

Self-test: 392/392, three consecutive runs, identical
Boot faults: 0
Verified how: headless Chromium with a real click — physical sounds, fire
  sounds, a guarded physical hit sounds as a parry, ice stays silent.
  NOT device-verified.
```

## Cost

```
5 clips, 64 kbps mono   24 KB base64
build   4.56 MB -> 4.59 MB
```

Ten effects now cost 110 KB against the music's 2.34 MB.

## Guarded beats element, and it is read not inferred

A guarded hit plays the parry whatever element threw it. The defender's answer
is the louder fact — the strike came in and was *turned* — so `guarded` is
checked before the element rather than beside it.

`guarded` is not recomputed here. `AF.battle` already derives it from
`st.guarding`, halves the damage with it, and puts it on the record; this reads
that field. A second idea of who is defending is exactly the drift AF-R-801
keeps catching.

## The old test failed, correctly

0.39.0 asserted that a `physical` hit stays silent. At 0.39.0 that was true.
Mapping `physical` to the swing made it false, and the suite said so
immediately.

That is the test doing its job rather than a regression: the property worth
guarding was never "physical is silent", it was **"an element with no entry is
silent."** It now asserts that with `ice`, `lightning`, `shadow` and `radiant`
— four elements that have a full `LOOK` in `AF.battleVfx` and no cue, which is
precisely the state the rule protects. The picture is there; the sound is
honestly absent.

Rewriting the assertion to name the real property, rather than deleting it or
patching in `physical`, is the difference between a test and a rubber stamp.

Revert-proven: removing the parry precedence fails with *"a guarded hit did not
reach the parry family"*.

## Measured behaviour

| Event | Result |
|---|---|
| physical hit | sound (swing) |
| fire hit | sound (fire) |
| physical hit, guarded | sound (parry) |
| ice hit | **silent** |

## Left for you

- **Four elements still silent** — ice, lightning, shadow, radiant. Four clips
  and four lines each.
- **Ten ambience beds unbuilt**, still waiting on a looping channel and the
  weather / day-night systems three of each set assume.
- **Nobody has heard any of it on a phone.**
