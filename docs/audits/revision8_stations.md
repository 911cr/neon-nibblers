# Revision8 station and lifecycle QA

Reviewer: same dx_research agent,2026-11-08. Reviewed outputs/NeonNibblers/game.py (Player, station_action, events, inputs, advance, draw/results) and stations.py. Added test_stations.py; no shared game code edited by reviewer. Tests use dummy SDL graphics/audio and synthetic controller objects, never actual USB proof.

## Pass1: source and state-transition review

Confirmed independent sparse station representation: P8 can start alone without activating P1–P7; contiguous quick-start presets remain optional. Active Start locates rather than resets the player. Eliminated joined stations cannot replenish lives/score during the same match. Paused/help phases ignore station joins; results Start begins a new match containing the selected station. Same-frame eight button presses create eight participants exactly once.

Found production presence defect: counting connected devices alone falsely satisfied a sparse P8 session with an unrelated P1-bound device. Root corrected controller_status to count required joined-station coverage while retaining raw actual count. The focused missing-P8 test passes before/after explicit reassignment. Ambiguous identical-GUID reconnects remain unassigned until explicit pairing; surviving instances never shift stations. Pairing cannot steal another live device's station.

## Pass2: adversarial executable checks

Ran all14 tests in test_stations.py successfully on Windows/Python3.14 with pygame-ce2.5.8. Coverage:

- P8 first; only its score/rank visible and no accidental phantom living players.
- Every count1–8 across all4 maps using non-contiguous station join order and actual rendered frames.
- Simultaneous eight controller Start events; repeated starts preserve all scores/lives/positions.
- Locator retrigger/expiration, pause/guide freeze, closed guide resumption, visible P8 marker and zero locator score.
- Eliminated-player repeat presses, sparse results restart, lobby and quick preset start.
- Score ties retain competition ranks; eight result rows render without clipping.
- Disconnect leaves surviving P2 intact; unique-model reconnect recovers P1 and routes independent directions correctly.
- One or two ambiguous same-model reconnects cannot silently take reserved stations; explicit pairing succeeds.
- Near-end join preserves existing score/remaining clock; result follows expiry. This is tested adaptation policy, not recovered DX policy.
- Identical eight-player fixed-step state after3 seconds using30,60,144Hz display scheduling.

An initial strict equality assertion for locator expiry saw residual2.1e-15 seconds from floating-point arithmetic; corrected the test to numerical tolerance. This was not a reproduced user-visible timing defect.

## Render inspection

Generated and visually inspected work/station-qa-lobby.png, work/station-qa-sparse-find.png and work/station-qa-results.png. Locator rings, arrow and P8 label are visible in the maze. Startup instructions and all eight result rows fit. Inactive station prompts were notably dim in the first capture; reported to root for contrast refinement. This is actual application rendering, not a mockup. No new original-game video sequence was viewed for this QA pass.

## Evidence boundaries

Manufacturer's DX-compatible Start/Find decal establishes the action exists; its exact visual,2-second duration, repeat behavior and game-state availability are still unknown. Immediate free-play late joining, rejecting eliminated rejoins and allowing final-moment joins are explicit adaptation policies. The state model is implementation support, not original-rule certification.

Station ownership is stable within a running session. GUIDs identify controller models, not unique identical devices; no cross-launch physical identity guarantee exists. Manual pairing covers ambiguity but has only synthetic software validation. Physical hotplug/input latency/mixed-device acceptance remains deferred to production by user direction.

No currently reproduced blocking station/lifecycle defect remains after the coverage fix. This does not certify perfect DX fidelity or physical hardware compatibility.

## Fresh native-browser reference pass — revision8

On2026-11-08 this same reviewer opened the actual released-cabinet video [efLgejKG_ls](https://www.youtube.com/watch?v=efLgejKG_ls), using native Chrome and fresh screenshots. This supersedes the earlier statement that this cycle had no new footage inspection. No source video or audio was downloaded. Only a research-comparison screenshot was saved outside the game at work/dx-reference-120s.png, paused2:00.

- At0:15, a POWERUPS/EARTHQUAKE instructional presentation overlays the title artwork, with character imagery and station credit prompts. This is direct attract/instructional evidence, **OBSERVED DX**. Our static lobby and separate guide do not yet reproduce that animated sequence.
- Watching the15–32-second portion showed a camera pan and editorial change into gameplay; it does not expose a continuous physical Start-to-player-gate sequence. Exact join/countdown/release timing remains **UNKNOWN**.
- At1:15 and2:00, the ghost enclosure visibly has two parallel rectangular contours separated by a dark gap, with a small central doorway segment. The initial source-code audit mistakenly called our baseline single-contour: its maze background already supplied an additional visible edge. A first inset patch produced three lines. The final correction clears that background edge and draws exactly two separated contours with a clear doorway. Dimensions/line width remain independently chosen approximations.
- At1:15,1:30 and2:00, cyan wall contours coexist with yellow hatch markings. The camera is across the table, so the main image is rotated relative to the game's logical player orientation; absolute left/right descriptions must account for this.
- The2:00 frame shows a500-point burst. Cause and simultaneous events are obscured; this does **not** verify any500-point scoring rule.
- Large station credit/SWIPE prompts, elongated capsule/U-shaped branches and a hollow rectangular wall island remain visible differences from Neon Nibblers' compact home-input prompts and authored maps. Glare/crop/perspective prevent recovery of full topology from this sample.

Post-fix validation:15 station tests now pass, including an all-four-theme pixel check for both house contours and an open inner doorway. Regenerated and inspected station-qa-sparse-find.png; exactly two deliberately separated outlines and a clear doorway are visible. Reference accuracy still limited to these observations, not full-map/animation equivalence.

### Adversarial correction during comparison construction

The explicit draw-call audit was insufficient: the preserved revision7 rendered house ALREADY has a second visible contour contributed by the maze background. The first revision8 inset-line patch created THREE visible contours. Reported this immediately to root; do not claim that patch improved fidelity. A useful correction must coordinate background and foreground rendering so the final image has the intended two outlines. The comparison figure exposed the mismatch that the pixel-presence test alone missed. Resolved: root clears the background house edge before drawing two explicit contours. Rechecked all four themes for exactly two bright pixel runs and absence of the old background line, plus an unobstructed inner doorway. All15 tests pass. The final figure describes controlled spacing, not an invented missing baseline outline.


Final analytical artifact: outputs/DX-house-comparison-r8.png, outside the playable ZIP, compares a rotated research crop from2:00 with the preserved baseline and current rendered den. Labels explicitly retain perspective/glare and distinguish tested contour count from unverified exact dimensions. No metric perspective correction or full-map equivalence is claimed.
