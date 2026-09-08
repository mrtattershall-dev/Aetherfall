# Aetherfall

Single-file JRPG. Everything — engine, data, text, art — lives in `aetherfall.html`.
Open it in a browser; there is no build step, no server, no dependencies.

Current build: **0.34.0** · branch `rowans-hold` · save schema v4
(the build stamps itself — see module `00 · BUILD IDENTITY`).

## One file, one name

The file is always `aetherfall.html`. Versions are tracked by git history and by
`AF.build.version` inside the file, never by the filename. Divergent side-by-side
copies (`aetherfall_3.html` vs `aetherfall-3.html`) have caused real bugs before;
that is the cheapest bug to prevent.

## Finding your way around

The header comment carries the module map. Search for a banner to jump, e.g.
`07b · STATS`, `18 · BATTLE`, `20e · THE INN`.

Rule IDs of the form `AF-R-###` refer to `docs/RULES_INDEX.md` in the design bible.

## Authority order (Bible §0)

1. The user's newest explicit instruction
2. A rule marked LOCKED
3. Existing verified implementation / data / assets
4. A rule marked FLEXIBLE
5. A proposal clearly labelled PROPOSED
6. Otherwise: leave undefined, or ask. Do not fabricate.

## Diagnostics

The game catches its own faults (`AF.fault`) and collects rule violations rather
than throwing them away — open the in-game diagnostics panel instead of hunting
for a console, which iOS does not give you.
