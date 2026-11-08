# Scoring, event attribution and interactions

Revision 8, 2026-11-08. Status **IMPLEMENTED AND TESTED** describes Neon Nibblers software; it does not mean **VERIFIED DX**. No scoring amount below has been recovered from an unambiguous DX scoring sequence in this cycle. Existing values are preserved as configurable adaptation settings in `score_ledger.DEFAULT_SCORES` / `Match(score_values=...)`.

## Score event audit

| Event | Current points / recipient | Exact trigger | DX value evidence | Next evidence needed |
|---|---|---|---|---|
| `dot` | 10 / collector | Successful movement step ends on an unconsumed dot | UNKNOWN | Isolated before/after score digits during one pellet pickup |
| `pickup` | 75 / collector | Any of all 11 power categories collected | UNKNOWN | Each category in isolation; identify whether item points differ |
| `ghost_eaten` | 200 / Crown or Titan holder | Roaming ghost contact or edge crossing | UNKNOWN | Single and consecutive ghost eats; possible escalating multiplier |
| `ghost_burned` | 200 / flame owner | Roaming ghost inside wall-bounded flame cells | UNKNOWN | Score before/after pepper attack |
| `rival_eaten` | 300 / giant attacker | Smaller rival takes damage on contact or crossing | UNKNOWN | Attacker and victim score indicators simultaneously |
| `rival_burned` | 300 / flame owner | Rival actually loses life to flame | UNKNOWN | Pepper hit with score and life indicators visible |
| `carried_ghost_hit` | 300 / living magnet owner | Carried ghost actually damages another player | UNKNOWN | Ownership and score attribution during carried attack |
| `stage_clear` | 500 / each surviving player | No dots remain, time remains, at least one survivor | UNKNOWN | Continuous DX transition sequence with all scores visible |
| Bonus life | 0 score / eligible player | First crossing of 10,000; up to five lives, no revival | Manual example supports 10,000 threshold; cap/once-only semantics UNKNOWN | Operator setting variants and repeat threshold crossing |
| Extra life item | Pickup points above, life +1 capped at five | Heart pickup | Basic extra-life category supported; cap and pickup points UNKNOWN | At-cap pickup and score before/after |
| Bump, death, survive, capture | No points | These events do not currently award score | UNKNOWN | Establish whether real game awards survival/capture or subtracts score |

No combo multiplier, separate special-food class, persistent high-score table or configurable credit accounting is implemented. These remain gaps, not evidence that DX lacks them. The three-minute timer, highest-score victory and early all-eliminated ending remain adaptation choices. Equal totals share a competition rank; station number only stabilizes row ordering and never breaks a tie. Eliminated joined players remain in rankings. Unjoined stations do not.

## Event ledger and replay

Every live score mutation now passes through `Match.award`. The same `Player.score` supplies the HUD and ranking values. Ledger records are deep-copied at event time and contain sequence, simulation timestamp, tick, event, one-based player ID, stage, score delta, resulting score and collision/power context. Zero-point records include match start/end, station joining, damage, extra life, threshold bonus, ghost capture and stage start. `ledger.totals()` independently reconstructs points awarded per player; gameplay tests assert equality with model totals.

`python replay.py record sample.json --players 8 --seconds 20 --seed 42` stores seed, settings, progression policy, fixed 1/60-second inputs, per-second state/event fingerprints, 10 Hz player/ghost movement traces and the complete ledger. `python replay.py verify sample.json` reconstructs the actual Match logic and rejects changed input, changed seed, changed events or divergent state. `Match.snapshot()` includes all logic timers, actors, effects, items, dots, ghost states, map ID/revision and random-generator state. This is a reproducible regression format for this game version, not a promise of replay compatibility after future rule changes. Versioned replays should retain the producing commit. It covers logic direction/join commands, not raw physical-device or operating-system events.

`FixedStepper` provides a 60 Hz accumulator so the same input schedule produces the same state at 30, 60 and 144 render updates per second. This is separately tested. Calling `Match.update` directly with arbitrary large deltas is **not** frame-rate independent: movement currently processes at most one cell per call. Use the accumulator or the fixed-step replay tool for timing comparisons.

## Interaction matrix: implemented approximation

The category-level reference is the [DX distributor description](https://primetimeamusements.com/product/pac-man-battle-royale-chompionship-dx/), plus the promotional poster reviewed in the preceding audit. These establish categories, not numerical timers, stacking, damage immunity or hit geometry. The [DX operation manual](https://bandainamco-am.com/cdn/shop/files/Pac-Man_Battle_Royale_Chompionship_DX_Manual_5_12_revise_Edit.pdf?v=18440531496271041764) documents operator controls/settings, not this combat matrix. Source details and confidence are tracked in `DX_REFERENCE_EVIDENCE.md`.

| Power | Ghost interaction | Rival interaction | Repeated/combined pickup and expiration | Fidelity status |
|---|---|---|---|---|
| Gold | Eat roaming ghosts, including during respawn safety | Does not eat rivals | Refresh seven seconds; magnet capture takes precedence | Category supported; precedence/timing UNKNOWN |
| Green giant | Eat roaming ghosts | Eat smaller rival; equal giants bump; `hurt` blocks damage | Refresh seven seconds; Rush still speeds giant | Category supported; blanket immunity/stacking UNKNOWN |
| Caffeine | Changes contact cadence through faster player speed | Same damage rules | Refresh seven seconds; quake doubles movement interval | Category supported; combined multiplier UNKNOWN |
| Smoke | Nearby smoke slows roaming ghosts | No direct damage | Trail seven seconds; clouds 2.5 seconds; quake combines | Category supported; range/stacking UNKNOWN |
| Banana | Normal vulnerability | No direct attack | Forced fast slide two seconds; takes precedence over Rush | Category supported; rebound/timing UNKNOWN |
| Lightning | Nearby ghost stun, not kill | Nearby rival stun, including safe/giant actors | Two-second stun overwritten; no persistent player power | Zap category supported; lethality/immunity UNKNOWN |
| Sheet | Removes holder from targeting, not incidental contact | No rival immunity | Refresh seven seconds; translucent rendering | Concealment supported; contact outcome UNKNOWN |
| Pepper | Burns roaming ghosts ahead through legal corridor cells | Damages nonimmune rival | Refresh three seconds; walls stop reach | Category supported; exact shape/range UNKNOWN |
| Earthquake | Doubles roaming ghost movement interval | Doubles all player intervals including collector | Refresh global five seconds; combines with Rush/Smoke | All-player slowdown supported; ghost scope/timing UNKNOWN |
| Extra Life | No direct effect | No direct effect | Immediate life +1, cap five; pickup score remains | Extra life supported; cap/value UNKNOWN |
| Magnet | Multiple contacted ghosts captured, held ahead | Carried ghosts damage rivals and award owner | Refresh seven seconds; death/expiry release harmless returning eyes | Carry weapon supported; count/immunity/release UNKNOWN |

Damage clears player effects and stun/movement clocks. Map transition clears powers, smoke, carriers and stun, preserving lives, score and remaining time. These persistence rules remain UNKNOWN for DX. Existing smoke tests cover local ranges, wall blocking, quake/Rush composition, head-on crossings, equal giants, multi-ghost capture, expired/dead-owner weapons and repeated ghost scoring protection. They prove the stated implementation, not undocumented reference rules.

## Two-pass review of this cycle

Pass 1: all previous 29 smoke tests passed after routing every score path through the ledger. Eight new ledger/replay tests pass, covering all eight reward routes, damage/bonus events, same-tick attribution, immune/repeated attacks, tied ranking, sparse joining, 1/2/4/8 players on four maps, JSON replay and deliberate tampering.

Pass 2: searched the whole game for score assignments; only `award` changes runtime score. Twelve ledger tests now pass, adding seeds 1–8, deterministic cycle/repeat/random progression, sparse P8/P4 joining in the same recorded tick, exact individual score popups, and paused/guide locator timing without catch-up. Tested grouped fixed-step timing at 30/60/144 Hz and score-total reconstruction. Found a pre-existing autoplay defect: selecting `g.dots` directly as a navigation goal set then discarding the current cell could remove an unscored dot. The main developer corrected the alias to copy the set. Recorded and verified the included 12-second eight-player sample: 720 simulation frames, 431 events. Main integration testing separately found a controller-reconnection assertion failure; the main developer fixed same-instance recovery and this reviewer independently reran the original test successfully. Remaining gaps include commercial scoring measurements, custom timer/finish rules, scoring UI comparison, durable high scores and full external-game interaction evidence.
