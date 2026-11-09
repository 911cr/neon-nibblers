# Revision 13 contour comparison

The latest research figure `outputs/DX-maze-comparison-r13.png` compares the complete68s/73s source boards with identical local geometry before and after rounded capsule/branch-end correction. This fixes a demonstrable square-tip discrepancy while preserving every tested route and thin stem. Fourteen map tests pass. See `audits/revision13_maps.md` for both review passes and explicit remaining uncertainty.

> Current status: see DX_RELEASE_STATUS.md. Earlier revision sections are historical.

# Revision 12 comparison update

Complete spectator-screen references at [1:08](https://www.youtube.com/watch?v=-cNOhumVZ74&t=68s) and [1:13](https://www.youtube.com/watch?v=-cNOhumVZ74&t=73s) now support two independently traced layouts. Source A has the large upper arch and two paired side-tunnel rows; B has the upper central T and one paired central tunnel row. Both have eight bays and a central top-opening house. These replace the previous cyan and violet authored graphs. Golden reuses observed family A and ember reuses family B with original palettes. There are two observed topologies and four palette profiles, not four verified commercial maps.

The new comparison figure is a research artifact outside the runnable ZIP. Red dots over perspective-normalized source frames show the exact independently authored movement graph; adjacent panels show actual app-rendered backgrounds. It is an evidence comparison, not a claim of pixel equivalence. Remaining differences include original character/art styling, approximate line width/rounding, grid-quantized coordinates, palette choices, and the unknown complete commercial catalog.

---

## Earlier comparison history

# DX visual comparison record

Updated 2026-11-08. Keep original branding and independently authored art. A passing software test is not a visual parity verdict.

## Preserved baseline

Revision 7 is commit `0f9c3c9`. Baseline source tests passed 29/29 before changes. Existing 1/2/8-player clips, preview and arena sheet were preserved in `work/revision8-baseline`. These are actual rendered simulations; neither physical controller input nor commercial matching is implied. `map_catalog_v1.png` is a geometry/debug diagram, not gameplay.

## Reference checkpoints and meaningful differences

| Area | Reference / timestamp | Current implementation and difference | Status / next comparison |
|---|---|---|---|
| Wall structure | [Front-facing projector reference](https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s), 1:34 | Thin capsule/L/T outlines improved in revision 5, but broad hooked blocks and small square islands remain authored | **OBSERVED**, non-DX supporting view. Need a full confirmed DX frame before reconstructing topology. |
| Gates | [Released DX cabinet](https://www.youtube.com/watch?v=efLgejKG_ls&t=75s), 1:15 / 1:30 / 2:00 | Yellow hatches are now independent of wall palette. Exact gate dimensions, opening timing and animation remain approximations | Hatch color **OBSERVED DX**; operation **UNKNOWN**. Continuous same-station entry/death/respawn sequence needed. |
| Outer border | [Cabinet reference](https://www.youtube.com/watch?v=GhSV1oQVA6g&t=57s), 0:57 | Twin contours and tunnel necks exist; outer corners still relatively square, unlike softer shapes in earlier review | Observation inherited from prior audit; configuration uncertain. Align a perspective-corrected full board before tuning. |
| Characters | Same cabinet 0:57 and projector 1:34 | Procedural shaded bodies, animated wedge mouths, directional eyes. Giant overhang and original proportions are not measured | **IMPLEMENTED AND TESTED** / exact shape and timing **UNKNOWN**. Compare a multi-frame normal/giant sequence, not one still. |
| Ghost house | Projector 1:34 | Four visible occupants and continuous return implemented; initial coordinates/release order are authored | **UNKNOWN DX**. Confirm house-only clip through all four exits. |
| Scores/stations | [DX manufacturer manual](https://www.bmigaming.com/Games/Manuals/namco/Pac-Man-Battle-Royale-Chompionship-Deluxe-Video-Arcade-Game-Manual-Bandai-Namco.pdf), control-panel diagram | Station/color order follows documentation; on-screen score size, placement, animation and leaderboard are not measured | Station diagram **VERIFIED DX**; display dimensions **UNKNOWN**. Capture startup/play/results at comparable counts. |
| Startup | [Manufacturer DX parts](https://bandainamco-am.com/collections/pac-man-battle-royale-deluxe), eight Find My Pac/Start decals | Baseline is a count-selected text lobby; independent station actions were missing | Action existence **VERIFIED DX**; exact join/locator animation **UNKNOWN**. Current engineering cycle addresses independent station control. |

No new reference video frame was captured in this map audit: the web reader could not retrieve the footage. Prior audits contain the actual observation history. Do not label this document an aligned side-by-side original/game comparison, or manufacture a reference image from a description. Reference capture, corner selection, perspective correction and frame-sequence comparison remain an explicit gap.

## This cycle: geometry provenance, not cosmetic certification

The map data migration preserves all four graphs exactly. There is therefore intentionally no claimed visual improvement from that migration alone. The new [catalog diagram](images/map_catalog_v1.png) exposes station order, topology and house placement for future corrections. The remaining visible discrepancies above stay open.

For each future reconstructed map, store a reference record with URL, cabinet/version confidence, exact timestamp, unobstructed corner coordinates and observation notes. Keep independently generated output captures separate. Compare equivalent player counts/states, normalize the playfield rectangle, annotate topology differences first, then wall width, sprites and HUD. Test collision edges against the revised rendered walls, regenerate moving clips and repeat critical review.

## Review outcome

First pass: verified the migration is data-only and preserves reachable routes. Second pass: checked the claim boundary; existing screenshots do not prove any DX transition rule, and four differently colored reflected maps do not establish a commercial map catalog. Full-frame reference reconstruction and aligned 4/8-player/startup comparison remain high-priority work, not completed items.

## Integrated station/UI comparison

![Local revision-7/revision-8 startup, P8-first join and results comparison](images/station_before_after_r8.png)

This comparison uses our own revision-7 lobby as the baseline. The new per-station controls, pairing prompt, first-player P8 and ranking list are visible. The ranking panel uses assigned test scores; it is explicitly labeled a controlled scene, not a completed match. This is deliberately not labeled a commercial-game comparison. The companion `gameplay_4_player.gif` records eight seconds of actual four-player simulation (96 frames, seed 24); frames at 0, 3.3 and 6.7 seconds were visually inspected. See `audits/revision8_maps.md` for tested cases and the reproduced, corrected and rechecked locator clipping.

## Revision 9 cyan topology correction

![Local cyan-map correction: before and after](images/map_before_after_r9.png)

Unlike the revision-8 data migration, this changes playable routes. Actual cabinet frames at [2:00](https://www.youtube.com/watch?v=efLgejKG_ls&t=120s) and [1:15](https://www.youtube.com/watch?v=efLgejKG_ls&t=75s) show the house separated from nearby branches by a corridor and distinct vertical wall islands. The view is rotated 180 degrees relative to our house entrance; the two raw-left vertical islands therefore belong on the game's right. Our revised cyan map opens the house perimeter and separates these walls. The figure above compares our old/new output; it does not pretend the estimated grid is a perspective-perfect original trace. See `audits/revision9_maps.md` for the tested change and remaining uncertainty.

## Revision 10: all four maps, broad-wall styling

![Every map before/after the broad-wall contour change](images/all_maps_before_after_r10.png)

Each row uses identical local geometry and frame state, comparing revision-9 rendering with revision-10 rendering. All four were separately reviewed against retained DX frame details. Violet's broad rectangle provides the clearest observed-style correction: its inner outline is now distinct from its outer outline, as on the rectangular island visible at 1:15. Applying this treatment to broad bent walls is an inferred style choice, not a measured commercial match. Thin capsules, ghost-house contours and gates are unchanged. See [the per-map evidence/difference matrix and pixel checks](audits/revision10_all_maps.md). No fresh video or exact four-map DX correspondence is claimed.


## Fresh released-DX enclosure comparison

The subsequent native-browser review did obtain new reference imagery, superseding the map-audit access limitation above. Actual efLgejKG_ls frames at75/90/120s were inspected, plus the15s instruction presentation. The research figure `outputs/DX-house-comparison-r8.png` is delivered separately from the playable ZIP. It contains a120s enclosure crop, rotated180 degrees for doorway orientation, beside baseline/current game crops. Perspective and glare remain; images are resized for inspection without invented geometric reconstruction.

The figure caught an initial regression: baseline already had two visible contours contributed by background and foreground layers; simply adding an inset produced three. Final rendering clears the background house edge and explicitly draws two consistently separated contours. All-four-theme checks count exactly two bright runs, reject the old third line and verify the inner doorway stays open. This is controlled render correction, not proof of exact commercial line dimensions, topology, actor states or animation.


## Fresh released-DX house comparison and corrective review

The reference reviewer subsequently accessed the actual video in native Chrome, inspecting15/75/90/120seconds. A research screenshot at2:00 supports the observed two house contours; the separate `outputs/DX-house-comparison-r8.png` figure compares this crop with our baseline/current rendering. It retains camera perspective/glare and is not part of the playable ZIP or commercial game assets. It does not establish exact proportions or complete map topology.

The first proposed inset outline was wrong: our background already supplied an outer edge, so the change produced three lines. Actual crop review exposed this despite a passing draw-location test. The correction clears the background house edge, then draws exactly two explicit contours and an open inner doorway. The final regression counts visible bright runs, rather than treating two drawing calls as proof. This cycle demonstrates why rendered comparison and critical retesting matter.


## Revision 11 â€” animation, proportions and fresh DX reference review

Fresh real DX footage was viewed safely through normal browser navigation after using a new tab with a verified address. New60/65/124/135second research captures and the report are recorded in audits/revision11_reference.md; camera edits/glare prevent exact cycle timing and a complete commercial map catalog. Distinct house-side geometry appears with the same cyan palette. Palette selection is now independent of layout: F12 cycles wall colors during play, or use `--palette 0..3`. This changes presentation only, not match logic or routes; default progression remains our approximation.

Fixed the left-facing eye/light flip, missing individual ghost stun feedback and tunnel copies, sorted-item animation identity jumps, short respawn/stage cache slides, and animation continuing during pause/guide/results. All11 power icons now use cached3x procedural artwork and position-independent bob phase. Fire is a continuous layered animated plume with a pale core, clipped to reachable corridor endpoints and split correctly at tunnels. Lightning arcs animate. Exact DX art proportions and timing are still unverified.

110 tests cover artwork/time samples, direction, icon sizes16â€“96px, ghost states, HUD/tunnels, effects, pause/results, respawn, item tracking,720/1080 resizing and palette changes without logic mutation. Two agent QA passes included discovered clipping and freeze regressions followed by corrections. Native1/2/8 render samples cover every map on Windows and Ubuntu/WSLg. These are short graphics checks, not hardware or performance certification; the final plume styling is also checked by the final render suite and recordings. Physical controllers remain deferred to production.

Each1/2/8-player GIF tours four separate6-second map scenarios (24seconds,288frames). New `gameplay_1_player.mp4`, `gameplay_2_player.mp4` and `gameplay_8_player.mp4` show the same tour at1280x720/60fps with original event audio, avoiding GIF color/frame-rate limits. They are actual computer-controlled game simulations. They do not prove a commercial stage sequence or physical-input compatibility.

Optional recording tools: `python -m pip install -r requirements-capture.txt`, then `python record_video.py --players 8 --seconds 6`. They are unnecessary for playing. Native Windows encoding was tested; playback files can be viewed on Windows/Linux with an H.264/AAC player. The game remains Python/Pygame source, not a standalone executable.

See animation_contact_r11.png, animation_review_r11.gif, fire_animation_r11.png and animation_world_effects.png for tested frame sequences and sizes. The matrices document finite reviewed cases; no exhaustive or perfect-commercial-match claim is made. Full DX topology, scoring/timing/AI, death/growth transitions and operator/spectator/attract systems remain unfinished.


## Revision 12 â€” reconstructed layouts and cabinet lifecycle

Current production routes are independently reconstructed from two full DX spectator views at68/73seconds in the IAAPA2022 source. All four color profiles use these two families; unsupported authored routes are retired. Quantization and glare-hidden endpoints remain approximate; no complete commercial catalog or pixel identity is certified. Ghost house paths, tunnels and bays now derive from each profile's geometry. Actual-width render checks caught and fixed erased wall stems, and new bay positions required a dynamic central HUD clearance fix.

AI actors were observed alongside join prompts. Vacant stations now have configurable AI opponents; human counts, controls, credits and rankings remain distinct. Human takeover resets bot scores, carried weapons and growth; eliminated humans cannot revive through Start. All-human elimination ends a match even if bots survive. Exact DX difficulty/replacement rules remain unknown.

Implemented smooth growth/shrink, death dissolve, bay arrival feedback, saved operator settings, credits/free play, persistent local human scores with failure retry, original idle instructional/high-score attract pages and optional spectator mirrors/ranking windows. Their detailed UI/timing are original adaptations. Native game+spectator pairs ran on Windows and Ubuntu/WSLg.

151 tests pass locally on both OS environments. Twelve complete automated human/AI matches ended with reconciled event totals and human-only rankings; native1/2/8 checks cover all four profiles on both systems. Physical controllers remain deferred to production. Current recordings use1/2/8 logical human slots with7/6/0 AI opponents; all actors are computer-controlled during capture.

Current acceptance/evidence boundaries are in DX_RELEASE_STATUS.md. Software features are implemented and tested; exact commercial score/multiplier values, timings, AI, joining/progression rules, full map inventory and overhead content by state remain unverified. Open evidence issues are not administratively closed to claim completion.


## Revision 13 — source measurements, rounded walls and scoring/AI corrections

Fresh confirmed DX footage43DcDXxEgzk was reviewed at quarter speed and paused positions. At9:22 red144640 has four ordinary dots ahead; at9:23 the corridor is cleared and score144680. This OBSERVED DX aggregate supports10 per ordinary dot; it does not recover other score awards or multipliers. At9:23–9:34 the final-life station displays CONTINUE/COIN while AI moves, followed by alphabet/name entry by9:45. No purchased continue, restored-life policy or score retention was observed. The fresh red full-board9:34 is independently identified as existing family A, corroborating color/layout independence, not adding a third maze. Candidate power sequences were rejected as exact duration measurements because of refreshes, occlusion and transition ambiguity. See audits/revision13_reference.md.

Rounded capsule ends and convex branch corners now retain narrow stems and the same validated corridor graph. Removed a faint third house underlay contour; actual-App scans require exactly two house borders on all four profiles. New comparison research images remain outside the runnable package. Exact20px quantization/hidden endpoints, source widths, full commercial catalog and progression remain unverified.

Corrected ledger totals after bot-to-human takeover: historical bot awards remain recorded, while station_join starts the new score account at zero. HUD, spectator rankings and ledger agree. Tested simultaneous dot/power/ghost/rival/bonus awards, duplicate fire attackers, expiry contact, carried ownership and same-tick damage. Bot routing now uses deterministic weighted legal paths, avoiding nearby lethal ghosts/giants/carried rival weapons and actively seeking capturable ghosts with Magnet. This improves our original strategy; exact DX difficulty/targeting remains unknown.

Power durations, movement intervals, ranges, slowdown multipliers and item cadence/cap are now validated per-Match tuning settings, loadable with --tuning tuning.example.json. Complete effective values and pickup duration/nominal expiry are captured in event logs/replays; quickstart and station START honor the same settings. Existing numerical defaults remain explicitly approximate. The on-screen guide reflects effective durations.

Added optional --untimed life-survival mode, also operator time limit0. Default180s remains an explicit custom score-attack mode, not a certified DX limit. Untimed progression, pause, elimination, spectator labels and replay are covered; CLI mode overrides do not silently rewrite saved operator settings. Exact final-life continue interval and background AI before original name entry remain a known presentation/behavior difference; no invented paid-continue policy is claimed.

Results now offer N for original three-letter initials for this session's qualifying top20 human rows. Atomic renaming uses session/player identity, protecting ties and historical/legacy rows. Failed writes roll back; cancelling discards only the active draft. Immediate replay and pending score-save retries remain intact. Exact cabinet entry UI, timeout and physical-controller entry are not reproduced or certified.

Final validation:187 tests passed on Windows and Ubuntu/WSLg, with source-frozen extracted-ZIP verification recorded separately. Native1/2/8 runs cover every profile on both systems, plus actual game/spectator pairs with audio initialization. Twelve complete automated human/AI matches reconcile ledger totals and rankings. Three48-second1280x720/60fps MP4s with original AAC event audio fully decode;24-second GIF previews and12-frame profile/count contact sheet were checked. All recording actors are automated; logical1/2/8 human stations have7/6/0 AI. Physical controllers, human multiplayer acceptance and audible speaker assessment stay in production.

Agent reviews ran initial and deeper passes with targeted fixes/rechecks. Their approval covers tested implementation scope, not undocumented original rules. Remaining exact scoring/power/AI/map/continue questions are tracked honestly; no perfect-match or zero-issues claim.
