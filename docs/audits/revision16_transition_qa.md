# Revision16 continuous transition QA

The new `Match.transition_arena` path is used for stage clear while `new_arena` retains initial/reset semantics. Tests exercise all16 ordered layout pairs: legal actor positions and full Player progress retained, disappearing cells relocated deterministically without displacing later valid actors, no living-cell overlap, private bay entry countdown, dead/inactive slots, continue timers, carried ghost owner/attachment/zap timers, and house/leaving/entering/eyes reaching roaming after the change. Score award and stage-start preservation marker are checked through an actual stage-clear update.

## Two-pass defect finding

The first pass found player preservation and ghost state behavior consistent with the new contract. The deeper pass reproduced an item reservation defect: transition0→2 with Heart at disappearing(0,17) and Crown at legal(1,17) moved the Heart onto(1,17), unnecessarily displacing the static Crown to(1,16). Root fixed this by reserving already-legal item cells before relocating others. The added regression requires the Crown stay fixed, both items survive on legal cells, and Heart direction metadata follow its relocation.

## Final checks

`test_transition_r16`: **9 tests passed in2.595s**. Refill tests reflect the current authored0.6–1.1s stagger: no hidden dots score, displayed/collectible dots appear together, pending dots prevent another stage clear, all arrive at1.1s, and pause freezes state. The actual App render test verifies the preservation event retains actor interpolation, rendering never mutates the Match digest, score HUD coordinates do not move during contraction/expansion, enlarged actors are presentation-only, and paused/guide/results renders remain byte-identical with no animation advance.

These checks support the implemented transition contract, not exact commercial relocation, persistence, radius multiplier, or refill timing. No hardware controller claim is made. Root owns integration source; this agent changed only its separate tests and reports for transition QA.
