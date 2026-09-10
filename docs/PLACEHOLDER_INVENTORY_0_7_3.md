# Aetherfall — what it takes to fill every placeholder

Measured against `aetherfall-0.7.3.html`, not recalled. Counts come from
`AF.text.placeholders()`, `AF.assets.todo()` and `AF.battle.todo()`.

**Short version:** 134 placeholder text ids, and **118 of them are mechanical
naming I can draft for you in one pass.** The genuine bottleneck is about
**nine decisions**, most of them canon, plus **art files I cannot see from
here**.

---

## 1. Text — 134 ids

| Owner | Count | Who unblocks it |
|---|---|---|
| Items | 57 | I draft, you approve |
| Abilities | 31 | I draft, you approve |
| Enemies | 18 | I draft, you approve |
| Statuses | 12 | I draft, you approve |
| Regions | 5 | **you** — canon |
| Party members | 4 | **you** — canon |
| Bosses | 2 | **you** — canon |
| Shops | 2 | I draft, you approve |
| Authored fight (`barrow_gate_ambush`) | 1 | I draft |
| Guildmaster's line | 2 | **you** — canon |

### The 118 I can draft

Every one already has real mechanics behind it. `salve_lesser` has a heal
value; `rend` has power 14, physical, and applies `bleed` for 4 turns at 65%;
`dust_crawler` has stats, drops and an AI gambit list. **A name that follows
declared function is a proposal, not invented canon** — you get a table of 118
suggestions with the numbers beside each one, and you strike or rewrite
whatever misses.

What I need from you: **one sentence of tone.** "Plain and grim" gives
different names than "folkloric" or "clinical/alchemical". That single answer
shapes all 118.

Under AF-R-203 they stay marked `[placeholder]` until you approve them — my
draft does not become canon by being written down.

### The 16 that are actually yours

These carry meaning nothing else can supply:

1. **The forest's name** — PASS_PLAN open question 1, still open across five versions.
2. **What the forest is to Rowan's Hold** — affects every line of text later, nothing structural.
3. **The other four region names** — `barrow_downs`, `deep_barrow`, `ashen_reach`, and Rowan's Hold's own display name.
4. **Four party members** — `survivor_01`, `warden_02`, `kindler_03`, `mender_04`. The protagonist is currently called Survivor.
5. **Two bosses** — `custodian_of_the_seal`, `the_hollow_dragon`.
6. **The Guildmaster's name and his one line** — the oldest placeholder in the build.

---

## 2. Art — and the one file I keep hitting

**I cannot see any art in this session.** The uploads were three files: the
build, `RULES_INDEX.md`, and `PASS_PLAN.pdf`. No packs. Every asset number in
your manifests was measured in an earlier session with the files present.

**So any art work needs you to upload the relevant pack first.** That is the
single biggest practical constraint on what I can do next.

| Placeholder | What it needs |
|---|---|
| Guild Hall interior floor | `x500.png`, which **does not exist in the pack** — confirmed against a fresh download, and now missing from the Mage Tower pack too. Either it turns up, or you authorise a cross-pack substitution from Medieval Interior (791281) under AF-R-303. **A decision, not a search.** |
| `barrow_downs` — all placeholder | A pack chosen for barrow ground and cairns, then uploaded and measured. Real map, honest picture, no art. |
| Battle screen — placeholder boxes | Blocked on **the battle draw scale decision** (below), not on art. The three enemy packs are fully measured already. |
| Party screen UI | Measured UI frame rects. The Franuka RPG UI Pack is already credited and in use; this is measurable work once the pack is here. |
| `sheet_master`, `sheet_rowans_world` | **Never becoming real.** These are the composed reference sheets, deliberately `verified:false` so diagnostics keeps reporting them. Bible §2 makes them art bible, not source. Not a gap to fill. |
| RPG Ultimate GUI (579 files) | **You** — locate the licence. Blocked at AF-R-1001 regardless of anything else. |

---

## 3. The one technical decision blocking the most

**The battle draw scale.** It blocks every enemy sprite declaration and sets
the atlas budget.

The problem is arithmetic, not taste. World art is 16px native drawn at
`WORLD_SCALE` 4. The enemy sprites are 64px and 128px native. `AF.render.blit`
refuses fractional scaling (AF-R-405), so the options are integer or nothing:

- 64px at 1× — same pixel density as the world, but small on a 540-wide screen.
- 64px at 2× — reads well; the enemy is drawn at twice the world's pixel size.
- 128px at 1× — four times finer detail than the world art; a deliberate
  break, like the book UI question in the manifest.

I can lay out the three with measured on-screen sizes and atlas costs. **The
choice is yours** because it decides what the game looks like, and it is the
kind of decision AF-R-802 wants recorded rather than drifted into.

---

## 4. Also undecided canon, from `AF.battle.todo()`

- **What defeat means.** The revive-at-1-HP-at-the-gate rule is a mechanical
  safety net, explicitly not a narrative decision.
- **Where the two bosses are fought.** Both are declared, phased and startable;
  no scene starts either.

---

## The order I would go in

1. **One sentence of tone**, and I draft all 118 names in a single pass. That
   is 88% of the placeholder count cleared in one exchange.
2. **The forest's name and what it is to the Hold** — unblocks writing, and it
   has been the open question for five versions.
3. **The battle draw scale** — unblocks all enemy art and the atlas budget.
4. **Upload the packs** you want used for barrow art and the party screen UI,
   and I measure and declare them.
5. **The Guild Hall floor call** — find `x500.png` or authorise the
   substitution. Either answer closes it; only silence keeps it open.

Nothing above needs a new engine feature. The placeholders are a content and
decision backlog, not a technical one — which is the good version of this
problem.
