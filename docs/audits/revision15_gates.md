# Revision15 closed yellow lip and uniform luminous rendering

Direct inspection of the user gate photo and an independent research-agent reading agree that the closed striped threshold has a continuous bright upper yellow lip. The old dark diagonal cuts interrupted both band edges. Added one continuous upper pixel row after drawing the cuts, for both upper and lower bays. The static photo does not establish whether an open gate retains a yellow line, so open behavior and all timing/permissions remain unchanged.

Gate and house art now share arcade_art.neon_sprite and NEON_SCALE/STROKE/CORE with walls:3x source ink,3px accent stroke,1px pale core, one downsample and premultiplied composition. House contours were upgraded from native-resolution drawing to the same3x treatment. Fully opaque striped bands remain opaque; upper mirroring occurs before applying the band, preserving stripe direction and lip placement.

Two QA passes: two new tests cover isolated continuous lip/underlying dark cuts/open clearing for allfive palettes and both orientations, plus100 actual App combinations (four maps×five palettes×five states), each checking eight station mouths and unchanged simulation digest. States include human/AI departure, distant travel, owner return, eliminated/continue and empty bays, with nine-digit score setup. Existing eleven gate-detail tests cover body fit, actual own-bay clipping, departure clearance, soft glow, parallel edges, house glow and HUD bounds. Combined13 tests passed in15.006s. Gate code is frozen after this reviewed pass; no Match changes were made here.

Actual comparison outputs/Gate-quality-comparison-r15.png, outside the distributable game directory, shows user-photo closed bay, previous closed, updated closed and updated open. It was reopened and visually inspected. Perspective crops and rescaling are labelled, not represented as measured dimensions or dynamic evidence. Before/after frames are retained in work/gates-r15-*.png.

Approved within the tested gate-rendering scope; not a claim of exact source art, source timing or hardware verification.

### Final independent tunnel-neck recheck

The shared-shader tunnel extension passed all three `test_gate_quality` tests (4.900s). Actual App renders were inspected across all four layouts, all five palettes, both ends and each configured portal; saved analytic contact sheet: `work/portal-matrix-r15.png`. Core/halo appearance is symmetric and consistent across palettes, and the extension respects the intended outside-board clip. A remaining geometric join was reported to the integration owner: the outside inner rail at ±23px ends at the board edge while the existing board cap is at ±27px; the 4px dead-end is visible on every profile. This is a connection-detail finding, not a claim that a particular commercial portal join is measured. No game/render source edits were made during this recheck.

The natural-continue replay fixture change from seed1 to seed0 preserves all assertions: an actual natural continue event/input must occur, replay digest must match, human count remains correct, score ledger totals reconcile, and continue events preserve score. Selecting a seed that actually exercises final-life loss under the new radius-aware contacts does not weaken those checks. Full replay execution is owned by the integration agent.

### Tunnel seam correction and second pass

The integration owner delegated the confirmed seam fix. `gate_art.py` now replaces a bounded 14px strip inside the board as well as the outside neck: paired luminous corner paths align to the actual left frame core columns1/4 (right mirrored columns-2/-5), removing the obsolete cap before premultiplied composition. This avoids both the dangling inner rail and double-bright overlap. No simulation or map graph changed. The old no-board-overpaint assertion was narrowed to the actual unchanged area beyond the14px seam; new checks require a continuous inner corner and an unpainted center passage. A separate clip test confirms caller clipping is honored and restored.

After-fix actual App sheet `work/portal-matrix-fixed-r15.png` was inspected for all four maps, five palettes, both ends and every portal. Connected corners replace the previously visible dead ends. Final combined gate-quality and legacy gate-detail suite: **15 tests passed in7.067s**. The earlier reported seam is resolved. The exact commercial portal corner shape remains unmeasured; this fix establishes coherent local geometry rather than asserting exact source reconstruction.
