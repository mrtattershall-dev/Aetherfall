# Asset verification — twenty-one packs against the 0.34.0 atlas

Run with the source archives present, which is the only way this check runs at
all. `AUDIT_0_9_3` records the same check for the 88 Franuka icons and says why
it can never become a self-test: it needs the packs, and the build does not ship
them. This is that check, applied to the enemy sprites and the barrow ground.

Method: decode the atlas out of `aetherfall.html`, crop each declared rect, and
compare it pixel-for-pixel against the source the asset's own `source` string
names — row 0 (front) of the named state sheet for enemies, the named 16px cell
index for ground tiles, the numbered individual file for icons.

**364 of 364 rects that could be checked are byte-exact.** Two packs cannot be
used at all until their terms are found.

| Family of check | Rects | Result |
|---|---|---|
| Enemy sprites (beast, boss, vermin, slime, revenant) | 131 | **131/131** |
| Franuka icons (57 items + 31 abilities) | 88 | **88/88** |
| Guild Hall character walks | 72 | **72/72** |
| Barrow ground set | 54 | **54/54** |
| Franuka UI | 19 | **19/19** |

---

## Result

| Pack | Declared as | Checked | Verdict |
|---|---|---|---|
| Fantasy RPG Icon Pack (Franuka) | `franuka_icons` | 88 icons | **88/88 byte-exact** |
| RPG UI Pack (Franuka) | `franuka_ui` | 19 rects | **19/19 located byte-exact** |
| Free Slime Mobs (craftpix 788364) | `craftpix_slimes` | 31 frames | **31/31 byte-exact** |
| Guild Hall Asset Pack (craftpix 189780) | `craftpix_guild` | 72 rects | **72/72 byte-exact** |
| Top-Down Pixel Ghost (craftpix 894297) | `craftpix_ghost` | 29 frames | **29/29 byte-exact** |
| Free Undead Tileset (craftpix 695666) | `craftpix_undead` | 54 rects | **54/54 byte-exact** |
| Top-Down Pixel Ent (craftpix 838021) | `craftpix_ent` | 48 frames | **48/48 byte-exact** |
| Giant Rat — 4 Direction (craftpix 415491) | `craftpix_rats` | 23 frames | **23/23 byte-exact** |
| Free Chapel (craftpix 477438) | *removed 0.19.0* | — | correctly gone, see below |
| Predator Plant Mobs (craftpix 284465) | — | — | new, undeclared — drop-in shaped |
| Pixel Art Slime Enemies (craftpix 743043) | — | — | **not the pack in the build** |
| RPG Ultimate GUI | — | — | **no licence of any kind — still blocked** |
| Free Raven Fantasy Icons | — | — | **no licence in the archive** |
| Mage Tower (craftpix 289481) | — | — | undeclared; settles x500, see below |
| Slime Monsters (craftpix 510319) | — | — | a **third** distinct slime pack |
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

### `x500.png` — the missing file was never missing, and the pack proves it

`PLACEHOLDER_INVENTORY` lists this as decision 5: *"find `x500.png` or authorise
the substitution. Either answer closes it; only silence keeps it open."* Neither
happened. **0.7.4 closed it a third way, by reading the pack's own layer data**,
and with the Guild Hall and Mage Tower archives both present that reading can be
checked:

```
x500.png present in either archive         no
x500 declared in Interior_1st_floor.tmx    YES — firstgid 1, 368 tiles,
                                           image "../../x500.png"
tiles actually using gids 1-368            0     (1st floor AND 2nd floor)
```

So the tileset is declared, points two directories above the pack root — a leak
from the artist's own project tree — and **no tile on either floor references
it**. The floor is built from `Walls_interior.png`, and the build's structural
claim about it is exactly right: the cells used are local ids 138/139/140,
162/163/164, 186/187 — a 3×3 autotile block at **cols 18-20, rows 5-7**, with
only the bottom-right corner unused.

Five versions of documents recorded a missing-file defect for a file the map
never asked for. The build's own note is the lesson worth keeping: *"a pack's own
.tmx layer data is source, read it before concluding something is not there."*

Two incidental counts in that note are slightly off — it says the Floor layer has
190 cells and its centre tile is used 153 times; the file gives **188 cells** and
**151**. Both off by two, both cosmetic: the diagnosis and the tile block are
correct, and nothing derives from the counts.

### `craftpix_guild` — 72/72, and its mirror argument holds

Three character sheets, each 192×128 = 6 frames × 4 rows at 32×32, taken as
whole untrimmed cells:

```
Citizen1_Walk.png   24 rects   Citizen2_Walk.png  24 rects
Fighter2_Walk.png   24 rects                      72/72 byte-exact
```

The row order (down, left, right, up) is confirmed for all three. The build does
not assume that order for Citizen2 — AF-R-923 forbids it — and instead argues it
from measurement, including that *"rows 1 and 2 are a pixel-exact horizontal
mirror of each other"*. Checked frame by frame: **6/6 mirror exactly.**

### `craftpix_ghost` — 29/29, and the trim rule predicts it

```
Ghost1 Idle    4 frames    union bbox
Ghost1 Attack 12 frames    union bbox
Ghost1 Hurt    4 frames    union bbox
Ghost1 Death   9 frames    per-frame bbox
                           29/29 byte-exact
```

`revenant` was declared at 0.10.0, and it follows the 0.10.0 rule exactly —
union for the looping states, per-frame for death. That rule was derived from
the ent pack and has now predicted a pack it was not derived from.

### Three slime packs, one right answer

The library now holds **three distinct CraftPix slime products**, all shipping
the identical `Slime1/Slime2/Slime3` × `With_shadow`/`Without_shadow` folder
shape, all at cell 64:

| Product | In the build |
|---|---|
| 788364 Free Slime Mobs | **yes** — `craftpix_slimes`, 31/31 verified |
| 743043 Pixel Art Slime Enemies | no |
| 510319 Slime Monsters | no |

Frame counts are the cheapest discriminator: 788364's Slime1 death is 10 frames,
510319's is 8. Nothing in a folder listing distinguishes them, which is why the
near-miss below is kept.

### `craftpix_slimes` — 31/31, and the earlier finding resolves

The **"Free Slime Mobs — Pixel Art Top Down Sprite Pack" (craftpix 788364)** was
supplied after the finding below, and it verifies completely:

```
Slime1 Idle     6 frames   sheet 384x256
Slime1 Attack  10 frames   sheet 640x256
Slime1 Hurt     5 frames   sheet 320x256
Slime1 Death   10 frames   sheet 640x256
                           31/31 byte-exact, per-frame trim throughout
```

Per-frame everywhere, as expected for a family declared at 0.25.0. The build's
ledger named the right pack all along — the earlier archive was simply a
different product with a confusingly similar name. **The finding below is
closed, and is kept because the near-miss is the point: two CraftPix slime packs
ship the same `Slime1/2/3` folder shape, and only a pixel check tells them
apart.**

### `franuka_ui` — 19/19, and the build's own claims reproduce

The UI rects carry their provenance in prose rather than an index table, so each
was located by searching the full pack: for all 19 `ui_*` rects, every one of the
631 files under `Individual files/1x/` was scanned for a byte-exact occurrence.

```
franuka_ui: 19/19 rects located byte-exact inside a full-pack file
```

All three offsets the build asserts at 0.7.8 land exactly where it says:

| Claimed | Found |
|---|---|
| `ui_panel` = BGbox_01A at 6,6 | BGbox_01A.png at 6,6 |
| `ui_barframe` = Slider02_Box at 0,3 | Slider02_Box.png at 0,3 |
| `ui_banner` = BannerSmall_01A at 0,2 | BannerSmall_01A.png at 0,2 |

The archive is also the full pack the comment claims, not the four-file demo:
`Individual files/` at 1x, 2x and 3x, plus `Examples/`, `Fonts/`, a reference
sheet and three composed sheets.

Two cuts are worth writing down because nothing else records them: **`ui_bar_red`
is `Button_02A_Normal.png` at 4,10** — a button, not a slider — and
**`ui_cur_right` is `Checkbox_01A_On.png` at 3,3**. Both are byte-exact, so they
are deliberate reuse rather than mistakes, but neither is where you would look.
`ui_slot_focus` is likewise `Slot_01_Necklace`.

### The chapel is fully gone — the 0.9.3 dead-weight finding is closed

`AUDIT_0_9_3` measured `bld_chapel` at 20,193 pixels, "87% of all dead weight",
and deferred removal to the next atlas pass. That pass was 0.19.0. The rect is
gone, `craftpix_chapel` is out of the credit ledger, and the only trace left in
the build is the comment recording why:

> 0.19.0 — craftpix_chapel removed. AF-C-003 took the chapel out of the world in
> 0.6.21 and its building art stayed in the atlas for thirteen versions, 20,193
> dead pixels, with its pack credited for art nobody could see.

The supplied chapel archive therefore has nothing to verify against, which is
the correct outcome. The credit ledger is "every pack with art on screen" again.

### Predator Plant Mobs — drop-in shaped, with one caveat

Same structure as the golem and gnoll packs: `PNG/Plant1..3/Without_shadow/`,
four direction rows, Idle / Attack / Hurt / Death present, cell **64**.

```
Plant1  idle 4, hurt 5, death 10, run 8, walk 6   — all clean at 64
Plant1  attack 448x256                            — content crosses the cell boundary
```

The attack sheet divides evenly at 64 (7×4) but its content does not stay inside
the cells, the same trap the orc attack sheets have. Slicing it on a flat grid
clips the lunge; it needs measuring per frame.

### THE EARLIER FINDING — the first slime pack was a different product

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
ledger names the pack it actually used. **Confirmed by the section above: the
real "Free Slime Mobs" pack verifies 31/31.**

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

## Licences — nineteen clear AF-R-1001, two do not

The seventeen CraftPix archives each ship `License.txt` (or `license.txt`) carrying
the standard file-licence link (`https://craftpix.net/file-licenses/`) and no extra credit
text — the same terms the build already records for its twelve other CraftPix
packs, `required: false`. Both Franuka packs ship their own terms
(`License and details.txt` in the UI pack) and are credited `required: true`
for the links their licences demand.

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
