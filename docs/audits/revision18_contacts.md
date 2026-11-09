# Revision18 contacts, power boundaries, and continuous rendering

## Reproduced defects and integration fixes

1. **Invalid carried ghost after owner damage.** A Flare hit occurred after carrier synchronization, cleared the holder's powers and life, but left the ghost in `carried` mode with a dead/inactive owner until the next update. Root moved owned-carrier release into `hurt()` itself. Direct damage now releases all held ghosts immediately; full-tick and actual-render checks require returning eyes in that same frame.
2. **Mutual fire depended on station order.** Two normal players facing each other with active Flare rays both intersecting would always favor P1: its damage removed P2's effect before P2's turn in `apply_fire`. Root snapshots eligible emissions and target positions before damage. Both attacks now complete, including final-life trades. A shared victim still takes only one damage; the original first-effective-hit credit policy remains explicit rather than introducing unverified split scoring.
3. **Trade score popup at respawn.** After snapshotting attacks, a killed emitter's later award used its new respawn position. Root also snapshots the original emission position for score-ledger/popup context. Regression checks require the award location remain at the battle, while lives and totals reconcile.
4. **Detached flame under continuous movement.** Actual App instrumentation measured a flame beginning at(280,80) while its visible actor was at(261.333,80), an18.667px separation after a logical step. This is a renderer integration defect, separate from the collision model. Root is integrating a visible-body/queued-corridor tail so the flame remains attached without diagonal wall shortcuts. Final status and targeted result are recorded below after retesting.

## Initial and deeper scope

The first pass reproduced carried ownership and tested expiry/refresh before contact. The deeper pass found mutual-fire ordering, then its spatial-ledger followup, and checked the newly continuous presentation for detached effects. Tests exercise all4maps and1/2/8 contact renders, max per-frame visual displacement at configured speed, no draw mutation of Match state, one damage per victim, actual wall-stopped flame rays, house/safety/Titan exclusions, both station orders, final-life scores, and same-tick Crown/Titan refresh versus expiry.

Independent cross-review passed the map agent's6 ghost-lifecycle tests and4 ghost-tint tests. Their direct power-flag contact matrix is classified as policy testing, not a complete test of applying all11 power-ups. The direct owned-carrier damage fixture was expanded from one to three ghosts after that agent's critical review.

## Limits

Grid/radius collision thresholds, recoil impulse/cooldown, simultaneous contested-hit credit and immunity rules remain authored policies, not exact recovered DX behavior. Logical Titan activation/expiry and its visual growth/shrink use different representations; these checks do not certify continuous physical disc collision during growth or eliminate the known discrete-grid contact gap. Research now bounds one observed Giant episode conservatively at8–12seconds; a provisional10s setting does not establish every power's exact timing. Physical controllers remain deferred.

## Final integration and freeze

The detached-flame fix now computes player presentation positions once and reuses them for the body and effects. Fire follows the track's existing axis-aligned waypoint path, then its logical ray; the validated public helper rejects wall/diagonal shortcuts and splits portals. A further adversarial powered-bay return/exit case exposed a43.333px separation because the public helper correctly excluded private cells. Root added a narrowly authorized connector only between that player's known spawn and entry, rendered under public and owner-pocket clips. It does not grant new damage range or permission through another player's bay.

Final `test_contacts_r18`: **12 tests passed in10.241s**. The new bay matrix covers all8 stations on all4maps, both entry/turn and return/reversal, visible-body origin, vertical-mouth alignment, owner-pocket/public clipping, and unchanged Match digest. The public corner regression verifies connected axis-aligned flame segments start at the current visible actor. The preceding combined contact/effect-path check passed20tests in10.001s before adding the final bay regression; independent helper tests remain9passing.

Original-only deterministic evidence artifacts were generated and visually inspected: `outputs/Contact-fire-sequence-r18.png` and `outputs/Contact-fire-gameplay-r18.gif`. They contain two staged QA scenes rendered by the actual App (contact/recoil, then moving fire and damage), not commercial footage or proof of exact DX feel. The still sequence shows the flame remaining connected during motion and the score popup appearing at the battle. Artifact creation does not alter simulation code.

Assigned source/tests are frozen. `player_contacts.py` did not require a new change in this revision. Root owns the integrated Game fixes; this agent supplied reproductions,12regressions, independent reviews, artifacts, and this audit. No remaining reproduced defect in the assigned checked scope; known approximation limits above remain open research questions.
