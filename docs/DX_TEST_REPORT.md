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
