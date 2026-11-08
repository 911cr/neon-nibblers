# Revision 10 gameplay timing and contact audit

2026-11-08. Baseline supplied by root: revision 9 commit `2165f5a`, 72 tests. Match changes only; root owns presentation/audio. Physical devices remain deferred. No new commercial timing measurement is claimed.

## First pass: simultaneous events and expiration

**Reproduced station-number advantage.** Place a lightning pickup at `(2,1)`, its collector at `(1,1)` moving right, and another player at `(5,1)` moving right. With a 0.1-second update, P1 collecting first prevented P2 from moving and left a 1.9-second stun; swapping the logical player numbers let the victim move to `(6,1)` and left a full 2.0 seconds. The same ordering defect exists at fixed 60 Hz, with one simulation tick of bias. Player timer aging and pickups were interleaved inside the player loop.

**Correction:** age all player and ghost timers before resolving new pickups, move all players, then resolve item contacts. Separate ghost timer aging from ghost movement so a newly created zap does not immediately lose a simulation interval. Two simultaneous lightning collectors now both complete that tick's movement and both receive the full configured stun. Competition for exactly the same collectible still uses stable station order; its commercial tie rule remains unknown.

**Reproduced expiration tail.** After exactly 120 fixed ticks, a two-second banana effect still contained a positive `2.1024848528838902e-15`, keeping its behavior active one extra tick. Similar floating-point tails affected safety and match time. Added `Match.countdown` with a small numerical tolerance. This preserves intended durations while making their endpoint reproducible. Applied to Match countdowns and, by root, locator duration. Every timed pickup category is tested immediately before and on its configured final tick. No assertion is made that those configured numbers are DX's exact durations.

## Second pass: moving collectibles and state integration

**Reproduced missed physical contact.** A moving caffeine item at `(4,1)` with established rightward travel entered a stationary or stunned player's `(5,1)` cell. The item remained on the player with no power or points because collection was checked only when the player's movement clock fired. It could subsequently leave without being collected.

**Correction:** a shared contact collector runs after player movement and after item movement for living players, even when they are stationary/stunned. It removes the item and stale direction entry, emits one pickup event/sound, and awards exactly one pickup score. The post-item movement phase also invokes the once-only bonus-life check: a player at 9,950 receiving the 75-point roaming item reaches 10,025 and gains the life in that same tick. Actual damage sounds remain driven by damage events, so an unrelated life gain cannot suppress them.

**Ghost checks:** retained current adaptation AI rather than importing classic single-player behavior without evidence. The review verifies hidden players and players inside bays do not enter the target-selection branch, roaming ghosts remain on legal corridor cells, and each tested move follows a valid edge. Reverse choices and probabilistic greedy targeting remain custom and are not certified as DX logic.

**Render/time checks:** root's locator expires exactly at 120 fixed ticks for its configured two-second duration. Pausing plus rendering does not mutate the Match state or consume remaining locator time. Updated simulation state and event fingerprints remain identical when the fixed-step runner receives render intervals grouped at 30,60,144 Hz.

## Verification

`test_revision10_gameplay.py`: **8 tests PASS**, covering swapped and simultaneous lightning pickups, all timed power endpoints, safety/match endpoints, ghost targeting exclusions, moving-item/stunned contact and same-tick bonus life, locator pause/boundary, deterministic grouped timing and replay.

Combined discovery reported **92 tests PASS** in 18.453 seconds after contact collection and before the final one-line post-contact bonus check. The full eight-test targeted suite passed again after that bonus correction; root performs final integrated platform/package runs. Source handed back to root with no further Match edits pending. Gameplay recordings and replay samples must be regenerated because the corrected event ordering and contact handling change trajectories.

## Fidelity distinction and remaining limits

These changes repair internally inconsistent movement, timing and collection semantics. They do not resolve undocumented DX lightning lethality, range, immunity, ghost AI, effect stacking, score values or exact life/round rules. Original artwork/code/audio remain independent. Reference evidence and unknowns remain in the seven DX tracking documents; this audit does not turn passing implementation tests into commercial-match proof.
