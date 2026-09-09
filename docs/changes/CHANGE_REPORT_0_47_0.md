# Change report — 0.47.0

**Build** `Aetherfall 0.47.0 · rowans-hold · save v5`
**Self-test** 402 / 402 (one new), three runs, 0 boot faults, no page errors
**Size** 5,992,609 bytes (+3,914 — one deletion, one test)
**Branch** `claude/newest-build-nv7xsl`

**From five screenshots of the game being played on a phone.** The first
play-through this project has had.

---

## Wren's line ran outside its box

Reported in a screenshot: the first row of dialogue sat on the panel's top
border and the last row was drawn *below the frame entirely*.

Reproduced at the device's geometry on the first attempt, then measured:

| | |
|---|---|
| box height | `34 + rows × 24 + 18` = **124px** for three rows |
| `ui_panel_slate` corners | `16 × UI_SCALE` = **48px, top and bottom** |
| usable interior | **28px** |
| three rows need | **72px** |
| first row's baseline | `by + 30` — **inside the top border** |

So the box was 96 pixels of frame around 28 pixels of room.

## The real bug was that one box had two implementations

`AF.speech.draw` had already solved this. Its box is
`max(108, 62 + lines × 24 + 20)` — 154px for the same three rows — and its
text starts at `by + 62`, clear of the border. Its header still carries the
0.9.2 note explaining the clamped corners, the fix, and why the minimum is
108.

**It was never called.** A grep for `AF.speech.draw` finds one call site in
the whole build: a self-test. Rowan's Hold carried a second, older renderer
inside its own draw, and that is the one the player saw.

```js
if (!sc.drawsOwnSpeech) AF.speech.draw();      // every other scene
```

`rowans_hold` sets `drawsOwnSpeech: true` — for a real reason, it interleaves
the bubble with the resonance prompt — and in claiming the job it also
inherited a copy that never got the 0.9.2 fix. That is why **Garrick Vale's
line in the guild hall rendered correctly in the same set of screenshots** and
Wren's did not: the guild hall uses the shared renderer.

The fix is a deletion. The scene still chooses *when* to draw the bubble, so
the interleaving is preserved; it no longer decides *how*:

```js
} else if (AF.speech.current()) {
  AF.speech.draw(ctx);
}
```

Rowan's Hold also gains what its copy never had: the name plate art, the fade,
and the six-pixel rise on arrival.

## The test that existed, and why it did not help

There was already a test for this. It called `AF.speech.draw` — the correct
implementation, and the one no player ever reached. **A test can only defend
the code that runs.**

The new one drives `sc.draw()` — the scene's own path, exactly as the frame
loop calls it — and measures what reaches the canvas by spying on
`AF.render.nineSlice` and the stage context's `fillText`. It asserts the
property rather than the arithmetic: every text baseline lands inside the
panel's **interior**, past the corners, with the panel at least the 108px its
frame needs.

It also asserts the cause, not just the symptom: a scene may choose when to
draw the bubble; it may not measure and draw a second one of its own
(AF-R-801).

> Writing it reproduced the same mistake in miniature. The first version spied
> on a scratch canvas — but `sc.draw()` takes no argument and renders to the
> real stage context, so it recorded nothing and reported "0 rows reached the
> canvas". Testing a path the game does not take, one layer down.

**Revert-proof.** With the old copy restored:
`a row is drawn at 756, past the panel's bottom (774)`.

## Verification

- 402/402 × 3 runs, 0 boot faults, no page errors
- Wren's exact line re-screenshotted at 414×736: three rows inside the box,
  name plate above it
- Garrick Vale's line in the guild hall re-screenshotted: unchanged and
  correct, confirming the shared renderer was not disturbed

---

## Seen in the screenshots and deliberately not changed

**The diagnostic band.** Three lines bottom-left — `engine clean · no faults`,
the build id, `2 assets still unverified`. Its own comment says it is drawn on
the canvas *"because the whole point is that it shows up in a screenshot
without anyone having to go looking for it"*, and it just did exactly that: the
build and asset state are legible in the photographs. It is deliberate and it
earned its place. It is also three lines of engine text in a demo someone might
show another person, so it wants a switch — that is a small addition, not a
repair, and it is the user's call.

**The d-pad art.** At phone size the four direction buttons read as small
wooden chests sitting on the grass rather than as arrows, and they are the most
visually prominent thing on the screen. That is the art the pack supplies and
it works; whether it is *right* is a taste question, not a defect.

## Still true

- Nothing else in the five screenshots is broken. The HUD, the banner, the
  battle log, the two-column party strip, the encounter flow and the interior
  scenes all render as designed at the device's real geometry.
- Balance remains simulated, not played.
