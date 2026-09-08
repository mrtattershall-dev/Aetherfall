# Aetherfall — Asset Manifest (measured, not guessed)

Every dimension below was read off the actual file with an image library. That is the only kind
of asset fact this project records (AF-R-1001).

Supersedes the 0.6.0 manifest, which described eighteen composed presentation sheets. Those
sheets are still listed at the end, still unsliceable, and are now reference only. The project
has real production tilesets.

## The finding that matters most

**Every owned pack has a 16px-native path.** Source art at 16px drawn at `WORLD_SCALE` 4 gives
the 64px world tile (AF-R-311) at integer scale, so `AF.render.blit` never has to refuse
(AF-R-405).

Two families, both usable:

| Family | How it ships | Native check |
|---|---|---|
| CraftPix *Tiled_files* | `.tmx` declares `tilewidth="16" tileheight="16"` | pixel block 1 — genuinely 16px |
| CraftPix *All Tileset* | folder of `16x16 / 32x32 / 48x48 / 64x64` variants | the 16px variant is the native master |

The RPG Maker MV folders inside the *All Tileset* packs are 48px because RPG Maker requires 48.
Those are 16px art upscaled 3×. Verified on `RF_Green Forest_A5.png`: downsampling by 3 and
re-upscaling reproduces the file byte for byte. Do not slice the 48px files — use the 16px
variant, or downsample by exactly 3.

## Ground — the gap that is now closed

`grass_field` has been declared `w:0, h:0, verified:false` since 0.6.0, with a self-test that
fails if anything claims otherwise. Two candidate replacements were measured.

| Source | Fill cell | Colour | Opaque | Seam (V / H) |
|---|---|---|---|---|
| Herbalist's Hut `Ground_grass.png` | (1,1) and (1,11) | `#7AAD55` flat, 1 colour | yes | 0.00 / 0.00 |
| Herbalist's Hut `Ground_grass.png` | (1,5) dirt | `#967E5D` flat, 1 colour | yes | 0.00 / 0.00 |
| Farm `ground_grass_bricks.png` | (1,17) | `#6EA24B` + dither, 3 colours | yes | textured |
| Green Forest `A5` (downsampled) | (1,0) tufted | textured | yes | edge columns identical |

**Herbalist fill tiles are a single flat colour.** They are seamless because they are flat. The
detail in that pack's ground comes from a separate scatter layer, which is how autotile sets are
built. `Ground_grass_details.png` (Farm pack, 21×14 cells, 277 filled) is that scatter layer:
pebbles, dirt specks and grass tufts on transparency.

**The two greens do not match** — `#7AAD55` vs `#6EA24B`. Under AF-R-303 (biome palettes
FLEXIBLE) this is a region distinction, not a defect. See the region binding below.

## Region binding (FLEXIBLE, AF-R-303 / Bible §3.1)

| Region | Packs |
|---|---|
| Rowan's Hold | Guild Hall, Glassblower, Chapel, Path & Road, Tavern, Undead |
| Forest / route | Herbalist's Hut (`Ground_grass`, `Trees_rocks`), Farm (`Ground_grass_details`) |
| Farmland | Farm (grass/bricks, plants, fences, animals, houses) |
| Coast | Fishing Village (docks, boats, water, NPCs) |
| Dungeon | Dungeon Tileset for RPG and Roguelike |

## Atlas budget (measured, PNG optimised, base64 ≈ ×1.33)

| Set | Packed size | PNG | base64 |
|---|---|---|---|
| **Current shipped atlas** | 512×450 | ~77 KB | **101 KB** |
| Forest fill: ground + scatter + trees + rocks | 336×784 | 63 KB | 83 KB |
| Farmland fill: grass/bricks + scatter + plants | 512×784 | 83 KB | 110 KB |
| Tavern NPC animations (25 sheets) | 640×3792 | 152 KB | 202 KB |

A complete region *fill* set costs less than the atlas already shipping. Buildings and animated
NPCs cost multiples of it. Fill tilesets therefore ride in the single embedded atlas; heavy
per-location art is deferred until a map needs it. No per-region atlas loader is required yet.

## Character animation — the battle blocker has a route through it

`Fantasy_RPG_character_pack` (Franuka) ships a real frame grid, and its own licence file states
the frame size rather than a caption inside artwork.

- 9 characters × `_idle` + `_walk` = 18 sheets, 1× and 2× variants
- Each sheet 64×96 = **4 columns × 4 rows at 16×24**
- Every one of the 16 cells is populated (verified per cell, bounding boxes 12–16 wide, 15–21 tall)
- A full spritesheet at 640×192 = 40×8 frames

Four rows and four columns is consistent with 4 directions × 4 frames, but **which row is which
direction is still unverified**. AF-R-923 forbids claiming a four-direction walk cycle without
inspecting it. Measure the row order before writing `byDirection`.

## Pack inventory (measured)

| Pack | PNGs | Grid | Native | Licence |
|---|---|---|---|---|
| Free Undead Tileset | 262 | tmx 16 | 1 | CraftPix file licence |
| Free Chapel | 240 | tmx 16 | 1 | CraftPix file licence |
| Free Guild Hall | 101 | tmx 16 | 1 | CraftPix file licence |
| Free Glassblower's Workshop | 46 | tmx 16 | 1 | CraftPix file licence |
| Free Path and Road | 17 | tmx 16 | 1 | CraftPix file licence |
| Free 2D Top-Down Dungeon | 23 | tmx 16 | 1 | CraftPix file licence |
| Herbalist's Hut | 18 | tmx 16 | 1 | CraftPix file licence |
| Top-Down Dungeon (RPG/Roguelike) | 38 | tmx 16 | 1 | CraftPix file licence |
| Tavern | 34 | tmx 16 | 1 | CraftPix file licence |
| Farm with Animals | 40 | tmx 16 | 1 | CraftPix file licence |
| Fishing Village | 94 | tmx 16 | 1 | CraftPix file licence |
| Green Forest | 9 | All Tileset | 16px variant | CraftPix file licence |
| Green Village | 12 | All Tileset | 16px variant | CraftPix file licence |
| Green Dungeon | 13 | All Tileset | 16px variant | CraftPix file licence |
| Farmlands | 38 | All Tileset | 16px variant | CraftPix file licence |
| Medieval Interior | 14 | All Tileset | 16px variant | CraftPix file licence |
| Miner's Cave | 13 | All Tileset | 16px variant | CraftPix file licence |
| Adventure Fantasy Book | 42 | see below | 1 | CraftPix file licence |
| RPG UI Pack (Demo) — Franuka | 4 | 16px grid, 1×/2×/3× | 1 | **Credit link required** |
| Fantasy RPG Characters — Franuka | 39 | 16×24 frames | 1 | **CC BY 4.0 — credit required** |
| HP/Mana/Stamina & Scroll Bars | 3 | packed, irregular | 1 | CraftPix file licence |
| RPG Ultimate (GUI + props) | 579 | — | 1 | **UNVERIFIED — no licence file in archive** |
| RPG UI Elements (149019) | 0 | — | — | vector PSD only — see below |

### Two packs that do not fit

**RPG UI Elements (149019)** ships three `.psd` files and no PNG. Its own description says it is
built from vectors and Layer Styles. Not pixel art. Excluded on AF-R-301 / Bible §17 grounds,
independently of the export problem.

**RPG Ultimate GUI** is 74 icons at 128×128 plus a 9472×128 strip (74 × 128 = 9472, so the strip
is the 74 in one row). All drawn at native 128 detail, pixel block 1 — four times finer than the
world art. There is no integer path from 128 to the 48px UI scale, so `AF.render.blit` would
refuse it (AF-R-405). Usable only inside item slots where finer detail is acceptable, and even
then the licence is unverified. **Do not declare any RPG Ultimate asset until the licence is
located.**

### Adventure Fantasy Book — measured grids

| Sheet | Size | Grid | Filled |
|---|---|---|---|
| `Open_book.png` | 1088×816 | 4×3 of 272×272 | 12/12 |
| `Close_book.png` | 1088×816 | 4×3 of 272×272 | 12/12 |
| `Turning_pages_left.png` | 1088×1088 | 4×4 of 272×272 | 15/16 |
| `Turning_pages_right.png` | 1088×1088 | 4×4 of 272×272 | 15/16 |

Those four are clean, verifiable animations. The icon sheets in the same pack are **not** grids —
`Icons_equipment.png` has a consistent 48px row pitch but irregular column gutters (28, 60, 159,
187, 220). Each icon needs its own measured rect.

Book art is native 272px detail. Using it means UI at a finer pixel density than the world. That
is a FLEXIBLE choice under AF-R-802 and must be recorded if taken, not drifted into.

## Verification status

| Field | Status |
|---|---|
| File dimensions | **verified** — measured |
| Colour mode / native pixel block | **verified** — measured |
| Tile grid, Tiled_files packs | **verified** — declared in `.tmx` and confirmed |
| Ground fill tiles, seam and opacity | **verified** — measured |
| Character frame cell size (16×24) | **verified** — measured, all cells populated |
| Character directional row order | **unknown** — AF-R-923 applies |
| Frame order and timing | **unknown** |
| Sprite bounding boxes, per prop | **partly measured** — forest props done, rest outstanding |
| Collision boxes | **unknown** — authored separately by design (AF-R-331) |
| Anchor points | **unknown** |
| RPG Ultimate licence | **unknown** — blocks use |

## The original eighteen sheets

Still present, still not production atlases: composed presentation sheets and gameplay mockups
with irregular offsets, non-uniform sizes, baked drop shadows, glow bleed and label text. Sheet
dimensions do not divide into 64 except by coincidence (1402×1122 is 21.9 × 17.5 cells). Two are
byte-identical duplicates. `IMG_0453.jpeg` is lossy and reference-only.

They remain declared in the build as `sheet_master` and `sheet_rowans_world` with
`verified:false`, so diagnostics keeps reporting the gap (AF-R-1002). Their role is what Bible §2
assigns: art bible, not source. Every name, stat block and label on them is non-canon (AF-R-201).

## What "production ready" still requires

```
id              stable snake_case, unique
src             file path or atlas
srcRect         {x, y, w, h} measured from the real file
pack            provenance — drives the credits screen, self-tested
placement       {w, h} in world pixels, multiple of 64 or 32
anchor          {x, y} — feet for actors
collision       [{x, y, w, h}] — authored, not derived
depthRule       'ysort' | 'ground' | 'overlay'
tags            []
verified        true only when srcRect was measured
```

Until `verified` is true the engine draws a labelled placeholder box in the asset's exact
placement footprint. Nothing looks finished that isn't (AF-R-1006).
