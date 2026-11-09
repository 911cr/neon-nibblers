# Revision17 control response and contacts QA

## Reproduced input failure

With UP held, a fresh RIGHT keydown set `Player.wanted` to right in `App.events`, but the immediately following `App.inputs` scan overwrote it with up because keys were considered in fixed direction order. This made turn response depend on which direction happened to appear last in the binding tuple. Reproduced through actual App event/input calls with mocked held-key state; no physical keyboard/controller latency is claimed.

Root fixed Game input handling with press-order tracking. The newest still-held direction wins, releasing it falls back to the remaining held direction, and no held direction leaves the existing turn buffer intact. Repeated KEYDOWN events do not gain a new priority. Bots ignore human keyboard input.

## Initial and deeper checks

New `test_response_r17.py` contains7 tests. They exercise all8 station bindings, releases, buffered intent, repeated-key events, bot isolation, an actual next-step turn on all4 maps, and App fixed-step cadence at30/60/144 rendering rates for1/2/8 players across all4maps. The cadence check compares final positions, scores, and buffered directions and requires10 normal steps during the simulated second.

Crowd recovery is tested across all4maps and1/2/8 counts: after one second of opposing held movement, all controls turn right for two seconds. Every living actor makes forward progress; all positions remain unique and each simulation tick moves at most one cell. In the deterministic8-player scenario, the slowest actor advances6cells during recovery, while the isolated actor advances20cells. This records crowd delay and absence of permanent sticking in the scenario, not a measurement of commercial collision timing or proof that the game feels fun.

Second-pass combined run: **25 tests passed in0.937s** (`test_response_r17`, `test_player_contacts`, `test_contact_critical_r15`). Existing cases include head-on and tunnel collisions, stationary/buffered receivers, radius contact, simultaneous crowd rollback, event cooldown, giant/small damage, following motion, wall separation, and avoiding rollback of respawned victims. No additional reproducible resolver defect justified changing `player_contacts.py`; it remains unchanged in this revision.

## Limits

The grid/radius rollback, recoil cadence, stun duration, cooldown, and wall contact rules remain original approximations. These automated checks do not certify subjective responsiveness, physical USB hardware, or an exact match to DX contact dynamics. Root owns the Game input fix; this agent owns the new regression tests and audit.

## Pacing revision and final response pass

Root subsequently changed the normal step interval to0.25s (4cells/s) based on the research agent's conservative observed movement range. Rush/Slick/ghost/item step intervals retain authored relative ratios; effect durations and spawn cadence remain unchanged. These are still approximations, not exact cabinet constants.

The owned legacy fixtures now derive their step counts, movement deadlines, ghost updates, item clocks and fractional remainders from effective tuning. No override restores the previous speed. Crowd recovery uses equal movement opportunities (10 approach steps,20 recovery steps), so changing the nominal movement rate does not silently reduce the amount of motion exercised. A separate fixed-time probe exposed a real tradeoff: under0.25s pacing, an8-actor opposing crowd changed to all-right had two actors with zero net progress and one with-1cell after2s; all progressed after4s. This is documented rather than called permanent sticking or hidden by the scaled-time test.

Root added immediate legal facing while retaining the normal movement budget. New checks confirm legal reversals face immediately without moving/resetting the clock, illegal turns remain buffered until a junction, Slick and pending recoil retain precedence, and repeated alternating directions cannot grant extra steps. Logical position response remains bounded by the unspent step interval plus one simulation tick (up to about250ms at the current default); these checks do not claim that direction-only feedback eliminates grid-step latency. Independent corridor presentation work is owned elsewhere.

Final owned response suite now12 tests. Combined with the updated revision9/revision10/ghost-navigation/smoke-burst suites: **34 tests passed in5.574s** against the new defaults. Independent review also ran the AI agent's6 navigation tests successfully (5.358s) and found no definite new safety/policy defect; risk costs remain a soft policy rather than guaranteed avoidance.
