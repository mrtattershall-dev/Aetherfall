# Change report — 0.43.0

**Build** `Aetherfall 0.43.0 · rowans-hold · save v4`
**Self-test** 395 / 395, two runs, 0 boot faults
**Size** 5,941,222 bytes (+483,705 from 0.42.0)
**Branch** `claude/newest-build-nv7xsl`

**The build ran on the device at 5.46 MB.** That is the first device data point
since 0.13.1 and it retires the open question that has gated every audio
decision for six versions. This version spends part of the headroom it bought.

---

## Music, halved

`AF.audio.VOLUME` **0.5 → 0.25**, as reported from the phone.

A level set by ear on a real speaker beats one set by a constant nobody had
heard. The FLEXIBLE choice stands; the number under it changed.

`AF.ambience.VOLUME` **0.32 → 0.20**, tracking it. The bed is mixed *against*
the score, not against silence — leaving it at 0.32 while the music went to
0.25 would have promoted the ambience above the thing it exists to sit under,
which is the one property that module's own self-test refuses.

**`AF.sfx.VOLUME` is untouched at 0.55, and that is now more than twice the
music.** Nothing reported it as a problem, so nothing was changed — but
halving one channel re-balances all three, and effects are the next thing to
listen for.

## Battle music

A fight has always played the field track. `Triumph of Steel` now plays
instead, and the field cue comes back when the fight ends.

Not in `TRACK_FOR`, deliberately — that table is keyed by *scene*, and a fight
is not a scene. It is an overlay that starts and ends inside whatever room the
player was standing in, which is precisely why the field music kept running
through every battle until now.

```js
AF.events.on("battle:started", () => { if (SRC[BATTLE_TRACK]) want(BATTLE_TRACK); });
AF.events.on("battle:ended",   () => want(TRACK_FOR[AF.state.sceneId] || null));
```

`battle:ended` re-reads the **scene table** rather than remembering what was
playing before. One answer to "what should this scene sound like" (AF-R-801),
and a fight cannot strand the wrong cue after an aftermath that moved the
player — which the Custodian's does.

Ambience keeps playing underneath, unchanged, because a fight is not a scene
change. That is the correct behaviour and it now has a verification line.

| | |
|---|---|
| Source | `Triumph_of_Steel.mp3`, 149.6 s stereo 48 kHz |
| Embedded | 60.0 s loop, MPEG-1 Layer III, 44.1 kHz mono, 48 kbps |
| Size | 360,176 bytes → 480,236 base64 |
| Loop | 4-second equal-power crossfade, same construction as the ambience beds |

## ⚠ The second battle track is not in the build, and the reason is arithmetic

`Untitled.mp3` is encoded and ready. It is not embedded because of this:

| | binary | base64 |
|---|---|---|
| `village_a` | 900 KB | 1,200 KB |
| `village_b` | 900 KB | 1,200 KB |
| `battle_a` | 360 KB | 480 KB |
| **music total** | | **2,880 KB — 48% of the build** |

The village pair is 90 s at 80 kbps mono, which is the spec **you chose**. A
second battle track at the same spec costs another 1.2 MB and puts the build
at **7.1 MB**. Even at this version's 48 kbps / 60 s it adds 480 KB and lands
at **6.42 MB** — past the 6.2 MB that the device refused at 0.13.0.

So the battle track shipped at 48 kbps rather than 80, and only one of the two
shipped at all. Both are consequences of one number, and there are three ways
out, all yours to pick:

1. **Test the ceiling.** 5.94 MB is what this build is. If it opens, we know
   more than we did, and 6.42 MB is the next question.
2. **Re-encode the village pair at 64 kbps.** Frees ~480 KB base64 with a
   quality step most phone speakers will not resolve, and both battle tracks
   fit at 60 s.
3. **Shorten the village loops.** 90 s → 60 s frees ~800 KB.

I have not done 2 or 3 on my own: you set 80 kbps / 90 s deliberately when
asked, and quietly walking it back to make room for something else is not my
call (AF-R-1007).

## Test

The reachability test caught this version's own mistake on the first run:

```
every embedded track is reachable from some scene
  — embedded but named by no scene: battle_a
```

That test exists because an unreachable asset still ships, decodes and is paid
for. It read `TRACK_FOR` only, and there are now **two** ways to be reachable.
It has been widened rather than exempted: it reads the constant, checks the
track is embedded, **and reads the source of `bind()`** to confirm something
actually switches on `battle:started` and gives the cue back on `battle:ended`.
Naming `BATTLE_TRACK` and never wiring it would be the same 469 KB of dead
download the test exists to refuse, and a check that only read the constant
would have passed on it.

Renamed to *"every embedded track is reachable, by a scene or by the fight"*.

## Verification

Headless Chromium behind a real trusted click:

| | |
|---|---|
| levels | music 0.25, ambience 0.20, sfx 0.55 |
| in `rowans_hold` | `village_a` + `forest` bed, web-audio backend |
| in `forest_route` | `village_a` + `forest` bed |
| **battle starts** | **`battle_a`** + `forest` bed still playing |
| **battle ends** | **`village_a`** restored, bed unbroken |
| decoded battle track | 60.03 s, 44.1 kHz, mono |
| page errors | none |

## Not fixed in this version

The two defects reported alongside the audio — **no d-pad in battle** and
**the enemies are hidden behind the command panel** — are a layout change, not
an audio one, and are 0.44.0. Both are confirmed reproduced.
