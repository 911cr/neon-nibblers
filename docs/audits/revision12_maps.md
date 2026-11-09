# Revision 12 — two observed maze topology reconstructions

## Evidence and method

Fresh native-browser frames from the confirmed DX IAAPA 2022 Arcade Heroes video, https://www.youtube.com/watch?v=-cNOhumVZ74, at **1:08 and 1:13** show the entire spectator board without hand obstruction. Same camera, top-facing house door, all corners and eight bays. The first has an upper arch and two paired tunnel rows. The second has a central upper T and one paired middle tunnel row. Both are cyan, so color is not a map identity. The visible lower-left counter changes 8 to 9. No inference of exact transition trigger or catalog order is made.

Perspective normalization uses independently estimated screen corner coordinates (stored in each map's observations). Wall centerlines were manually transcribed, then used to construct one-cell movement graphs between wall contours. Final gameplay reads explicit lane rows; it does not use or distribute source screenshots. Map A replaces cyan slot3, map B replaces violet slot1, both revision3. Local violet styling is explicitly original. Golden now uses family A and ember family B; their prior authored geometries are retired. Four palette profiles represent only TWO observed layouts. Source images in the comparison are research artifacts outside the runnable game ZIP.

## Changes

| Detail | Prior implementation | Observed-derived implementation |
|---|---|---|
| Main topology | Authored reflections with a cyan local fix | Two distinct complete wall/junction configurations |
| Tunnel rows | 9 and25 on every map | A5/25; B17 |
| House | x23,y15,w9,h5 | x25,y15,w9,h5 on reconstructed maps |
| Bay columns | Uneven5/17/29/41/53 | 6/20/38/52 top and bottom, measured through homography |
| Lane cells | Cyan578, violet589 | A582, B569 |
| Floor carve radius | 32px | 26px reconstructed maps with 2px rounding, all four profiles; renderer retains32px/5px support for historical data |

## QA pass 1

Parsed both records through full validation: connected routes, no unintended dead ends, no2x2 dot blocks, declared paired tunnels, eight unique adjacent bay entrances, solid house interior and complete one-line perimeter. All player counts1–8 on all4 maps ran180 steering ticks then forced a map transition, preserving identities/lives/scores. Sparse first-player station selections and locator bounds also passed. Initial11 map tests passed.

## QA pass 2 — critical actual rendering

Actual App renders exposed a defect missed by graph-only validation: 26px floor carving plus existing wall rounding removed thin stems between corridors only3 cells apart. This erased part of the arch/T and house flanks. An initial22px carve preserved stems but made wall bands too thick. A further critical comparison instead retained the26px carve and reduced morphological rounding from5px to2px for these narrower walls. This preserves stems while leaving52px corridors around34px normal players. Capsule end contours remain approximate. Added a regression that inspects every rendered traversable edge at the map's actual radius, plus continuity pixels through the formerly erased stems. Final12 map tests PASS; repeated after the radius/rounding correction. Actual A/B images were inspected against normalized reference and graph overlays. The new top-bay score positions also exposed overlap with the center clock; reported to the root HUD owner for correction.

## Remaining differences and uncertainty

- Quantization to59x31 movement cells changes exact junction positions and wall widths. Gates rounded to20px cells, approximate half-cell uncertainty.
- Glare obscures the house doorway and the upper endpoint of the immediately adjacent left wall. Adjoining contours/complementary footage support the inferred continuation, but exact hidden pixels are not verified.
- Rounded wall contours remain procedural style approximations; ordinary reconstructed walls have no extra inset contour. The source has narrower-looking wall bands and softer glow in several regions.
- House opening size, gate animation, original characters and palette are independent adaptation art. Neither map is called pixel-exact.
- Four palette profiles use two observed families. There is no claim of four distinct recovered maps. Full DX catalog, selection order, cycle trigger and frequency remain unknown.

## Artifacts

`outputs/DX-maze-comparison-r12.png`: source / previous local background / updated actual app maze, both layouts. `outputs/DX-maze-lane-evidence-r12.png`: red movement cells over normalized source. Both are outside the runnable package. Working traces are in `work/build_observed_maps.py`; runtime data is `outputs/NeonNibblers/maps.json`.

## Final production catalog pass

Retired both remaining unsupported authored graphs: golden now shares A, ember shares B. All four records explicitly carry `layout_family` and `palette_provenance`. Repeated all12 map tests, including all32 count/profile combinations and pixel clearance on every edge. Viewed actual eight-player golden and ember renders; gates, house, routes and wall stems match their tested A/B family. No extra topology is invented from palette differences.

## Final contour correction

The old broad-island inset heuristic created extra inner rectangles on the reconstructed layouts' ordinary capsules. References68s/73s show a single contour on these bands. The renderer therefore omits the inset pass for reconstructed profiles (radius<30), retaining the separately drawn double ghost-house outline. Added an exact scanline regression: the upper-left capsule must have two separated accent runs (its two outer edges), not four (outer edges plus inner rectangle), on all4 profiles. The house remains independently rendered; this does not remove its double border.
