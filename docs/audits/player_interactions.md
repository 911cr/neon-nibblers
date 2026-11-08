# Player-player interaction audit — 2026-11-08

## Evidence and version distinction

The official **2022 CHOMPionship Deluxe** manual is readable through web search/open at:
https://www.bandainamco-am.com/Ecommerce/Site/Content/PDFs/Pac-Man%20Battle%20Royale%20Chompionship%20DX%20Manual_5_12_revise_Edit.pdf

Its Adjustments screenshot explicitly shows `Lives to Start: 3` and `Bonus Life at 10,000`. Its Control Panel Test shows top row 4,8,7,3 and bottom row 1,5,6,2. It is an operator/hardware manual and does **not** document detailed combat, knockback, immunity or victory timing. Web tool retrieved the complete 470-line extracted document successfully (root may have hit hostname without www). Do not infer absence of a rule from absence in this manual.

CHOMP-specific product power list: https://www.gameroomguys.com/Namco-Pac-Man-Battle-Royale-Chompionship — gold makes ghosts edible; green enlarges the player and allows eating ghosts and normal opponents. This corroborates our Crown/Titan distinction. Commercial listing, not a timing specification.

Official predecessor description: https://bandainamco-am.com/collections/pac-man-battle-royale — equal-size players bounce, powered players eat smaller rivals, round winner is last standing. This describes **original four-player Battle Royale**, not CHOMPionship. The original manual likewise describes knockback into ghosts. Those cannot automatically be treated as verified sequel rules.

CHOMP overview https://www.mobygames.com/game/198053/pac-man-battle-royale-chompionship/ confirms sequel, eight players and competing to eat one another. CHOMP-specific firsthand/secondary descriptions say multiple lives and score leaderboard. They do not establish the exact scoring or finish conditions.

## Current implementation and recommendations

- `combat()` only resolves a Titan-vulnerable rivalry. Normal-normal and Titan-Titan contacts overlap/pass through. A visibly responsive equal-size bump is a worthwhile fidelity fix, but label its exact displacement/cooldown as adaptation until verified in CHOMP footage. Suggested implementation: use the already available previous positions to separate pair members, reverse away along valid corridor edges, and a short per-pair cooldown. Do not push through walls/gates or award points merely for bumping.
- Crown cannot eat players; Titan can eat normal/Crown players. This matches the CHOMP-specific description. Preserve it.
- Equal Titans cannot eat each other, reasonable from equal-size behavior but not independently verified for CHOMP. Add pairwise tests (normal/normal, normal/Titan, Crown/Titan, Titan/Titan, crossing collisions and immunity). Current tests cover mostly Titan attacks and crossing.
- Titan unconditionally blocks `hurt()` from all causes and slows movement (.14s vs .10s). Neither universal immunity nor slowdown is established by the CHOMP references. Keep these identified as custom, or narrow protection to physical bites/ghost contact while deciding how lightning/fire interact from power audits. Do not cite the original game's faster power pellet as sequel proof.
- Start with three lives matches the official example setting. There is no score-threshold bonus-life logic. Add one configurable first bonus at 10,000 if matching the shown default, with a once-only flag and tests crossing threshold by multiple simultaneous rewards.
- Three-second respawn immunity and .8-second gate release are custom values. Do not call exact.
- Highest score after 180 seconds, all-player elimination finish and winner eligibility of eliminated players are custom/unverified. Do **not** replace with predecessor last-player-standing without sequel evidence. Expose/document timed score-attack as an adaptation if retaining it.

## High-value regression checks

All ordered 2/8-player pairings for normal and powered states; collision at intersection, opposite crossing and following; no multi-frame score farming; separation remains inside owner-accessible graph; safe respawn cannot immediately lose another life; bonus awarded exactly once at 10,000.

No shared game files were edited.

## QA PASS 1 — current revision implementation

Executed `python outputs/NeonNibblers/test_smoke.py` with local `work/deps`: **23 tests passed**. Code review confirms Crown/Titan distinction retained, normal/equal-size bump added, Titan movement slowdown removed from actual movement calculation, first bonus life at 10,000 added, and Veil no longer shields rival damage. Tests cover attack crossings, ordinary separation and first bonus life once. Note: ITEMS Titan guide text still says "slower" although speed calculation no longer slows Titan; update player-facing help.

Reference limits remain: exact CHOMP normal/equal-size knockback, universal Titan damage immunity, timer/end conditions, knockback distance and cooldown are not verified. Passing implementation tests cannot certify exact matching.

## QA PASS 2 — adversarial local reproductions

Executed `work/player_interaction_qa.py` against current code (no shared code edits):

1. **FAIL: opposite crossing moves players through one another.** Start P1 `(1,1)` facing right, P2 `(2,1)` facing left, no powers/foes/items, zero safety, then `update(.11)`. Actual P1 `(3,1)`, P2 `(2,1)`, both facing right. Original left player ends to the right of the other. `bump()` excludes the old position because the other player now occupies it, so chooses a forward cell. Fix crossing first by restoring the two prior positions and reversing outward; then apply normal valid-cell separation. Preserve no-wall/no-owner-gate rules.

2. **FAIL: cooldown suppresses collision resolution completely.** A first same-cell contact at `(5,1)` separates to `(6,1)` and `(4,1)`. Recontact at `(5,1)` while pair cooldown remains returns both at `(5,1)`. A cooldown can throttle new impulses/animation, but must not disable overlap or crossing prevention. Add regression using genuine successive movement/input steps, not only direct combat calls.

3. **Crowded intersection weakness:** eight normal players placed together at `(5,1)` resolve to only two unique positions, alternating `(6,1)`/`(4,1)`. This intentionally adversarial starting state exposes single-pass pair-ordering; later pair pushes reoccupy earlier resolved positions. Consider a bounded global occupancy-resolution pass after pair interactions. This is secondary to the reproducible two-player crossing bug.

4. Stage clear crossing 10,000 awards the bonus on the following update rather than the same update, because bonus check precedes stage-clear score. Reproduction: 9,950 score + clear =>10,450/lives3/bonusFalse; next update =>lives4/bonusTrue. Minor consistency issue, not repeated-award bug.

Status: functional QA **NOT clear** until crossing and cooldown collision bugs are addressed. Exact commercial interaction match still unknown even after fixes.

## Targeted fix recheck — resolved

Reran the original adversarial script against the fixes and inspected/executed the new crowd/crossing/gate-reset regression plus prior ordered-pair/crossing and bonus checks. All three selected tests pass.

- Head-on crossing now preserves player ordering: P1 `(1,1)` facing left; P2 `(3,1)` facing right. Both retain three lives.
- Recontact during cooldown now separates to `(6,1)` and `(4,1)` rather than overlapping.
- Eight coincident players now resolve into eight distinct owner-accessible cells.
- The stage-clear threshold awards its one bonus life in the same update, with no second award next update.
- Titan help now omits the removed slowdown.

Previously reported functional defects are resolved in these reproductions. No additional confirmed failure found in this targeted recheck. This is functional clearance of the audited cases, NOT certification of exact commercial knockback distances, timing, immunity or winner rules; the reference gaps above remain.
