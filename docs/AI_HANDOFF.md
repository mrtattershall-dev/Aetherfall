# Aetherfall — AI handoff

Paste the header below above any implementation request.

---

## The header

> You are working on **Aetherfall**. Treat the Aetherfall GDD & Production Bible as authoritative,
> and `docs/RULES_INDEX.md` as its stable ID index — cite rules as `AF-R-###` rather than
> paraphrasing them. Read `docs/RULES_INDEX_ADDENDUM.md` too: the index is optimistic about
> enforcement, and the addendum records what is actually checked, which Bible sections have no ID
> at all, and which FLEXIBLE choices are already in force.
>
> Obey LOCKED rules exactly. FLEXIBLE rules may be adjusted only when the task benefits, and you
> must say which choice you made. UNDEFINED areas are not permission to invent canon.
>
> Packs frequently declare tile ANIMATION data in their `.tmx` that is easy to miss — the chapel had
> 122 animated tiles and shipped dead because they were baked flat. Check for it before compositing
> a room, and before concluding a door cannot animate.
>
> Never infer sprite mappings, atlas coordinates, animation rows, collision sizes, filenames, IDs,
> story facts, quest facts or game data from appearance alone. Inspect real source assets or leave
> an explicit TODO. `AF.anim.define()` will refuse unverified frame data; do not work around it.
> **A pack's own `.tmx` layer data is source. Read it before measuring pixels, and before
> concluding something is not there.**
>
> 64×64 is the master world grid, not a universal asset size. Source art is 16px-native and drawn
> at integer scale — `AF.const.WORLD_SCALE` (4) and `AF.const.UI_SCALE` (3).
>
> The current build is **`aetherfall-0.6.19.html`, branch `rowans-hold-undead`, save schema 3**.
> Before you change anything, read `AF.build`, and confirm with me which file is the current base
> if more than one exists.
>
> Preserve working systems. Make the narrowest safe change. After implementing, run
> `AF.selftest.run()` and report the result along with: files/sections changed, behaviour added or
> fixed, assumptions made, unresolved data needed, and regression checks performed.
>
> **Do not report a change as complete on the strength of a syntax check.** If you cannot run the
> build, say so plainly and label the work unverified.

---

## Six things the header can't carry

### 1. Confirm the base file first

Divergent Aetherfall files with different designs have existed side by side. The build stamps
itself — `AF.build.id()` prints `Aetherfall 0.6.19 · rowans-hold-undead · save v3`, and it appears
on the HUD and inside every save. Check the stamp before editing.

**The filename is not the stamp.** The 0.6.18 pass began from a file named
`aetherfall-0_6_17.html` while every document in the repo described 0.6.2. Read `AF.build`.

**Three canon changes are in force; read all of them.** AF-C-003 removed the chapel and put a
glassblower's workshop in its place, so any chapel reference in older docs is dead.
**The first two:** `AF.canon.changes` holds
both. AF-C-001 made Rowan's Hold a besieged settlement; **AF-C-002 supersedes it** — Rowan's Hold
is "a bright, living settlement in daylight. No undead presence, no siege." Read the entries
before writing anything about the setting.

Consequence: the scene id was renamed to `rowans_hold` in 0.6.19, shipping with a v2→v3 save
migration — a rename is a save migration here, because `AF.save.read` refuses an unknown scene
(AF-R-931). The **branch name** `rowans-hold-undead` is still stale and deliberately left alone:
it is a real git branch, and editing the stamp would only desync it from the repo.

### 2. Adding a rule means adding an enforcement point

0. Check first: `diff` the AF-R ids cited in code against the ids in `RULES_INDEX.md`. In 0.6.19
   that diff found four rules (AF-R-519…522) that were implemented, enforced, failing builds, and
   present in no index — the worst state a rule can be in. Re-run it whenever the index is touched.
1. Add a row to `docs/RULES_INDEX.md` with a fresh ID. Never reuse a retired number.
2. If it is machine-checkable, add the check in the build and cite the ID in the code.
3. Add a self-test that proves the check actually fires.

If step 3 is skipped, the rule is `review`-grade and the index must say so.

**This has been audited three times and the index was found optimistic every time.** At 0.6.18:
77 rules cited in code, 17 actually enforced (0.6.21). The gap has *widened* since 0.6.2 (47 → 55). Do not
add to it. AF-R-622 still names `AF.encounter.roll`, which does not exist. (AF-R-803's `AF.data`
now does — that gap closed.) As of 0.6.19 **nothing is pending approval**: the `AF-P-###` scheme is
retired and every proposed rule has been adopted into the index.

### 3. Refusals are the design, not friction

| Refusal | Rule | Why not just make it work |
|---|---|---|
| `AF.integrity.spend()` refuses below the floor | AF-R-812 | Clamping consumes the resource and teaches the player the meter lies. |
| `AF.anim.define()` throws without verified frames | AF-R-921 | A guessed frame map looks correct until animation work has been built on top of it. |
| `AF.render.blit()` refuses non-integer scaling | AF-R-405 | Fractional resampling of pixel art is subtle enough that it ships. |
| `AF.mode.set()` refuses an unimplemented mode | AF-R-102 | A name in a list is not an implementation. |
| `AF.assets.declare()` refuses `verified` without a rect | AF-R-1001 | A manifest that looks measured is worse than one that admits it isn't. |
| Boot refuses a player link resolving to nobody | AF-R-904 | A blank HUD and a protagonist-less battle, discovered later instead of at boot. |
| `AF.save.migrate()` refuses an unmigratable save | AF-R-932 | Silent reinterpretation of old fields corrupts progress invisibly. |
| `AF.scene.enter()` refuses an unknown scene or arrival id | AF-R-905 | Spawning "somewhere" is how a transition bug hides for a version. |

If a future change makes one of these inconvenient, supply the missing data. Do not soften the
refusal.

### 4. One source per piece of truth, including position and scene

`AF.state.player` is the only store of player position. The scene's player object exposes
`x`/`y`/`facing` as **accessors onto it**. There is no mirror step, because a mirror step is a
thing to forget. `AF.actors.player()` is the one resolver answering "which actor is the player?"

**0.6.18 added the scene equivalent.** `AF.state.sceneId` is the only record of which map you are
in. Before that, `scene` was written into every save since 0.6.x and read by nothing, and
`AF.interact.current()` was hardcoded to `AF.demo.sceneId` — which would have silently broken the
moment a second scene existed. Do not reach for `AF.demo.sceneId`.

### 5. Debugging at an opaque origin

In a phone file preview the browser strips `window.onerror` down to the literal string
`"Script error."` — no message, no line. Do not chase it there. Catch locally with `AF.fault()`,
which records the real Error, and read the on-canvas fault band.

### 6. Geometry is not logic — the 0.6.18 lesson

0.6.18 was reported complete twice and was broken both times. The door did nothing when pressed;
the interior had an entrance and no exit. **Every self-test passed through all of it**, because
the tests emitted `interact:trigger` directly and never touched `AF.interact`.

The pattern to avoid: testing that a system *responds*, without testing that a player can *reach*
it. Three separate bugs, one shape — an interact zone correct as data and wrong as geometry.

Consequences now baked in, and worth preserving:

- **Drive the real path.** Round-trip tests go through `input:confirm`, not through a synthesised
  event. If a test bypasses the input layer, it is not testing interaction.
- **`AF.authoring.validateInteractables()`** runs the walk-up test over every registered scene:
  approach from each side, move until collision stops you, probe from where you actually ended up.
  Its first two versions caught none of the bugs they were written for — "reachable from somewhere"
  is not the property players rely on.
- **It does not check visibility.** An interactable sitting on nothing a player can see still
  passes. That remains a review item; see the addendum.
- **Prove a new test fails.** Every fix in that pass was confirmed by reverting it and watching the
  test go red. A test that has never failed is not known to test anything.
- **Interact zones are sized to the reachable band, not to the art.** The probe sits 32px ahead of
  the feet and a blocker stops the player short, so a zone matching the door rectangle is
  unreachable. Both doors' zones are deliberately larger than and offset from their sprites. Do not
  "tidy" them to match the art.

### Running the build without a browser

The build boots headlessly under node with a DOM/canvas stub (document, window events with real
listener storage, a stable element registry so pad buttons the engine binds are the ones tests
dispatch on, and an `Image` that reports loaded).

**Validate the harness before trusting it.** Run the *previous* version through it first and
require its known-good score — 0.6.17 gives 139/139. The first harness built in 0.6.18 produced
three false failures; without that baseline they would have masked real ones.

This exercises logic and geometry. It does **not** exercise touch input, real rendering, or phone
performance. Those are confirmed by the user or not at all.

---

## Change reporting template

```
Files / sections changed:
Behaviour added or fixed:
Rules touched (AF-R-###):
FLEXIBLE choices made (AF-R-802 requires stating these):
Assumptions made:
Data still needed:
Self-test: __/__ passing
Regression checks: boots ✓ / movement ✓ / save-load ✓ / mode switch ✓ / credits intact ✓
Verified how: (headless run / syntax only / browser) — say plainly which
```
