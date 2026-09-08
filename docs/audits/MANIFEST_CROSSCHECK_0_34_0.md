# Cross-check — `ASSET_MANIFEST.md` against the archives

The manifest opens by saying every dimension in it "was read off the actual file
with an image library", and that this is "the only kind of asset fact this
project records (AF-R-1001)". With all 43 archives unpacked, that claim is
checkable. It holds.

## Pack inventory — 22 of 23 rows exact

Every PNG count in the manifest's inventory table reproduces exactly:

| Pack | Manifest | Measured |
|---|---|---|
| Free Undead Tileset | 262 | **262** |
| Free Chapel | 240 | **240** |
| Free Guild Hall | 101 | **101** |
| Free Glassblower's Workshop | 46 | **46** |
| Free Path and Road | 17 | **17** |
| Free 2D Top-Down Dungeon | 23 | **23** |
| Herbalist's Hut | 18 | **18** |
| Top-Down Dungeon (RPG/Roguelike) | 38 | **38** |
| Tavern | 34 | **34** |
| Farm with Animals | 40 | **40** |
| Fishing Village | 94 | **94** |
| Green Forest | 9 | **9** |
| Green Village | 12 | **12** |
| Green Dungeon | 13 | **13** |
| Farmlands | 38 | **38** |
| Medieval Interior | 14 | **14** |
| Miner's Cave | 13 | **13** |
| Adventure Fantasy Book | 42 | **42** |
| Fantasy RPG Characters — Franuka | 39 | **39** |
| HP/Mana/Stamina & Scroll Bars | 3 | **3** |
| RPG Ultimate (GUI + props) | 579 | **579** |
| RPG UI Elements (149019) | 0 | **0** |

Twenty-two rows, twenty-two exact matches. For a document that has not been
re-measured in roughly twenty-five versions, that is the manifest doing its job.

## The one row that is stale

| Pack | Manifest | Measured |
|---|---|---|
| RPG UI Pack — Franuka | **4** (marked "Demo") | **1,906** |

The build already knows this and says so at 0.7.8:

> this is the FULL pack, not the demo. Verified by locating every shipped `ui_*`
> rect as a byte-exact match inside a full-pack file (ui_panel = BGbox_01A at
> 6,6; ui_barframe = Slider02_Box at 0,3; ui_banner = BannerSmall_01A at 0,2).
> The demo was a four-file sampler cut from the same art.

Independently confirmed here — all three offsets reproduce, and all 19 `ui_*`
rects were located inside full-pack files (`ASSET_VERIFY_0_34_0.md`). So the
correction was made in the build and never carried back to the manifest. Same
shape as the twelve adopted-but-never-added rules the 0.7.0 addendum describes:
**the decision was recorded in one place and the row was never updated in the
other.**

## Claims that also hold

- **"RPG UI Elements ships three .psd files and no PNG."** Exact: 5 files, 3 of
  them `.psd`, zero PNG at any size.
- **"RPG Ultimate … no licence file in archive."** Exhaustively re-checked: 590
  files, 579 PNG, and zero licence, terms, readme or link of any kind.
- **Adventure Fantasy Book grids** — `Open_book.png` and `Close_book.png` at
  1088×816, `Turning_pages_*` at 1088×1088, all present as described.

## Claims now overtaken by the build

- **"Current shipped atlas 512×450, ~77 KB."** It is now **512×2764, 730 rects**.
  The atlas budget table is a planning document from before the region fills
  landed; its arithmetic is not wrong, its baseline is just old.
- **"`grass_field` declared w:0, h:0, verified:false."** The ground gap it
  describes as "now closed" is indeed closed — `ground_grass` verifies against
  `Ground_grass.png` (`ASSET_VERIFY_0_34_0.md`).
- **"Character directional row order — unknown — AF-R-923 applies."** Still true
  of the Franuka character pack, which remains undeclared. But the rule has been
  satisfied by measurement four times since, for Citizen2, the slimes, the rats
  and the guild hall walks — including the pixel-exact mirror argument for
  Citizen2, which this audit confirmed 6/6.
