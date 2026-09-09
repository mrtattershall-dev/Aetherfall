# Systems audit — 0.44.0

**Method.** Everything below was measured by driving the live build in headless
Chromium — the real registries, the real `AF.battle`, the real `AF.ascension`,
the real `AF.equipFlow`. Nothing here is read off the source. Where a number is
a simulation it says so and says how many trials.

**Scope.** Abilities, the skill board, items, equipment, statuses, enemies,
the XP and gold economy, boss difficulty.

---

## What is sound

These were tested and work. Listing them matters as much as the defects,
because several are systems the handoff docs still describe as unproven.

| System | Verified |
|---|---|
| **Skill board** | 4 boards, 41 nodes. Every node reachable from its root; a full board costs 19 SP. Refusals are correct and change nothing (`"bal_def1 still requires bal_steady"`). Bought abilities appear in the battle menu and cast — `gut_punch` dealt 19 for 3 MP through the real command path. |
| **Abilities** | 31 defined. **None is unreachable by everyone** — 22 are player-reachable (start kit or board), 9 are enemy-only by design. |
| **Consumables** | All 15 do what they declare: heals heal, draughts restore MP, `field_dressing` cleared `bleed`, `clear_water` cleared `poison`, `clarity_leaf` cleared `silence`, the three flasks dealt 40/30/37 to a live target. All consume exactly one. |
| **Equipment** | 24 items, 22 equipped through `AF.equipFlow.wear` with correct stat deltas (`barrow_plate` def+12 mdf−4; `seal_breaker` atk+5 mat+6). The rest move agi/luk, which this pass did not sample. |
| **Statuses** | 12 defined, all referenced by an ability, item or enemy. None orphaned. |
| **Boss phases** | The Custodian's 50% phase **fires reliably** — 10/12 fights at level 5, 12/12 at 10 and 15. It is not decorative. |
| **XP and gold** | Both award correctly: a Husk gave 9 exp and 6 gold through a real won fight. |
| **Selling** | `AF.vendor.sell` exists, so the 14 materials have a purpose (1,354 gold of drops) even without crafting. |

---

## Findings, worst first

### 1. Healing does not scale with anything — CONFIRMED

```js
t.hp = Math.min(t.hpMax(), t.hp + ab.power);       // AF.battle, the whole heal path
```

`ab.power` is a constant. Healing reads no stat, no level, no equipment.
`mend` restores **45 HP at level 1 and 45 HP at level 30.**

Measured against the survivor's own HP curve (`hpMax = 20 + level·6 + vit·4`):

| level | hpMax | one `mend` |
|---|---|---|
| 1 | 54 | **83%** of the bar |
| 5 | 94 | 48% |
| 10 | 144 | 31% |
| 20 | 248 | 18% |
| 30 | 352 | **13%** |

Enemy damage scales with their stats; the healer's output does not. Cass gets
strictly worse every level, and the support board's `mat` and `spr` nodes buy
her nothing for the job she exists to do.

**This is the most consequential balance defect in the build.** Two obvious
fixes, both one line: scale by `mat` the way damage scales by `atk`, or make
heal power a fraction of the target's `hpMax`.

Related, and cosmetic by comparison: all five healing abilities declare
`kind: "physical"`. Nothing reads `kind` on a heal, so it is inert — but it is
data that says something untrue, and `offStat = kind === "magical" ? "mat" :
"atk"` sits one function away.

### 2. The Custodian's difficulty window is three levels wide

**30 simulated fights per level**, through the real engine, party of four with
a competent policy (heal below 50%, otherwise the strongest affordable
ability), levels and SP reset before every fight:

| party level | victories | avg rounds |
|---|---|---|
| 1 | **0%** | — |
| 3 | **3%** | 21 |
| 5 | **73%** | 6.3 |
| 8 | 97% | 3.9 |
| 10 | 100% | 3.4 |
| 15 | 100% | 2.2 |
| 18 | 100% | 1.9 |

Arrive at 5–7 and it is a real fight. Arrive at 8 and it is a formality.
Arrive at 3 and it is impossible. At 10+ the fight is over in three rounds —
the 50% phase fires and then the boss dies before it matters.

The demo has no level gate on the barrow trail, so which of those three
experiences a player gets is decided by how much they happened to grind.

> **A correction on how this number was reached.** My first run of this
> simulation reported **100% wins at every level including 1**. Two harness
> bugs, both mine: the party levelled up on boss XP between trials so later
> runs were not at the stated level, and — the one that mattered — I inferred
> victory from "someone is still alive", while `AF.battle.active()` returns
> null after a fight and a defeat leaves the party at 1 HP each. Every defeat
> read as a win. The table above uses the engine's own `battle:ended`
> outcome. A turn-by-turn trace is what exposed it: a level-1 party does 8
> damage a round to a 230 HP boss that hits for 35–41.

### 3. The boards are priced for a game four times longer than the demo

One full board is 19 SP. SP is one per level. So a complete board is **level
20**, which needs 21,712 cumulative exp:

| target | exp | ≈ barrow fights (avg 42 exp) | ≈ forest fights (avg 11) |
|---|---|---|---|
| level 5 | 473 | 11 | 41 |
| level 8 | 1,802 | 43 | 158 |
| level 10 | 3,338 | 79 | 292 |
| **level 20** | **21,712** | **513** | 1,900 |

A player arriving at the Custodian around level 5–8 holds 4–7 SP and has
unlocked 4–6 of a board's 11 nodes, including 2–3 of its 6 ability nodes.

That is a reasonable *demo* slice — roughly half a board. It is worth saying
plainly anyway: the boards were built for a full game, so a demo player will
never see the far half of one, and the ultimates that sit there
(`executioner`, `thunderhead`, `long_mending`) are effectively not in the demo.

### 4. Three top-tier consumables cannot be obtained

Not stocked by any of the three shops, not dropped by any of the 20 enemies:

| item | price | tier |
|---|---|---|
| `salve_grand` | 280g | the 400 HP heal |
| `draught_grand` | 340g | the 160 MP restore |
| `rousing_ember` | 520g | the **full** revive |

Every *other* tier of each line is stocked — `salve_lesser`/`greater`,
`draught_lesser`/`greater`, `rousing_ash` (the 50% revive). Only the top of
each ladder is missing, and these are exactly the items a player would want
for the boss. They have prices, icons, names and working behaviour; nothing
sells them.

### 5. Two key items are completely dead

`barrow_key` and `guild_writ` are defined, named, given atlas icons — and
**nothing grants them and nothing requires them.** Not a progression blocker
(no door asks for either), but they are content that cannot enter the game.

For contrast, the other two key items are fine: `seal_fragment` is granted,
and `custodian_token` drops from the Custodian.

### 6. No crafting, and 14 materials

`AF.crafting`, `AF.forge` and `RECIPES` do not exist. All 14 materials drop
and their only use is being sold. That is a legitimate design — drops as
currency — but 14 distinct named materials is a lot of surface for one
purpose, and the names imply crafting that is not there.

---

## Numbers worth keeping

**Enemy roster** — 20 enemies, level 1 → 18:

| tier | enemies | hp range | exp | gold |
|---|---|---|---|---|
| forest | husk_lesser, grave_moth, giant_rat, slime, husk_gaunt, dust_crawler, bone_picker | 40–68 | 7–17 | 4–12 |
| barrow | barrow_rat, cairn_hound, rime_wraith, ash_revenant, mourn_caller, storm_chitin, gloom_eater | 74–144 | 22–82 | 14–60 |
| unreachable in demo | dawn_moth, pale_choir, barrow_knight, iron_shade | 120–194 | — | 55–110 |
| bosses | seal_custodian (L15, 230hp, 1 phase), hollow_dragon (L18, 288hp, 2 phases) | | | 300 / 520 |

**Shops** — 36 items across three: `hold_supplies` (8, starter), 
`guild_quartermaster` (13, mid), `rowans_smithy` (15, gear, 60–780g).

**Gold** — start 30. Forest averages 7.7/fight, barrow 29.7. The priciest
stocked item is `seal_breaker` at 780g ≈ 26 barrow fights.

---

## Not audited in this pass

- Dialogue, quests and text coverage (the `[placeholder]` inventory is its own
  document and has not been re-run since 0.7.3).
- Save/load round-tripping of the fields this pass touched (`nodes`, `sp`).
- The overworld: collision, interactables, chest placement.
- Whether any of this is *fun*, which no simulation can answer.
