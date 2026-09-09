# Change report — 0.46.0

**Build** `Aetherfall 0.46.0 · rowans-hold · save v5`
**Self-test** 401 / 401 (three new), three runs, 0 boot faults, no page errors
**Size** 5,988,695 bytes (+13,210 — comments, tests and one migration)
**Branch** `claude/newest-build-nv7xsl`

Every finding from `AUDIT_0_45_0_DEEP.md`. Three were code defects and are
fixed; two are content gaps and are now **declared** rather than accidental;
two were documentation and are closed.

---

## A · ☰ no longer opens a menu over a fight

The menu button stayed visible in battle, and tapping it laid the whole pause
menu — PARTY, ITEMS, EQUIPMENT, SAVE, REST, RETURN TO ROWAN'S HOLD, NEW GAME —
over the fight. Nothing was exploitable (B closes it, the warp is refused, the
fight survives), but **the refusals were silent**: no row disabled, no message,
so a player tapped and the game appeared to ignore them.

```css
body.battle #menuBtn{display:none}
```

Hidden rather than disabled row-by-row, because a fight already has its own
menu and every row worth pressing mid-fight (Item, Skill) is in it. This is the
rule the line above it has followed since 0.14.3 — **a control is shown only
where it does something**.

## B · The board screen no longer shows ◀▶ that do nothing

`AF.partyScreen.update` reads `AF.input.axis().y` and nothing else, and the
screen drew a full d-pad: two of a phone's four direction buttons were dead
thumb-space.

This is **the same defect 0.44.0 fixed for battle**, and it survived that fix
because the fix was scoped to `body.battle` rather than to the rule underneath
it. Two halves were missing, and both are now in:

```js
document.body.classList.toggle("menu", e.next === "menu");   // the class was never set
```
```css
body.menu .pad .l,body.menu .pad .r{display:none}
```

## C · Save migration 4 → 5 clears items a build no longer declares

0.45.0 retired `barrow_key` and `guild_writ`. A save written before it kept
them forever: no crash, `AF.data.item()` returning null, and the bag drawing
`«missing text: placeholder.name.barrow_key»` for the rest of that save's life.

The migration **asks the registry** rather than naming those two ids, so it
still works the next time an item is retired. Worn equipment is checked the
same way, since a removed item could be in a slot rather than the bag.

Deliberately not a refusal. A save is a player's time and a retired trinket is
not worth refusing one over: the entry is dropped, the drop is reported through
`AF.diag` so it is visible in the panel rather than silent, and everything else
loads. `saveSchema` 4 → 5.

**Verified on a forged legacy save**, loaded through the real path: `ok`,
**0 ghosts left**, the 3 real salves kept, still playable.

## D · Two mapless regions are now *declared*, not accidental

`deep_barrow` and `ashen_reach` carry nine weighted encounter rows between
them, naming eleven enemies — three of which (`pale_choir`, `iron_shade`,
`dawn_moth`) exist nowhere else and cannot be met by any route.

None of that is a bug: it is authored content waiting on two maps. **What was
a bug is that nothing said so** — a region with an empty `scenes` list looked
identical to one whose map had been deleted by accident, and the suite could
not tell them apart.

`planned: true` is the difference, and the new test reads it both ways: an
empty region without the flag fails, and a region that *has* a map and still
carries the flag fails too, so it cannot be left behind as a lie once one is
built.

## E · The empty chest system — recorded, not invented

The save schema carries a `chests` field and zero chests exist in any scene.
Nothing is broken; it is a persisted system with no content, the same shape as
D. Placing chests is authoring — what goes in them and where — so it is in
`todo()` as a gap rather than answered with invented content.

## F · `docs/RULES_CITED_0_46_0.md` — the gap made measurable

`docs/RULES_INDEX.md` has never existed in this repository, and two addendum
files amend an index that is not here. Since 0.9.3, "cited but not indexed" and
"indexed but not cited" have both been unanswerable.

`tools/rules-census.py` derives half the answer from the build:

| | |
|---|---|
| distinct rules cited | **89** |
| total citations | **839** |
| machine-enforced | **16** |
| cited in reasoning only | **73** |

That last row is the useful one. Sixteen rules stop the build or refuse an
action if broken. **Seventy-three are cited in comments and `todo()` lines
where nothing fails if the code drifts from them** — those are the ones worth
reading against the Bible first.

The header says plainly what it is not: it cannot say what a rule MEANS, or
whether it is LOCKED or FLEXIBLE. Supply the index and the other half follows.

## G · A stale comment

The `AI_PATTERNS` header claimed coverage was *"deliberately partial: two real
enemies… the other 16 enemies + 2 bosses fall through"*. Measured: **all 20
carry a pattern, 17 with real gambits**. The three attack-only ones
(`husk_lesser`, `dust_crawler`, `slime`) are not a gap — a tier-one husk that
shambles forward *is* the behaviour, and giving it conditions to inflate a
number is what AF-R-1006 refuses.

The replacement notes its own lesson: a comment describing coverage goes stale
the moment coverage changes, and nothing fails when it does.

---

## Tests

**`each mode shows exactly the controls it reads`** — the general form of A, B
*and* the 0.44.0 battle fix. For each mode it reads the source of that mode's
`update` to see whether it consumes the X axis, the Y axis, or neither, and
asserts the stylesheet shows exactly that much: up/down wherever Y is read,
left/right only where X is read, ☰ only where its menu can act, and A/B
everywhere because nothing could be confirmed or cancelled without them.

**It caught its own weakness during revert-proof.** The first version set
`body.className` by hand, so deleting the line that *sets* the class still
passed — it proved the CSS and not the wiring, which is half the bug. It now
also drives the real `mode:changed` listener and asserts the class lands.

**`a save keeps only items this build still declares`** — drives migration 4
with a mixture of real and invented ids, in the bag and in a worn slot, and
asserts the real ones survive and the invented ones do not.

**`content that cannot be reached is declared, not accidental`** — D, both
directions.

## Revert-proof

| Reverted | Caught as |
|---|---|
| show ☰ in battle | `battle shows ☰, which opens a menu whose rows cannot run there` |
| show ◀▶ in the menu | `menu never reads the X axis and still shows left/right` |
| stop setting `body.menu` | `entering menu did not put "menu" on the body — the stylesheet cannot see the mode` |
| stop setting `body.battle` | `entering battle did not put "battle" on the body` |
| remove migration 4 | `no 4→5 migration` |
| migration keeps everything | `an undeclared bag entry survived the migration` |
| drop `planned` from `deep_barrow` | `region deep_barrow has no scene and is not marked planned (6 encounter row(s) stranded)` |
| add `planned` to `forest_route` | `region forest_route has a map and is still marked planned` |

## Verification

- 401/401 × 3 runs, 0 boot faults, no page errors
- Live at 414×736 touch: ☰ **hidden in battle**, visible in the overworld,
  restored on exit; board screen carries `body.menu` with ◀▶ hidden and ▲▼ and
  A/B shown; forged schema-4 save loads with **0 ghosts** and its real items
  intact
- Battle screenshot re-taken with a full party — ☰ gone, everything else
  unchanged from 0.44.0

## Not fixed, deliberately

- **Two maps** for `deep_barrow` and `ashen_reach`, and **chests**. Both are
  authoring, not repair. Declared in `todo()` and guarded by a test so they
  cannot rot silently.
- **The rules index itself.** Only the Bible can say what a rule means.
- Nothing device-verified since 0.43.0; nothing about the game has been
  *played*.
