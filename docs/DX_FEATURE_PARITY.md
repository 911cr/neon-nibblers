> Current status: see DX_RELEASE_STATUS.md. Earlier revision sections are historical.

# DX feature parity — revision 8 working assessment

Baseline: `0f9c3c98e097d2fb16b058896ba872b31783d2ed`, 29 smoke checks passed locally on 2026-11-08. Previous gameplay/screenshots preserved in `work/revision8-baseline` (local evidence, not distributed commercial media). This assessment precedes broad changes. Original branding, graphics, code and sounds remain required.

Statuses are independent: **VERIFIED DX**, **OBSERVED DX**, **HISTORICAL ONLY**, **INFERRED**, **UNKNOWN** describe reference evidence; **IMPLEMENTED AND TESTED**, **BLOCKED** describe our engineering. Passing our own tests never upgrades reference confidence.

| ID / subsystem | Reference behavior / evidence | Baseline implementation | Difference / priority / status | Required verification / next action |
|---|---|---|---|---|
| JOIN-01 stations | DX manufacturer parts list names Start/Find My Pac for eight colors; [manufacturer](https://bandainamco-am.com/collections/pac-man-battle-royale-deluxe), no timestamp, primary | Count selection starts P1..Pn together | P0; action existence VERIFIED DX; join windows UNKNOWN | Independent stations, stable identity, simultaneous starts, no eliminated-player resurrection; test explicit approximation |
| JOIN-02 locator | Same primary evidence; animation, timing and cooldown UNKNOWN | No locator | P0 missing | Original readable highlight, configurable duration; footage needed for matching appearance |
| LIFE-01 lifecycle | DX operation manual documents operator setup; full startup/results behavior not established | Lobby, active, pause, guide, results; 180-second score attack | P0; timer/end conditions UNKNOWN | Formal states, late join/pause/results tests; do not inherit 2011 rounds |
| MAP-01 geometry | Prior timestamped audits: efLgejKG_ls 75/120s released DX; JSp72DKyW5U 94s mobile, not DX proof | Four runtime mirrors of authored paths | P0; OBSERVED DX thin walls, UNKNOWN full topology | Explicit versioned geometry, baseline-equivalence checks; reconstruct only from identifiable frames |
| MAP-02 transitions | Complete repeat DX sequences not yet recovered | Dot clear awards survivors500 and advances fixed theme order | P0; UNKNOWN, implemented custom | Catalog persistence/trigger/order policy, all1..8 counts across maps |
| SCORE-01 awards | Exact pellet/power/ghost/rival/clear values not established | 10/75/200/300/500 scattered score mutations | P0; UNKNOWN | Central event ledger, time/stage/context, deterministic replay and score reconciliation |
| SCORE-02 ranking | Individual scores supported CHOMP material; tie/end display unknown | Highest score overlay; no persisted high scores | P1 UNKNOWN details | Ranked results with ties; keep persistence/operator controls tracked |
| GATE-01 | efLgejKG_ls75/90/120s yellow hatches on cyan pockets (prior direct inspection) | Yellow hatches, twin contours, owner-only .8s release/reentry | P1; OBSERVED DX appearance, UNKNOWN permissions/timing | Retain tests; obtain continuous death-to-release evidence; issue2 |
| POWER-01 inventory | CHOMP promotional poster and published11-category list (see reference evidence) | All11 original procedural icons/effects | P1 IMPLEMENTED AND TESTED; descriptions do not verify edge cases | Full interaction matrix and measured sequences; issue4 |
| POWER-02 timing/spawns | Prior footage GhSV1oQVA6g95–101s moving peel/interior orbs, DX identity uncertain | Fixed3s/cap12, corner orbs, roaming others | P1 UNKNOWN cadence/weights/orb exception | Configurable approximations; multi-session event census; issue3 |
| GHOST-01 | House occupancy observed mobile94s; exact DX order/AI unknown | Four ghosts, staged exit/eyes return, greedy chase | P1 UNKNOWN exact rules | Preserve lifecycle checks; collect DX start/return sequence; issue5 |
| MOVE-01 | No calibrated DX speed/turn/bounce measurement | Tile updates, buffered turns, wrap, bump; variable render dt | P1 UNKNOWN reference values | Fixed simulation driver/replay; timing equivalence across render rates |
| ART-01 | Slim outlined maze, shaded bodies, stations observed in prior audits | Procedural spheres/ghosts/powers, custom map silhouettes | P0 remaining topology/display differences | Sequence comparisons, not beauty-image certification; issue1 |
| AUDIO-01 | Exact DX cues/layers unmeasured | Three synthesized tones | P2 incomplete original sound design | Layer event cues; audible review remains unverified |
| CTRL-01 | Manufacturer station colors/order documented | Connection-order mapping shifts on unplug | P0 implementation defect | Stable per-session station ownership; explicit pairing for indistinguishable devices; mocked tests separate physical acceptance |
| DISPLAY-01 | 75-inch central and two overhead displays documented; overhead content UNKNOWN | Single resizable window | P2 missing spectator architecture | Avoid claiming mirrors; define independent view model before optional second window |
| OP-01 | Manual service/operator settings | No credits/settings/high-score storage | P2 partial | Research defaults/options before implementing operator configuration |
| QA-01 | No cabinet available; physical controllers deferred by user | Windows/Linux CI, WSLg native graphics,29 tests | IMPLEMENTED AND TESTED software; BLOCKED physical acceptance | Expand1..8 all maps, native captures, replay, maximum-load timing; issue6 production validation |

Architecture: `Arena` owns lanes/bays/portals; `Match` mutates rules/timers/players/ghosts; `App` handles SDL devices, menu events, rendering and synthesized sounds; `arcade_art.py` draws independently authored assets. Tests cover internal rules, not DX identity. Existing audit history and all six open GitHub issues were inspected; no issue is closed solely because its code runs.

## After implementation and critical review

| IDs | Revision8 change/status | Verification and before/after evidence | Remaining next action |
|---|---|---|---|
| JOIN-01/02, CTRL-01 | **IMPLEMENTED AND TESTED** independent starts, sparse identities, locator, per-session stable bindings, explicit pairing |15 station checks; local before/after `station_before_after_r8.png`; wrong-station availability bug fixed; top-bay locator clipping fixed/rechecked | DX join windows and locator dimensions/timing **UNKNOWN**; physical acceptance deferred |
| SCORE-01/02 | **IMPLEMENTED AND TESTED** central ledger, separate score popups, tied rankings, deterministic traces/replay |12 ledger tests; sample720-frame replay; rendering cannot mutate score/state; autoplay dot-deletion defect fixed | Exact DX awards, bonus repetition and results/high-score behavior **UNKNOWN** |
| MAP-01/02 | **IMPLEMENTED AND TESTED** explicit versioned geometry and progression modes |7 map tests, all1–8counts×4maps, baseline route equivalence and64 locator cases | Geometry remains authored and visually different; continuous DX map census still required |
| MOVE-01 | **IMPLEMENTED AND TESTED**60Hz application logic and elapsed-time visual interpolation |Same state/events at30/60/144Hz; pause/guide freeze checks | Commercial speeds, bounce magnitudes and turn timing **UNKNOWN** |
| ART-01/GHOST-01 | Two explicit enclosure contours after actual-pixel review caught redundant background overlap; freshly inspected DX video75/120s |All-theme contour/doorway pixel check; actual new reference screenshot retained as research evidence; separate annotated house comparison | Exact house proportions, ghost appearance/AI and complete maze still differ/unknown |
| LIFE-01 | Explicit state dispatch and transition table; **IMPLEMENTED AND TESTED** adaptation |Repeated simultaneous starts, last-moment joins, results/rematch, elimination and pause tested | Credit/join policy not verified DX; full attract instructional sequence missing |
| QA-01 |63 checks; new native Windows/Ubuntu1/2/8 renders, stress scenario and updated clips |See DX_TEST_REPORT and latest TEST_RESULTS.txt for actual run outcomes; three agents plus fix/retest passes | No physical or exact-fidelity certification |

Fresh source at15seconds of [released DX footage](https://www.youtube.com/watch?v=efLgejKG_ls&t=15s) shows an animated power-up instructional attract overlay. This makes the missing full attract sequence an observed discrepancy, rather than a purely inferred polish task. Operator controls, persistent high scores, original layered audio and spectator views remain open scope. No unchanged feature in the baseline table is silently promoted to verified DX.


## Revision 9 — 2026-11-08

Fixed scores/lives/start prompts overlapping gate bounds, including giant locator clearance and long score values. Cyan Circuit map revision2 opens the continuous house perimeter and separates two nearby vertical wall sections, informed by real DX footage at75/120seconds after180-degree orientation normalization. Exact coordinates remain estimated and the full DX topology is still unresolved.

Preserved movement timer remainders and boundary precision: normal movement now10cells/s, caffeine15 and banana18 under the configured approximation, versus8/15/15 previously. Damage cues now follow damage events even when another player earns a life simultaneously. Lightning ignores inactive stations.

72 tests pass locally on Windows and Ubuntu. New native300-frame1/2/8 runs used real Windows/X11 drivers; Windows58.39/60.27/59.93FPS; UbuntuWSLg34.49/33.64/45.20FPS under concurrent capture load. Physical controllers remain deferred. Three agents performed reference/code reviews, deeper QA and rechecks. No perfect-match claim.

The separate1/2/8-player clips now show corrected Cyan Circuit,12seconds each; the montage covers allfourmaps. `hud_before_after_r9.png` and `map_before_after_r9.png` are controlled local before/after comparisons. A new reference-only figure outside the gameZIP records actual footage observations. Replay sample regenerated after timing changes.


## Revision 10 — all-map review and simultaneous interactions

Reviewed all four authored maps against retained real DX75/120second frames. The footage does not establish four complete DX layouts; a fresh viewing attempt was stopped by browser URL-verification policy. No unsupported geometry changes were made. Every map already has a continuous house perimeter; the catalog now validates those routes and door approaches. Broad wall interiors have an inset contour based on the visible rectangular-island style; application to broad L-shaped walls remains an explicit visual approximation. No floor, frame, gate or house-outline pixels changed in the comparative render QA. See audits/revision10_all_maps.md for the four-row evidence matrix.

Fixed lightning outcomes depending on station order, tiny floating-point power/safety expiration tails, roaming collectibles not collecting on stationary/stunned players, and same-tick bonus credit after that contact. Added ten original layered event cues on separate channels. Mute stops active cues immediately; unavailable audio is handled gracefully. Sounds are synthesized locally, not commercial recordings. Audible speaker quality and physical controllers remain unverified/deferred.

92 automated tests pass locally on Windows and Ubuntu. Actual native1/2/8 rendering runs now cover all four maps (12 short120-frame scenarios on each OS). These are startup/render samples, not benchmarks or human gameplay certification. The supplied1/2/8-player GIFs each show four separate seeded6-second map scenarios (24seconds total); they do not assert that the commercial game uses that stage sequence. All game GIFs are silent. sound_preview.wav demonstrates the original cues.

Source, event replay and captured gameplay were regenerated after the simulation fixes. Complete commercial geometry, exact scoring/timing/AI, stage transitions, joining windows, attract/operator and spectator behavior remain open evidence/work items. Physical controller acceptance stays in production.


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


## Revision 13 — source measurements, rounded walls and scoring/AI corrections

Fresh confirmed DX footage43DcDXxEgzk was reviewed at quarter speed and paused positions. At9:22 red144640 has four ordinary dots ahead; at9:23 the corridor is cleared and score144680. This OBSERVED DX aggregate supports10 per ordinary dot; it does not recover other score awards or multipliers. At9:23–9:34 the final-life station displays CONTINUE/COIN while AI moves, followed by alphabet/name entry by9:45. No purchased continue, restored-life policy or score retention was observed. The fresh red full-board9:34 is independently identified as existing family A, corroborating color/layout independence, not adding a third maze. Candidate power sequences were rejected as exact duration measurements because of refreshes, occlusion and transition ambiguity. See audits/revision13_reference.md.

Rounded capsule ends and convex branch corners now retain narrow stems and the same validated corridor graph. Removed a faint third house underlay contour; actual-App scans require exactly two house borders on all four profiles. New comparison research images remain outside the runnable package. Exact20px quantization/hidden endpoints, source widths, full commercial catalog and progression remain unverified.

Corrected ledger totals after bot-to-human takeover: historical bot awards remain recorded, while station_join starts the new score account at zero. HUD, spectator rankings and ledger agree. Tested simultaneous dot/power/ghost/rival/bonus awards, duplicate fire attackers, expiry contact, carried ownership and same-tick damage. Bot routing now uses deterministic weighted legal paths, avoiding nearby lethal ghosts/giants/carried rival weapons and actively seeking capturable ghosts with Magnet. This improves our original strategy; exact DX difficulty/targeting remains unknown.

Power durations, movement intervals, ranges, slowdown multipliers and item cadence/cap are now validated per-Match tuning settings, loadable with --tuning tuning.example.json. Complete effective values and pickup duration/nominal expiry are captured in event logs/replays; quickstart and station START honor the same settings. Existing numerical defaults remain explicitly approximate. The on-screen guide reflects effective durations.

Added optional --untimed life-survival mode, also operator time limit0. Default180s remains an explicit custom score-attack mode, not a certified DX limit. Untimed progression, pause, elimination, spectator labels and replay are covered; CLI mode overrides do not silently rewrite saved operator settings. Exact final-life continue interval and background AI before original name entry remain a known presentation/behavior difference; no invented paid-continue policy is claimed.

Results now offer N for original three-letter initials for this session's qualifying top20 human rows. Atomic renaming uses session/player identity, protecting ties and historical/legacy rows. Failed writes roll back; cancelling discards only the active draft. Immediate replay and pending score-save retries remain intact. Exact cabinet entry UI, timeout and physical-controller entry are not reproduced or certified.

Final validation:187 tests passed on Windows and Ubuntu/WSLg, with source-frozen extracted-ZIP verification recorded separately. Native1/2/8 runs cover every profile on both systems, plus actual game/spectator pairs with audio initialization. Twelve complete automated human/AI matches reconcile ledger totals and rankings. Three48-second1280x720/60fps MP4s with original AAC event audio fully decode;24-second GIF previews and12-frame profile/count contact sheet were checked. All recording actors are automated; logical1/2/8 human stations have7/6/0 AI. Physical controllers, human multiplayer acceptance and audible speaker assessment stay in production.

Agent reviews ran initial and deeper passes with targeted fixes/rechecks. Their approval covers tested implementation scope, not undocumented original rules. Remaining exact scoring/power/AI/map/continue questions are tracked honestly; no perfect-match or zero-issues claim.
