# Revision 9 — released DX reference review

Date: 2026-11-08. Reviewer: dx_research. Two critical passes completed; no perfect-match certification.

## Source and capture method

[Seals on the Move: Pac-Man Battle Royale Chompionship Deluxe Arcade Gameplay](https://www.youtube.com/watch?v=efLgejKG_ls), released cabinet footage. Inspected in native Chrome, paused at 0:45, 1:15 and 1:45 this revision. After each keyboard seek, a separate fresh screenshot was taken to avoid treating the previous decoded frame as the requested timestamp. The 1:15 screenshot is saved only as a local research artifact at `work/dx-reference-75s-r9.png`. No video/audio was downloaded. The previous 2:00 research screenshot remains useful for the opposite part of the maze.

## Pass 1 — visible differences and actionable findings

- **Observed at 1:15:** station SWIPE prompts lie outside the small entrance bays, beyond the perimeter wall. A station number is further outboard. The bay chamber is dark, surrounded by paired cyan contours; yellow diagonal hatching crosses its narrow neck. Home keyboard labels are an adaptation, but putting text over the bay is not supported by this reference. Root received this finding while correcting score/life overlap.
- **Observed at 1:15:** the house has a central doorway segment on the bottom-facing edge of the photographed screen. Rotate the reference 180 degrees to compare to our top-exit logical map. Never copy raw screenshot left/right directly into map coordinates.
- **Observed at 1:15:** three separate horizontal capsule wall islands appear to the right of the photographed house, with dotted corridors separating them. A hollow double-contour rectangular island appears above them. A dotted route separates the house right edge from the long bent wall beside it. These are the opposite side of the normalized map after rotation. Sent the screenshot and these observations to the map reviewer.
- The previously captured 2:00 view shows separated vertical capsule structures on the other side. The two partial views complement one another but do not constitute a complete maze survey.
- The 0:45 and 1:45 frames are closer player/cabinet shots. They do not resolve the missing full-maze boundaries. They were inspected, not used to invent geometry.

## Pass 2 — adversarial interpretation checks

1. **Orientation:** the 1:15 house opening independently supports the same 180-degree normalization used for the 2:00 crop. Camera rotation is not evidence of a second map variant.
2. **HUD claim narrowed:** this clean 1:15 frame demonstrates inactive SWIPE placement, not a precise active-score baseline or font size. Keeping active score/life text outside the bay is a layout fix; exact original score offsets remain unverified by this frame.
3. **No route inference through glare:** bright reflections conceal some cells. Only visibly dotted paths and separated wall contours are described. Exact game grid spacing, capsule lengths, corner cells and every house-perimeter connection require further evidence; map edits remain authored approximations unless separately traced.
4. **No behavioral claim from stills:** hatch appearance does not establish gate release delay, collision state, re-entry policy or animation. No continuous Start-to-release sequence was captured. Likewise, visible point bursts do not isolate a collectible's scoring cause.
5. **Rendering versus topology:** paired contours and narrow-looking lanes do not alone prove collision rules or movement routes. Gameplay tests must separately exercise the authored paths.
6. **No borrowed version rules:** these observations concern the released DX cabinet. Older Battle Royale or 2013 prototype behavior cannot fill the remaining DX gaps.

## Review artifact

`outputs/DX-route-reference-r9.png` is an annotated research crop from 1:15, inspected after creation. It preserves perspective and glare and explicitly labels its limited scope. It is outside the playable app and ZIP; it is not a game asset. It shows the evidence used for gate/HUD separation and capsule/corridor review. The whole reference screenshot remains in `work` only.

## Remaining uncertainty

Full maze topology, exact active-score typography/offsets, gate animation/timing, all scoring values, power-up intervals and full original behavior remain unverified. Physical controllers remain deferred by the user; this visual audit does not test them. No claim that all differences are resolved is warranted.
