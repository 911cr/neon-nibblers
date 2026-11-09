# Revision 14 - four observed maze families and bounded stem correction

## New evidence and implementation

Fresh full-board footage from https://www.youtube.com/watch?v=qcO9tzgsdjo establishes two additional visibly distinct layouts. Family C at4:10/4:30/4:53/4:59 has upper corner U shapes with posts, side triple capsules, lower rectangular islands and nested open enclosures around the house. Family D at5:05, corroborated by a larger tabletop view at5:15, has long center horizontal rails, short top/bottom center capsules and different side branches. Both are distinct from the established A/B layouts. The existence of these four families does not prove a complete commercial catalog or fixed ordering.

The map agent independently traced C's585-cell graph with offset side corridors. The research agent independently traced D's569-cell graph; the map agent critically reviewed its wall/route overlay before integration. C replaces the previous duplicated B profile at slot2 (Ember Courtyard), and D replaces duplicated A at slot0 (Golden Rails). A remains slot3 and B slot1. C/D map revision4 and catalog version5 preserve source URLs, timestamps, perspective corners and inferred regions. All four retain the same house/bay anchor convention; C has paired tunnel rows5/25, D17.

## Local rendering correction

Existing isolated narrow wall bars were only8px wide because neighboring routes sometimes sit three cells apart. Normalized source bars appear approximately18-24px wide, subject to camera blur and perspective. Isolated straight bars are now widened to16px, expanding at most6px per side. Connected thin stems, maze frame and house are excluded. This is a bounded original approximation, not a claim of exact source dimensions. A new mask-based regression verifies20px body clearance throughout every public lane and every connecting movement segment, exceeding normal player/foe body radii.

## QA pass 1

Reviewed all existing A/B route overlays and found no evidence-backed missing junction. Traced C and integrated the independently traced D. Both passed catalog validation: complete connected graphs; no2x2 dot blocks; no unintended degree-one dead ends; legal paired tunnels; eight unique owned bays; no public lanes through the ghost house; complete house perimeter and door approach. Actual eight-player App renders were inspected against normalized full-board references.

## Deeper QA pass 2

Eighteen map tests pass after the user-photo wall pass. Coverage includes every player count1-8 on all four maps, forced map transitions, sparse first-station identity, every visible movement edge, full20px body clearance over all routes, exactly two explicit house contours, single capsule contours, rounded capsule ends, thin connected stems and bounded isolated-bar width. Added C/D-specific landmarks: C's offset side route and lower enclosure path, solid lower-left island, D's uninterrupted upper lane and blocked center shortcut through its long rail. Inspected source/previous/current comparison for every profile. Source C/D perspective and actor occlusions are cross-checked with adjacent captured frames; coordinates remain estimated.

## Remaining uncertainty

- Twenty-pixel coordinate quantization and oblique camera perspective leave local offsets and unequal apparent wall thicknesses. C's half-grid side-column offsets are estimated rather than software-coordinate measurements.
- Bay centers retain the established cabinet-proportion estimate; exact gate dimensions and player body sizes are not recovered from these frames.
- Source strokes and glow are camera-softened; exact software stroke widths are not inferred from apparent bloom.
- Full map count, commercial names, color policy, timing, selection and transition triggers remain unverified. The four original profile names are not commercial names.
- No claim of identical appearance, exhaustive map reconstruction or exact hidden endpoints is made.

## Artifacts

- `outputs/DX-maze-comparison-r14.png`: all four source/prior/current layouts.
- `outputs/DX-new-layout-evidence-r14.png`: exact independently authored movement graphs over C/D reference frames.
- `outputs/DX-stem-detail-r14.png`: before/after isolated wall-width correction.

Research images are excluded from the runnable package. Runtime code/data are original and contain no commercial screenshot assets. Reproducible working traces are `work/trace_dxC.py` and `work/trace_dxD.py`.

## User-provided clearer photo - final wall pass

The user's clearer spectator-screen photo (retained outside the game as `work/user-reference-D-r14.png`) independently confirms family D. Compared every visible major junction: long top and upper-center rails, short center capsules, asymmetric side L/U branches, paired middle tunnels, four house-side vertical bars and lower horizontal rails. No additional route change was justified. Its blue presentation also corroborates that topology is independent of palette.

The photo exposes a real presentation gap: the local opaque outline was crisp but dim, with much less halo and pale core than the reference. Added original procedural Gaussian halos and a pale inner stroke inside the existing opaque silhouette. No commercial bitmap is used, and no collision or movement coordinate changes. A new regression checks the halo, brighter inner ink, preserved outer accent and dark lane center on every profile. The full body-clearance mask now includes the new pale ink as opaque, rather than accidentally omitting it. All18 map tests pass after this correction, including20px body clearance and house contour scans.

Gate proportions were reported to the App owner: source bays approximately55-62px wide on a1060px-wide field suggest roughly62-69px at the local1180px field width, with roughly51-57px scaled depth. A64x48px original bay treatment and48x10px hatch strip were recommended, subject to the App's header layout. Exact dimensions remain perspective estimates, not recovered game coordinates. Gate implementation and its final verification belong to the root App audit.

Independent research-agent review also compared C's graph overlay, actual render and complementary source frames. It found no demonstrable missing passage, added connection or mirroring, and independently reran the17-test map suite before the subsequent user-photo wall treatment. Exact endpoints and widths remained explicitly uncertified.

## Final integrated photo review and freeze

After the App's gate, house and fifth blue-palette integration, captured actual eight-player D gameplay both at initial open-bay release and after three seconds of simulated play with all eight hatches closed. Reviewed enlarged top/bottom pockets: player bodies sit inside their bays; double U outlines join the field continuously; yellow/black hatch diagonals retain the same screen direction on both sides; no score/footer clipping or residual house underlay seam was visible. Actual gate/house halos were rechecked after alpha-aware glow compositing was corrected by the App owner.

The final wall change rounds the outermost board-frame corners to16px rather than retaining square corner pixels. This only removes corner wall material. A dedicated regression checks all four missing corner tips and preserved straight edges. The final19-test map suite passes, including full20px opaque-body clearance, all movement edges, all1-8 player/profile cases, house borders counted using accent plus pale ink, and actual halo/core pixels. No further art changes were made after these checks.

Final artifacts: `outputs/NeonNibblers/maze_D_blue_r14.png` (actual three-second eight-player gameplay), `maze_D_blue_open_r14.png` (actual initial open pockets), and `outputs/DX-user-photo-comparison-r14.png` (photo / prior wall preview / final playable blue D, with enlarged bay details). The reference photo is outside the runnable package. The blue palette is now selectable independently of topology. The desktop HUD remains upright; the cabinet photo's upper station prompts are rotated for players on the opposite side of the table. This deliberate desktop presentation difference is not an unverified claim of cabinet equivalence.
