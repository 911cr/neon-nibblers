# Revision 13 implementation and verification status

This is the current status; historical revision notes elsewhere are retained as history. No software test can certify undocumented commercial rules.

| Requirement | Implementation | Evidence / checks | Remaining limit |
|---|---|---|---|
| Maze routes | All four production color profiles use two independently reconstructed observed DX layouts; unsupported authored routes retired | Full spectator views at68/73s, perspective-normalized trace overlays, every corridor edge and house/station approach checked | Quantized geometry, inferred glare-hidden endpoints, exact contours, complete commercial inventory and progression order remain unverified |
| Human/AI interaction |1–8 human stations; AI fills vacancies; human takeover removes inherited bot state; human-only ranking and end condition | Observed AI labels with join prompts; bot roster/input/takeover and full-match tests | Difficulty, exact replacement timing and cabinet configuration not measured |
| Core gameplay |11 power categories, player/ghost combat, scores/lives, staged ghost exit/return, wrapping and transitions | Deterministic event traces/replays, interaction and collision regressions | Specific payout values, multipliers, ranges, durations, ghost AI and stage trigger remain explicit approximations |
| Lifecycle animation | Smooth growth/shrink, old-position death dissolve, arrival pulses; physics unaffected |12 lifecycle checks plus actual-frame storyboard and eight-actor cache/render sample | Original animation lengths and silhouettes not measured |
| Joining/start/end | Independent Start/Find, sparse rosters, pause/guide, results/restart, keyboard fallback | Simultaneous starts, elimination, repeated Find, missing-controller and state tests | Exact DX join windows and Find effect timing remain unknown |
| Operator/credits | Saved lives/bonus/time/free-play/attract-sound/AI settings; keyboard credit insertion |17 cabinet checks, save failures do not debit credits, corrupt load recovery | Original service UI and physical coin hardware not reproduced/tested |
| High scores | Human results saved once, ranked with ties; failed writes queued as immutable snapshots for retry | Immediate restart/Escape, write recovery/throttle/dedup and reload tests | Entries use station names; exact commercial name-entry/results flow remains unknown |
| Attract | Original idle instructional power cycle, saved scores and configurable sound | Idle actual render/input-reset and mixer-loss checks | Original artwork/timing/menu sequence not copied or certified |
| Spectator displays | Optional local mirror of actual game canvas and separate original ranking view; two viewers can share a feed | Real game+viewer pair on Windows and Ubuntu/WSLg; strict/stale feed handling | State-specific DX overhead behavior is not fully recovered; custom auto policy is documented |
| Graphics/audio | Original supersampled sprites/icons, continuous bounded flame, animated lightning/stun, consistent pause and wrap behavior; ten original sound cues | Frame/time/size/clip regressions; HD video decode; actual native graphics/audio initialization | Audible speaker quality and exact DX art/sound identity not certified |
| Platforms/controls | Python/Pygame Windows/Linux source, launchers, USB/hats/axes/keyboard, stable session station ownership |187 automated checks, Windows and Ubuntu/WSLg native runs, Linux/Windows CI | Physical controllers, latency/mixed devices/eight humans and standalone Linux hardware remain production validation |

The source was reviewed by agents, followed by deeper passes and fix/retest loops. Reconstructed maps required narrower corridor carving and adaptive corner rounding to preserve thin stems. Portable test fixtures now derive tunnel, bay and ghost-house coordinates from each map, rather than assuming the previous authored geometry.

The build implements the previously missing software features. Exact DX fidelity is still **not fully verified**. Open reference questions remain tracked rather than being closed merely because tests pass. In particular, visible800/1600 point bursts and an orange250→650 change do not isolate the scoring cause; no invented multiplier is certified.

Physical controller acceptance is deferred by explicit user direction. Development's SIMULATED availability label never counts as physical testing.


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
