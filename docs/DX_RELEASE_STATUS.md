# Revision 12 implementation and verification status

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
| Platforms/controls | Python/Pygame Windows/Linux source, launchers, USB/hats/axes/keyboard, stable session station ownership |151 automated checks, Windows and Ubuntu/WSLg native runs, Linux/Windows CI | Physical controllers, latency/mixed devices/eight humans and standalone Linux hardware remain production validation |

The source was reviewed by agents, followed by deeper passes and fix/retest loops. Reconstructed maps required narrower corridor carving and adaptive corner rounding to preserve thin stems. Portable test fixtures now derive tunnel, bay and ghost-house coordinates from each map, rather than assuming the previous authored geometry.

The build implements the previously missing software features. Exact DX fidelity is still **not fully verified**. Open reference questions remain tracked rather than being closed merely because tests pass. In particular, visible800/1600 point bursts and an orange250→650 change do not isolate the scoring cause; no invented multiplier is certified.

Physical controller acceptance is deferred by explicit user direction. Development's SIMULATED availability label never counts as physical testing.


Final render correction: ordinary capsules in the reconstructed layouts retain their two outer contour runs; the retired broad-wall inset effect is disabled for these profiles. Explicit double ghost-house outlines remain. All151 tests passed on both OS environments after this correction.
