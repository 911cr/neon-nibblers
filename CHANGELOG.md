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


## Revision 15 — reference audit, uniform graphics and player contact

Fresh continuous DX footage qcO9tzgsdjo around5:00–5:05 shows C morphing into D while walls remain amber. At5:07–5:08 red enlargement accompanies red walls; by5:10/5:13 red and blue giants coexist and walls alternate their colors. The build now retains its base hue through map changes and cycles active giant colors. The1.25-second interval, station order and expiry fallback remain explicit approximations; exact commercial blending/priority is unresolved. Map morphing itself is still not implemented: our stage changes/reset policy remains different.

Native-resolution cardinal outlining made curved wall strokes8.1–8.7% dimmer than horizontal sections. Supersampled circular outlines and a shared premultiplied material reduce the sampled mean difference to0.07–0.34% across four blue maps. Gates, house and tunnel extensions now share luminous stroke construction. Closed gate hatching has the continuous yellow upper lip from the user's photo. All11 pickup icons, eight player colors/directions/sizes, ghost states and world effects were inspected in animation/contact sheets; this does not certify identical commercial assets. Smoke now has soft animated shading and appears immediately on stationary pickup, while the retained trail remains unverified against DX.

The collision report exposed multiple-cell instantaneous shoves and a cooldown that did not prevent repeated impulses. Contact resolution now rolls back the complete group and affected followers, then takes one outward step at normal movement cadence while retaining buffered input. Radius-aware bounded corridor checks reduce visible interpenetration, including tunnels and stationary giant growth. Separate QA caught stationary recoil in the wrong direction and rollback after a later giant hit; both were corrected. This remains a discrete corridor approximation, not recovered continuous DX physics.

HUD scores now show their actual digits, removing the invented six-digit leading-zero padding absent in the user's photo (1760/9460/13530). Existing gate clearance and long-score fitting remain tested. Desktop orientation and the remaining typography/life indicators are still different or unresolved.

Full final source: 271 checks pass on Windows and Ubuntu/WSLg. These include all1–8 rosters/maps and11power categories; no physical-controller certification. A natural continuation replay fixture needed seed0 because the former seed1 survives the60-second window under corrected contact rules; its continuation, score and replay assertions are unchanged. Native1/2/8 runs cover every map; regenerated actual automated gameplay videos include labelled continue scenarios. Source/package tests and decoded media are recorded in current reports.

The full current comparison is DX_CURRENT_GAP_AUDIT.md. All11 categories exist, but numerical power rules, global ghost vulnerability, blanket giant immunity, ghost AI/count/order, attack/combo scoring, spawn distribution, map catalog/progression, paid continuation and several graphical states remain unverified. Agent approval covers stated test scopes only. Controllers remain deferred to production. No exact-match claim.


## Revision 16 — exterior spacing and continuous maze changes

The user's annotated image exposed a real mismatch: exterior wall cores were3px apart while bay cores were6px apart. The exterior now has the same6px separation, concentric corner curves, aligned gate shoulders and continuous tunnel joins. A second review found and fixed lower gates being dimmer due to inconsistent supersampling phase. All four maps/five palettes/eight station joins were checked, with unchanged public lanes and body clearance.

Two fresh passes through Harold Zheng's DX footage (qcO9tzgsdjo,5:02–5:04) show actors staying on the field, maze compression/change, temporary enlargement of both players and ghosts, and scattered dot refill. The game now preserves actors across stage changes instead of resetting everybody to bays/house. Legal actor and item positions are reserved before displaced objects get the nearest free lane. Ghost release/return/carrier state, scores, lives, ongoing effects and continue timers persist. Exact relocation and power persistence remain our stated policy, not recovered source rules. The initial/new-match reset is unchanged.

An original1.1-second shrink/blend/expand animation replaces the instant layout swap. Actor enlargement is visual only; it never changes combat size or grants a power. Dots refill visibly and become collectible together between0.6 and1.1 seconds, with no accidental second stage-clear during refill. HUD scores stay stationary and pause/help/results freeze the animation. The0.90 maze scale,1.35 actor pulse, short midpoint overlap, timing and trajectories remain approximations; source footage does not establish an exact curve or whether movement pauses.

The deeper transition review caught a moving item stealing an already-valid static pellet position; the reservation fix is covered by a regression. Legacy tests that required a global respawn were updated to require continuous legal placement. The independent transition tests cover all16 ordered map changes, eight-player conflicts, private bays, inactive stations, continuation, carried/returning/releasing ghosts, refill and render immutability.

All288 checks pass on Windows and Ubuntu/WSLg. Native checks cover1/2/8 on all four maps (24 cases), plus actual transition runs for those counts on both systems (six cases). Twelve complete simulated matches reconcile scoring/rankings, and a720-frame472-event replay verifies deterministically. Audio initialized; physical input and audibility are not certified. Initial geometry construction still causes a first-use render delay; short native startup-inclusive figures are not steady-state performance claims.

Three new88-second1280x720/60fps recordings contain48seconds of all-map gameplay, an8-second labelled controlled C-to-D transition, and32seconds of labelled continue acceptance/expiry. All actors are automated;1/2/8 human-designated stations have7/6/0AI. Fresh24-second GIF map tours, all11-power/player/ghost animation sheets and actual transition frame sequences accompany review.

The source clearly shows a3000 popup associated with this transition; its universal award/recipient/scaling rules remain unknown, so the configurable500 simulation clear award is not promoted as authentic. All11 power categories are present and tested internally, but exact durations/spawn rates/stacking, global ghost vulnerability, ghost targeting/release and several source artwork details remain unresolved. Original sprites/audio/branding are retained. Controllers remain deferred to production; no perfect-match or zero-issue claim.


## Revision 17 — responsive input, continuous motion and reference-informed pace

Two normal-looking actors in real DX footage qcO9tzgsdjo4:09/4:11/4:13 cover approximately12–15 dot spacings in nominal4seconds. Whole-second timestamps and camera perspective leave a conservative2.4–5dots/second range; hidden power status is not fully excluded. Our previous10dots/second was likely materially faster. The new provisional default is4dots/second (.25s per20px cell). Rush/Slick/ghost/item intervals are.1625/.1375/.40/.60s, preserving earlier authored relative speeds; those ratios are not recovered DX facts. The old fast profile remains selectable with --tuning tuning.fast.json. Power durations, probabilities, spawn interval and collision impulse constants were not guessed from this footage.

Fixed a concrete keyboard bug: held Up overwrote a freshly pressed Right in the next input poll. Every station now uses its most recently pressed held direction; releases fall back to remaining held keys, and no-key state retains buffered intent. Legal facing/reversals update without granting distance or resetting movement clocks. Invalid turns stay buffered until a junction. Slick/recoil remain in control during their effects. Discrete travel decisions still occur on the movement cadence; immediate facing does not eliminate the possible250ms positional wait or constitute a continuous subcell physics model.

Replaced exponential visual easing with constant-speed axis-aligned waypoint motion for players, ghosts and moving items. This avoids bursts/holds at the slower cadence and prevents rounded diagonal cuts through corners. Logical reversals cancel abandoned forward waypoints, tunnel coordinates wrap, damage/restart reset tracks, and50px gate movement receives its own distance scaling. Pause/help/results freeze motion; rendering changes no Match state. Very long frames crossing multiple unseen turns can snap to the final cell rather than inventing a route. Normal30/60/144Hz default-speed tests do not encounter that case.

Bot navigation now recognizes nearby powers across tunnel connections, prioritizes vulnerable rivals while giant even when ghosts are in their house, and chooses a legal safer fallback when goals disappear during refill. Six adversarial/navigation tests and independent review cover these fixes. No new collision-resolver defect was reproduced; all-map crowds recover, retain controls and avoid overlaps/extra-cell jumps. With slower speed, densely packed eight-player crowd recovery takes longer in wall-clock time; this tradeoff remains documented.

Paired90-second eight-actor simulations isolate pace from the bot changes: death events140→54, rival hits93→30, pickups298→285 and mean stage4.75→2.25. Near-rival proximity rises.190→.227, but it is a Manhattan-distance proxy, not a collision measurement. Separate1/2-actor experiments do not include the application's vacant-station bots. These metrics show less rapid churn and fewer attacks, not greater enjoyment. All90s observations are censored for finish time; no survival-length conclusion. No human multiplayer fun-equivalence test has been completed.

Maze geometry is now prepared before play. One local dummy-render comparison moved first-layout-change rendering from.9999s to.0084s, with3.5794s spent preparing four mazes before play; this is a measured cold-start comparison, not a guaranteed native FPS claim. The game shows Preparing mazes during that work. Actual four-map slow tour review found zero off-centerline positions across17,117 player samples, and straight/tunnel motion at60Hz consistently1.333333px per moving frame.

All328 checks pass Windows and Ubuntu/WSLg. Native runs cover all four maps with1/2/8 human-designated stations plus six transition runs, using7/6/0AI fill; audio initializes, physical input/audibility remains uncertified. Twelve full automated matches reconcile scores and rankings; deterministic replay, stress checks and extracted-package validation are recorded separately. Updated104-second720p60AAC videos show64seconds of four-map play,8seconds of labelled controlled C-to-D transition and32seconds of labelled continue scenarios. All capture actors are automated.

Agents completed initial and deeper passes, with targeted fixes/rechecks. The task-owned research YouTube tab/window was closed and its removal verified; other user applications were left untouched. Physical controllers remain deferred to production. Exact DX power timing, ghost rules, collision physics, scoring, artwork and subjective fun are not certified. Original assets/code/audio remain independently authored.
