# Changelog

## Revision 8 — 2026-11-08

- Independent station Start/Find, stable session controller ownership and station-specific missing-device warnings.
- Tie-aware rankings, attributed score event ledger, seeded deterministic replay and movement traces.
- Fixed60Hz native logic; elapsed-time animation interpolation. Fixed autoplay silently deleting dots.
- Versioned explicit map catalog preserves existing routes; no claim of recovered DX geometry.
- Added evidence/history/parity documents and adversarial agent QA; hardware remains deferred.


## Revision 7 – 2026-11-08

- Add explicit development controller-availability stub and development launchers.
- Keep production detection real, with missing/disconnect warnings and keyboard fallback.
- Clear stale disconnect messages on reconnection.
-29 integrated tests and two-pass targeted QA with fix recheck.
- Physical validation deferred to production; simulations are visibly labeled.

## Revision 6 – 2026-11-08

- Correct power icon silhouettes against promotional poster, preserving original artwork.
- Fix gate hatch to yellow across maze themes using newly inspected Deluxe footage.
- Add honest controller-input diagnostic; zero detected devices cannot pass.
- Run real local Ubuntu/WSLg1/2/8 graphics/audio-initialization checks and27 tests on both local OS environments.
- Keep unverified fidelity/hardware issues open pending evidence.

## Revision 5 – 2026-11-08

- Ten reference audits, two same-agent QA passes each, and targeted fix rechecks.
- Thinner walls, reopened upper paths, double-contour gates, station order from manual and tunnel necks.
- Ghost house staging, continuous exits and returning eyes.
- Corrected smoke, skid, local lightning, sheet targeting, quake and magnet categories; corridor fire.
- Normal/equal-size bumps; crossing/crowd fixes; bonus life at10000; respawn transient-state cleanup.
- Seam transparency/giant/collectible fixes and effect clipping protects score text.
-25 integrated tests, native Windows autoplay, Windows/Linux CI and six tracked verification issues.

## Revision 4 baseline

Imported original-code Pygame local1–8-player game with shared corridor/navigation graph, colored characters,11 power categories, four maps, controller/keyboard controls, gates and16 smoke tests.

## Revision10 — 2026-11-08
- All-four-map reference matrix and house-route validation; broad-wall inset contours.
- Fix station-order lightning bias, effect-expiry float tails and stationary/stunned roaming-item pickups.
- Add ten original event sounds with independent channels, immediate mute and graceful mixer failure.
-92 tests, native1/2/8 on all4maps for bothOS, regenerated all-map gameplay tours/replay. Physicalcontrollers deferred; complete DX layout correspondence remains unverified.


## Revision 11 — animation, proportions and fresh DX reference review

Fresh real DX footage was viewed safely through normal browser navigation after using a new tab with a verified address. New60/65/124/135second research captures and the report are recorded in audits/revision11_reference.md; camera edits/glare prevent exact cycle timing and a complete commercial map catalog. Distinct house-side geometry appears with the same cyan palette. Palette selection is now independent of layout: F12 cycles wall colors during play, or use `--palette 0..3`. This changes presentation only, not match logic or routes; default progression remains our approximation.

Fixed the left-facing eye/light flip, missing individual ghost stun feedback and tunnel copies, sorted-item animation identity jumps, short respawn/stage cache slides, and animation continuing during pause/guide/results. All11 power icons now use cached3x procedural artwork and position-independent bob phase. Fire is a continuous layered animated plume with a pale core, clipped to reachable corridor endpoints and split correctly at tunnels. Lightning arcs animate. Exact DX art proportions and timing are still unverified.

110 tests cover artwork/time samples, direction, icon sizes16–96px, ghost states, HUD/tunnels, effects, pause/results, respawn, item tracking,720/1080 resizing and palette changes without logic mutation. Two agent QA passes included discovered clipping and freeze regressions followed by corrections. Native1/2/8 render samples cover every map on Windows and Ubuntu/WSLg. These are short graphics checks, not hardware or performance certification; the final plume styling is also checked by the final render suite and recordings. Physical controllers remain deferred to production.

Each1/2/8-player GIF tours four separate6-second map scenarios (24seconds,288frames). New `gameplay_1_player.mp4`, `gameplay_2_player.mp4` and `gameplay_8_player.mp4` show the same tour at1280x720/60fps with original event audio, avoiding GIF color/frame-rate limits. They are actual computer-controlled game simulations. They do not prove a commercial stage sequence or physical-input compatibility.

Optional recording tools: `python -m pip install -r requirements-capture.txt`, then `python record_video.py --players 8 --seconds 6`. They are unnecessary for playing. Native Windows encoding was tested; playback files can be viewed on Windows/Linux with an H.264/AAC player. The game remains Python/Pygame source, not a standalone executable.

See animation_contact_r11.png, animation_review_r11.gif, fire_animation_r11.png and animation_world_effects.png for tested frame sequences and sizes. The matrices document finite reviewed cases; no exhaustive or perfect-commercial-match claim is made. Full DX topology, scoring/timing/AI, death/growth transitions and operator/spectator/attract systems remain unfinished.


## Revision 12 — reconstructed layouts and cabinet lifecycle

Current production routes are independently reconstructed from two full DX spectator views at68/73seconds in the IAAPA2022 source. All four color profiles use these two families; unsupported authored routes are retired. Quantization and glare-hidden endpoints remain approximate; no complete commercial catalog or pixel identity is certified. Ghost house paths, tunnels and bays now derive from each profile's geometry. Actual-width render checks caught and fixed erased wall stems, and new bay positions required a dynamic central HUD clearance fix.

AI actors were observed alongside join prompts. Vacant stations now have configurable AI opponents; human counts, controls, credits and rankings remain distinct. Human takeover resets bot scores, carried weapons and growth; eliminated humans cannot revive through Start. All-human elimination ends a match even if bots survive. Exact DX difficulty/replacement rules remain unknown.

Implemented smooth growth/shrink, death dissolve, bay arrival feedback, saved operator settings, credits/free play, persistent local human scores with failure retry, original idle instructional/high-score attract pages and optional spectator mirrors/ranking windows. Their detailed UI/timing are original adaptations. Native game+spectator pairs ran on Windows and Ubuntu/WSLg.

151 tests pass locally on both OS environments. Twelve complete automated human/AI matches ended with reconciled event totals and human-only rankings; native1/2/8 checks cover all four profiles on both systems. Physical controllers remain deferred to production. Current recordings use1/2/8 logical human slots with7/6/0 AI opponents; all actors are computer-controlled during capture.

Current acceptance/evidence boundaries are in DX_RELEASE_STATUS.md. Software features are implemented and tested; exact commercial score/multiplier values, timings, AI, joining/progression rules, full map inventory and overhead content by state remain unverified. Open evidence issues are not administratively closed to claim completion.
