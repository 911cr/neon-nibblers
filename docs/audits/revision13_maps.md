# Revision 13 - maze contour audit

## Evidence and scope

Re-reviewed the complete spectator-screen frames at [1:08](https://www.youtube.com/watch?v=-cNOhumVZ74&t=68s) and [1:13](https://www.youtube.com/watch?v=-cNOhumVZ74&t=73s), including normalized views and movement-graph overlays. The four selectable profiles remain original palettes over two independently reconstructed observed topologies: Golden/Cyan Archway (A) and Violet/Ember Crosscurrent (B). No new commercial layout, route, exact dimension, transition rule or timing was invented.

## Demonstrable discrepancy corrected

Reference isolated wall bars have rounded capsule ends. The revision12 two-pixel morphology preserved thin stems but left ordinary bars and branch ends conspicuously square. Revision13 rounds the larger convex branch corners while retaining long thin features that would otherwise vanish. Isolated straight narrow wall components are given semicircular ends. Every replacement is intersected with its prior wall mask, so the correction cannot introduce a visible obstacle into an existing route. The house and board frame remain separately handled, and ordinary walls still have one contour rather than an unsupported interior rectangle.

| Profile | Evidence family | Topology / gates / house | Contour review |
|---|---|---|---|
| Golden Archway | A,68s | Same tested582-cell graph, paired tunnels5/25, eight measured bays | Rounded capsules and arch/hook ends; viewed actual8-player render |
| Cyan Archway | A,68s | Same geometry as Golden | Compared directly to68s reference and before-render |
| Violet Crosscurrent | B,73s | Same tested569-cell graph, paired tunnel17, eight measured bays | Rounded capsules and T/L ends; viewed actual8-player render |
| Ember Crosscurrent | B,73s | Same geometry as Violet | Viewed actual8-player render; palette is an original choice |

## QA pass 1

All12 existing map tests passed after contour changes, including every1-8 player count on each profile, map transitions, sparse station ownership, house perimeter and door approach, no2x2 dot areas, no unintended dead ends, every rendered movement edge, thin-stem continuity and the single-contour capsule scan. No maps.json graph edits were required.

## Deeper QA pass 2

Added a new rendered capsule test on all4 profiles: the square corner recedes, while the rounded side midpoint, straight upper edge and filled wall body remain. All14 map tests passed, including the additional actual-App house contour test. Independently generated actual App images for both the prior and current renderer using identical geometry, match seed and current App overlays. Inspected both observed families side-by-side with normalized source frames. The rounded version visibly corrects the square-tip discrepancy without losing arch/T stems or introducing extra outlines. Rounded replacement masks are constrained to the original component as a defensive guarantee against obstacle expansion.

Also identified faint residual background-house glow outside the explicit house clear rectangle; root enlarged only that clear area to remove it. A new actual-App pixel scan verifies exactly two house border contours on both the bottom and left sides for every profile. All four final actual renders were reviewed after this integration. This is a separate overlay issue, not a new wall route.

## Limits retained

Exact wall widths, some junction locations and gate coordinates remain quantized to the20px movement grid. Long narrow stems preserve connectivity and may still differ in thickness from footage. Camera perspective and glare prevent pixel-level certification; the house door and adjacent wall endpoint inference remains explicitly recorded in map provenance. Glow softness, original characters, palette profiles, bay numbering and game rules are independent adaptation choices. Full DX catalog and exact transition scheduling remain unverified. No claim of identical appearance or complete commercial reconstruction is made.

## Artifact

`outputs/DX-maze-comparison-r13.png` shows source / revision12 / revision13 for both families using the same local map geometry. Source-derived research images remain outside the runnable package. Actual local all4-profile snapshots are `work/map_r13_after_0.png` through `_3.png`.

## Independent fresh-footage cross-check

A fresh full spectator-board frame at [9:34 in43DcDXxEgzk](https://www.youtube.com/watch?v=43DcDXxEgzk&t=574s), retained as `work/dx13-haid-574-board.png`, independently shows family A in red. The upper arch, flanking capsules, two side-tunnel rows, house-side vertical bars, lower hooked branches and center lower bars match the68s family. This is corroboration of the existing topology and color/layout independence, not a third reconstructed family. The board occupies approximately540 source pixels horizontally, with globally soft dots, text and character edges; apparent stroke brightness/thickness cannot distinguish game rendering from camera blur and scaling. No additional topology or stroke-width change was justified by this frame.
