# Revision 9 gameplay adversarial review

2026-11-08. Two deeper passes across Match timing, powers, score/audio attribution, sparse stations, simultaneous attacks and actual HUD draw calls. This review fixes demonstrated implementation inconsistencies; it does not establish undisclosed DX values.

## Pass 1: reproduced defects and corrections

### Configured movement speeds were being rounded down

At 60 simulation ticks per second, one second of normal movement produced only eight steps, with movement on ticks 7,14,21,28,35,42,49,56. The configured interval is 0.10 seconds, which should permit ten steps. Resetting the clock to zero threw away overshoot; floating-point comparison added a full extra tick at the 0.10 boundary. Rush and Slick both produced fifteen steps even though Slick is configured faster (0.055 versus 0.065 seconds).

Changed Match movement, ghost, spawn and roaming-item clocks to retain fractional remainder and use a small comparison tolerance. Tested one second of unobstructed movement: normal **10**, Rush **15**, Slick **18** steps. Tested three seconds of simulation: one three-second spawn tick, item clock remainder 0.12 after twelve 0.24-second intervals, and ghost clock remainder 0.12 after eighteen 0.16-second intervals. Single large direct update calls still do not replace the fixed-step driver; they intentionally process at most one movement step per call.

These are the game's declared adaptation timings. No claim is made that ten cells/second or the power multipliers are exact DX measurements.

### Concurrent bonus life hid the damage sound

Reproduced P1 moving from score 9,995 to 10,005 and receiving a bonus life in the same update that P2 lost a life to a ghost. Lives changed from `[3,3]` to `[4,2]`. Because the code compared the sum of lives before/after, it emitted only a dot sound despite an actual damage event.

Changed damage feedback to inspect the authoritative `player_hurt` events produced by combat, rather than net life counts. Regression confirms the damage sound remains present while the bonus and death both resolve correctly.

### Lightning mutated absent stations

Sparse station slots are represented with zero lives and default positions. A nearby lightning pickup previously set their stun timers as if they were participating. Limited rival stun to living players. Tested that absent slots remain unstunned and a newly joined, living adjacent station still receives the effect. This does not decide undocumented DX lightning lethality or immunity.

## Pass 2: combinations and render review

- Four carried ghosts contacting one rival produce exactly one life loss, one 300-point award and one scoring event. Existing safety prevents multi-ghost score farming.
- All eleven power categories were collected twice by both P1 and sparse P8. Scores remain 150 for two pickups; timed powers refresh to their configured duration, instantaneous powers do not acquire bogus effect timers, and damage clears held effects/stun.
- Independently reviewed root's station score layout. Six score digits clear ordinary/giant bodies, remain inside the screen and leave player bays unobscured. Found an additional edge case: the giant locator ring could reach radius 52 and overlap the first bottom-station score digit beginning at center+50.
- Root capped locator radius near border bays at 44. Added actual draw-call interception for 1/2/8 players on all four maps with scores 0,999999,999999999. Every captured giant locator ring stays within that radius and clears all captured station-score rectangles. This is a geometric rendering check; it is not a DX image-match certification.

## Verification

`test_revision9_gameplay.py`: **7 tests passed**, including 36 rendered station/count/score combinations. Full discovery after the Match fixes and before adding the final locator test: **70 tests passed** in 15.249 seconds. Main integration subsequently runs the complete combined suite including other agents' additions.

Timing corrections change seeded trajectories. The old replay sample and gameplay captures must be regenerated; root has been notified. Preserve revision-8 evidence as historical rather than silently treating its digest as current.

## Reference limits

No new unobstructed commercial collision/timing sequence was observed during this code-focused pass. Existing DX category evidence remains in `DX_REFERENCE_EVIDENCE.md` and earlier power audits. Lightning damage versus stun, giant immunity, magnet precedence, ghost-sheet contact, exact durations, scoring values and custom stage progression remain unknown or inferred as already documented. Physical controllers remain deferred to production. Passing these cases is not proof of a perfect commercial match.
