# Revision14 continuation model QA

Research observed final-life CONTINUE while other actors kept moving, then name entry; fresh sampling reportedly showed countdown9 and approximately9–11 seconds of continue presentation. The adaptation therefore uses an estimated10-second offer after an original one-second death/reveal delay. Neither restored score/lives nor purchase completion was observed. Restoring configured lives while preserving score and the already-earned bonus-life flag is an explicit original policy.

## Pure model

cabinet_flow.ContinueOffers contains no payment, SDL, game or persistence dependency. It tracks independent station windows and reveal delays. Active includes pending reveals, allowing session settlement to wait while the world continues. Accept is unavailable during the reveal delay and removes a ready offer exactly once. Duplicate open does not refresh a live offer. Zero seconds disables offers. Advance splits a tick crossing the reveal boundary; pause behavior is controlled by callers advancing only during active simulation. Snapshots are detached, sorted and JSON-safe.

## Two critical unit passes

Seven tests passed in0.004s: eight independent offers, duplicate opening, one-use acceptance, staggered deaths, new offers after a successful continuation, exact expiry at30/60/144Hz, reveal-delay and window boundaries including a partial crossing tick, disabled mode, detached snapshots, zero/large elapsed time, and malformed station/duration/delay inputs rejected without changing state. Payment and Match/App integration require separate tests after root integration; this unit result alone is not evidence of full cabinet continuation behavior.

Integration design recommendation: defer final elimination settlement rather than saving then reopening the same completed session. Freeze eliminated human scores; continue AI simulation while an offer exists. Validate redeemability before atomic debit, then restore deterministically. Only settle/freeze final rankings after all humans are gone and no offer remains (or the optional global timed mode ends). Existing pending-results persistence stays responsible for retry after settlement.


## Integrated second pass

Fourteen integration tests passed in1.882s after root integration. Final-life reveal/accept preserves score and bonus flag, restores configured lives and normal gate/safety state, and accepts once. Dead human scores remain frozen while bots keep moving. An individual expired offer does not end another human's play; last-human settlement waits for all offers; optional timed expiry overrides them. Pause/guide blocks redemption and freezes the complete logic digest. Raw Match defaults leave continuation disabled for explicitly legacy simulations.

Payment tests cover insufficient credit, failed atomic debit with unchanged credit/offer/player, successful retry, no second charge for FIND, and independent new-station joining. A real input defect was reproduced: using C for credit during an active offer conflicted with P6 down movement and inserted a credit. Root changed active-game credit input to INSERT while retaining C in the lobby; the real keyboard-event regression now passes. The actual continuation renderer also displays storage failure text, verified by captured text calls.

Final timeout saves qualifying rows then opens initials automatically. Timed termination does not force that editor. A failed automatic save leaves the result pending and explicit retry recovers. Pending-save state survives immediate restart without losing or duplicating final scores. Bot deaths never open human continuation offers. These tests exercise software paths with simulated controller availability only.

## Recovered scoring cross-check

Independently viewed work/dx14-score-panel-crop.png from the research agent's confirmed DX instructional screen. The legend visibly reads ordinarydot10PTS, yelloworb100PTS and greenorb1000PTS. New test_revision14_scoring.py verifies Crown100 and Titan1000, while the other nine items remain75 estimates; events remain pickup with an explicit score_rule. A second test verifies independent override values and single bonus-life awarding. Both tests passed. The prior simultaneous dot+Titan+ghost+rival test now expects1510, preserving its one-award-per-event assertions; all fourteen prior interaction tests pass. Other power scores, ghost/rival awards, durations and AI decisions remain unverified original tuning.


## Final render/audio/navigation review

The all-eight-station prompt bounds check reproduced a lower-HUD defect: CONTINUE10 occupied y699..711 while the footer began at708. Root moved lower prompts to y696 (sy+21), preserving the upper placement; all four layouts and both alternating countdown/START text states now fit width108 and end at or before the footer. Fifteen continuation integration tests passed in3.334s after this fix.

Real generated life/continuation events revealed audio mismatches: the legacy bonus_life mapping did not match score_bonus_life/extra_life, and station_continue lacked its entry cue. Root added these mappings. Deeper testing then caught a bonus cue when gained=0 at the five-life cap. Audio consumption now filters only those actual life-event types on positive gained, retains Heart's generic pickup cue, and preserves legacy bonus_life compatibility. Three actual-event audio tests passed in0.361s and the ten legacy audio tests previously passed in5.408s. Dummy-mixer checks do not prove speaker audibility.

Root replaced roaming-ghost Manhattan pursuit with legal-corridor graph distances and avoided immediate reversal when a forward route exists; dead ends still permit return. Five new navigation tests passed in0.011s (U-corridor wall detour, actual portal distance, frightened fleeing, random nonreversal and dead-end return). These improve the original AI's navigation and motion; they are not a claim of recovered DX targeting rules. Source inspection found no additional concrete defect in the reviewed changes. Final combined discovery remains the parent agent's responsibility after the map edits freeze.
