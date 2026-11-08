# DX visual comparison record

Updated 2026-11-08. Keep original branding and independently authored art. A passing software test is not a visual parity verdict.

## Preserved baseline

Revision 7 is commit `0f9c3c9`. Baseline source tests passed 29/29 before changes. Existing 1/2/8-player clips, preview and arena sheet were preserved in `work/revision8-baseline`. These are actual rendered simulations; neither physical controller input nor commercial matching is implied. `map_catalog_v1.png` is a geometry/debug diagram, not gameplay.

## Reference checkpoints and meaningful differences

| Area | Reference / timestamp | Current implementation and difference | Status / next comparison |
|---|---|---|---|
| Wall structure | [Front-facing projector reference](https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s), 1:34 | Thin capsule/L/T outlines improved in revision 5, but broad hooked blocks and small square islands remain authored | **OBSERVED**, non-DX supporting view. Need a full confirmed DX frame before reconstructing topology. |
| Gates | [Released DX cabinet](https://www.youtube.com/watch?v=efLgejKG_ls&t=75s), 1:15 / 1:30 / 2:00 | Yellow hatches are now independent of wall palette. Exact gate dimensions, opening timing and animation remain approximations | Hatch color **OBSERVED DX**; operation **UNKNOWN**. Continuous same-station entry/death/respawn sequence needed. |
| Outer border | [Cabinet reference](https://www.youtube.com/watch?v=GhSV1oQVA6g&t=57s), 0:57 | Twin contours and tunnel necks exist; outer corners still relatively square, unlike softer shapes in earlier review | Observation inherited from prior audit; configuration uncertain. Align a perspective-corrected full board before tuning. |
| Characters | Same cabinet 0:57 and projector 1:34 | Procedural shaded bodies, animated wedge mouths, directional eyes. Giant overhang and original proportions are not measured | **IMPLEMENTED AND TESTED** / exact shape and timing **UNKNOWN**. Compare a multi-frame normal/giant sequence, not one still. |
| Ghost house | Projector 1:34 | Four visible occupants and continuous return implemented; initial coordinates/release order are authored | **UNKNOWN DX**. Confirm house-only clip through all four exits. |
| Scores/stations | [DX manufacturer manual](https://www.bmigaming.com/Games/Manuals/namco/Pac-Man-Battle-Royale-Chompionship-Deluxe-Video-Arcade-Game-Manual-Bandai-Namco.pdf), control-panel diagram | Station/color order follows documentation; on-screen score size, placement, animation and leaderboard are not measured | Station diagram **VERIFIED DX**; display dimensions **UNKNOWN**. Capture startup/play/results at comparable counts. |
| Startup | [Manufacturer DX parts](https://bandainamco-am.com/collections/pac-man-battle-royale-deluxe), eight Find My Pac/Start decals | Baseline is a count-selected text lobby; independent station actions were missing | Action existence **VERIFIED DX**; exact join/locator animation **UNKNOWN**. Current engineering cycle addresses independent station control. |

No new reference video frame was captured in this map audit: the web reader could not retrieve the footage. Prior audits contain the actual observation history. Do not label this document an aligned side-by-side original/game comparison, or manufacture a reference image from a description. Reference capture, corner selection, perspective correction and frame-sequence comparison remain an explicit gap.

## This cycle: geometry provenance, not cosmetic certification

The map data migration preserves all four graphs exactly. There is therefore intentionally no claimed visual improvement from that migration alone. The new [catalog diagram](images/map_catalog_v1.png) exposes station order, topology and house placement for future corrections. The remaining visible discrepancies above stay open.

For each future reconstructed map, store a reference record with URL, cabinet/version confidence, exact timestamp, unobstructed corner coordinates and observation notes. Keep independently generated output captures separate. Compare equivalent player counts/states, normalize the playfield rectangle, annotate topology differences first, then wall width, sprites and HUD. Test collision edges against the revised rendered walls, regenerate moving clips and repeat critical review.

## Review outcome

First pass: verified the migration is data-only and preserves reachable routes. Second pass: checked the claim boundary; existing screenshots do not prove any DX transition rule, and four differently colored reflected maps do not establish a commercial map catalog. Full-frame reference reconstruction and aligned 4/8-player/startup comparison remain high-priority work, not completed items.

## Integrated station/UI comparison

![Local revision-7/revision-8 startup, P8-first join and results comparison](images/station_before_after_r8.png)

This comparison uses our own revision-7 lobby as the baseline. The new per-station controls, pairing prompt, first-player P8 and ranking list are visible. The ranking panel uses assigned test scores; it is explicitly labeled a controlled scene, not a completed match. This is deliberately not labeled a commercial-game comparison. The companion `gameplay_4_player.gif` records eight seconds of actual four-player simulation (96 frames, seed 24); frames at 0, 3.3 and 6.7 seconds were visually inspected. See `audits/revision8_maps.md` for tested cases and the reproduced, corrected and rechecked locator clipping.

## Revision 9 cyan topology correction

![Local cyan-map correction: before and after](images/map_before_after_r9.png)

Unlike the revision-8 data migration, this changes playable routes. Actual cabinet frames at [2:00](https://www.youtube.com/watch?v=efLgejKG_ls&t=120s) and [1:15](https://www.youtube.com/watch?v=efLgejKG_ls&t=75s) show the house separated from nearby branches by a corridor and distinct vertical wall islands. The view is rotated 180 degrees relative to our house entrance; the two raw-left vertical islands therefore belong on the game's right. Our revised cyan map opens the house perimeter and separates these walls. The figure above compares our old/new output; it does not pretend the estimated grid is a perspective-perfect original trace. See `audits/revision9_maps.md` for the tested change and remaining uncertainty.


## Fresh released-DX enclosure comparison

The subsequent native-browser review did obtain new reference imagery, superseding the map-audit access limitation above. Actual efLgejKG_ls frames at75/90/120s were inspected, plus the15s instruction presentation. The research figure `outputs/DX-house-comparison-r8.png` is delivered separately from the playable ZIP. It contains a120s enclosure crop, rotated180 degrees for doorway orientation, beside baseline/current game crops. Perspective and glare remain; images are resized for inspection without invented geometric reconstruction.

The figure caught an initial regression: baseline already had two visible contours contributed by background and foreground layers; simply adding an inset produced three. Final rendering clears the background house edge and explicitly draws two consistently separated contours. All-four-theme checks count exactly two bright runs, reject the old third line and verify the inner doorway stays open. This is controlled render correction, not proof of exact commercial line dimensions, topology, actor states or animation.


## Fresh released-DX house comparison and corrective review

The reference reviewer subsequently accessed the actual video in native Chrome, inspecting15/75/90/120seconds. A research screenshot at2:00 supports the observed two house contours; the separate `outputs/DX-house-comparison-r8.png` figure compares this crop with our baseline/current rendering. It retains camera perspective/glare and is not part of the playable ZIP or commercial game assets. It does not establish exact proportions or complete map topology.

The first proposed inset outline was wrong: our background already supplied an outer edge, so the change produced three lines. Actual crop review exposed this despite a passing draw-location test. The correction clears the background house edge, then draws exactly two explicit contours and an open inner doorway. The final regression counts visible bright runs, rather than treating two drawing calls as proof. This cycle demonstrates why rendered comparison and critical retesting matter.
