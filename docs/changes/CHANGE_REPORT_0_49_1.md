# Change report — 0.49.1

**Build** `Aetherfall 0.49.1 · rowans-hold · save v5`
**Self-test** 405 / 405 (two new), three runs, 0 boot faults, no page errors
**Branch** `claude/newest-build-nv7xsl`

**From five landscape screenshots of 0.48.0 on a phone**, walking the Hold, the
shop, the forest route, the barrow, and into the Custodian.

---

## A refusal that erased the story it was refusing

The boss screenshot shows the battle log holding **five identical lines**:

```
round 1 · authored
this battle cannot be fled
this battle cannot be fled
this battle cannot be fled
this battle cannot be fled
this battle cannot be fled
```

The log is five lines deep, so five taps on Flee flushed it — and what they
flushed was **the Custodian's own warning**. 0.35.2 deliberately routes his one
spoken line through the battle log rather than the speech bubble, because the
bubble is not drawn in battle mode. The player pressed a button the game
offered them, and it deleted the only thing the boss says.

Two defects, one stacked on the other.

### The menu did not know what the command layer knew

`command()` has refused this since AF-R-622 — *a story battle you can walk out
of is not one* — and goes on refusing it. What was missing is that the **menu**
knew, so the refusal arrived after the press instead of before it.

`options()` already states the principle two branches down, for targets:

> the menu shows only legal targets, so the command layer's refusal is a
> backstop rather than the player's first hint

Flee was the one command that did not follow it. It now reads
**`Flee (no escape)`**, greyed, in the same shape as `Item (none)` and a spell
with no MP — and `choose()` has refused disabled rows since it was written, so
the press does nothing at all.

```js
: (c === "flee" && st.kind === "authored") ? "(no escape)"
```

### A log any repeated line can flush

Disabling Flee stops *that* five from recurring. It does not fix the log, and
a miss streak or a blocked command produces the same five just as easily. A
repeat is now **tallied** rather than stacked:

| before | after |
|---|---|
| five lines of `this battle cannot be fled` | one line, `… x5` |
| the boss's warning gone | the warning still there |

Re-running the exact reported sequence — five taps on Flee at the Custodian —
on this build:

```
Custodian of the Seal appears.
Custodian of the Seal: "You will not pass while I stand."
```

Both lines intact, and the five presses wrote nothing.

## What the screenshots also showed, measured rather than guessed

**The Custodian is a level gate that nothing announces.** The party in the
screenshot is level 1 — 54/54 HP, no board spent — in an unfleeable fight.
Thirty simulated fights per level, best play:

| party level | wins | |
|---|---|---|
| 1 – 3 | **0%** | not a hard fight; an impossible one |
| 4 | 13% | |
| 5 | 37% | |
| 6 | 77% | |
| 8 | 90% | |

That is a **well-shaped boss** — it wants a party around 5–6 and the curve is
smooth. The problem is not the tuning. The problem is that a player who avoids
encounters on the way there arrives at level 1 and nothing on the barrow trail
says a word about it. Losing is handled (defeat revives at the Hold's gate), so
it is a wall rather than a softlock.

**Not fixed here.** Whether to gate the seal band, warn on approach, or leave it
as a lesson is pacing — canon, and the user's call (AF-R-1007). Inventing that
answer quietly is what AF-R-1006 refuses. The numbers are now in `todo()` so the
decision has something to stand on.

**Landscape works on the device.** The d-pad and A/B fall in the letterbox
either side of the canvas rather than over it, so `AF.controls` measures roughly
zero side band and reserves nothing — which is what measuring rather than
assuming is for. The forest route reads fine wide; the corridor worry from
0.48.0 looks smaller than the arithmetic suggested.

> One thing worth knowing rather than fixing: in Safari with the tab bar
> showing, landscape loses about 20% of the height to browser chrome, and since
> the game holds 16:9 it loses width with it — hence the wide black bars.
> Add to Home Screen gives it the whole screen.

## Tests

**`a story battle does not offer the way out it is going to refuse`** — the
Flee row must be disabled in an authored battle and enabled in a random one,
and five presses must write nothing. The cursor is walked onto Flee **through
the vertical axis and `update`**, the way a player walks it, rather than by
writing `ui.cursor` — "the row is disabled" and "the press is refused" are two
claims and only the second is what the player experiences.

**`the battle log tallies a repeated line instead of filling itself with it`** —
six repeats make one line ending `x6`, and a line separated by another starts a
new entry rather than resuming the tally.

**Revert-proof**

| Reverted | Caught as |
|---|---|
| Flee offered in a story battle | `a story battle offers Flee as if it worked; five presses on a disabled Flee wrote to the log: this battle cannot be fled` |
| `choose()` honours no `disabled` | `five presses on a disabled Flee wrote to the log` |
| the log stacks repeats | `six repeats made 4 lines: the same line / the same line / …` |

The first revert reproduces the device's exact symptom, verbatim.

## Verified

- 405/405 × 3 runs, 0 boot faults, no page errors
- The reported sequence re-driven at 896×414: `Flee (no escape)` greyed, log
  intact, five presses inert
