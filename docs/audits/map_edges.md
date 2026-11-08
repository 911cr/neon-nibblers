# Map edges and tunnels audit — 2026-11-08

Scope: current game.py and arcade_art.py, direct browser inspection of https://www.youtube.com/watch?v=GhSV1oQVA6g&t=57s . No game code edited.

## Observed reference details
The cabinet frame at 0:57 shows two horizontal tunnel mouths on each side. Each is a short neck continuing outward from the main border, with two narrow parallel yellow contour lines. The main outer boundary also uses twin contours; top/bottom player pockets are integrated into that line. The left edge is substantially more visible than the right, so the exact right-hand neck length is not measurable from this camera view. This observation establishes silhouette, not teleport timing, exact map coordinates or every level's geometry. Front-view source used elsewhere is https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s (mobile presentation, not proof of all Deluxe behavior).

## Current implementation
- Arena.portals=(9,25), paired left/right. step wraps x=-1 to58 and x=59 to0 on these rows. These positions are custom, not measured exact commercial coordinates.
- A focused local check passed all16 transitions (four maps x two mouths x two directions). Destinations are traversable. No traversable floor neighbor escaped global map bounds.
- Rendering cuts tunnels off exactly at OX and OX+COLS*TILE. The reference has projecting tunnel necks. Extend the two upper/lower rail lines into the side margin by roughly one tile as an authored approximation, and permit tunnel sprites within that neck region.
- World clipping uses one rectangle with extended vertical height for gates but no horizontal margin. That neatly clips away the current tunnel sprite at its first/last cell, before its center has left the visible playfield. Change to a world layer with corridor/tunnel masks or a controlled horizontal extension at portal rows only, keeping score text protected.
- Current smoothing resets old=target whenever distance exceeds3tiles. Every portal wrap therefore visibly snaps from one partial edge sprite to the opposite partial sprite. Implement periodic interpolation on portal rows: choose shortest virtual horizontal displacement, draw the wrapped copy shifted by the field width, and clip each side. Do not smooth all the way across the middle of the screen.
- Outer border is derived from rounded tube carving plus copied boundary wall cells. This creates overlapping corner remnants/slivers near the rectangular surface edge, visible in revision4 previews. Replace the hard rectangular perimeter remnant with a clean continuous double-contour outer path, breaking only at actual portal mouths and player bays.
- Gate render/collision geometry is a separate audit; coordinate outer-frame work with that change so the hatch sits exactly on the boundary.

## Regression tests recommended
1. All four maps, both portal rows, both directions, for players, foes and roaming collectibles.
2. No wrap on other rows; top/bottom border blocked except valid owner bays.
3. Render a normal and giant player at each seam for several intermediate frames; assert no middle-screen flash and no HUD spill.
4. Opposing players swap through a portal in the same step: collision resolves exactly once and neither leaves the graph.
5. Screenshot sampling confirms neck rail positions match the traversable corridor opening.

Unknown: exact original tunnel traversal speed, wrap delay, neck length, whether every commercial level uses the same two portal heights. Do not claim the custom portal configuration is exact.

## QA1 — implementation re-audit
Current revision5 code adds outward four-rail tunnel necks, widened horizontal clip, periodic nearest-displacement interpolation and wrapped player/foe copies. These address the main revision4 defects. Outer frame carving now stays inside an inset perimeter before cutting real openings; the previous copied edge-remnant procedure is gone. These are code-confirmed fixes, not certification of exact commercial dimensions. Item rendering still uses old distance-reset interpolation, so roaming power-ups snap rather than traverse seams smoothly.

## QA2 — adversarial seam/render checks
Reproducible local scripts: work/map_edges_qa.py (results work/map_edges_qa.json), work/edge_hud_qa.py. Use PYTHONPATH=work/deps and Python from workspace root. No shared game files edited.

- PASS:32 player seam scenarios =4maps x2rows x2directions x normal/Titan.512 rendered transition frames showed no erroneous center-screen interpolation flash.
- FAIL: Veil twin opacity. A Veil player at(0,9) draws primary at(60,235),opacity150, then wrapped twin at(1240,235),opacity255. Pass same opacity/effect state to both calls.
- FAIL: fixed30px twin threshold is smaller than Titan radius36 (plus glow). At(1,9), center30px from left seam, the giant crosses the periodic boundary but only one muncher draw occurs. Derive threshold from rendered radius/halo rather than constant30. Normal/ghost thresholds should likewise follow actual extents.
- FAIL: widened global world clipping allows lightning over the score strip. With all moving entities removed and g.zaps=[((5,1),.2)],38pixels change in header region x180:300,y13:32 compared with identical render without zap. Limit environmental effects/popups to board bounds; extend only actor clipping for gates/tunnels, or render HUD after all world effects.
- REMAINS: roaming pickups lack periodic interpolation/copies. Their logic wraps but rendering resets; use shared seam helper for all roaming world entities.

Exact original wrap delay/speed and portal geometry remain unverified. Fixing these deterministic rendering inconsistencies does not establish pixel identity.

## Targeted fix verification
Reran original reproduction scripts against latest revision5. All three reported defects now resolve: Veil primary/twin both opacity150; giant at30px seam distance now draws two copies; lightning modifies0pixels in previously affected HUD strip. All32 player seam scenarios/512frames still pass with no center-screen flash. Added narrow collectible check (work/item_seam_recheck.py):16 scenarios/256frames across all maps, both mouths/directions; no center-screen flashes and wrapped duplicate present. No remaining reproducible failure from this audit's targeted set. This verifies rendering fixes, not exact commercial tunnel dimensions/timing.
