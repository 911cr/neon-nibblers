# Power-up spawn/movement audit — 2026-11-08

## Evidence and limits
- CHOMPionship-specific distributor descriptions say powers appear randomly; BMI's CHOMPionship catalog explicitly says random times. This supports irregular random arrivals, not the current exactly-three-second cadence.
- CHOMPionship-specific secondary references describe power-ups bouncing around the maze, similar to Ms. Pac-Man. This supports visible hopping/roaming. It does NOT establish exact speed, turning probability, entry portal, lifetime, or whether gold/green orbs are exceptions.
- No examined CHOMPionship source specifies a complete placement table, per-type weights, exact spawn interval, initial counts, or maximum concurrent powers.
- The 2022 DX manufacturer-authored operation manual (28 pages, BMI mirror read successfully) is predominantly installation/service/setup; it does not give those detailed spawn rules.
- Fruit refreshing dots/power pellets is explicitly documented in the ORIGINAL Battle Royale manual. Some reseller CHOMP listings reuse that paragraph, including predecessor round rules. Do not automatically import that rule into CHOMP or present it as verified.

## Current implementation audit
- New arena: four Crown orbs at corner cells; two Titan orbs nearest center-upper/lower anchors; three randomly chosen other categories at uniform random lane cells. None of these exact counts/positions is established by the sources above.
- Every3seconds adds one random type, up to12 total. Uniform category selection, interval3, cap12 are custom.
- Non-orbs roam one logical tile every0.24seconds, preferring existing heading with80% probability. Crown/Titan stay fixed. These exact parameters and orb exception are custom/unverified.
- New random powers avoid current players and existing powers; gates are excluded through arena.lanes. Good implementation invariant, but not proof of commercial placement.
- item_clock and item_walk_clock are not reset inside new_arena; stage carryover can cause an immediate arrival/move after transition. Reset both for a predictable configurable policy.

## Recommended implementation policy
Make a small public rules/config object that explicitly labels spawn settings as adaptation tuning, e.g. initial_orbs, initial_roaming_count, interval_min/max, max_items, weights, roam_step_seconds, persist_direction_chance. Use reproducible seeded random intervals instead of a fixed metronome to match the supported random-timing description; a2–5second range is an illustrative custom default, NOT a recovered original value. Keep all placement inside validated corridors; exclude bays/house and occupied cells. Reset clocks on stage change. Add tests for range/cap/placement/seed reproducibility and all11 eligibility. Do not fabricate fruit/dot triggers or exact commercial spawn tables. Existing stage-on-dot-clear remains custom until independently observed.

For visuals, give roaming items an obvious downward shadow and rising/falling bob synchronized with travel; current tiny sinusoidal vertical bob is a weak approximation of a hop. Avoid claiming all categories roam until the two orb exceptions are observed.

## Sources
- CHOMP-specific distributor random appearance description: https://primetimeamusements.com/product/pac-man-battle-royale-chompionship/ (search-index content accessible; direct page403)
- CHOMP-specific BMI catalog random-times wording: https://worldwide.bmigaming.com/games-catalog-namco-mp.htm (search-index content accessible)
- CHOMP-specific movement summary: https://www.mobygames.com/game/198053/pac-man-battle-royale-chompionship/
- Secondary CHOMP mechanics summary: https://pacman.fandom.com/wiki/Pac-Man_Battle_Royale_CHOMPionship
- Manufacturer-authored2022 DX manual, successful mirror: https://www.bmigaming.com/Games/Manuals/namco/Pac-Man-Battle-Royale-Chompionship-Deluxe-Video-Arcade-Game-Manual-Bandai-Namco.pdf
- Predecessor-only fruit/dot refresh rule (NOT CHOMP evidence): https://www.bandainamco-am.com/Ecommerce/Site/Content/PDFs/Pac-Man%20Battle%20Royale%20Manual.pdf

## QA1 — same-agent verification of fixes
Source inspected after root's implementation. SPAWN_INTERVAL=3.0 is explicitly marked custom/commercial cadence unpublished; MAX_ITEMS=12 and ITEM_STEP_INTERVAL=.24 are centralized. new_arena now resets BOTH spawn/movement clocks to0 and clears directions. Lane-only spawning still excludes current player cells and existing items. No unsupported claim of exact commercial location/frequency is justified. The optional suggestion of random intervals was not adopted: cadence remains deterministic3seconds, now truthfully labeled.

## QA2 — adversarial execution
Ran work/qa_powerup_spawns.py with local work/deps (pygame-ce2.5.8). PASS16 scenario groups:
- Four maps, pairs of same-seed180-second simulations: identical item dictionaries on every update; runtime count never exceeds12; all items stay on lanes, none in player gate cells.
- Four stage changes with clocks just below thresholds: both reset to0; tiny first update causes no immediate arrival or move.
- Each of11 named categories,100 direct spawns on each map: avoids eight occupied player cells, respects lane membership and requested category.
- Four dense roaming scenarios: count preserved, actual motion occurs, all placements remain in lanes.
Test fixture initially tried roaming after a completed match (updates correctly stopped); replaced with fresh active match and reran successfully. This was not a game failure.
Public spawn_item helper does not itself cap count; the production update caller guards MAX_ITEMS. Direct stress calls deliberately exceeded cap to test placement. There is no current gameplay path found that exceeds cap, but encapsulating the cap in spawn_item would be defensive if new call sites are added.
Commercial exact cadence, spawn weights/anchors, and orb exceptions remain unknown; software tests cannot certify those.

## Additional timestamped footage inspection
Reference: JurassicVerse64, https://www.youtube.com/watch?v=GhSV1oQVA6g&t=95s . Viewed actual video through native Chrome because IAB was unavailable. This video's title says CHOMPionship Gameplay; cabinet/version identity beyond that title is not independently established as DX, so treat it as CHOMP visual evidence, not a certified DX rule table.

Observed sample: one short sequence around1:35–1:41, plus a paused1:40 frame. Camera is oblique and shifts, and reflections obscure upper center; not a full spawn census.
- Around1:35, a clearly recognizable yellow peel collectible is in the right-side interior corridor below the upper-right stack of short horizontal wall bars. In the1:40 frame it is farther up that right-side corridor, near the upper bars. This is direct visual evidence of collectible translation through the maze, not merely a stationary bob.
- At1:40, a yellow round collectible is visible on the LEFT interior horizontal lane below the upper-left U-shaped wall; another greenish round collectible is on a RIGHT interior lane. Neither is a screen corner. This refutes treating four screen-corner gold anchors as an established universal placement rule; it does not prove where they initially spawned or whether these orb sprites moved there.
- Multiple distinct collectible silhouettes can coexist. I could not reliably isolate a first-appearance frame from collection, movement or reflection, so no measured inter-spawn interval or complete event count is reported. No supported claim of an exact3-second interval follows from this small sample.
- Near1:41, a pale/sheet-like trail and bright starburst appear in the right corridor, but cause and affected player cannot be identified confidently from this sample; do not use it as an effects proof.

Practical consequence: current roaming behavior is directionally supported; current fixed corner layout is an adaptation choice, not a reproduced observed layout. Exact initial/map-dependent positions, distribution, cadence and persistence require additional clean continuous footage. Native browser window5771396 was handed to gate agent after inspection; no commercial media was downloaded or bundled.
