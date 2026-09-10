# Change report — 0.41.0

**Build** `Aetherfall 0.41.0 · rowans-hold · save v4`
**Self-test** 392 / 392, three consecutive runs, 0 boot faults, no page errors
**Size** 4,836,431 bytes (+13,538 from 0.40.0)
**Branch** `claude/newest-build-nv7xsl`

---

## What changed

The magic half of combat made no sound. `physical` had the sword swing since
0.40.0 and `fire` had its cue since 0.39.0; **ice, lightning, shadow and
radiant** — four of the six elements the game draws an impact for — landed in
silence. Every spell in the book is one of those four: `rime`, `arc`,
`gloom_lance`, `dawn_mote` and twenty more.

They are voiced now.

| | |
|---|---|
| New clips | `magic_1`, `magic_2`, `magic_3` |
| Source | `Spell_Impact_1/2/3.wav`, supplied by the user |
| Encode | 44.1 kHz mono, 64 kbps MP3 — the same recipe as every clip since 0.38.0 |
| Sizes | 3,551 / 2,924 / 3,551 bytes → 13,492 chars base64 |
| Durations | 0.372 / 0.308 / 0.372 s, decoded in a real `AudioContext` and measured |

`AF.sfx.ELEMENT` gains four entries, all pointing at the one new family:

```js
const ELEMENT = { fire: "fire", physical: "swing",
                  ice: "magic", lightning: "magic", shadow: "magic", radiant: "magic" };
```

Total effect payload is now 101,537 bytes across 18 clips, all of which decode
without error in Chromium.

---

## The decision this softens, stated plainly

0.39.0 wrote a rule into the module and this version bends it. That is worth
being explicit about rather than letting the diff carry it quietly.

> a mapping only, and an element with no entry is SILENT rather than borrowing
> another element's sound. A wrong sound reads as a bug; no sound reads as a
> gap, and the gap is honest until the recordings exist.

Four elements now share one recording. Under the strictest reading of that
sentence they should have stayed silent until four bespoke cues existed.

**The reason for going ahead.** The rule's actual target is *impersonation*.
`ice` playing the FIRE cue would be a specific wrong claim — the player hears
a whoosh of flame over white shards and reads it as a bug, which is exactly
what the rule was written to prevent. `magic` claims no element. It is the
sound of a spell landing, which is true of all four, in the same sense that
one physical impact serves every weapon that will ever swing.

The identity is not lost, because it was never the sound's job. `AF.battleVfx`
draws ice as white shards, lightning as a yellow bolt, shadow as a violet
pulse and radiant as a gold ring, on the same frame the cue fires. A player
looking at the screen is never in doubt which element hit.

**The cost, honestly.** Four elements sound alike. That is a real quality
ceiling and it is recorded as one. The gain is that the magic half of the game
stops being mute, which was the louder defect of the two.

**FLEXIBLE (AF-R-802).** One bespoke cue per element is strictly better and
needs four recordings that do not exist yet. When they arrive, each element
takes its own family in `VARIANTS` and `magic` retires. Nothing else has to
move — the map is still a map.

---

## The test that was quietly going obsolete

0.40.0 proved the silence property with `ice`:

```js
const unmapped = Object.keys(AF.battleVfx ? { ice:1, lightning:1, shadow:1, radiant:1 } : {})
                       .filter(e => !AF.sfx.ELEMENT[e]);
if (!unmapped.length) bad.push("no unmapped element left to prove silence with");
```

That was correct at the time and it had a fuse in it. `ice` was the witness
*because* `ice` happened to be silent — so voicing `ice` was guaranteed to
either fail the test or force the witness list to be edited. The guard on line
3 shows the shape was already suspected: it knew the witnesses could run out.

The property under test is *"an element with no entry plays nothing"*, and that
should hold whether or not a real gap exists on the day the suite runs. It is
now asserted against a name no element will ever have:

```js
AF.events.emit("battle:hit", { element: "no_such_element_probe", final: 1 });
```

Which is a test that cannot go obsolete when the roster fills.

## And a new one, in its place

The vacated slot is filled by a stronger claim — the picture and the sound are
held to the same roster:

```js
const unheard = Object.keys(AF.battleVfx.LOOK).filter(e => !AF.sfx.ELEMENT[e]);
if (unheard.length) bad.push(`drawn but silent: ${unheard.join(", ")}`);
```

`AF.battleVfx.LOOK` is exported read-only (and frozen) for this. It is the
closest thing the build has to a list of elements the game actually *draws*,
and an element drawn without a cue is precisely the gap this version closed.
The seventh element, whenever it arrives, cannot ship silent without the suite
saying so.

Also added: each of the four elements is asserted to reach the family
individually rather than the first one standing in for all four, the family is
asserted non-empty, and the 0.40.0 precedence rule — *a guarded hit is a parry
whatever threw it* — is re-asserted with `shadow`, since it now has to survive
four new entries in the element map.

## Revert-proof

Each new assertion was undone in a live page and observed to fail:

| Change | Result |
|---|---|
| `delete AF.sfx.ELEMENT.radiant` | `drawn but silent: radiant; a radiant hit played no cue` |
| `AF.sfx.VARIANTS.magic = []` | `family magic is empty` + all four elements report an empty family and no cue |
| voice the probe element | `an element with no entry borrowed a sound instead of staying silent` |
| `AF.battleVfx.LOOK.physical = null` | no effect — the table is frozen |
| all restored | PASS |

---

## Clips supplied and NOT used

Ten clips arrived in that batch. Three are in the build. **Seven are not, and
none of them is an oversight.**

| Clip | Why it has no home |
|---|---|
| `Bow_Attack_1/2` | There is no bow. The string `"bow"` appears exactly once in 19,854 lines of source, inside the word *elbow*. No ranged weapon, no ranged ability, no ranged enemy behaviour. |
| `Bow_Blocked_1/2/3` | Same absence. A blocked arrow needs an arrow. The nearest live concept is a guarded hit, and that is a parry — it already has `parry_1/2`, recorded on a sword, which is the weapon actually being parried. |
| `Rock_Meteor_Throw_1/2` | No earth element and no thrown-projectile animation. The game *does* have thrown flasks (`fire_flask`, `frost_flask`, `static_jar` carry `throwPower`), and a throw whoosh would genuinely belong there — but no event fires at the moment of the throw, only at the impact. Wiring it means adding that event, which is a combat-timing change and not an audio change. |

Filing them against the nearest-sounding event would put a bowstring on a
sword swing, which is the mistake the element rule exists to prevent. They stay
on the shelf until the systems behind them exist, and this table is the record
of what each one is waiting for.

## Still silent after this version

- menus and cursor movement
- death, save, encounter start, the vendor, and every refusal
- a missed attack — `battle:miss` fires in four places and plays nothing
- ambience of any kind: 14 beds are on hand (5 forest, 5 interior, 3 cave,
  1 torch loop) and none can play, because `AF.audio` has one music channel
  and no looping ambience bus. The Rain/Storm and Day/Night variants need
  weather and time-of-day systems that do not exist either.

---

## Files touched

- `aetherfall.html` — version, three clips, one family, four element entries,
  `LOOK` frozen and exported, one status line, one self-test rewritten and
  three assertions added

## Verification performed

- Self-test 392/392 × 3 consecutive runs, headless Chromium, 540×960
- 0 boot faults, no page errors
- All 18 effect clips decoded in a real `AudioContext`; 0 failures; sample
  rate, channel count and duration read back off each decoded buffer
- The three source WAVs confirmed distinct by hash before encoding, and the
  three MP3s confirmed distinct after, so the no-repeat picker has real
  variants to choose between
- Every new assertion individually reverted and observed to fail

## Not verified

- Nothing has been heard. The suite counts whether a cue was *asked for*; no
  part of this pipeline can tell whether the result sounds good, whether the
  magic impact sits right against the sword swing at `VOLUME = 0.55`, or
  whether it reads as cheap when four elements in a row use it.
- Nothing device-verified. No iPhone has played this build.
- The Custodian fight still has never been played end to end.
