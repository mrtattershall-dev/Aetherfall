# Asset verification — thirteen packs against the 0.34.0 atlas

Run with the source archives present, which is the only way this check runs at
all. `AUDIT_0_9_3` records the same check for the 88 Franuka icons and says why
it can never become a self-test: it needs the packs, and the build does not ship
them. This is that check, applied to the enemy sprites and the barrow ground.

Method: decode the atlas out of `aetherfall.html`, crop each declared rect, and
compare it pixel-for-pixel against the source the asset's own `source` string
names — row 0 (front) of the named state sheet for enemies, the named 16px cell
index for ground tiles, the numbered individual file for icons.

**213 of 213 rects that could be checked are byte-exact.** Two packs cannot be
used at all until their terms are found, and one supplied pack turns out not to
be the one the build drew from.

| Family of check | Rects | Result |
|---|---|---|
| Franuka icons (57 items + 31 abilities) | 88 | **88/88** |
| Enemy sprites (beast, boss, vermin) | 71 | **71/71** |
| Barrow ground set | 54 | **54/54** |

---

## Result

| Pack | Declared as | Checked | Verdict |
|---|---|---|---|
| Fantasy RPG Icon Pack (Franuka) | `franuka_icons` | 88 icons | **88/88 byte-exact** |
| Free Undead Tileset (craftpix 695666) | `craftpix_undead` | 54 rects | **54/54 byte-exact** |
| Top-Down Pixel Ent (craftpix 838021) | `craftpix_ent` | 48 frames | **48/48 byte-exact** |
| Giant Rat — 4 Direction (craftpix 415491) | `craftpix_rats` | 23 frames | **23/23 byte-exact** |
| Pixel Art Slime Enemies (craftpix 743043) | — | — | **not the pack in the build** |
| RPG Ultimate GUI | — | — | **no licence of any kind — still blocked** |
| Free Raven Fantasy Icons | — | — | **no licence in the archive** |
| Golem (craftpix 625807) | — | — | new, undeclared — drop-in shaped |
| Top-Down Pixel Gnolls (craftpix 393827) | — | — | new, undeclared — drop-in shaped |
| RPG UI Elements (craftpix 149019) | — | — | **PSD only, no PNG** |
| Free Top-Down Orc (craftpix 363992) | — | — | new, undeclared |
| Free Top-Down Trees (craftpix 385863) | — | — | new, undeclared |
| Top-Down Cute Farm Animals (craftpix 213727) | — | — | ambiguous, see below |

### `franuka_icons` — 88/88, the 0.9.3 result reproduced

`AUDIT_0_9_3` ran this check and got 88/88. Twenty-five versions later it still
holds, against the same source of truth: the numbered individual files under
`Base set/Individual icons (16x16)/` and `Expansions/03 - Spells/…`, never the
spritesheet. The build's own comment explains why that distinction matters —
v2.1 "rearranged the main sheet", and slicing it by position "produced a staff
for a healing potion and a tomato for clear water".

```
57 item icons      via ICON_INDEX          57/57 exact
31 ability icons   via ABILITY_ICON_INDEX  31/31 exact
                                           88/88, 0 mismatches
```

Both index tables resolve cleanly, so a re-cut can still be checked against the
pack's own numbering rather than by eye. This is the check that carries a
mandatory CC BY 4.0 credit link behind it, and `franuka_icons` is in the ledger
with `required: true`.

### `craftpix_ent` — 48/48, and the trim rule is not one rule

The ent pack backs two families: `beast` from `Ent1` and `boss` from `Ent3`,
48 frames between them. All 48 are byte-exact — but only once the right trim is
applied, and **the build uses two different trims**:

| Family | Declared | idle / attack / hurt | death |
|---|---|---|---|
| `beast`, `boss` | 0.10.0 | **union bbox** across the state's frames | **per-frame bbox** |
| `vermin` | 0.25.0 | per-frame bbox | per-frame bbox |

That is not drift, it is two recorded decisions meeting. 0.10.0 cut every state
to a union box so a looping animation would not jitter. 0.24.0 added `death`,
and 0.25.0 changed placement to "follow the ART, rounded up to the 32px
half-grid, instead of a flat 64x64" — because, as the source says, "the slime's
last death frame is a 6px puddle, and a fixed 64 box floated it a whole
half-grid above its own pixels". A dying sprite shrinks, so a union box is
exactly wrong for it.

**Correction to this document.** Its first version described the enemy method as
"trimmed to the alpha bounding box" and reported 23/23 for `craftpix_rats` on
that basis. The count was right and `vermin` is genuinely per-frame throughout —
but the description was a half-rule, and applying it to the ent pack produced 26
spurious mismatches before the real rule was measured. Stated properly, the
enemy total is 71/71 across three families.

### Golem and Gnolls — no work needed to declare them

Both ship the same shape `AF.enemyArt` already consumes: `PNG/<Name>1..3/
Without_shadow/`, four direction rows, front on row 0, with Idle / Attack /
Hurt / Death present.

```
Golem1   cell 128   idle 4, attack 9, hurt 4, death 8   (also run 8, walk 8)
Gnoll1   cell  64   idle 4, attack 10, hurt 4, death 6  (also run 8, walk 6)
```

Adding either is two entries in `PACK_OF` / `SRC_OF` plus a credit-ledger row —
"adding a nineteenth husk needs no art work", as the module says. Both cells are
sizes the build already handles (128 for ent and rat, 64 for skeleton and ghost).

### RPG UI Elements (craftpix 149019) — nothing to measure

Five files: `license.txt`, `Description.txt`, and **three layered `.psd`
sources**. No PNG at any size. Nothing here can be measured or declared without
flattening the PSDs first, which is an art decision rather than a measuring
one. Not blocked on licence — it ships one — but blocked on there being no
raster art in the archive.

### `craftpix_undead` — confirmed, at cell precision

The barrow ground set declares its provenance per tile — *"Ground_rocks.png cell
54"*, *"details.png cell 283"* — which is precise enough to check outright. Every
cell index was resolved against the pack's own `Tiled_files` sheets
(`Ground_rocks.png` 416×1392 = 26 cols, `details.png` 640×224 = 40 cols) at 16px
and compared to the atlas rect:

```
barrow ground set: 54/54 exact, 0 mismatches
```

Both blob autotile sets, the base fill, and all 26 scatter tiles land exactly
where the comments say they do. Note the build's `PNG/` folder holds a
differently-packed `Ground_rocks.png` (496×592) whose cell numbering cannot
reach the indices used — the `Tiled_files/` sheet is the one the rects came
from, and only that reading verifies.

**One provenance note does not reproduce.** `bd_stone` is annotated as the base
ground *"the pack's own map uses 796 times"*. Counting gid 55 (tileset
`Ground_rocks`, firstgid 1, so local id 54) across `Undead_land.tmx` gives
**784 on the `ground` layer and 1008 across all layers** — not 796 either way.
The *identification* is right and is what the annotation is for: that tile is
the most-used by a wide margin, 1008 against 158 for the runner-up. Only the
number is off. The art itself is byte-exact, so nothing downstream is affected.

### `craftpix_rats` — confirmed

Every frame the build draws for the `vermin` family is byte-identical to
`Rat1/Without_shadow/Rat1_<State>_without_shadow.png`, row 0, trimmed:

```
Idle    6 frames   sheet 768x512    6 cols of 128
Attack  8 frames   sheet 1024x512   8 cols of 128
Hurt    4 frames   sheet 512x512    4 cols of 128
Death   5 frames   sheet 640x512    5 cols of 128
                                    23/23 exact, 0 mismatches
```

The declared frame cell (128), the row order (front = row 0) and the trim are
all confirmed against the artist's own files. This is the check that would catch
a spritesheet mis-cut in one step.

### THE FINDING — the slime pack is a different product

The build declares `craftpix_slimes` as **"Free Slime Mobs — Pixel Art Top Down
Sprite Pack"** and cuts the `slime` family's 31 frames from `Slime1/…`. The
uploaded archive is **"Pixel Art Slime Enemies Top-Down Sprite Pack"**
(craftpix 743043). Both ship `Slime1/Slime2/Slime3` in the same folder shape,
which is what makes this worth stating carefully rather than by eye.

`enemy_slime_idle_0` was searched for across **every PNG in the uploaded
archive**, at every row and column of a 64px grid, trimmed the same way:

```
exact matches: NONE
```

So the art in the build did not come from this archive. Nothing is wrong with
the build — its provenance strings are internally consistent and its credit
ledger names the pack it actually used. The consequence is narrower and worth
recording: **the slime frames remain unverified against source**, and this
archive cannot verify them. The "Free Slime Mobs" pack is the one to send.

### The farm-animals ambiguity

`craftpix_farm` is declared as **"Top-Down Farm with Animals Pixel Art Asset
Pack"** and is the build's most-used pack (24 declarations, mostly ground
scatter — `tuft_a`, `tuft_b`, `tuft_c`). The upload is **"Top-Down Cute Farm
Animals Pixel Sprite"** (craftpix 213727), which is a sprite pack, not a tileset.
Similar names, different products, and the uploaded one contains no ground
tiles. Treated as undeclared until the ground art it is credited for is matched
to a file.

---

## Measured frame geometry, for whatever gets declared next

Derived by testing which cell size leaves every cut line fully transparent, not
by looking at the sheets.

| Pack | Cell | Grid | Rows |
|---|---|---|---|
| Orc (363992) | **64×64** | e.g. idle 256×256 = 4×4 | 4 directions |
| Slime (743043) | **64×64** | e.g. run 512×256 = 8×4 | 4 directions |
| Giant Rat (415491) | **128×128** | e.g. attack 1024×512 = 8×4 | 4 directions |
| Farm animals (213727) | **64×64** small, **128×128** horses | goat 192×256 = 3×4 | 4 directions |
| Trees (385863) | n/a — 165 standalone files at 32², 64², 128² | — | — |

**One trap worth writing down.** On the orc *attack* sheets, 7 of 32 cells have
content touching a vertical cell edge — the weapon swing crosses the 64px
boundary. Idle and walk cut cleanly at 64; the attack sheets do not, and slicing
them on a flat 64 grid clips the swing. Those sheets need measuring per frame.
The rows are clean throughout, so the 4-direction split is unaffected.

## Licences — eleven clear AF-R-1001, two do not

The ten CraftPix archives each ship `License.txt` (or `license.txt`) carrying
the standard file-licence link (`https://craftpix.net/file-licenses/`) and no extra credit
text — the same terms the build already records for its twelve other CraftPix
packs, `required: false`. The Franuka icon pack ships its own terms and is
already credited `required: true` for the CC BY 4.0 link its licence demands.

**`rpgultimate.zip` — confirmed blocked.** `AUDIT_0_9_3` recorded it as the one
pack in the whole library shipping no terms file. Re-checked exhaustively here,
not by spot check: every file in the archive was listed, and it contains

```
579 .png   5 .aseprite   5 .DS_Store   1 __MACOSX
590 files total, of which ZERO are a licence, terms, readme, or link
```

Six folders (Bows & Arrows, Environment & Nature, GUI, Loot & Props, Staves,
Swords) and nothing else. The 579-file count matches the audit's exactly, so
this is the same archive it examined. Nothing has changed, and **AF-R-1001
still blocks all 579 files** — locating the terms remains a task only you can
do, from wherever the pack was bought.

**`Free__Raven_Fantasy_Icons.zip` — the audit's reading is correct.** Its only
non-image file is `Special Note to the Dev.txt`, and the audit calls it *"a
thank-you note from the artist, not a licence"*. Read in full, that is exactly
what it is: a greeting from Caio of Clockwork Raven Studios thanking the buyer,
asking for a store review, and linking a Patreon. It states no grant, no
restriction, and no attribution requirement.

So its 6,580 PNGs are in the same position as RPG Ultimate: **terms exist only
on the itch page**, and AF-R-1001 wants them on the asset. The pack is
undeclared and credited to nothing, which is consistent — the 0.9.3 audit lists
Raven Fantasy Icons among the packs "measured and used by nothing", and it still
is.

## Atlas integrity, re-run properly

`tools/atlas-report.py` parses the `RECTS` table and decodes the embedded atlas:

```
rects            730
declared atlas   512x2764
packed extent    512x2764
zero-sized       0
out of bounds    0
duplicate coords 0
```

177 of those 730 rects are enemy battle frames: revenant 29, boss 27, husk 23,
knight 23, vermin 23, beast 21, slime 31.
