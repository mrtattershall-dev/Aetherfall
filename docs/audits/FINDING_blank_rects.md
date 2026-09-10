# Finding — three declared assets are entirely transparent

Found while verifying `craftpix_farm` against **Top-Down Farm with Animals
(craftpix 471853)** at 0.34.0. Not a documents problem: measured against the
atlas the build ships.

---

## What is wrong

Three atlas rects contain no pixels at all:

| Asset | Rect | Opaque pixels | Distinct RGBA |
|---|---|---|---|
| `trail_break_b` | `0,2104 16x16` | **0 / 256** | 1 |
| `trail_chip_a` | `34,2104 16x16` | **0 / 256** | 1 |
| `trail_chip_b` | `51,2104 16x16` | **0 / 256** | 1 |

They are declared assets with `verified: true`, they have real rects inside the
atlas, and they draw nothing. For comparison, their siblings in the same lists
carry 21–216 opaque pixels each.

## What it costs on screen

All three are reached by real draw calls, so this is visible absence, not dead
weight.

**1. Rowan's Hold — one tile that never draws.** In `AF.demo`'s ground pass:

```js
if (ty === 24) AF.render.blit(img, AF.atlas.rect("trail_chip_a"), sx, sy, T, T);
```

Unconditional, no probability gate, one specific tile at `tx = 9, ty = 24`. It
paints nothing, every frame, forever. The 0.13.5 comment above it states the
intent plainly:

> The forest then carries broken Farm-road fragments for several rows before
> settling into dirt. Geography now reads continuously.

**2. The forest route — one third and two thirds of a scatter missing.** In
`AF.forestRoute.drawGround`:

```js
const band = (ty <= 3) ? TRAIL_BREAK : TRAIL_CHIP;
if ((h % 100) < (ty <= 3 ? 38 : 28)) AF.render.blit(img, R(band[h % band.length]), sx, sy, T, T);
```

The list index is `h % 3`, so each entry is picked about equally often:

| Band | Rows | Blank entries | Effect |
|---|---|---|---|
| `TRAIL_BREAK` | ty ≤ 3 | 1 of 3 | ~⅓ of selected tiles draw nothing |
| `TRAIL_CHIP` | ty 4–5 | **2 of 3** | ~⅔ of selected tiles draw nothing |

The density gate (`h % 100 < 38`) already controls how often a fragment
appears. A blank list entry is a second density control that no reader can see
and no comment mentions — which is the argument that these are mis-cuts rather
than a deliberate "sometimes nothing".

## Why nothing caught it

This is the exact class every audit since 0.6.19 has said it cannot reach:

> **Rendering is still only checked by execution, not by appearance.** The new
> guards prove a panel runs and draws the right number of rows. They cannot
> tell you an icon is 32px too high — that took a phone.
> — `AUDIT_0_9_3`, open finding 6

A blank rect executes perfectly. It is in bounds, non-zero-sized, uniquely
positioned, and declared with real provenance, so:

- the atlas integrity self-test passes (checks size, bounds, duplicates — not content);
- `AF-R-1001` passes (it has a measured rect);
- `AF-R-941` passes (its pack is credited and genuinely in use);
- every draw path "runs clean" against a recording context, because `blit` of an
  empty rect is a successful `drawImage`.

## Where the missing art probably is

`Road.png` in the Farm pack is 192×272 = 12×17 cells at 16px. `trail_chip_c` was
located byte-exact at **x=160, y=240**, and that row holds exactly three small
chip-sized cells:

```
x=128 y=240   22 opaque px
x=144 y=240   19 opaque px
x=160 y=240   21 opaque px   <- trail_chip_c
```

Three cells, three `trail_chip_*` ids, and only the last one landed. **`chip_a`
and `chip_b` are almost certainly `128,240` and `144,240`.**

`trail_break_a` and `trail_break_c` are byte-exact at `32,16` and `32,32` of the
same file, and the x=32 column is broken-road cells all the way down (125–236
opaque px per cell), so `break_b` is somewhere in that column — but which cell
is a judgement call, not a measurement, so it is not asserted here.

## The guard this wants

A rect that draws nothing is cheap to detect and needs no source archives, so
unlike the icon-integrity check this one **can** be a self-test:

```
no declared asset's srcRect is fully transparent
```

That is one pass over the atlas at boot, in the spirit of AF-R-1006: a thing
that cannot be seen should be refused or labelled, never silently drawn. It
would have caught all three the version they were cut, and it closes a sliver of
the appearance gap that has been open since 0.6.19 — not the whole gap, but the
part a machine can see.

Changing the rects themselves means a repack and re-encode, and picking
`break_b`'s cell is a decision (AF-R-1007 territory), so **this is recorded,
not fixed.**
