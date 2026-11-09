# Revision18 ghost lifecycle and power audit

## Scope and source limits
Read current Match ghost state/update/combat/render code and prior ghost_starts.md, ghost_exit.md and player_ghost_powers.md audits. Current maps derive house, door and homes from metadata; older audit coordinates and .16s default timing are historical, not current. R17 default ghost interval is.4s. No invented classic chase/scatter, fixed corner targets or commercial release sequence was introduced.

Known source evidence: Harold Zheng https://www.youtube.com/watch?v=qcO9tzgsdjo&t=314s shows colored normal bodies, large white eyes and returning eyes in adjacent315s frame. Same source303s transition shows temporary actor enlargement. These do not establish release delays, exact route choices, edible-ghost damage for unpowered players, stun immunity, recovery or power stacking. Existing DX product-category evidence at https://primetimeamusements.com/product/pac-man-battle-royale-chompionship-dx/ supports eat-ghost, carry-ghost, ghost-sheet, smoke and lightning categories; exact state precedence remains an adaptation choice. Research agent owns fresh footage review; no independent new browser footage claimed here.

## Findings and disposition
No new concrete simulation lifecycle/path defect reproduced. Prior teleport-return, stale carrier and safety-suppressed hunting fixes remain intact in tested paths. A long inherited foe_ticks value cannot produce a movement burst because the global ghost cadence gates each step. Smoke/Quake expiry is quantized to this cadence; changing that policy without measured original evidence would be speculative.

Root separately identified and owns two concrete R18 fixes: ghost eyes faced raw distant targets across wrap/queued corners rather than actual visual motion; holder damage needed to release carried ghosts immediately. These are not edits made by this audit agent, and their dedicated tests/results belong to root/ledger.

Current authored choices retained: initial release thresholds .9+.6*i seconds sampled on the ghost cadence;1.2s home recovery; house/leaving/eyes/entering protected from damage and slow/stun; shortest legal path for eyes; roaming combines path-aware nearest visible target with70% directed decisions and30% wandering, avoids immediate reversal when alternatives exist; fleeing reverses distance preference against the selected powered target. House slot lengths can change actual emergence order. None of these is certified as the exact DX algorithm.

## Initial pass
Six new test groups in test_ghost_lifecycle_r18.py PASS(.376s):
-48 full cycles across4maps,4ghosts,3return starts (both portal sides and far corner). Every move is adjacent or a legal wrap; eye return traverses door/home; house->leaving->roaming completes.
-4maps x30/60/144Hz: over four base intervals, normal moves4steps, smoke2, Quake2, both1, individual zap0.
-Protected eye return reaches home under simultaneous smoke, Quake, global stun and individual zap.
-Veil removes targeting but allows roaming movement.
-All11 named power-state contact categories on4maps and harmless/nonfarmable protected states. This isolates contact policy; setting an effect is not a test of each instant power's collection side effect.
-Mixed partial smoke/Quake expiry and local stun, including100s inherited movement accumulator, never leaves lanes or moves more often than the .4s base cadence.

## Deeper pass
Existing test_ghost_navigation.py5tests PASS(.011s): shortest legal route around walls, tunnel chase on all maps, frightened distance preference, no immediate random reversal when an alternative exists, dead-end reversal. Reviewed stale previous-position, inherited tick and recovery effects; no justified new simulation change found. Soft chase/flee policy does not guarantee survival or optimal ghost intelligence.

Contact policy remains explicit: Crown/Titan eat roaming ghosts; Lure captures; other effect flags alone do not grant contact immunity. Veil prevents tracking, not touch damage. Returning/protected modes cannot be farmed for points. Global blue appearance while only certain players can eat ghosts remains a source-evidence gap; no assertion of commercial parity. Stunned normal ghosts' contact damage and carry-vs-Crown precedence likewise require better evidence.

## Changed files and remaining verification
Initial simulation audit changed only test_ghost_lifecycle_r18.py and this audit; no reset/update simulation edit was needed. After fresh visual evidence and explicit root coordination, this agent additionally changed exactly two App foe-render tint expressions and added test_ghost_tint_r18.py. Root and ledger own ghost-facing/carry-release runtime fixes and full-suite integration. Fresh research findings may refine source confidence; current passing tests certify the specified adaptation invariants, not exact cabinet behavior.

## Fresh reference supplement
Independently inspected research agent's work/r18-ghosts-259b.jpg, paused HaroldZheng qcO9tzgsdjo4:19. Two blue/cyan ghost bodies are visible inside the house while blue bodies are also outside. This establishes that house location does not always exclude the global blue visual state; current roaming-only tint is a likely presentation gap, reported to root. Nearby earlier/later colored states may involve flashing/expiry, still under research. No contact vulnerability or release timing is inferred from tint alone.


## Source-supported presentation correction and independent review
After inspecting4:19 evidence, expanded global blue tint from roaming only to roaming/house/leaving. Housed bodies are directly supported by the frame; including leaving bodies is a visual-continuity inference, not a measured collision-state flag. Carried bodies and returning eyes retain previous presentation. No ghost simulation/damage/state timing changed.

Four actual-renderer tint tests PASS4.240s: all maps and six mode flags, sampled blue house pixels, both tunnel copies, normal colors without a living hunter, and unchanged protected/nonfarmable house combat. Original-only package evidence outputs/NeonNibblers/ghost_states_r18.png rendered and visually inspected: normal/blue actualApp scenes and magnified house crops, plus original normal/frightened/stunned/eyes silhouettes. Exact expiry flashing remains unverified.

Independently reviewed root CorridorTrack.direction implementation and four ghost-facing tests (PASS4.427s). Direction follows the segment actually traversed, including shortest horizontal wrap; retains last direction while stopped/paused; resets neutral on relocation. Queued corners face the active axis rather than a future diagonal target. No definite new defect found.

Ledger independently reviewed and ran six lifecycle groups (PASS.409s). Its qualification is preserved: injected Spark/Quake/Heart flags test contact classification/ignored flags, not collect() side effects; actual pickup integration is covered separately. Reviewed ledger test_contacts_r18 source for order/expiry/house/immunity/render-state invariants; final execution results appended below.

Independent ledger-contact execution: all10 test_contacts_r18 tests PASS9.598s, including actual rendered death->eyes and continuous1/2/8player/allmap contact motion. No new runtime defect found. Suggested expanding the single-ghost fixture behind the all-owned-ghosts test title to exercise multiple simultaneous carriers; implementation already iterates owned identities.

## Final integrated presentation review
Reviewed root's single player-visual prepass before gates/effects: exactly one sampling path; actor rendering reads cached coordinates. remaining_path exposes an immutable tuple; corridor_segments rejects invalid/diagonal/nonpublic links and splits portal wraps. Private Flame connector is constrained to its owner's x and bay-entry y interval, drawn through separate public/own-pocket clips and restores the previous clip. HUD outside that pocket remains excluded. Independently reran final12 contact tests PASS10.173s and11 gate-detail tests PASS6.096s, including all-station powered departure/return, wall-safe corner flame attachment, no Match mutation during drawing and movement bounded to one visual step. No additional definite defect found; source freeze approved. Ledger also independently passed4 tint tests3.942s and expanded direct-hurt coverage to three carried ghosts.
