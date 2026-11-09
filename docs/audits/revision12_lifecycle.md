# Revision 12 lifecycle animation review

2026-11-08. Added `presentation.py`, an independently authored presentation layer. It reads Match state and ledger events; it never modifies player positions, collision geometry, scores, lives, powers or invulnerability. Timings below are explicit configurable original tuning, not measured DX values.

## Implementation

- Giant growth and shrink use a smooth cubic transition between radii 17 and 36 over a default 0.25 seconds. Rendering receives integer sizes only, so procedural-art cache keys remain bounded. A rapid power change reverses smoothly from the current visual size instead of snapping to an endpoint.
- A `player_hurt` event creates a default 0.45-second dissolving core and outward colored fragments at the **old position recorded by the event**. It does not move or delay the actual respawn.
- A living respawn or newly joined station gets a default 0.45-second arrival pulse clipped to its bay. A last-life death produces no false arrival effect.
- The layer has its own event cursor. Repeated rendering cannot replay a death event. Stage changes clear previous-map effects; a different ledger/session resets all presentation state. Zero effective frame time freezes growth, fragments and pulses during pause, guide and results.
- Tunnel deaths duplicate at the periodic seam. Death effects are clipped to the field; arrival effects use their narrow station pocket so adjacent score digits remain untouched. Drawing restores the caller's original clip.

## Pass 1

Tested grow/shrink endpoints, integer bounds, immediate underlying power behavior, interrupted transitions, old-position damage evidence, once-only event consumption, no false last-life arrival, Match digest invariance, pause pixel invariance, stage/session resets, tunnel duplication, bay-score separation and clipping restoration.

## Pass 2

Found and corrected a presentation-frame delay in initial growth observation: new target/event detection now occurs before consuming that frame's elapsed presentation time. A shared intermediate timestamp of one sixth of a second produces the same radius at 30,60,144 Hz, without requiring a special zero-delta priming frame. This affects only visual timing; simulation state remains untouched.

`test_lifecycle_animation.py`: **12 tests PASS** after App integration. Added actual-App checks for intermediate growth, paused presentation, old-position death, bay arrival and reset. A separate eight-player grow/shrink check proves only eight lighting-template calculations occur while the bounded size cache supplies intermediate radii. `capture_lifecycle.py` generated `lifecycle_animation.png`, a 24-frame isolated storyboard showing growth, shrink, dissolve and arrival at 0.00,0.08,0.16,0.25,0.35,0.45 seconds. The storyboard was visually inspected; labels were separated from individual frames to prevent overlap. It is an isolated animation plate, not a recording of human gameplay.

## Integration contract and limits

App creates one `LifecyclePresentation`, resets it in `reset_visuals`, calls `update(match,effective_dt)` once per draw, and uses `radius(player.idx)` for both the main player image and its tunnel twin. `draw_effects` runs after actors while the wider actor clip still includes station bays, before switching to the stricter popup/field clip. This integration was reviewed and tested. The old immediate-giant seam fixture now waits 0.25 seconds of presentation time before asserting radius 36; this retains its original seam/Veil assertion while accommodating the new deliberate transition.

The prior sphere cache had 64 entries; eight colors across twenty growth radii could exceed that working set and repeatedly recompute lighting. Root optimized artwork to use one normalized lighting template per color, a bounded 32-template cache and a 256-size cache. A 60-frame actual drawing check on an SDL dummy surface with eight actors growing/shrinking measured mean 4.440 ms, maximum 8.612 ms and p95 6.471 ms per draw; eight templates and 112 size entries were used. See `LIFECYCLE_RENDER_CHECK.json`. This measures rendering cost in one local headless sample, not physical-display FPS or a hardware guarantee.

Full integration discovery passed 120 tests before the last two lifecycle integration tests were added; root performs the final combined/platform run. No Match logic was changed by this animation implementation.

No primary source was newly observed by this code-focused agent establishing commercial death/growth durations or shape. Original lifecycle animation design remains an approximation and should not be marked VERIFIED DX. Physical controllers remain deferred; these tests make no hardware claim.


## Observed-map portability follow-up

The first full run after the observed map geometry update ran 141 tests and found five failures: four fixtures assumed tunnel row 9; one assumed house door column 27. Fixtures now derive portal rows and door coordinates from the actual Arena. Geometry rendering tests also pass the map lane radius, rather than implicitly rendering every graph with the old radius. No production geometry was altered to satisfy fixtures.

A deeper pass updated connectivity traversal to Arena.step and checked ghost spawn positions against Arena.homes and the derived den bounds; returning ghosts begin at Arena.exit. Continuous one-cell return movement and entering/house transitions remain asserted.

A new actual arcade_digits draw-call regression checks timer and score rectangles for all four layouts, 1/2/8 players, and six/nine-digit scores (24 combinations). The current dynamically positioned timer clears every score rectangle and stays in the top HUD. This verifies draw-call bounds, not commercial-game visual identity.

Validation: two full headless runs passed 142 tests (22.058s and 22.619s), with the second run including the deeper ghost-house and graph-traversal fixture changes. Physical controllers remain untested as agreed.
