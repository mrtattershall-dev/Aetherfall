# Deep audit — 0.45.0

**Method.** Everything below was measured by driving the live build in headless
Chromium at the reporting device's geometry (414×736, touch, mobile UA). Where
a claim could be made from source it was instead made from behaviour — this
audit found three of its own false positives that way, and one near-miss
described at the end.

**Scope.** The areas `AUDIT_0_44_0_SYSTEMS.md` listed as *not audited*: save and
load, the overworld, text and dialogue, plus performance, determinism, event
wiring, touch coverage, atlas integrity and rules coverage.

---

## Verified sound

Most of this audit is this list. Several of these are things the handoff notes
still describe as unproven.

| Area | Result |
|---|---|
| **World traversal** | Hold → forest → barrow → back, **walked** with real input and collision. Every leg landed exactly on its authored arrival point. No stuck geometry, no unreachable exit. |
| **Save → reload → Continue** | Saved through the real menu, reloaded the page, drove the title cursor and confirm. Restored money 777, level 4, `forest_route` — exact. |
| **Save round-trip** | `level`, `exp`, `sp`, `nodes`, `abilities`, `money`, `inventory`, party size all identical across write/read. |
| **Legacy saves** | A pre-0.45.0 save carrying the two items 0.45.0 deleted **loads, stays playable**, and renders them as labelled placeholders rather than crashing. |
| **Interactables** | `AF.authoring.validateInteractables` reports **clean in all six scenes**. |
| **Atlas** | 753 rects, **0 never named** by any code path. |
| **RNG** | Deterministic on a seed, and different seeds diverge. |
| **Performance** | 816 ms to load 5.98 MB; 28 MB JS heap; **flat 16.7 ms** p50/p95/max in all three scenes *and* the boss fight. No spikes. |
| **Touch coverage** | Every mode shows exactly the controls it reads — one exception, finding B. |
| **Enemy AI** | All 20 enemies have patterns; 17 carry real gambits, 3 are attack-only by design. |
| **Text** | 179 ids, 12 placeholders, **all correctly marked `[placeholder]`** per AF-R-203. |
| **Enemy reachability** | Every enemy appears in a table or an authored encounter — see finding D for the ones whose region has no map. |

---

## Findings

### A — The pause menu opens over a live battle · MEDIUM

The ☰ button stays visible in battle. Tapping it overlays the full pause menu
on the fight: PARTY, ITEMS, EQUIPMENT, SAVE, REST, **RETURN TO ROWAN'S HOLD**,
NEW GAME.

The dangerous rows are already refused — `RETURN TO ROWAN'S HOLD` does not
warp, the fight survives, and B closes the overlay. So this is not a trap and
not an exploit. **But the refusals are silent**: nothing is marked disabled and
nothing says why, so a player taps a row and the game appears to ignore them.

There is a precedent for the fix one line above it in the stylesheet:

```css
body.title #menuBtn{display:none}
```

with the reasoning *"the in-game menu has nothing to show before a game
exists"*. The parallel holds: a fight has its own menu, and half the pause
menu's rows cannot run. Either hide ☰ in battle, or disable and label the rows
the way 0.15.0 does for Continue on an empty slot.

### B — The party and board screen shows ◀▶ that do nothing · LOW-MEDIUM

`AF.partyScreen.update` reads `AF.input.axis().y` and nothing else, yet the
body class in menu mode is empty, so the full pad renders. Two of a phone's
four direction buttons are dead thumb-space on that screen.

This is **exactly the defect class 0.44.0 fixed for battle**, missed because
that fix was scoped to `body.battle`. Same one-line shape:

```css
body.menu .pad .l, body.menu .pad .r{display:none}
```

— which also needs the mode to actually set `body.menu`, since today it sets
an empty class.

### C — Deleted items linger in old saves as ghosts · LOW-MEDIUM

A save written before 0.45.0 can hold `barrow_key` or `guild_writ`. Loading it:

- does **not** crash, and the game stays playable
- `AF.data.item()` returns `null`; `nameOf()` returns
  `«missing text: placeholder.name.barrow_key»`
- the entries survive every subsequent save

So the failure mode is honest (AF-R-1006's shape — a labelled placeholder
rather than nothing) but permanent. `AF.save.MIGRATIONS` already has three
steps; a schema-5 migration that drops inventory ids the build no longer
declares would clear them and generalise to any future removal.

### D — Two regions have encounter tables and no maps · MEDIUM

| region | scenes | encounter rows | distinct enemies |
|---|---|---|---|
| `deep_barrow` | **0** | 6 | 8 |
| `ashen_reach` | **0** | 3 | 3 |

Nine authored encounter rows can never roll, and three enemies —
`pale_choir`, `iron_shade`, `dawn_moth` — have stats, resistances, art,
AI gambits and drop tables and **cannot be met by any route**. (`barrow_knight`
is reachable through the authored gate ambush.)

Recorded in `todo()` since 0.9.2; this quantifies it. It is authored content
waiting on two maps, not a defect in the code.

### E — The chest system is declared and empty · LOW

The save schema carries a `chests` field and the state object exists. **Zero
chests are declared in any scene.** Nothing is broken; there is simply a
persisted system with no content, which is the same shape as D.

### F — Twenty events have no listener · INFO

`damage:applied`, `item:used`, `money:change`, `quest:*`, `battle:round`,
`battle:tick`, `battle:status`, `ascension:unlocked`, `vendor:*`, `menu:*` and
others are emitted and heard by nothing.

**Not a defect.** Checked the one that looked risky: status-tick damage
(poison, burn) reaches the player through `st.log`, which the battle draws —
not through `battle:tick`. These are hooks a presentation layer can take, and
no listener means no cost.

### G — `docs/RULES_INDEX.md` is still missing · INFO

**89 distinct `AF-R-###` rules are cited in the source.** There is no index
document to diff them against, so "cited but not indexed" and "indexed but not
cited" have both been unmeasurable since 0.9.3. Two addendum files exist; the
index they amend does not.

### H — A stale comment · INFO

The `AI_PATTERNS` header says coverage is *"deliberately partial: two real
enemies (cairn_hound, ash_revenant) prove the schema… The other 16 enemies + 2
bosses fall through"*. That is no longer true: 20 patterns are declared and 17
carry gambits.

---

## Three false positives, and one near-miss

Worth recording, because each is a way this audit could have reported a bug
that does not exist — and the fourth nearly did.

**"139 text ids are never referenced."** They are `name.*` ids resolved
dynamically through `nameOf(id)`. A regex cannot see a dynamic lookup.

**"`barrow_downs` is never entered."** My pattern looked for
`transition.to("scene", "arrival")`. The wilderness uses
`AF.sceneKit.edgeExit`, which the pattern missed. Walking the world proved the
graph complete.

**"The player is stuck in the forest."** An artifact of calling
`AF.transition.settle()` inside my own walk loop. Probing each direction
separately showed 300 px of movement every way.

**The near-miss.** After saving through the menu, `AF.save.peek(1)` reports
`{exists: false}` and `AF.save.read(1)` returns `"empty slot"`, while
`localStorage` holds `aetherfall:slot1`. That reads exactly like *"the game
tells you it saved and the save is unloadable"* — a catastrophic bug, and I
was one step from writing it up.

The game's slot id is the string `"slot1"`. My calls passed `1`, which is a
different, unused slot. Driving the real path — save, reload the page, move
the title cursor to Continue, confirm — restored money 777, level 4 and
`forest_route` exactly.

**The save system is sound.** The lesson is the one this project keeps
relearning: drive the path a player takes, not the API you assume they use.

---

## Not audited

- Whether any of it is *fun*. No simulation answers that.
- Anything on a device since 0.43.0.
- Audio content — levels and mixes are unheard, as recorded in `todo()`.
- Long-session behaviour: memory over an hour, save-file growth over many
  saves, and what happens after several hundred battles.
