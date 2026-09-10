# The 0.12.5 README's gap list, re-checked at 0.34.0

`README_0_12_5.md` closes with thirteen gaps "stated plainly" and a suggested
order of work. Twenty-two versions later, measured against `aetherfall.html`.

## Closed

| Gap at 0.12.5 | State at 0.34.0 |
|---|---|
| **`AF-R-911` icon warnings flood the console** — 88 icons with no `{w,h}` | **Closed at 0.13.8**, and closed the right way. The code says AF-R-911 "demanded a WORLD placement from every declared asset" and an overlay has no answer to that, so the rule now asks overlays for `drawSize` and validates it against `srcRect × scale`. Its own note: *"Nothing was softened: AF-R-911 keeps its grip."* |
| **No New Game** — "once slot 1 exists, boot always continues from it" | **Closed.** There is an `AF.title` module with a New Game flow behind a confirmation, and a self-test that asserts *"New Game must not destroy the save"* — one press to ask, one to confirm. This was suggested-order item 3. |
| **`bld_chapel` is still in the atlas, 20,193 dead pixels** | **Closed at 0.19.0.** Rect gone, `craftpix_chapel` out of the credit ledger, only the comment recording the removal remains. This was suggested-order item 6. |
| **The merchant is provisional** | Named. The provisional set is now `barrow_downs`, `deep_barrow`, `ashen_reach`, `hold_supplies`, `guild_quartermaster`, `rowans_smithy` — still six, but a different six: `npc_merchant` left it and the smithy joined it (0.31.0, after its unnamed panel header rendered a visible `«missing text»` marker, which is AF-R-1011 working as designed). |

## Still open

| Gap | State at 0.34.0 |
|---|---|
| **`AF-R-601` still names `AF.player.step`** — "ninth version" at 0.12.5 | **Still true.** `AF.player` has zero occurrences; movement is `AF.sceneKit.walk`. |
| **Both bosses are triggered by nothing** | **Still true, and the build says so itself** — `AF.battle.todo()` carries the line verbatim: *"custodian_of_the_seal and the_hollow_dragon are declared, phased, and triggered by nothing — no scene starts either boss."* |
| **Two wilderness regions have no maps** | `deep_barrow` and `ashen_reach` are still named and still unbuilt. Seven scenes are registered; neither is one. |
| **Six provisional names, placeholder lines remain** | Six provisional (above). Approved canon has grown 128 → **135**. |

## Not determinable from the source

- **The "aborted" HUD leak.** Every `AF.battle.end("aborted")` call site is
  inside the self-test block, which is consistent with the diagnosis (a
  boot-time test battle reaching the forest's encounter banner) but does not
  say whether the leak still occurs. That is a runtime observation.
- **The inn spur, the guild hall chest, the four bedrooms.** All three are
  asset/authoring decisions rather than code states.
- **Balance.** *"A level-1 party still loses to the Outwood."*

---

## The enforcement census, no longer stale

`RULES_INDEX_ADDENDUM_0_12_5_SECTION.md` carries two PENDING items. **One of
them can be closed without the index**, and is closed here:

> **PENDING** — The enforcement census is stale at 23 (0.9.1). Two modules with
> new refusals have landed since.

Measured at 0.34.0 by scanning the build:

```
distinct AF-R ids cited in code    89     (88 at 0.7.0 final and 0.12.5)
enforced by AF.rules.refuse        20
enforced by AF.rules.require        7
enforced by AF.rules.forbid         1
distinct ids machine-enforced      24     (23 at 0.9.1, 21 at 0.7.0 final)

102 203 311 331 401 402 605 611 622 702 707 711 803 812 821
903 904 905 921 922 923 1001 1010 1011
```

Three ids gained a machine check since the 0.7.0 final list of 21:

- **AF-R-203** — the two-sided placeholder guard added at 0.11.0 when `WORDS`
  split into `NAMES` + `WORDS`. Approved names must render unmarked *and* be
  absent from `AF.text.placeholders()`; provisional names must render marked
  *and* be present.
- **AF-R-331** — collision is authored, not derived.
- **AF-R-1001** — `verified` refused without a measured rect.

**The other PENDING item stays open.** The cited-vs-indexed diff needs
`RULES_INDEX.md`, which is not in this repo. Half of it is mechanical here —
`./tools/cited-rules.sh` prints the 89 ids — and the dangerous direction
(rules the build enforces that the index does not contain) **has not been
measured since 0.9.3**, now across roughly twenty-five versions. That is the
same gap that went unmeasured for four versions before 0.7.0 and turned out to
be hiding twelve rules, one of them cited 52 times.
