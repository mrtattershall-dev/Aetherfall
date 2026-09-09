# Change report — 0.42.0

**Build** `Aetherfall 0.42.0 · rowans-hold · save v4`
**Self-test** 395 / 395, three consecutive runs, 0 boot faults, no page errors
**Size** 5,457,517 bytes (+621,086 from 0.41.0) — **read the size warning below**
**Branch** `claude/newest-build-nv7xsl`

---

## What changed

`AF.ambience` — the second looping channel. Every scene in the game now has a
room tone under the music.

Fourteen ambience beds have been on the shelf since 0.37.0 with nowhere to go.
`AF.audio` holds exactly one looping cue and a scene change replaces it, so a
bed could only ever have played *instead of* the score. Three beds play now,
crossfading on every scene change, on their own gain, under the music.

| Scene | Bed |
|---|---|
| `rowans_hold` | forest |
| `forest_route` | forest |
| `barrow_downs` | **cave** |
| `guild_hall_interior` | inside |
| `shop_interior` | inside |
| `inn_interior` | inside |

Three beds, 150,204 bytes each: **MPEG-1 Layer III, 44.1 kHz, mono, 40 kbps**,
30-second loops. `VOLUME = 0.32` against the music's `0.5`.

---

## Why `barrow_downs` gets the cave bed

This is a judgement, and it is the one entry in the table worth arguing about.

The barrow is drawn out of doors — ruins, dead trees, grave markers, open sky.
The *literal* answer is the forest bed. But the forest bed is birdsong, and
birdsong over a field of skulls makes an active claim about the place:
pleasant woodland. The cave bed claims stillness and depth, which is what the
scene, the Custodian's canon and the seal at the end of the trail are all
saying.

The less literal cue is the less wrong one. **FLEXIBLE (AF-R-802)** — change
that one table entry to `"forest"` to hear the other reading. Nothing else
moves.

There is a related irony now recorded in `AF.battle.todo()`: the barrow's
*ambience* is right and its *music* is still village music, because neither
supplied track is barrow music. The bed is carrying the scene and the score is
fighting it.

---

## The bug the new test caught, in my own work

I encoded the first pass of the three beds with `lame -b 32`. LAME chose
**MPEG-2 Layer III at 22.05 kHz** on its own, because that is the better
trade at 32 kbps — and MPEG-2 Layer III is precisely the encode iOS Safari
refuses to decode.

That is the 0.13.11 bug, reproduced exactly. It cost that pass four versions
of chasing `NotAllowedError` before anyone measured the bytes.

It did not survive one test run this time, because the first thing I did with
the encode test was widen it:

```js
for (const id of AF.audio.ids())     sources.push([`music/${id}`,    AF.audio.uriOf(id)]);
for (const id of AF.ambience.ids())  sources.push([`ambience/${id}`, AF.ambience.uriOf(id)]);
for (const id of AF.sfx.ids())       sources.push([`sfx/${id}`,      AF.sfx.uriOf(id)]);
```

The test had only ever read the music. Nothing about that failure is specific
to music — an ambience bed or a sound effect encoded the same way is just as
silent on the same phone for the same reason, and until this version there was
no test that would have said so. It now reads the first MPEG frame header of
all **24** embedded clips.

Re-encoded with `--resample 44.1` forcing MPEG-1, plus an 11 kHz low-pass
before the encoder so 40 kbps is spent on the band that carries a room tone
rather than on hiss it cannot afford to keep.

---

## The seam, and why `loop = true` was not enough

An MP3 decoder hands back more samples than were encoded. **Measured in
Chromium, not assumed:** each 30.000 s bed decodes to **30.0408 s** — 40.8 ms
of padding, split between LAME's ~1105-sample encoder delay at the head and
the tail pad out to a whole 1152-sample frame. Both decode as silence.

`srcNode.loop = true` on the raw buffer therefore puts a ~40 ms hole in the
bed every thirty seconds. That is the audible join `AF.audio`'s own header has
admitted to since 0.13.1 and never fixed.

```js
n.loopStart = LOOP_TRIM;                    // 0.05
n.loopEnd   = buf.duration - LOOP_TRIM;     // measured live: 29.9908
n.start(0, n.loopStart || 0);
```

Fifty milliseconds clears both ends with room to spare. The cost is that the
loop point moves 50 ms relative to the seam the material was built around —
and the material was built for this:

> each bed is a 30 s loop whose first three seconds are an **equal-power
> crossfade** with the material that follows the end, so the two ends are
> continuous by construction

Fifty milliseconds of drift inside a three-second blend of broadband noise is
not audible. A forty-millisecond hole is.

**This is a candidate fix for the music too.** `AF.audio` still loops its raw
buffer and still gaps. I have not touched it — that module cost 0.13.0 through
0.16.1 to stabilise and it is not mine to change on the way past — but the
technique is now proven in the same build, on the same context, and the change
would be two lines.

### How the beds were built

```
mono fold  →  RMS-normalise to −26 dBFS  →  low-pass 11 kHz
head  = source[0..3]   faded IN  (equal-power)
      + source[30..33] faded OUT (equal-power)
loop  = head + source[3..30]                      # 30.000 s
```

At the loop point the end of the body (source t=30) flows into the head, which
*opens* on source t=30 at full level. Continuous by construction rather than
by luck.

Normalising after the mono fold, not before — the first attempt normalised the
stereo file and the fold then lost ~3.5 dB of decorrelated content, leaving the
three beds 1.5 dB apart instead of matched. Measured mono RMS after: **0.0464 /
0.0465 / 0.0393**.

---

## ⚠ Size — the one thing that needs you

**The build is now 5.46 MB.** The only hard device data point this project has
is a rejection:

> 0.13.0 embedded BOTH at mono 32 kHz 64 kbps and the build went 1270 KB →
> 6202 KB. **The device rejected that build.**

5.46 MB is 88% of the size that failed on your phone, and **nothing since
0.13.1 has been tested on a device at all**. Every size decision in this
version was made against that number:

- 30-second loops, not the supplied 60 (would have been 5.8 MB)
- 40 kbps, not 64
- three beds, not fourteen

**Before any more audio goes into this build, it needs to open on your iPhone.**
That is a five-minute check that unblocks every remaining decision, and I
cannot do it from here.

---

## Design notes

**A third module, not a second table.** Music is a cue the player notices; an
effect is fire-and-forget; ambience is a bed that must never be noticed at all,
and the way it fails — a gap, a click, a level that fights the score — is
nothing like the way a track fails.

**The context is shared for the third time**, deliberately. iOS unlocks a
*context*, not a sound. The gain node is private, so the three levels are
genuinely independent.

**`AF.audio.unlock()` now emits `audio:unlocked` on every call**, not just the
first. Ambience needs the same retry-on-every-gesture property that module
learned the hard way in 0.13.1 and 0.16.1 — one rejected start must not poison
the state forever. Giving it the signal is cheaper and safer than letting it
keep a second idea of who is unlocked (AF-R-801). Emitted *before* the rest of
`unlock()` so a throw in `start()` cannot skip the listener.

**An unknown bed is refused silently**, matching `AF.sfx.play`. A warn would be
correct in principle and wrong in practice: the only caller is a table the
suite proves total on every boot, so the only way to reach that line is a probe
from that suite — and a diagnostics panel that cries wolf once per boot is one
nobody reads when something is actually wrong.

---

## Tests

Three new (395 total, up from 392), plus the widened encode check.

**`every scene has an ambience bed and every bed named exists`** — stricter than
the music equivalent, deliberately. That one checks its own table is well
formed; this one also checks the table is **total**. Music has a defensible
reason to leave a room quiet. A room with no ambience is not quiet, it is
dead, and the absence reads as a bug rather than a choice.

**`ambience is its own channel, under the music, and mutes independently`** —
level ordering, three-way mute isolation, both bounds on `LOOP_TRIM` (a trim of
0 and a trim of 2 s are both silent failures), and that the unlock listener is
still wired.

**`a scene change asks for that scene's bed, and asking twice is idempotent`** —
drives the real `want()` through the real table.

That last one **skips when a bed is already audible.** At boot, which is when
it always runs, nothing is playing and the whole test executes. Re-run from the
diagnostics panel mid-game it would otherwise crossfade the player's ambience
to another room and back — a session leak you can *hear*. The suite's contract
is that it leaves the player's game exactly as it found it, and that has to
cover the speaker as well as the save. The runner has no skip state, so the
skip announces itself through `AF.diag.note` rather than passing silently.

## Revert-proof

Every new assertion was undone and observed to fail.

| Change | Result |
|---|---|
| `delete BED_FOR.inn_interior` | `inn_interior has no ambience bed` |
| `BED_FOR.inn_interior = "swamp"` | `inn_interior names missing bed "swamp"` |
| `LOOP_TRIM = 0` | `LOOP_TRIM 0s does not clear an MP3 decoder's head padding` |
| `LOOP_TRIM = 2.0` | `LOOP_TRIM 2s is wider than the seam it is protecting` |
| remove the `audio:unlocked` listener | `ambience no longer listens for the unlock, so it can never start on a phone` |
| `VOLUME = 0.9` | `ambience 0.9 is not under the music 0.5 — a bed that competes with the score has failed` |
| first encode pass (`lame -b 32`) | `ambience/forest: not MPEG-1 (version bits 2)` ×3 |
| all restored | 395 / 395 |

## Live verification

Headless Chromium with a real trusted click, not a synthetic unlock:

| | |
|---|---|
| context after gesture | `running`, unlocked |
| bed playing in `rowans_hold` | `forest`, 1 start |
| loop window on the live node | `{ start: 0.05, end: 29.9908, looping: true }` |
| decoded duration / padding | 30.0408 s / **40.8 ms**, all three beds |
| `want("cave")` | playing → `cave`, **1** new start, **1** old bed retired |
| `want("cave")` again | 0 additional starts — idempotent |
| decoding | lazy; `cave` was not decoded until it was asked for |
| page errors | none |

---

## Supplied and NOT used — 11 of 14 beds

| Clip | What it is waiting for |
|---|---|
| `Forest_Day_Rain`, `Forest_Day_Storm`, `Forest_Night_Rain`, `Inside_Day_Rain`, `Inside_Night_Rain`, `Inside_Night_Storm`, `Cave_Rain`, `Cave_Storm` | A weather system. There is none — no rain state, no storm state, nothing that could ever select these. |
| `Forest_Night`, `Inside_Night` | A clock. The game has no time of day; `AF.scene` renders one daylit grade. |
| `Torch_Loop`, `Light_Torch_with_Starting_Loop_1` | A lit torch, and positional audio. This build **removed torch pools** when it went daylit (`"Day grade replaces the night grade for this scene; torch pools removed."`), and there is no per-emitter audio at all — every channel here is global. |

Two of these are systems worth building and one is a prop. None of them is an
audio task, which is why none of them happened in an audio pass.

## Still silent

- menus and cursor movement
- death, save, encounter start, the vendor, every refusal
- a missed attack — `battle:miss` fires in four places and plays nothing
- `Bow_Attack` ×2, `Bow_Blocked` ×3, `Rock_Meteor_Throw` ×2, shelved at 0.41.0

---

## Files touched

- `aetherfall.html` — version, `AF.ambience` (≈250 lines + three beds),
  `audio:unlocked` emitted from `AF.audio.unlock`, `AF.ambience.bind()` beside
  the music, three new self-tests, the encode test widened to all three
  channels, two `todo()` lines

## Not verified

- **Nothing has been heard.** The suite proves a bed was *asked for*, that the
  loop window is programmed correctly and that the encode is one iOS accepts.
  It cannot tell whether the cave bed sits right under the Custodian fight,
  whether 0.32 is the correct level against the score, or whether 30 seconds
  is long enough before the forest bed starts to loop noticeably.
- **Nothing device-verified**, and at 5.46 MB that is now the highest-value
  outstanding item in the project.
- The Custodian fight still has never been played end to end.
