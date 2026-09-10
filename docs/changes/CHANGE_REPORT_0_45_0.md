# Change report — 0.45.0

**Build** `Aetherfall 0.45.0 · rowans-hold · save v4`
**Self-test** 398 / 398 (two new), three runs, 0 boot faults, no page errors
**Size** 5,975,485 bytes (+34,263 — comments and tests, no assets)
**Branch** `claude/newest-build-nv7xsl`

All six findings from `AUDIT_0_44_0_SYSTEMS.md`, fixed. Two of them are
balance and interact, so they were measured together rather than in sequence.

---

## 1. Healing now scales — `spr`, and why not `mat`

Healing was `t.hp + ability.power`: a flat number reading no stat, no level
and no equipment. `mend` restored 45 HP at level 1 and 45 at level 30.

The new arithmetic lives in `AF.damage.heal` beside `resolve`, because that is
the one home for combat arithmetic (AF-R-801):

```js
function heal(o) {
  const { healer, power = 10 } = o;
  const spr = (healer && typeof healer.stat === "function") ? healer.stat("spr") : 10;
  return Math.max(1, Math.round(power * spr / 10));
}
```

**Why `spr`.** Both candidates were measured against the pool they have to
keep up with:

| level 1 → 30 | growth |
|---|---|
| Cass `mat` | 11 → 54 (**×4.9**) |
| Cass `spr` | 10 → 68 (**×6.8**) |
| Aren `hpMax` | 54 → 352 (**×6.5**) |

`spr` tracks the HP curve almost exactly; `mat` does not. The same formula on
`mat` still decays by half over thirty levels. It also gives SPIRIT its first
real mechanical job — the stat a healer should have been buying all along.

**Why proportional, not `1 + spr/20` like damage.** Damage is divided by the
defender's ratio and lands on enemy pools authored per-enemy that never grow
with the player. A heal lands on a pool that grows every level, so it has to
grow *with* it rather than merely lean on it.

**Measured through a real cast**, hero at 1 HP, Cass casting `mend` through
the battle command path:

| level | Aren hpMax | mend | **share of bar** | steady | regen/turn |
|---|---|---|---|---|---|
| 1 | 54 | 30 | **56%** | 30% | 4 |
| 5 | 94 | 54 | **57%** | 34% | 8 |
| 10 | 144 | 84 | **58%** | 36% | 13 |
| 20 | 248 | 144 | **58%** | 37% | 23 |
| 30 | 352 | 204 | **58%** | 38% | 33 |

Flat at 56–58%, where it was 83% → 13%.

`power` is a **coefficient** now, not an amount, so all five heals were
retuned in the same edit: mend 45→30, mend_all 38→22, steady 24→**40**,
renewal 20, long_mending 24→18; `regen` 22→10 and `mending` 38→16 per turn.
Steady being *larger* than mend is the formula working — Aren has a quarter of
Cass's spirit, so the same share of a bar costs a bigger coefficient.

Lingering healing scales too, from the **bearer's** spirit: the caster is long
gone by the time regen ticks, and a blessing sitting on someone is theirs.

`kind` is now stated as `"magical"` on all five. It was never authored — the
registration default is `"physical"`, which is what made every heal read as a
physical ability in the audit, one function away from
`kind === "magical" ? mat : atk`.

## 2. The Custodian is a boss now

**vit 30 → 85 (230 → 450 HP), atk 30 → 27.** 30 simulated fights per level
through the real engine, competent policy, party reset before every fight:

| party level | 4 | 5 | 6 | 7 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|
| **before** | 50% | 88% | 81% | — | 100% | 100% | 100% |
| rounds | 7 | 6 | 6 | — | **4** | 3 | 3 |
| **after** | 13% | 37% | 77% | 80% | 90% | 97% | 100% |
| rounds | 9 | 10 | 9 | 7 | 7 | 5 | 4 |

A ramp from 4 to 10 instead of a cliff between 5 and 8, and fights lasting
seven to ten rounds at the levels a player actually arrives — so the 50% phase
is part of the fight rather than a footnote it never reached.

ATK came **down** because the length had to come from health rather than
burst: at atk 30 the low-level runs were losses decided in two turns, which
reads as a wall rather than a hard fight.

**These two fixes were measured together, and had to be.** The first pass
landed on 370 HP — correct against one skill point per level, and 65% at level
5 and 100% at level 8 once the rate became two. The number was re-derived
rather than kept. Two balance changes in one version are each measured against
a game that no longer exists unless they are measured at the same time.

## 3. Two skill points per level

A full board is 19 points. At one per level that is **level 20**, which needs
21,712 cumulative exp — roughly 513 barrow fights, in a demo that ends at the
Custodian around level 5–8, where a player held 4–7 points and had seen a
third of one board.

At two, **every board completes at level 11**, and level 8 is 14 of 19 — most
of a board with the last tier still to earn. The boards keep their job: you
cannot have everything, and buy order is still a choice.

The cheapest of the three levers. The others were shortening the boards, which
throws away authored content, and making levels faster, which changes every
encounter's pacing to fix a progression problem.

## 4. The Grand tier is on sale

`salve_grand` (280g), `draught_grand` (340g) and `rousing_ember` (520g) — the
top rung of all three consumable ladders — were declared, priced, iconed,
named and fully working, and sold by nobody and dropped by nothing while every
rung below them was on sale. They join `guild_quartermaster`.

Price-gated rather than flag-gated: at ~30 gold a barrow fight a Grand Salve
is nine or ten fights of saving, so it stays a decision rather than becoming
standard kit, and no new mechanic was needed to make it one.

## 5. `barrow_key` and `guild_writ` removed

Both were declared, named and iconed; nothing granted either and nothing
required either. They could not enter a bag by any route.

**Removed rather than wired**, because wiring means inventing progression the
game does not have. The barrow already has a gate and it opens by clearing
`barrow_gate_ambush`, so a key would be a second answer to a question already
answered (AF-R-801). The guild hall is open to anyone, so a writ would be a
new gate on a room the demo wants the player inside. Either is canon and
therefore **yours** (AF-R-1007) — the item rows, `NAMES` entries and
`ICON_INDEX` entries are gone; the atlas rects remain and cost nothing.

Say the word and either comes back with a job.

## 6. Materials and crafting — recorded, not invented

14 materials drop and can only be sold. No crafting system exists and **none
was built here**: that is a feature, not a fix, and it was not asked for.
Drops-as-currency is a real design and it works — `AF.vendor.sell` takes them,
and key items are correctly refused for sale.

What is true is that the names imply recipes. That is now in `todo()` as a
user decision: a crafting pass, or a rename.

---

## Tests

Two new (398 total), and both exist because the audit's findings could not
have been caught by anything that shipped.

**`healing keeps its share of the health bar as the party levels`** — asserts a
**ratio**, not an amount, so it survives every future retune of power, of the
HP curve and of the growth rates. That is the point: the defect was that one
of those three moved and healing did not move with it. A 15-point band across
levels 1–30; the pre-fix build spanned 70. It also asserts the heal reads the
*healer* (a support healer must out-heal a fighter), that regen scales, and —
as a source-level claim — that nothing adds `ability.power` to `hp` directly.
It builds synthetic actors rather than touching the party, because it walks a
level curve and the suite must leave the player's game as it found it.

**`every declared item can be obtained by some route`** — shop, drop or
starting kit. Same shape as the 0.43.0 audio reachability test: a complete
asset nobody can reach still ships, is still paid for, and reads to a player
as content that isn't there.

Three existing tests **correctly failed** on the skill-point change and were
rewritten to assert the *rule* rather than the number — they now read
`AF.ascension.SP_PER_LEVEL` instead of restating `1`, and the board test
gained the bound it was missing: a board must complete somewhere a player can
reach (6 ≤ level ≤ 14), and all four must complete at the same level or one
role finishes its identity while the others are still buying theirs.

## Revert-proof

| Reverted | Caught as |
|---|---|
| flat heal (`hp + ab.power`) | `a heal path still adds ability power to hp without scaling it` |
| `heal()` returns `power` unscaled | `mend swings from 9% to 65% of the bar` |
| un-stock the Grand tier | `salve_grand (consumable, 280g) is sold by nobody, dropped by nothing…` |
| `SP_PER_LEVEL = 1` | `19 points completes at level 20, past the demo's reach` |
| `SP_PER_LEVEL = 5` | `completes at level 5 — the board is spent before the boss` |
| stock a non-existent item | boot refuses: `AF-R-803 … stocks undeclared item` — a **pre-existing** guard, stronger than my test, which I did not know about until I tried to break it |

## Verification

- 398/398 × 3 runs, 0 boot faults, no page errors
- Item reachability re-run: **0 orphans** in all four kinds (was 5)
- Boards complete at level 11, all four
- Boss: vit 85 / atk 27 / 450 HP, Grand tier stocked, dead keys gone
- Heal curve measured through a real cast at five levels
- Boss curve measured at 30 fights per level, party fully reset each fight

## Not verified

- **Nothing has been played.** Every balance number here is simulated with a
  scripted policy, and a scripted policy is not a person: it never panics,
  never misreads a phase, never saves a Grand Salve for a fight it does not
  reach. `todo()` says so.
- Nothing device-verified since 0.43.0.
- The Hollow Dragon is still at the pre-0.45.0 boss scale (288 HP against the
  Custodian's 450). It is unreachable — no scene starts it — and needs the
  same pass before it becomes reachable.
- Status **damage** is still flat while status healing now scales. Poison on a
  growing party HP pool has the same shape of defect healing just lost, but
  the same numbers land on enemies whose pools do not grow, so it is an
  enemy-balance pass rather than a one-line change.
