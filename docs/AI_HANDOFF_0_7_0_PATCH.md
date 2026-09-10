# AI handoff — 0.7.0 update

**This is a PATCH to `docs/AI_HANDOFF.md`, not a replacement.** The original
was not among this session's uploads, so it has not been reproduced.
Everything in it still applies — especially §3 (refusals are the design),
§4 (one source per piece of truth), §6 (geometry is not logic) and the
"validate the harness before trusting it" rule. Apply the two edits below and
append the new sections.

---

## Edit 1 — the header's build line is stale

Replace:

> The current build is **`aetherfall-0.6.19.html`, branch `rowans-hold-undead`, save schema 3**.

with:

> The current build is **`aetherfall-0.7.0.html`, branch `rowans-hold`, save schema 3**.

`AF.build.id()` now prints `Aetherfall 0.7.0 · rowans-hold · save v3`. The
branch string was corrected in 0.6.19; the handoff never caught up. **If your
git branch is still literally `rowans-hold-undead`, the stamp and the repo
disagree — your call which one moves.**

## Edit 2 — the enforcement numbers in §2 are four versions old

Replace *"At 0.6.18: 77 rules cited in code, 17 actually enforced (0.6.21)"*
with the 0.7.0 final measurement: **88 cited, 21 enforced**. And delete the
sentence *"AF-R-622 still names `AF.encounter.roll`, which does not exist"* —
it exists now, and `AF.forestRoute` calls it.

---

## New: the index diff finally paid out, four versions late

§2 step 0 says to `diff` the AF-R ids cited in code against the ids in
`RULES_INDEX.md`, and to re-run it whenever the index is touched.

**Nobody ran it for four versions.** At 0.7.0 that diff returned **twelve**
ids cited in code and present in no index — AF-R-519…522, 524, 605,
709/710/711, 1009, 1010/1011/1012 — including **AF-R-711, cited 52 times**,
the most-cited rule in the build. The addendum had recorded them as
"Adopted 2026-09-03 — nothing is left pending". The decision was recorded;
the rows were never added.

This is the exact failure §2 was written to prevent, and it survived four
change reports that each dutifully noted "the index gap is still 12
cited-but-unindexed rules" without anyone closing it. **Noting a gap is not
closing it.** Run the diff.

## New: four kinds of leak that only appear on the second run

0.7.0 added a lot of state to the battle system, and found **three separate
cross-test pollution bugs** that a single green suite run could not have
caught. All were found by running `AF.selftest.run()` **four times in one
session** and diffing the results.

1. **Mode leak.** A test walked the player through the forest without
   disabling encounters; a battle fired mid-test and left
   `AF.state.mode === "battle"` for everything after it.
2. **Transition leak.** Giving defeat a real consequence (a transition to the
   Hold's gate) broke two *pre-existing* tests that called
   `AF.battle.end("defeat")` and never settled the transition it now starts.
3. **Inventory leak.** Inventory is global; item tests added stock that
   changed what later tests saw in the bag.

**The rule that falls out of this:** if a test mutates global state —
`AF.state.mode`, the transition, the inventory, the party, the RNG — it must
snapshot and restore it, and the suite must be run more than once before the
result is believed. A suite that passes once is not known to be repeatable.

## New: the failing message can point at the wrong component

Two bugs in 0.7.0 reported confidently against innocent code:

- A phase test failed with `phase 0 did not fire at 50% hp`, which reads as a
  phase-system bug. The phase system was fine; the test had used a level-1
  party against the Hollow Dragon, which killed them before the later
  thresholds could be probed.
- A growth test failed with `the reward summary did not report the ability`.
  The reward path was fine; `levelled` lives on `summary.rewards`, not on
  `summary`.

Both were resolved by inspecting the live object rather than trusting the
message. **When a new test fails, suspect the test first** — it is the thing
that has never worked.

## New: `AF.sceneKit` — compose it, don't re-copy it

Every scene used to hand-write the same player proxy, walk step and player
blit. Three copies at 0.6.24; the forest would have made a fourth and the
remaining wilderness regions a seventh. `AF.sceneKit` now holds them.

- A new scene should call `AF.sceneKit.playerProxy()`, `walk()`,
  `drawPlayer()` and — for wilderness — `drawGround()`, `placeProp()`,
  `blockersOf()` and `edgeExit()`.
- **This is not a base class.** The registry is still additive; a scene joins
  by exposing `{sceneId, SPAWN, update, draw}`. A scene that needs different
  movement simply does not call `walk()`.
- `AF.demo` deliberately keeps its own late `AF.camera.follow` (after props
  move) and its villager animation. That difference is real; do not "tidy" it
  into the shared helper.

## New: what is data now, and must stay data

`AF.content` grew from eight tables to twelve. Every one is validated at load
and **a bad row refuses the boot** rather than failing later:

`ITEMS · STATUSES · ABILITIES · ENEMIES · ENCOUNTERS · AUTHORED · REGIONS ·
ROSTER · SHOPS · AI_PATTERNS · PHASES · GROWTH · LEARNSETS`

Rules that now hold and should not be softened:

- An **AI pattern may only gambit on abilities its enemy actually has**, and
  `AI_CONDITIONS` is a locked vocabulary — an unknown condition is a load
  error, not a silent no-op.
- **Every boss must have `PHASES`; no non-boss may have them.**
- **Every roster role must have a `GROWTH` curve**, and every curve must
  cover the whole eight-stat family.
- **A learnset may not grant something its role already starts with** (that
  entry could never fire), may not grant at level 1 (starting kit belongs in
  `ROSTER`), and must be in ascending level order.
- **Roleless actors use an all-zero growth curve.** Every enemy is roleless,
  so enemy records mean exactly the numbers they declare. A growth curve
  leaking onto enemies would silently rebalance every fight in the game.

## New: saving a new actor field is two edits, not one

Actors gained `role` and `abilities` in 0.7.0 and **the save serialiser was
not updated in the same change**. A loaded character would have come back
`role: null` — the zero-growth curve — with only its starting kit, silently
losing both stat progression and every learned ability.

Caught before shipping, but it is the third time this exact shape has
occurred (`scene` written and never read, `statusEffects` owned and never
saved). **Adding a field to `AF.actors.create` means adding it to
`AF.save.serialize` in the same edit**, and asserting it with a round-trip
test.

## New: run the build in a real browser

The node/DOM stub described in the original handoff still works, but 0.7.0
was verified by loading the HTML in **headless Chromium via Playwright** and
calling `AF.selftest.run()` in the page. That is strictly better: it exercises
the real canvas, the real event wiring and the real image decoding.

Three tests fail in that environment for an environmental reason
(`drawImage` rejecting the stubbed atlas image) — `a fractional blit is still
refused`, `a character sprite is centred…`, `footInset lifts a sheet…`. This
was confirmed by running the **untouched 0.6.24 baseline** through the
identical harness and getting the same three. Validate the harness against a
known-good build before trusting a failure, exactly as the original handoff
says.

**A real browser still is not a real device.** Touch, rendering fidelity and
phone performance remain confirmed by the user or not at all.


---

## Added after the vendor / recruiting / barrow / NPC work

### A zone does one job

The Mender was briefly offered by the workshop counter — the same
interactable as the shop. Two consequences: the counter stopped opening the
shop on a first visit, and the vendor walk-up **self-test** pressed A there
and recruited her into the live party, so the game booted with a party member
the player had never met.

**One interactable, one job.** A self-test that drives the real input path can
change the running game, and the suite runs at boot. There is now a test
asserting the party contains nobody whose recruit flag is unset — it guards
the class, not the instance.

### Four kinds of leak, now five

The earlier section listed mode, transition and inventory leaks. Add:
**recruitment**. Every one was found by running `AF.selftest.run()` more than
once and diffing. The rule stands and is worth restating: if a test mutates
global state, it must snapshot and restore it, and a suite that has passed
once is not known to be repeatable.

### Content validation runs before the scene modules parse

`AF.content` validates every text id, flag, ability, scene and zone its tables
name — at install, which happens **before** `AF.demo`, `AF.interiorGuildHall`,
`AF.shopInterior`, `AF.forestRoute` and `AF.barrowDowns` are parsed.

So anything a content table refers to must be declared inside `AF.content`
itself. NPC prose lived in `AF.demo` and was "undefined" at the moment it was
checked. Story flags declared in a scene module have the same problem.
**Scene modules own sprites, geometry and placement; names, prose, flags and
tables are content.**

### Where things live now

| Thing | Home |
|---|---|
| Player proxy, walk step, player blit, ground, props, edge exits | `AF.sceneKit` |
| One line of speech, its timer, its bubble | `AF.speech` |
| Buy/sell, prices, the shop overlay | `AF.vendor` |
| Who joins, where, and the flag that records it | `AF.content.RECRUITS` |
| What an NPC says, and under what conditions | `AF.content.NPCS` |
| Growth curves, learnsets, AI gambits, boss phases | `AF.content` |

A new scene should compose `AF.sceneKit` rather than reimplement it, and put
its prose and tables in `AF.content` rather than beside its sprites.

### Do not do index arithmetic on this file

Moving the NPC prose, I computed string offsets and cut a block out of the
middle of `AF.content.recruit()`. The syntax check caught it and the last
packaged build was restored, but on a 10,000-line single file, unique-anchor
replacement is the only sane edit method. The saving from index math is not
worth the failure mode.

### A clean validator run is necessary, not sufficient

`AF.authoring.validateInteractables()` approved the workshop counter while
pressing A at it did nothing. It is stricter now — every approach walked,
partial failures reported — but **no fixture has been built that proves it
catches that shape.** What caught it was a self-test driving `input:confirm`.
When you add an interactable, add the walk-up test too.
