# AI handoff — 0.12.5 update

**This is a PATCH to `docs/AI_HANDOFF.md`, not a replacement.** Everything in
the original still applies — especially §3 (refusals are the design), §4 (one
source per piece of truth), §6 (geometry is not logic) and "validate the
harness before trusting it". Apply the edits below and append the new sections.

---

## Edit 1 — the build line

Replace the 0.7.0 line with:

> The current build is **`aetherfall-0.12.5.html`, branch `rowans-hold`, save
> schema 4**.

## Edit 2 — the six things, now seven

Add to the list: **7. The device is the only renderer that counts.** Twelve
versions of "NOT device-verified" ended when the user started checking every
build on a phone. In the four versions since, the device found four bugs that
337 self-tests passed — a crash behind a catch, a room with no walls, an
unreachable exit, and a tree across a path. None of them were logic errors the
suite could have caught.

---

## New: a caught throw is a silent failure

`AF.interact` catches handler throws. `AF.interiorGuildHall` called a bare
`say()` — a local inside `AF.demo`'s IIFE that had never been in scope there —
so talking to the Guildmaster threw `ReferenceError` on every press, for an
unknown number of versions, and the only symptom was that nothing happened.

**A test that asserts "no error" is useless behind a catch.** The test that
now covers it drives `input:confirm` and asserts a line actually lands. Any
handler behind a catch needs a test that asserts the positive outcome.

## New: layer NAMES are not layer ROLES

The handoff already says a pack's own `.tmx` layer data is source and must be
read rather than inferred from appearance. 0.12.0 followed that and still
shipped a room with no walls, because what was inferred was the **meaning of
the layer names**:

- The Tavern pack's second-floor room shell is in `Walls_top2` and
  `Walls_top1`, not in `Walls`. Excluding the "top" layers as overlay-only left
  the entire wall band walkable.
- Its `floor` layer extends *under* the walls, so floor-minus-Walls is not a
  walkable set at all.

Derived correctly, that map yields a corridor one tile tall, disconnected from
its own stairs — it is a cutaway display piece, not a walkable floor.

**Two rules fall out.** First, render each layer alone and look at what is in
it before assigning it a role; the guild hall's comment says this and it was
not done for the second floor. Second, **a method validated on one map of a
pack is not thereby validated on another map of the same pack.**

When derivation is wrong for a map, author the collision and *say so in the
code*, with the failed derivation recorded beside it. `AF.innInterior` does
this.

## New: measure the rectangle the complaint is about

`herb_prop_04` moved twice. The first move checked its **blocker** (64×32)
against the road and stopped there. Its **art** is 212×256 and spans four
columns, so the canopy still lay across the spur.

AF-R-341 — art extends beyond footprint — is usually invoked to stop collision
being derived from sprite boxes. It cuts the other way too. **A visual
complaint is measured against the art; a movement complaint against the box.**

## New: an interact zone sized to the floor is the 0.6.18 bug again

The inn's exit zone was sized to the two tiles the player stands on. The probe
sits half a tile ahead of the feet, so the only facing that reached it was
"up"; pressing A at the stairs did nothing from almost everywhere.

This was written in the same session as reading §6. The rule is not "be
generous with zones" — it is: **the zone must cover where the PROBE lands,
which is outside the walkable area by construction.** Every door in this build
is sized that way and the reason is in each of their comments.

## New: a rule about walkability is not a rule about appearance

AF-R-521 refuses an authored road tile under a blocker, correctly — authored
road is a promise that a player can walk it. That refusal was blocking a purely
cosmetic fix (a path that stopped a tile short of a door it pointed at).

`ROAD_UNDER` separates the two: tiles drawn as road that are not authored road.
`isRoad` reads both, so drawing and autotiling see a continuous network;
`roadTiles()` returns `ROAD` alone, so AF-R-521, the reachability tests and the
resonance check are untouched.

**When a rule blocks something it was not written about, check whether one name
is serving two questions** — before softening the rule (§3).

## New: moving a value means moving everything that names it

The workshop spur moved from column 16 to 17 in 0.10.2. The self-test asserting
`R.has("16,13")` did not move with it, failed for two versions, was reported
from a device as one of three failures, and was not chased.

Same shape as 0.7.0's serialiser finding. **A change to a value is a change to
every assertion, comment and document that names it, in the same edit.**

## New: approving canon can empty the mechanism that guarded it

`AF.content.WORDS` was not a name table with a marker on it — it *was* the
approval backlog, and a self-test asserted every id in it renders marked.
Approving 118 of 122 entries would have left that test green over an almost
empty table.

The table split into `NAMES` (approved, drawn clean) and `WORDS` (the
backlog, drawn marked), `install()` refuses an id in both, and the guard is now
two-sided. **When a mechanism's job is to shrink, check what its test asserts
when it reaches zero.**

## New: a complete system nobody can reach is not a feature

Save had been complete since 0.6.x and unreachable: nothing called
`AF.save.write` outside the self-tests, boot never called `read`, and the menu
said so in a line everyone had stopped reading. Third instance of this exact
shape — the door in 0.6.18, the Items backend before 0.10.0, saving before
0.11.0.

**When diagnostics says "system ready, no screen", that is a bug report with a
date on it.**

## Still true, and now overdue

- **The cited-vs-indexed diff has not been run since 0.9.3.** §2 step 0 says
  run it whenever the index is touched. It has been touched.
- **The enforcement census is stale at 23** (0.9.1). Two new modules with
  refusals have landed.
- **`AF-R-601` still names `AF.player.step`.** Ninth version.
- **A real browser still is not a real device**, and the last four versions
  are the strongest evidence this project has produced for that sentence.
