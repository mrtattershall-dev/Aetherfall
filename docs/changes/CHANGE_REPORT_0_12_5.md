# Aetherfall — change report, 0.10.0 → 0.12.5

Names became canon, saving became reachable, and the third building became an
inn. Every number below was read out of the running build, not recalled.

```
Files / sections changed:
  aetherfall-0.12.5.html
    · AF.build        — 0.10.0 -> 0.12.5 (save schema unchanged at 4)
    · AF.atlas        — 512x2265 -> 512x2569, 295 -> 369 rects
    · AF.content      — WORDS split into NAMES (canon) + WORDS (backlog)
    · AF.save         — + peek(): a slot's headline without loading it
    · AF.rest         — NEW MODULE: price, problem, take
    · AF.conversation — start() accepts opts.lines for a runtime sequence
    · AF.menu         — NEW SCREEN: Save, with save and load
    · AF.anim         — NEW: grug_idle, 12 frames at the pack's own 150ms
    · AF.innInterior  — NEW SCENE, sixth in the registry
    · AF.demo         — inn door, two-column spur, ROAD_UNDER, tree moved
    · boot            — Continue: reads slot 1 after the self-tests
    · AF.interiorGuildHall — bare say() fixed; chest blocker trimmed

Rules touched (AF-R-###):
  AF-R-203   approved canon draws clean; the backlog stays marked and listed
  AF-R-331   the house's collision box is why the road stops where it does
  AF-R-341   art extends beyond footprint — which is why the tree moved twice
  AF-R-521   authored road stays walkable; the apron is drawn, not authored
  AF-R-524   the inn exit is a probe band, not the tiles you stand on
  AF-R-801   AF.rest owns heal/charge/save; the scene only calls it
  AF-R-812   money moves through AF.inventory.spend, which owns the floor
  AF-R-921   150ms is the artist's number from Characters.tmx
  AF-R-923   one row, one facing — no invented directions for Grug
  AF-R-932   peek() describes a slot it cannot load rather than migrating it
  AF-R-941   room and sprite declared with pack provenance
  AF-R-1001  every new rect measured before anything claimed verified
  AF-R-1007  moving a row from WORDS to NAMES is a canon decision

FLEXIBLE choices made (AF-R-802 requires stating these):
  1. Two name tables, not a flag. An `approved:true` set would have made the
     existing AF-R-203 guard carry exceptions; the property stays absolute.
  2. `survivor_01` holds "Aren" as a DEFAULT. The rename screen will override
     the string rather than delete the row.
  3. Rest costs 10 gold + 5 per level, priced off the LEAD actor. Recruiting
     a fourth member should not quadruple the bill.
  4. One save slot. Multi-slot is naming, ordering and overwrite confirmation,
     none of which is needed to stop a session being lost.
  5. Continue runs AFTER AF.selftest.run(), never before.
  6. The rest confirm reuses AF.conversation: its cancel already declines
     without running `then`, so B is "no" and A is "yes" with no new UI.
  7. The inn's four bedrooms are drawn and not entered.
  8. No door swing on the east house — that pack ships no door animation.

Assumptions made:
  None. Every rect, frame count, frame duration and doorway position came from
  a pack's own files or from the running build.

Self-test: NOT RUN in this session — no jsdom, no network. Syntax checks and
  static symbol/geometry checks only. Everything here is UNVERIFIED at runtime
  except what the user confirmed on a device.
```

---

## 1 — Names are canon now

The 118 mechanical names (57 items, 12 statuses, 31 abilities, 18 enemies)
were drafted against the running tables and approved, along with the party and
the forest.

| Slot | Name |
|---|---|
| `survivor_01` | **Aren** — default; player-renaming is future work |
| `warden_02` | **Bulwark** |
| `kindler_03` | **Zephyr** |
| `mender_04` | **Cass** |
| `forest_route` | **The Outwood** |
| `npc_grug` | **Grug** |
| NPC in the Hold | **Wren**, unchanged |

`AF.content.WORDS` was not a name table with a marker on it — it *was* the
approval backlog, and a self-test asserted every id in it renders with a
`[placeholder]` prefix. Approving 118 of 122 entries would have emptied the
mechanism rather than used it.

So it split. `NAMES` holds approved canon, registered as `name.<id>`, drawn
exactly as written. `WORDS` holds what is still undecided, registered as
`placeholder.name.<id>` with the marker. `install()` refuses an id present in
both, because nameOf's precedence must never silently settle a canon question.

The AF-R-203 guard is now two-sided: a one-sided test would have gone green on
an emptied table.

```
approved     128
provisional    6   — barrow_downs, deep_barrow, ashen_reach,
                     hold_supplies, guild_quartermaster, npc_merchant
placeholder text ids  10  (was 140)
```

## 2 — Saving is reachable

The diagnostics panel had said *"Save works — no slot screen"* since 0.6.17.
That was true and had stopped being harmless: nothing called `AF.save.write`
outside the self-tests, and boot never called `read`. A complete, unreachable
system — the same shape as the Items backend before 0.10.0, and as the door in
0.6.18.

- **A Save screen** in the menu, one slot, with save and load.
- **`AF.save.peek()`** reads a slot's headline without loading it, and
  deliberately does not migrate: a slot too new to load should still be
  describable.
- **Continue at boot**, after the suite. The suite mutates mode, scene,
  inventory and party and restores them; 0.7.0 found four leaks doing exactly
  that. Loading first would hand the tests a live session to trample.

Every failure path falls through to a fresh game with the reason said aloud.

**There is no New Game.** Once slot 1 exists, boot always continues from it.
Listed in diagnostics rather than left implicit.

## 3 — The inn

`AF.rest` was built **before** the scene, so the scene composes it rather than
growing its own copy. It reads no scene id: a campfire calls the same
function.

Grug is the Tavern pack's `Animation_watcher` — 12 frames, 150ms from the
pack's own `Characters.tmx`, trimmed to the union bounding box of the whole
animation so the frames stay registered to each other. One row, one facing.

The room is the Tavern pack's **second floor**; the guild hall is already its
first, which is why no new pack enters `AF.credits`.

```
atlas   512x2265 -> 512x2569   (+304 rows: 272 room, 32 Grug)
rects   295 -> 369
base64  403 KB -> 433 KB
file   1206 KB -> 1265 KB
```

## 4 — Four bugs the device found that no test did

1. **The Guildmaster crashed on every press.** `AF.interiorGuildHall` called a
   bare `say()`, which is a local inside `AF.demo`'s IIFE and had never been
   in scope there. `AF.interact` catches handler throws, so a ReferenceError
   looked like "pressing A does nothing" — no red, no failing test, just a
   fault band nobody had open. Now calls `AF.speech.say`, with a walk-up test.

2. **The inn had no walls.** Collision was derived from the pack's layers the
   way the guild hall's is, and the room SHELL is not in the `Walls` layer —
   it is in `Walls_top2` and `Walls_top1`, which were excluded as "overlay
   only". `floor` also extends *under* the walls, so floor-minus-Walls is not
   a walkable set on this map at all. Deriving it correctly gives a corridor
   one tile tall, disconnected from the stairs: the map is a cutaway display
   piece, not a walkable floor. Collision here is **authored**, and says so.

3. **The inn exit could not be pressed.** The zone was sized to the two tiles
   the player stands on. The probe lands half a tile ahead of the feet, so the
   only facing that reached it was "up". This is the 0.6.18 door in its purest
   form, made by someone who had read the note about it. Sized to where the
   probe lands now.

4. **A self-test assertion had been failing for two versions.** It asserts the
   workshop spur is at `16,13`; the spur moved to column 17 in 0.10.2 and the
   assertion did not move with it. Reported as one of three device failures
   and not chased at the time.

## 5 — Road under a building

The inn spur stopped a tile short of its door because `bld_house`'s blocker
spans y1076-1172 and eats the top of row 18. An authored road tile under a
blocker is refused by AF-R-521 — correctly, since authored road is a promise
that a player can walk it.

But the rule is about **walkability** and the gap was about **appearance**,
and those two questions had one answer. `ROAD_UNDER` is drawn as road and is
not authored road: `isRoad` reads both, so the apron autotiles into the network
and suppresses scatter on itself, while `roadTiles()` — which AF-R-521, the
reachability tests and the resonance check all read — still returns `ROAD`
alone. A tile added there can never weaken a rule about where the player can
stand.

The workshop's problem was the opposite: its door is 192 wide (tiles 16-18) and
a one-tile spur met a third of it. Tiles `16,13` and `18,13` are ordinary
walkable road.

The inn door could not be centred by moving one column, as the workshop was in
0.10.2: that door is 192 wide and its centre lands exactly on tile 17's centre,
while this one is 68 wide, centred on x1674, against tile centres at x1632 and
x1696. A two-column spur centres on x1664 — 10px off instead of 22.

## 6 — The tree, twice

`herb_prop_04` moved (17,13) -> (15,14) in 0.10.2 and (15,14) -> (13,14) here.
The first move measured its **blocker**, which is 64x32. Its art is 212x256 and
spans four columns, so at (15,14) the canopy still lay across the spur at
column 17 even though nothing there stopped the player.

AF-R-341 — art extends beyond footprint — is usually invoked to stop collision
being over-generous. It cuts the other way when the art is the complaint.

## Left for you

- **`AF-R-911` icon warnings flood the log.** The 88 icons declared in 0.9.3
  carry no `{w,h}` placement. Harmless, and they bury anything real.
- **"aborted" leaks onto the HUD.** That string comes only from
  `AF.battle.end("aborted")`, which only self-tests call. A boot-time test
  battle is reaching the forest's encounter banner — a sixth member of the
  state-leak family enumerated at 0.7.2.
- **The inn spur still stops a tile short** in walkable terms. Closing it means
  re-anchoring `bld_house`'s collision, an AF-R-331 asset decision that changes
  where the player can stand around the whole building.
- **The guild hall chest still overlaps its doorway** in the art. The room is
  one baked 336x224 atlas rect; moving the chest means recompositing from
  `Interior_1st_floor.tmx` and repacking.
- **No New Game.**
- **The four inn bedrooms are drawn, not entered.**
- **Six provisional names and ten placeholder lines remain**, including the
  Guildmaster's two and Grug's three.
- **`bld_chapel` is still in the atlas**, 20,193 dead pixels. This pass
  appended rows again rather than repacking.
