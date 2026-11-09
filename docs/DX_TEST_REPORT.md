> Current status: see DX_RELEASE_STATUS.md. Earlier revision sections are historical.

# Revision 8 verification and remaining work

2026-11-08. Baseline `0f9c3c9` passed29 checks before changes; previous captures were preserved. Read the complete master directive, source/scripts, historical audits, results and six existing GitHub issues. No restart or replacement project was made.

## Engineering cycles

1. Research found manufacturer Start/Find decals and independent station wiring, but no definitive joining window or locator animation. Implemented per-station actions, sparse rosters and explicit approximation timing. Two-pass station QA found a false-positive availability check for a controller assigned to the wrong station; fixed and retested. Same-GUID reconnect ambiguity remains explicit and requires pairing.
2. Centralized all score mutations into an attributed event ledger. Replay exposed an old autoplay helper that removed the current dot without scoring; fixed it. Reviewed simultaneous awards, immunity, damage, ties, bonus lives and sparse joins; rendering now consumes individual score events rather than lumping all changes into one popup. Paused/guide states do not consume logic or locator time.
3. Serialized existing maps into validated explicit records. This preserves authored routes, not a reconstruction of DX. All1–8 counts and transitions exercised. Render review found the top-bay locator label clipped above the screen; it now flips below the character.64 station/map/size label cases pass.
4. Fresh released-DX video inspection at75/120seconds identified double ghost-house contours. A first implementation accidentally produced three visible contours because the background already contributed one. Side-by-side review caught that mistake. The final renderer clears the background house edge before drawing two explicit contours with an open doorway; pixel-run checks guard against a third line. Exact dimensions remain custom. See the reference/visual documents for the source and observation limits.

## Evidence and tests

Run `python -m unittest discover -p "test*.py" -v`. The expanded suites exercise original smoke rules, map validation, score/replay and station lifecycle. The final suite has63 checks including the dedicated visible house-contour/doorway regression. See TEST_RESULTS.txt for platform and extracted-package outcomes.

-1–8 independently joined participants ×4 maps; sparse P8/P4 ownership, all32 count/map combinations, transitions and preserved scores/lives.
- All11 power categories and interaction checks; no assertion that unknown ranges/timers are exact DX values.
- Every scoring route, no phantom score for immune/repeated damage, equal-rank ties, event totals and exact popup attribution.
- Replay seeds1–8,1/2/4/8×4maps, sparse joining and corrupted-replay rejection. Supplied12-second replay has720frames and verified events/movement fingerprints.
- Actual `App.advance` at30/60/144Hz produces the same180 logic ticks and complete state/event digest over3seconds.
- Same-frame eight Start presses; repeated Find; pause/guide; last-moment join; eliminated player cannot regain lives; results/new session.
- Synthetic disconnect/unique reconnect/ambiguous identical-GUID pairing and missing-controller coverage. These are software tests, not physical USB acceptance.

## Native rendered runs

Each count rendered600frames on the actual platform display, with audio initialized44.1kHz signed16 stereo. Physical input was not used and audibility was not confirmed. These are samples under desktop/capture load, not performance guarantees.

| Platform |1player|2players|8players| Evidence |
|---|---:|---:|---:|---|
| Windows SDL |59.54FPS|60.08FPS|60.16FPS|`NATIVE_REVISION8_Windows.json`|
| Ubuntu/WSLg X11 |40.25FPS|39.17FPS|61.54FPS|`NATIVE_REVISION8_Linux.json`|

These native runs preceded the final house-outline-only correction. Final captures and headless render checks include it. Linux WSLg is not standalone Linux hardware acceptance.

Additional headless stress:360frames,8giants with combined effects,4ghosts,12item cap,121smoke cells and8zap effects rendered at95.46frames/s after cache warmup. This is explicitly a dummy-driver render stress result, not native FPS. See STRESS_REVISION8.json. It confirms bounded execution under this scenario, not every possible load.

## Application state policy

| State | Station Start/Find | Enter | Pause/guide | Escape |
|---|---|---|---|---|
| Attract/lobby | Start one station | Start quick-play preset | F1 guide | Quit |
| Playing | Unjoined joins; living joined locates; eliminated does nothing | No reset | P pause/F1 guide | Lobby |
| Paused | Blocked; locator frozen | No reset | P resume/F1 guide | Lobby |
| Guide | Blocked; logic frozen | Existing keyboard behavior preserved | F1 closes | Close guide |
| Results | New session for pressed station | Replay preset | Guide available | Lobby |

These are explicit free-play adaptation choices. Exact DX late-join/final-moment/results rules remain UNKNOWN. Device ownership is independent from the joined roster; inactive slots never receive points or lives. Bindings are session-local; persisted serial-number-based cabinet assignment is not implemented.

## Remaining discrepancies and next actions

The project is not complete or certified identical. Highest priority: continuous confirmed-DX footage across joins, isolated score events and multiple map transitions. Current topology is still authored; score values,3-minute end rule, gate timing/permissions, power timings and ghost AI remain approximations. An annotated house-crop research comparison was completed from actual DX footage, retaining camera glare/perspective. A full-field commercial-versus-game alignment remains incomplete. Local before/after images are labeled accordingly.

Still missing: credits/operator UI, persistent high scores, full attract demonstration, layered original audio, comprehensive UI/input replay and optional independent spectator windows. Overhead display content by state remains unknown. Physical controllers, eight humans, audible sound and standalone Linux hardware are deferred to production; no simulated check is recorded as their acceptance.

Three agents each performed focused review plus deeper passes; fixes were rechecked. Their absence of new reproduced bugs is not proof of commercial fidelity. Historical audits are preserved under docs/audits, including earlier failures and their resolution.


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


Final render correction: ordinary capsules in the reconstructed layouts retain their two outer contour runs; the retired broad-wall inset effect is disabled for these profiles. Explicit double ghost-house outlines remain. All151 tests passed on both OS environments after this correction.


## Revision 13 — source measurements, rounded walls and scoring/AI corrections

Fresh confirmed DX footage43DcDXxEgzk was reviewed at quarter speed and paused positions. At9:22 red144640 has four ordinary dots ahead; at9:23 the corridor is cleared and score144680. This OBSERVED DX aggregate supports10 per ordinary dot; it does not recover other score awards or multipliers. At9:23–9:34 the final-life station displays CONTINUE/COIN while AI moves, followed by alphabet/name entry by9:45. No purchased continue, restored-life policy or score retention was observed. The fresh red full-board9:34 is independently identified as existing family A, corroborating color/layout independence, not adding a third maze. Candidate power sequences were rejected as exact duration measurements because of refreshes, occlusion and transition ambiguity. See audits/revision13_reference.md.

Rounded capsule ends and convex branch corners now retain narrow stems and the same validated corridor graph. Removed a faint third house underlay contour; actual-App scans require exactly two house borders on all four profiles. New comparison research images remain outside the runnable package. Exact20px quantization/hidden endpoints, source widths, full commercial catalog and progression remain unverified.

Corrected ledger totals after bot-to-human takeover: historical bot awards remain recorded, while station_join starts the new score account at zero. HUD, spectator rankings and ledger agree. Tested simultaneous dot/power/ghost/rival/bonus awards, duplicate fire attackers, expiry contact, carried ownership and same-tick damage. Bot routing now uses deterministic weighted legal paths, avoiding nearby lethal ghosts/giants/carried rival weapons and actively seeking capturable ghosts with Magnet. This improves our original strategy; exact DX difficulty/targeting remains unknown.

Power durations, movement intervals, ranges, slowdown multipliers and item cadence/cap are now validated per-Match tuning settings, loadable with --tuning tuning.example.json. Complete effective values and pickup duration/nominal expiry are captured in event logs/replays; quickstart and station START honor the same settings. Existing numerical defaults remain explicitly approximate. The on-screen guide reflects effective durations.

Added optional --untimed life-survival mode, also operator time limit0. Default180s remains an explicit custom score-attack mode, not a certified DX limit. Untimed progression, pause, elimination, spectator labels and replay are covered; CLI mode overrides do not silently rewrite saved operator settings. Exact final-life continue interval and background AI before original name entry remain a known presentation/behavior difference; no invented paid-continue policy is claimed.

Results now offer N for original three-letter initials for this session's qualifying top20 human rows. Atomic renaming uses session/player identity, protecting ties and historical/legacy rows. Failed writes roll back; cancelling discards only the active draft. Immediate replay and pending score-save retries remain intact. Exact cabinet entry UI, timeout and physical-controller entry are not reproduced or certified.

Final validation:187 tests passed on Windows and Ubuntu/WSLg, with source-frozen extracted-ZIP verification recorded separately. Native1/2/8 runs cover every profile on both systems, plus actual game/spectator pairs with audio initialization. Twelve complete automated human/AI matches reconcile ledger totals and rankings. Three48-second1280x720/60fps MP4s with original AAC event audio fully decode;24-second GIF previews and12-frame profile/count contact sheet were checked. All recording actors are automated; logical1/2/8 human stations have7/6/0 AI. Physical controllers, human multiplayer acceptance and audible speaker assessment stay in production.

Agent reviews ran initial and deeper passes with targeted fixes/rechecks. Their approval covers tested implementation scope, not undocumented original rules. Remaining exact scoring/power/AI/map/continue questions are tracked honestly; no perfect-match or zero-issues claim.


## Revision 14 — four observed layouts, recovered pellet awards and station continues

Fresh confirmed eight-station DX footage qcO9tzgsdjo at0:01/0:03 displays HOW TO PLAY awards: ordinary dot10, yellow pellet100, green pellet1000. These are OBSERVED DX for the pictured build, independently read by root and mechanics reviewer. Gold/Giant no longer receive the generic75 pickup award; other items, ghost/rival awards and combos remain explicitly unrecovered estimates. Pickup events retain their event identity and now identify the score rule. Repeat-pickup and same-tick tests use the newly observed values.

The same source at4:10/4:53 and5:05/5:15 shows two more distinct mazes. The runtime catalog now has four independently reconstructed observed families:0 Golden Rails/D569cells,1 Violet Crosscurrent/B569,2 Ember Courtyard/C585,3 Cyan Archway/A582. C was traced by the map reviewer and independently checked by the research reviewer; D was independently traced by research and critically reviewed by maps. Isolated narrow wall bars were widened from8 to16px, while every route retains20px normal-body clearance. Seventeen map checks cover all1-8 counts, edges, tunnels, gates, house contours, landmarks and no unintended open2x2/dead ends. Coordinates and hidden endpoints remain approximations; four observed families do not prove the complete commercial catalog or stage order.

Source43DcDXxEgzk brackets CONTINUE near9:25–9:35; qcO9tzgsdjo shows CONTINUE6 at5:11 and2 at5:15. A source-informed10-second station offer now follows a custom1-second reveal delay after final human death. AI/ghost simulation continues; all-human elimination is deferred until offers expire. Living humans keep playing while another station has an offer. Start redeems a valid offer after atomic software-credit/free-play authorization; failure/pending/paused/repeated inputs never debit incorrectly. The independent restoration policy preserves score and earned-bonus flag and restores configured starting lives. Actual paid source continuation and its score/life policy remain unobserved. Timed expiration overrides offers. Last-offer timeout settles scores once and automatically opens qualifying initials; other results retain optionalN entry.

Continuation state is deterministic, snapshot/replay-visible and pause/guide-safe. Raw Match defaults disable offers for explicit legacy/timed scenarios; normal App defaults enable10seconds. --continue-seconds0 disables; --continue-delay adjusts the explicitly custom reveal. INSERT supplies development credits during an offer; C remains lobby credit/P6-down during active play. Continue text was moved to clear the lower footer. Tests found and fixed that input conflict and footer overlap, and verify pending score-write retry, no duplicate charge, simultaneous/staggered stations and automatic name-entry recovery.

Ghost navigation now uses legal corridor distance rather than Manhattan shortcuts through walls or across the long side of a tunnel. It avoids immediate reversal when another exit exists. Five navigation checks cover a formerly oscillating U-shaped wall trap, all-map shortest tunnel routes, frightened retreat, normal wandering and dead-end return. Bot risk weights, ghost target choices and difficulty remain original, not recovered cabinet AI.

Actual extra-life and score-threshold events now trigger the original bonus cue; capped/eliminated zero-gain events do not falsely celebrate a life. Continue uses the original join cue. A spectator export check uncovered an image-save exception; pygame image I/O errors now leave play running with a visible message. Native test feed paths were also separated by platform to avoid two test writers sharing one file. The corrected game/viewer pairs passed on both systems.

Final source-frozen verification:238 tests passed on Windows and Ubuntu/WSLg; extracted-ZIP verification is recorded separately. Twelve complete automated matches reconcile score accounts and human rankings. Native1/2/8 checks cover every map on both systems; native final-life/countdown/accept/expiry/automatic-initials sequences pass Windows and Ubuntu. Three80-second1280x720/60fps AAC recordings fully decode:48seconds of four-map gameplay plus two16-second clearly labelled controlled continue scenarios. All actors are automated;1/2/8 logical human stations have7/6/0 AI opponents. Twenty-one decoded frames cover all maps and continue states. GIF previews show24seconds of map gameplay. No physical controllers, eight-human acceptance, audible speaker assessment or standalone Linux hardware are certified.

Two-pass map/reference/mechanics reviews and targeted fix/retests are documented in revision14 audits. Exact power durations/stacking, remaining award/combo values, complete map inventory/order, paid source continuation and original AI remain unresolved. Candidate stage-during-continue evidence was specifically falsified: the new maze already existed before the source offer. No fabricated certainty or perfect-match claim is made.


## Clearer user photo — gates and wall rendering

The supplied higher-quality photo independently matches family D / Golden Rails at all visible major junctions; no new topology was needed. Added a fifth selectable luminous blue palette (`--palette 4`) independent of all four maps. New `photo_map_windows.bat` and `photo_map_linux.sh` launch that map/color in development simulation and untimed mode.

The image exposed undersized, weakly lit pockets and sparse line hatches. New independently drawn64x48 continuous double-U bays have48x10 filled lemon-yellow strips with dark diagonal slashes, pale cores and real alpha-aware glow. Upper/lower stripe directions match. The outer field corners are rounded, walls have soft halos and pale inner ink, and the house has clearly separated double contours with an open inner doorway. Source dimensions and camera bloom remain estimates; no commercial bitmap enters the game.

Normal actors now sit at the actual outside-pocket center; their dedicated bounded render pass lets them enter/leave through the mouth while protecting score/life text. AI occupancy opens its physical gate even though its human HUD remains unjoined. The enlarged bays fit a720p canvas after a5px field shift; lower HUD stays fixed and the controller/simulation footer occupies a reserved central gap. Full save-error messages use a bounded toast. Desktop score orientation remains upright, while the photo's opposite-side cabinet prompts are rotated.

Critical QA found and fixed invisible transparent-surface halos, stale spawn-center rendering, AI hatches staying shut, and a widened house inner line crossing its door. Eleven new gate checks and19 map checks cover actual pixels, soft glow, parallel borders, body fit, departure/return, all8stations/all4profiles, empty/dead/continue states, five palettes, score/life/footer clearance and the full house opening. Combined targeted24 checks passed, followed by full238-check Windows/Ubuntu runs. The final recordings and native checks were regenerated after these fixes, with Golden Rails in blue.

The static photo improves visual evidence; it does not measure original gate release timing, paid-continuation restoration or physical-controller behavior. Controllers remain deferred to production.
