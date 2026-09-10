# Aetherfall — change report, 0.36.1 → 0.37.0

Two music tracks, and the first honest look at the audio that was already
shipping.

```
Files / sections changed:
  aetherfall.html
    · AF.build     — 0.36.1 -> 0.37.0 (save schema unchanged at 4)
    · AF.audio     — SRC now holds two tracks; TRACK_FOR splits indoor/outdoor
    · AF.selftest  — 388 -> 389

Rules touched (AF-R-###):
  AF-R-303   a region with no cue of its own borrows one, visibly
  AF-R-1002  the borrowed cue is reported in todo() rather than hidden

FLEXIBLE choices made (AF-R-802 requires stating these):
  1. 80 kbps mono, 90-second loops. The user's call on the quality/size
     tradeoff, made against a measured table.
  2. Interiors get the second arrangement; exteriors and the barrow keep the
     first. Also the user's call.
  3. The loops are CROSSFADED, not cut. See below — neither piece has a
     natural loop point.
  4. The barrow keeps village music, deliberately and visibly.

Assumptions made:
  None.

Self-test: 389/389, three consecutive runs, identical
Boot faults: 0
Verified how: headless Chromium — both tracks decode, the map switches
  outdoors -> village_a and indoors -> village_b. NOT device-verified, and
  nobody has heard this through a phone speaker.
```

## What was already in the build

`village_a` was **the first 75 seconds of track 1 at 48 kbps mono**. Confirmed
rather than assumed: its loudness envelope matches track 1 from offset 0 at
0.981, against 0.862 for track 2.

48 kbps mono is roughly speech-grade. It was the most compressed thing in the
build by a distance, in a project that otherwise verifies every atlas rect
byte-for-byte against its source.

## The two supplied files are different pieces

| | Duration | Encode |
|---|---|---|
| `Welcome_to_the_Village.mp3` | 233.6 s | 190 kbps stereo, 48 kHz |
| `Welcome_to_the_Village_2.mp3` | 238.0 s | 183 kbps stereo, 48 kHz |

Their loudness envelopes correlate **0.766** — related, but not the same
performance. Two arrangements, not two exports of one take. That is what makes
the indoor/outdoor split worth the bytes.

## Neither piece has a loop point, so the loop is built

A 90-second cut clicks. Searching 70–110 s for a seam where the tail leads
naturally back into the head found nothing usable — best correlations were
+0.09 and +0.07, which is essentially uncorrelated. These are through-composed
four-minute pieces, not loop-designed game cues.

So the loop is constructed with an equal-power crossfade:

```
out[0..f]  = head[0..f] * sin + tail[T..T+f] * cos
out[f..T]  = source[f..T]
```

At the wrap, `out[T-1] -> out[0]` reproduces `source[T-1] -> source[T]` —
adjacent samples in the original. The seam is continuous by construction, and
the material that would have been cut off is folded back over the opening
instead of discarded.

## Size, stated plainly

```
before   2.74 MB    one track,  440 KB mp3
after    4.46 MB    two tracks, 879 KB each
```

**That is 1.7 MB more, not the 0.6 MB the one-track option quoted** — two
tracks at the chosen quality cost the quality choice twice. The number is here
rather than buried because it is the single biggest cost in the build:

| | KB |
|---|---|
| Audio (2 × 879 KB, base64) | 2,344 |
| Atlas (base64) | 432 |
| Everything else — engine, content, 389 tests | ~1,800 |

`DOMContentLoaded` moved 1,320 ms → 1,327 ms locally, because a `data:` URI is
not decoded until something asks for it. On a phone over cellular the transfer
is the cost, and that is not measurable from here.

**The lever, if 4.46 MB is too much:** interiors are short visits. Dropping
`village_b` to a 60-second loop saves ~290 KB; 64 kbps saves ~440 KB. One
re-encode either way.

## The barrow still plays village music

Deliberately. Neither supplied piece is barrow or boss music, so the Custodian
fights to the settlement's theme. That is the same call AF-R-303 makes for
ground with no measured art: borrow visibly and report it, rather than hide the
gap with silence. `AF.battle.todo()` names it.

## A test for the shape this project keeps finding

`every embedded track is reachable from some scene` — the reverse of the
existing cue test. `village_b` costs 879 KB of the download whether or not any
scene names it, so a remap that quietly pointed everything back at `village_a`
would leave those bytes shipping, decoded, and never heard. A complete asset
nobody can reach, in the family of the door in 0.6.18 and saving before 0.11.0.

Revert-proven: pointing the three interiors back at `village_a` fails it with
*"embedded but named by no scene: village_b"*.
