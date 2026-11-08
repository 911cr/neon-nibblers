# Wall look/feel audit — 2026-11-08

Directly inspected browser video at https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s and local revision4 preview.png; read current arcade_art.py and game.py. Clear reference is mobile/projector presentation, so this supports wall appearance without claiming every Deluxe map identical. Existing cabinet cross-check is https://www.youtube.com/watch?v=GhSV1oQVA6g&t=57s .

Confirmed visual differences:
- Reference interior walls are slim rounded capsule/L/T strokes with nearly black interior and pale yellow outline. Current walls are noticeably thick slabs at matched playfield width, especially upper central bent wall and lower-left complex.
- Typical reference narrow wall thickness is approximately half our current normal wall thickness by visual proportional comparison (camera perspective prevents exact pixels). Current graph pitch80px and tube radius26 produce28px wall slabs. Radius32 would leave16px slabs and move closer to the observed slender proportions. This is a tuning recommendation, not a recovered original dimension.
- Thin bright outline plus restrained pale halo suits the reference. Keep near-black fill. Do not add textured/metal/3D wall fills. Current outline broadly correct; improve antialiasing at rounded turns rather than making halo much stronger.
- Reference outer border visibly has twin contours; current frame has a single outline plus artifacts from retaining boundary cells. Gate/border agent should unify that geometry.
- The largest mismatch is topology: several current wide blocks and the row of small square islands are not the capsule/L/T silhouettes in the inspected reference. The node-pruning step can merge large wall regions, and stroke tuning alone cannot fix that. Do not call this identical merely after thinning.
- The house is an outlined small rectangular enclosure with visibly occupied interior; current revision4 treats it as a broad opaque wall island. Parent is already updating ghost-house lifecycle and draw.

Implementation recommendations:
1. Increase carved corridor radius toward32 only with explicit outer clipping/frame handling: naive radius32 crosses the 30px distance to the first corridor center and will remove the edge frame. Carve interior inside an inset, then open only actual tunnel and gate mouths.
2. Keep same graph for art/collision, one line of dots and full reachability tests. Single-line dots can remain even with wider clearance; do not restore multiple parallel dot rows.
3. Give maze and bays common double-contour rendering, same colors and gap.
4. Revisit broad merged wall components separately. Preserve thin wall branches while adding missing center-line routes; do not change random paths simply to produce more visual density.
5. Render a large still before/after and compare upper central bend, lower-left hooked branches, right-center islands, house, outer corners. Current authored layouts are not established reference maps.

No shared game files edited. No exact wall dimensions, glow values or full commercial topology were recovered from camera footage.

## QA1 — same-agent verification of implemented fixes
Inspected current code plus work/revision5-refined.png. Radius is now32 and carve clipping preserves a6px frame, with explicit tunnel/gate openings. Narrow walls now read as slim outlined capsules rather than revision4 slabs. Upper-central large merged block has been substantially reduced by opening the extra routes. Filled house island replaced with outlined, visibly occupied enclosure. These audit fixes are implemented and visually improved; they do not establish an exact commercial topology.

## QA2 — adversarial geometry/render pass
Ran Smoke.test_all_arenas_connected and Smoke.test_single_lane_geometry_and_visible_routes: both PASS across all4 maps. Rendered fresh eight-panel stress sheet work/walls-qa-allmaps.png: every map with8 giant players at corners/tunnel mouths, then normal sizes. No crashes, disconnected authored navigation, center-line wall crossings or lost border frame found. Gates and mouths stay present on all themes.

Remaining reference differences:
- Outer frame corners remain square right angles rather than the reference's softer corner transitions. Low priority cosmetic correction; preserve gate/tunnel cuts if rounding.
- Row of small rounded square islands and several lower-left branches remain authored geometry, not the inspected reference map. No pixel/topology identity can be claimed.
- Giant sprites visibly overhang outer wall corners/tunnel mouth bounds. Normal sprites fit. This is a rendering observation, not established collision failure or confirmed original mismatch: exact commercial giant-wall occlusion is unverified. Edge agent should decide clipping policy consistently rather than clipping all giants arbitrarily.
- Exact glow/line width/color values cannot be inferred from angled camera footage. Current blackfill/paleyellow/slimdoubleframe is closer to observed visual language.

No new blocking functional wall bug found in these two passes. No shared code edits made.
