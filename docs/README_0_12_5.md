# Aetherfall — 0.12.5 · branch `rowans-hold`

Not the game yet. But you can now walk out of the settlement, get jumped in the
Outwood, fight the thing with real sprites, buy salves from a shopkeeper who
talks, sleep at an inn, and save.

```
aetherfall-0.12.5.html                  open this — it boots and runs on a phone
docs/RULES_INDEX.md                     every Bible rule with a stable AF-R-### id
docs/RULES_INDEX_ADDENDUM.md            enforcement audit + amendments, measured
docs/ASSET_MANIFEST.md                  measured pack inventory + what is still unknown
docs/AI_HANDOFF.md                      the header to paste above implementation requests
docs/CHANGE_REPORT_0.12.5.md            this version
docs/AUDIT_0.9.3.md                     deep audit — fifteen areas
docs/PLACEHOLDER_INVENTORY.md           what it takes to fill every placeholder
```

**Everything below was read out of the running build, not from memory.**

## What runs right now

Portrait 540×960 viewport. Move with arrows/WASD or the on-screen pad. Menu
button top-left; diagnostics lives inside it.

**Three modes of four are implemented** — `overworld`, `battle` and `menu`.
Only `boot` still reports pending. 369 measured atlas rects across 12 credited
packs, drawn at integer 4× (world) and 3× (UI).

### Six scenes

| Scene | World | Notes |
|---|---|---|
| `rowans_hold` | 2176×1664 | real floor; south gate leads to the Outwood |
| `guild_hall_interior` | 1344×896 | the Guildmaster; quartermaster's counter |
| `shop_interior` | 1152×1216 | the merchant talks, then opens his shop |
| `forest_route` | 1408×2560 | wilderness, 32 props, wild encounters |
| `barrow_downs` | 1280×2176 | **all placeholder art** — real map, honest picture |
| `inn_interior` | 1664×1088 | **new** — Grug, and a bed that heals and saves |

### Content

```
items        57    statuses  12    abilities  31    enemies      18
regions       5    roster     4    shops       2    encounters    4 (+3 authored)
ai patterns  18    phases     2    growth curves 5  learnsets     4
recruits      3    npcs       5

names       128 approved canon · 6 still provisional
text         10 placeholder ids remain (was 140)
atlas       512×2569 · 369 rects · 433 KB base64 · 1265 KB file
```

## Changed since 0.10.0

**Names are canon.** 118 mechanical names plus the party and the forest were
approved. `AF.content` now holds two tables: `NAMES` for approved canon, drawn
clean, and `WORDS` for the shrinking backlog, drawn with its `[placeholder]`
marker. An id in both refuses the boot.

**The party has names.** Aren, Bulwark, Zephyr and Cass. Aren is a *default* —
a rename screen is future work.

**The forest is the Outwood.**

**You can save.** A Save screen in the menu, one slot, save and load. Boot
continues from slot 1 if it is there, after the self-tests rather than before.
No autosave, by design.

**There is an inn.** The east house — the building whose road spur has pointed
at a door that did not exist since 0.6.x. Grug charges 10 gold plus 5 per
level, heals the party, refills MP and writes a save. `AF.rest` owns all of
that; the scene only calls it, so a campfire needs no second copy.

**The road runs under the buildings.** `ROAD_UNDER` is drawn as road without
being authored road, so a path can reach a threshold that sits inside a
building's collision box without weakening AF-R-521.

**The Guildmaster speaks.** He had been throwing a ReferenceError on every
press for an unknown number of versions, silently, because the interact path
catches.

## Known gaps, stated plainly

- **`AF-R-911` icon warnings flood the console.** The 88 icons added in 0.9.3
  carry no `{w,h}` placement. Harmless, and they bury anything real.
- **"aborted" leaks onto the HUD** from a boot-time self-test battle reaching
  the forest's encounter banner.
- **No New Game.** Once slot 1 exists, boot always continues from it.
- **The four inn bedrooms are drawn and not entered.** The pack's second-floor
  map is a cutaway; its collision is authored here, not derived.
- **The inn spur stops a tile short** in walkable terms — `bld_house`'s
  collision reaches into that row. Closing it is an AF-R-331 asset decision.
- **The guild hall chest overlaps its doorway** in the art. The room is one
  baked atlas rect; moving it means recompositing and repacking.
- **Six provisional names**: the three unnamed regions, two shops, and the
  merchant. **Ten placeholder lines**, including the Guildmaster's two.
- **Both bosses are triggered by nothing.** Declared, phased, startable; no
  scene starts either.
- **Two wilderness regions have no maps** — `deep_barrow`, `ashen_reach`.
- **Balance is unproven.** A level-1 party still loses to the Outwood.
- **`bld_chapel` is still in the atlas**, 20,193 dead pixels.
- **AF-R-601 still names `AF.player.step`.** Ninth version.

## Suggested order from here

1. **Clear the `AF-R-911` warnings**, so the log is readable again.
2. **Fix the "aborted" leak** — sixth member of a family enumerated at 0.7.2,
   and the enumeration still lives in a change report rather than in code.
3. **New Game**, or a title screen, which is Continue's natural home anyway.
4. **Name the three regions**, the two shops and the merchant; write the
   Guildmaster's line and Grug's three.
5. **Play a fight and rebalance.**
6. **An atlas repack**, dropping `bld_chapel` and stopping the append-only
   growth.
