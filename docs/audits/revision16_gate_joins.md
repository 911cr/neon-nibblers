# Revision16 exterior joins and critical QA

## Confirmed defects and fixes

The annotated user image highlights exterior corners and gate shoulders. The old perimeter had two cores3px apart while gate rails were6px apart. The map/art agent changed the frame to9px with shared core offsets(1,7). Gate/tunnel rendering now consumes that spacing: tunnel frame cores1/7 (right mirrored-2/-8), top/bottom neck rails6px apart, top gate shoulder cores align to board rows1/7 and bottom cores to rowsH-2/H-8. The U-pocket radii are now10/4, preserving6px separation around the upper/lower rounded pocket corners (previous10/6 reduced the corner gap).

Old gate clear rectangles ended before their sprite glow, so gate shoulders composited glow over existing frame glow. The replacement is now bounded by the clear rectangle, with lines extending beyond the clip for continuous glow at its boundary. Caller clipping is preserved.

A deeper actual-App pixel test then found a separate sampling defect: using round((coordinate+.5)*3) invokes ties-to-even rounding and alternately shifts different rows by one supersample. Lower gate cores were roughly6–10% dimmer than the existing frame while upper cores matched. Coordinates now round the geometry first and then add the fixed supersample pixel-center offset. Both orientations now meet the same shoulder brightness tolerance.

## Verification

Combined `test_exterior_joins_r16`, `test_gate_quality`, and `test_gate_detail_r14`: **17 tests passed in8.112s**. Coverage includes actual App all4maps×5palettes×8station shoulder joins, core gap6px, shoulder brightness continuity, visible dark gap, pocket rail spacing, and legacy five station-state matrix (release/away/return/dead/empty), AI gate operation, normal actor body/pocket clipping, long-score clearance, yellow threshold lip, tunnel join paths, and caller clip restoration. Existing tunnel pixel fixtures changed from the old3px frame coordinates to the new6px coordinates; no behavioral assertions were removed. Source frozen after these checks; map/art agent independently captures the final full render comparisons.

## Gameplay follow-up

Read current pickup, effect expiry, ghost state/navigation, carried-ghost, flame, bonus-life, combat, continuation, and moving-item resolution paths after the graphics changes. No additional definite code defect was reproduced in this pass. The revision15 power parity limitations remain: exact commercial durations/ranges, global-blue-ghost ownership semantics, blanket giant immunity, forward-only flame, smoke trail extension, and fixed ghost population/strategy are not certified. This review is not an exhaustive proof of all power combinations or commercial behavior.
