# Asset verification — five packs against the 0.34.0 atlas

Run with the source archives present, which is the only way this check runs at
all. `AUDIT_0_9_3` records the same check for the 88 Franuka icons and says why
it can never become a self-test: it needs the packs, and the build does not ship
them. This is that check, applied to the enemy sprites.

Method: decode the atlas out of `aetherfall.html`, crop each declared
`enemy_*` rect, and compare it pixel-for-pixel against the source sheet named in
the asset's own `source` string — row 0 (front), trimmed to the alpha bounding
box, exactly as `AF.enemyArt` says it cut them.

---

## Result

| Pack | Declared as | Frames | Verdict |
|---|---|---|---|
| Giant Rat — 4 Direction (craftpix 415491) | `craftpix_rats` | 23 | **23/23 byte-exact** |
| Pixel Art Slime Enemies (craftpix 743043) | — | — | **not the pack in the build** |
| Free Top-Down Orc (craftpix 363992) | — | — | new, undeclared |
| Free Top-Down Trees (craftpix 385863) | — | — | new, undeclared |
| Top-Down Cute Farm Animals (craftpix 213727) | — | — | ambiguous, see below |

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

## Licences — all five clear AF-R-1001

All five ship `License.txt` carrying the standard CraftPix file-licence link
(`https://craftpix.net/file-licenses/`) and no extra credit text — the same
terms the build already records for its twelve other CraftPix packs, `required:
false`. None is blocked the way `rpg-ultimate.zip` is.

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
