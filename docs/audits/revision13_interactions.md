# Revision13 scoring and interaction audit

## Reproduced defect and fix

A bot could earn 75 points, then be replaced by a human starting at zero. Player.score, the HUD and spectator rankings correctly reset, but ScoreLedger.totals continued to report the bot's points, then added the new human's awards. Reproduced mismatch: after one human dot, ledger85 versus HUD10.

ScoreLedger.totals now treats station_join as a new score account using the event's authoritative score snapshot. All historical bot awards remain in the ledger. There are no fabricated negative-point events. This records the original adaptation's fresh-human replacement policy; it is not evidence about commercial scoring rules.

## First pass

Reviewed current movement, power application, contact/combat/fire ordering, life thresholds, end-state selection, carried-ghost ownership, AI targeting, ledger aggregation, replay grouping and spectator/HUD consumers. Existing logic already grants stage-clear bonus lives during the same update. Moving-item collection happens in a later phase than combat; without source timing evidence this order is documented behavior rather than labelled a confirmed defect.

## Deeper second pass

Seven new tests in test_revision13_interactions.py verify:

- Bot takeover resets current ledger totals while preserving history and nonnegative awards; actual HUD digit calls and spectator ranking match the new account.
- A single update containing dot collection, Titan pickup, ghost eating, rival eating and score-threshold life generates each event once (four maps).
- Two fire attackers cannot duplicate credit for one ghost or one victim (four maps).
- Eight personal timed powers expire on the same simulation tick under 30/60Hz render grouping through FixedStepper.
- Lure expiration releases its carried ghost before contact; the expired weapon grants no damage or credit.
- Crown expiration with two contacting ghosts creates one life loss, one death event at the old position and one hurt cue.

All seven targeted tests passed in0.792s after the fix. No additional confirmed interaction defect was found within these scenarios. Exact source power precedence, duration, AI strategy and portal range semantics remain unverified. Physical controllers were not tested.


## New tuning and AI second review

Found a second concrete integration defect: quickstart passed App.tuning to Match, but station START created Match with default tuning. Root fixed the station constructor. A new actual App station-start regression confirms a Rush11s/spawn9s override survives station creation and controls the collected effect.

The new root-owned risk-weighted AI was reviewed independently. Additional tests exercise deterministic legal choices across all four maps with bot-only steering, preservation of human input, avoiding a normal ghost when a safe alternative exists, retaining danger from giant rivals while Crown is active, distance1 across side tunnels, and no distance3 shortcut through a separating wall. No changes to arcade_ai.py were necessary for these cases. Eleven targeted tests passed in1.153s. The preceding full suite passed159 tests in60.699s; the latest full suite is recorded below after completion.

New research did not establish exact overlap, portal-effect or stun-contact immunity rules. These tests check original internal behavior rather than asserting cabinet equivalence.


Latest full run passed170 tests in68.563s against its loaded source snapshot. One other full run exposed a faulty test assumption that every real map contained a particular three-cell wall gap. No map graph change was established as its cause. The fixture now uses an explicit U-shaped legal corridor: endpoints Manhattan2 but graph6 must not become nearby threats; graph distance3 remains included, and the separating wall remains excluded. Actual tunnel distance1 is still checked in all four real maps. All eleven targeted tests passed again in1.029s after this portable fixture correction.


## Final frozen-source integration review

Fourteen targeted tests passed in1.812s. Added strict malformed-type coverage for tuning (boolean, string, null and nonfinite values) and match duration (only integer0 enables untimed; booleanFalse is rejected). Sixteen all-map carried-ghost AI scenarios verify only a living rival owner with an active Lure creates a threat; own, dead-owner and expired-owner weapons do not. An actual App scenario combines untimed mode and an overridden0.5s Rush: pause/guide preserve the entire logic digest and discard accumulated time, resumed play expires the effect after30 fixed steps, and human elimination ends the match with the correct reason; results then remain unchanged during advancement/rendering. No further concrete defect was found. These checks approve internal correctness for this reviewed scope, not exact source equivalence or every possible input.

Final source-frozen root checks:187 PASS on Windows and187 PASS on Ubuntu, including10 initials checks.
