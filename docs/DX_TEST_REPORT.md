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
