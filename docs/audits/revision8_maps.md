# Revision 8 map/station/render QA

2026-11-08; review of integrated revision-8 working code against revision-7 commit `0f9c3c9`. No physical devices or commercial cabinet used.

## Pass 1: map migration

Verified all four old/new lane sets, bays, entry coordinates, portals and ghost houses equal. Rendered all four old/new maze backgrounds with the existing art code and compared RGB bytes: **4/4 equal**. This proves the explicit database migration preserves geometry/art; it does not prove similarity to DX. Raw result: `work/revision8_map_render_qa.json`.

## Pass 2: integration and unusual rosters

`test_maps.py` now has seven passing tests. New integrated cases run counts 1, 2, 3, 4, 5, 6, 7 and 8 on every map for 180 moving simulation ticks and force a transition. The next map ID, time, lives, position membership and retained/nondecreasing score are checked. Every station 1–8 is also joined first on each map, creating the sparse eight-slot player list; after transition it remains the only joined identity, inactive slots retain zero lives/score, and rankings contain only that station. No map/station regression reproduced.

## Rendered observations

Generated genuine eight-second four-player gameplay (`gameplay_4_player.gif`, 96 rendered frames, seed 24). Inspected frames 0, 40 and 80: four colored players leave their gates, move through corridors, collect items and change size; ghosts depart the house. Scores at capture end: 675/415/555/900. This is seeded computer navigation through the game, not footage of humans or physical controls.

Generated and inspected `station_before_after_r8.png`: revision-7 lobby beside new lobby, P8 joining first, and eight-player ranking screen. The figure labels itself a **local baseline comparison, not a commercial reference**. The ranking panel uses assigned test scores and is labeled a controlled scene, not a completed match. Lobby controls and all eight results rows fit without clipping. P8 keeps the blue identity and proper station while other bays remain unused.

Reproduced bug: the new locator label/arrow above a player in a top bay was clipped (P8 first join, text above y=0). Root corrected it by moving the label below the ring near the top edge and clamping its horizontal position. Re-rendered P8-first screenshot visibly shows the P8 label inside the field. Added regression covering all eight station bays, all four themes, normal and giant radii (64 label cases): every label fits inside the playfield. All seven tests pass after correction. Unused station prompts were also brightened and the comparison recaptured. Real-cabinet viewing-distance readability remains untested.

## Scope of conclusion

Map loading and sparse-station transitions pass software checks. The migration intentionally preserves authored geometry, including remaining broad blocks/square islands and exact map progression uncertainties. No fresh unobstructed DX frame was acquired in this audit, and no reference match is claimed. Separate DX catalog/visual documents record that gap.
