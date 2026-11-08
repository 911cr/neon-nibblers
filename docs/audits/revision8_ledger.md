# Revision 8 ledger/replay adversarial review

Reviewed 2026-11-08 by the scoring/replay implementation agent. Two passes plus integration recheck. These are software findings, not certification of DX scoring values or commercial fidelity.

## Pass 1: attribution and preservation

All runtime score changes now route through `Match.award`. Tested all eight reward paths: dot, pickup, eaten/burned ghost, eaten/burned rival, carried-ghost hit and stage clear. Each generates a player-specific event with timestamp/tick/stage/delta/result and interaction context. Zero-point events cover relevant lifecycle changes. All 11 pickup categories retain their existing custom behavior. Immune attacks and repeated hits cannot create phantom rewards; bonus life is logged once. The previous 29 smoke tests passed immediately after ledger integration.

Rankings preserve score ties and exclude unjoined sparse stations. `join_station` retains another player's score, does not revive an eliminated participant for free, and rejects joining during pause/results. Same-tick P8/P4 join order is reproduced by the replay tool.

## Pass 2: determinism and tampering

Tested JSON round-trip replay for 1/2/4/8 players on all four maps, seed sweep 1–8, seeded random/cycle/repeat progression, and deliberate seed/input/event corruption. Divergence is rejected rather than silently accepted. Fingerprints include map ID/revision, RNG state, complete logic state and event history. Ten-Hz movement traces provide inspectable positions and ghost modes alongside fingerprints. The packaged 12-second eight-player replay verifies 720 frames and 431 events.

Separate fixed-step runner tests group the same simulation at 30/60/144 Hz. An independent App test then started only P8, used seeded autoplay for three seconds, and called the actual `App.advance` 90/180/432 times. All yielded 180 simulation ticks and identical complete state/event digest `58de45dd4b2d18df2d15cf374f97e29a467d2615255aa910b053f959f0e1ab6d`; the locator expired in each.

## Render/UI integration recheck

Two additional tests bring `test_revision8_ledger.py` to **12 passing tests**:

- Two 75-point pickups before one draw produce two separate `75` popups, never an invented combined score notification. The next draw does not duplicate events. HUD score memory equals the model, and drawing leaves the complete Match digest unchanged.
- A pending half-step is discarded on pause/guide, ten seconds of suspended time produce no catch-up, rendering during suspension does not expire the locator, and resuming advances exactly one requested tick. Sparse inactive stations retain zero lives and zero score.

Found and reported a pre-existing autoplay alias that could remove an unscored dot. Main developer fixed it by copying the goal set. During integration an existing reconnect test failed (`missing=1` after same-instance reconnection). Main developer added same-instance reservation recovery; independently reran `test_production_controller_warning_and_hotplug_recovery`: **PASS**. No physical USB claim is implied.

## Limits and next work

The replay tool covers simulation direction/join commands, not complete OS input, physical devices or App locator-button playback. Locator time currently belongs to App; recorded Match-only scenarios do not invent those UI events. Native rendering smooths positions/animations using elapsed draw time; logic reproducibility is verified independently of pixel identity. Direct arbitrary large `Match.update(dt)` calls remain unsuitable for timing fidelity measurements; use the fixed-step App/runner.

No reference evidence establishes current 10/75/200/300/500 values, score-attack duration, tie presentation, reward combinations or stage-clear bonuses as exact DX behavior. Persistent high scores and actual commercial scoring measurements remain open. See `DX_SCORING_AND_INTERACTIONS.md` and the feature parity matrix.
