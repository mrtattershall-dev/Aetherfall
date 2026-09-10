# Rules Index Addendum — 0.12.5 section

**This file is a SECTION to append to `docs/RULES_INDEX_ADDENDUM.md`, not a
replacement.** Nothing above the 0.12.5 heading has been reproduced; appending
preserves the 0.7.0 audits, the AF-R-524 discussion and every earlier FLEXIBLE
choice, all of which remain in force.

---

## Measurement — 0.12.5

Scanned from `aetherfall-0.12.5.html`, not read off the index.

- **88** distinct AF-R ids cited in code (unchanged since 0.7.0 final).
- **Enforcement not re-counted this pass.** The `refuse`/`require` census was
  last measured at 0.9.1 (**23**). Two new modules landed since with new
  refusals in them, so that number is stale in the safe direction — but it is
  stale, and saying so is the point of this document.
- **Cited-but-unindexed: not re-run.** Four versions of work happened without
  it. §2 step 0 says to diff on every touch of the index; this section touches
  it. **Run the diff.**

## FLEXIBLE choices added, 0.10.1 → 0.12.5

| Choice | Rule | Recorded |
|---|---|---|
| **Two name tables, not a flag.** `NAMES` is approved canon registered as `name.<id>`; `WORDS` is the backlog registered as `placeholder.name.<id>`. An id in both refuses the boot rather than letting `nameOf`'s precedence settle a canon question silently. | AF-R-203 | 0.11.0 |
| **The AF-R-203 guard is two-sided.** Approved names must render unmarked and be absent from `AF.text.placeholders()`; provisional names must render marked and be present. A one-sided test goes green on an emptied table. | AF-R-203 | 0.11.0 |
| **`survivor_01` holds a DEFAULT name.** "Aren" is canon as the default; the rename screen will override the string, not delete the row. | AF-R-1007 | 0.11.0 |
| **Rest costs `10 + 5 × (level − 1)`**, priced off the LEAD actor. Measured against the economy in the build: tier-1 drops are 4-12 gold, tier-3 are 55-110. Recruiting a fourth member must not quadruple the bill. | AF-R-802 | 0.11.0 |
| **A rest that would restore nothing is refused, not charged.** The 0.10.0 items rule applied to a bed: with no turn at stake, paying for nothing is a misclick. | AF-R-802 | 0.11.0 |
| **One save slot.** Multi-slot is naming, ordering and overwrite confirmation, none of which is needed to stop a session being lost. | AF-R-802 | 0.11.0 |
| **`AF.save.peek()` does not migrate.** A slot the build cannot load is still described. Migration stays `read()`'s job. | AF-R-932 | 0.11.0 |
| **Continue runs AFTER `AF.selftest.run()`.** The suite mutates global state and restores it; loading first hands the tests a live session. It is a LOAD — nothing on that path writes. | AF-R-1004 | 0.11.0 |
| **`AF.conversation.start` accepts `opts.lines`.** Content remains the default and still owns *which* line is spoken (AF-R-1012); explicit lines exist so a runtime number — the inn's price — can be spoken without a second confirm flow. | AF-R-801 | 0.12.0 |
| **Resting is the innkeeper's job, not a bed's.** `AF.rest` reads no scene id. A campfire calls the same function. | AF-R-801 | 0.12.0 |
| **The inn's collision is AUTHORED, not derived.** Recorded because it breaks the guild hall's pattern deliberately — see below. | AF-R-331 | 0.12.1 |
| **`ROAD_UNDER`: road drawn without being authored road.** `isRoad` reads both for drawing and autotile; `roadTiles()` returns `ROAD` alone, so AF-R-521, the reachability tests and the resonance check are untouched. | AF-R-521 | 0.12.4 |
| **No door swing on `bld_house`.** That pack ships no door animation and declaring unmeasured frames is refused. The inn door transitions immediately. | AF-R-921 | 0.12.0 |
| **The inn's four bedrooms are drawn and not entered.** Opening them changes the collision filter, not the art or the atlas. | AF-R-802 | 0.12.1 |

## New findings

### A pack's layer NAMES are not its layer ROLES

The guild hall's collision is derived from the Tavern pack's first-floor
layers, and the same method applied to the second floor produced a room with
no walls at all.

Two reasons, both worth keeping:

1. **The room shell is not in the `Walls` layer.** It is in `Walls_top2` and
   `Walls_top1`, which were excluded as "overlay only" on the strength of
   their names.
2. **`floor` extends under the walls.** So floor-minus-Walls is not a walkable
   set on that map.

Derived correctly, the second floor gives a corridor one tile tall,
disconnected from its own stairs: it is a cutaway display piece, not a
walkable floor. **A method that worked on one map of a pack is not thereby
validated for another map of the same pack.** The handoff's rule — read the
layer data, do not infer from appearance — was followed. What was inferred was
the *meaning* of the layer names.

### AF-R-341 cuts both ways

AF-R-341 ("art extends beyond footprint") is normally invoked to stop
collision boxes being derived from sprite boxes. `herb_prop_04` moved twice
because the first move measured its blocker (64×32) against the road while its
art (212×256, four columns wide) still lay across the path. **When the
complaint is visual, measure the art; when it is about movement, measure the
box. AF-R-341 is the reminder that these are different rectangles.**

### An interact zone sized to the floor is still the 0.6.18 bug

The inn's exit was sized to the two tiles the player can stand on. The probe
lands half a tile ahead of the feet, so the only facing that reached it was
"up". This was written by someone who had read §6 of the handoff in the same
session. **The rule is not "make the zone generous" — it is "the zone covers
where the PROBE lands, which is outside the walkable area by construction."**

### A caught throw is a silent failure

`AF.interiorGuildHall` called a bare `say()` that had never been in scope
there. `AF.interact` catches handler throws, so the symptom was "pressing A
does nothing" — no red, no failing test, only a fault band nobody had open.

The self-test that now covers it emits `interact:trigger` and asserts a line
lands, because asserting "no throw" is not available through a path that
catches. **Any handler behind a catch needs a test that asserts the positive
outcome, not the absence of an error.**

### A moved rule needs its assertion moved in the same edit

The workshop spur moved from column 16 to 17 in 0.10.2. The self-test
asserting `R.has("16,13")` did not move with it and had been failing since,
reported from a device as one of three failures and not chased.

Same shape as the 0.7.0 serialiser finding: **a change to a value means a
change to everything that names it, in the same edit.**

## Amendments

| Date | Change |
|---|---|
| **0.11.0** | `AF.content.WORDS` split into `NAMES` + `WORDS`. 128 approved, 6 provisional. The AF-R-203 guard is now two-sided. |
| **0.11.0** | `AF.rest` added and `AF.save.peek` added. Saving reachable from the menu; boot Continues from slot 1. |
| **0.12.0** | Sixth scene registered: `inn_interior`. Atlas 512×2265 → 512×2569, 295 → 369 rects. |
| **0.12.0** | `AF.conversation.start` gains `opts.lines`. Content still owns line selection. |
| **0.12.1** | The inn's collision is authored, with the derivation failure recorded in the code beside it. |
| **0.12.4** | `ROAD_UNDER` added — drawn road that is not authored road. AF-R-521's surface is unchanged. |
| **0.12.4** | Stale workshop-spur assertion corrected, `16,13` → `17,13`. |
| **0.12.5** | `herb_prop_04` moved (15,14) → (13,14): its art, not its blocker, lay across the spur. |
| **PENDING** | **The cited-vs-indexed diff has not been run since 0.9.3.** This document touches the index; §2 step 0 says run it. |
| **PENDING** | **The enforcement census is stale at 23 (0.9.1).** Two modules with new refusals have landed since. |
