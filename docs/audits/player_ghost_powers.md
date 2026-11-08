# Player–ghost / power interaction audit — 2026-11-08

Audited current revision5 work-in-progress game.py without editing it. Independently retrieved the CHOMPionship DX-specific distributor description:
https://primetimeamusements.com/product/pac-man-battle-royale-chompionship-dx/

## Supported categories across all eleven

| Analog | Supported interaction category | Current direction / limit |
|---|---|---|
| Crown | Eat ghosts | Basic category correct; protection currently suppresses eating (bug below). |
| Titan | Eat ghosts and smaller rivals | Correct category; blanket immunity to all attacks remains custom. |
| Rush | Faster movement | Changes encounter speed; no documented direct immunity. |
| Mist | Smoke slows ghosts | Local smoke slowdown now matches category; radius/duration custom. |
| Slick | Uncontrolled skidding | Holder skid now matches category; ghost damage remains normal. |
| Spark | Zap nearby actors | Nearby stun is provisional; lethality not specified. |
| Veil | Invisible to ghosts | Suppressed targeting matches category; contact vulnerability unverified. |
| Flare | Burn nearby actors | Corridor fire is provisional; direction/range/lethality unverified. |
| Quake | Everyone slows | Collector included now; ghost inclusion/timing not firmly specified. |
| Heart | Extra life | No direct ghost behavior change. |
| Lure | Carry a ghost as weapon | New carry category correct; release/capture precedence custom. |

The source establishes categories, not damage matrices, ranges, stacking or durations. Do not certify current implementation as exact. Predecessor pages often mix original round-based rules into sequel descriptions; excluded those paragraphs.

## Concrete code findings

1. **Stale carried ghost can kill after owner dies or power expires.** `update_foes` reconciles carried mode only on its 0.16-second tick, while `combat` trusts carrier ownership immediately. Reproduced with dead holder/no Lure, a carried ghost at victim position, and `combat()`: owner gains300, victim loses a life. Reconcile owner validity every simulation frame before combat, or guard carried branch; reset/release exactly once. This also matters when holder dies earlier in the same combat loop.
2. **Respawn safety suppresses active ghost eating.** `if p.safe>0: continue` is before Crown/Titan handling. This prevents a protected player from eating a ghost despite active power, but Lure capture already occurs before the check. Put protection in the hurt branch (hurt already checks it), keeping active hunter power effective.
3. **Carried weapon lags holder.** Its logical position updates at ghost cadence rather than player cadence; fast Rush/Slick holders can move several times between attachment updates. Update carried position each frame after player movement, with a valid-lane anchor and consistent visible offset. Add a test for fast movement plus pickup/drop.
4. **Global blue rendering versus local damage rule is ambiguous.** Any living Crown/Titan holder turns all roaming ghosts visually edible, but an unpowered player touching them still dies. This might be intended original behavior or not; the inspected sequel sources do not settle it. Do not call it exact. A clearly documented danger rule is needed until footage resolves it.
5. Returning/house/leaving ghosts are intentionally harmless, but exact doorway combat window and stun/quake immunity remain custom. Existing player-ghost crossing logic addresses opposite-direction swaps; add a regression to prevent later state refactors breaking it.
6. Magnet stacking currently wins over Crown/Titan (captures instead of eating), and multiple ghosts may be captured. The public description does not define precedence or maximum count. Document and test these choices rather than silently presenting them as source facts.

## Targeted checks

- Normal collision and opposite-edge crossing both lose exactly one life; safety prevents repeated loss.
- Crown/Titan consume roaming ghosts once, including while safe; house/return eyes cannot be farmed.
- Veil removes tracking but does not protect against rivals; contact outcome explicitly tested as chosen custom rule.
- Smoke slows only ghosts inside its region; outside movement unaffected; Quake includes its collector.
- Capture, carry following, rival contact, expiration and holder death; no stale kills or score after release; no duplicate ghost identities.
- Spark near/far targets; Flame blocked by walls; timed effects expire and do not leak to next stage.

No shared game files edited. Findings sent to root before final report.

## QA1 — defect verification after root fixes

Executed `work/qa_player_ghost.py` against the current source with pygame-ce from work/deps. Four focused groups PASS:
- Dead and expired magnet holders cannot award weapon kills; their carried ghost becomes returning eyes.
- Respawn-protected Crown/Titan holders can now eat roaming ghosts once.
- Carried position follows holder on sub-tick updates, before the normal ghost cadence.
- Returning eyes traverse the doorway and move home in steps of at most one cell; entering and house states both observed.

Original concrete findings1–3 are resolved in this tested source. This does not verify commercial timings or exact state rules.

## QA2 — adversarial interaction pass

Four additional scenario groups PASS:
- Opposite-edge crossing for normal/Crown/Titan/Lure: ordinary damage, hunter eating and capture each resolve correctly.
- Four simultaneous captures: all identities retained, victim loses only one life per protected contact, holder receives one300-point reward, and expiration releases every capture without duplicate bodies.
- Holder bitten by a Titan in the same combat frame: after its effects clear, a subsequent contact cannot award another stale weapon kill.
- Ordinary respawn protection prevents ghost damage; house/leaving/eyes/entering ghosts cannot be eaten repeatedly for score.

Total:8 focused scenario groups, all pass. No additional concrete blocking bug found in this pass. Source is actively changing, so these results apply to the version read/executed during this review.

Still UNKNOWN/custom rather than bugs proven against reference: global blue ghost appearance vs per-player vulnerability, lightning stun vs kill, ghost-sheet incidental contact damage, Titan immunity to fire/weapon damage, multiple magnet captures, stacking precedence, doorway immunity windows, and exact durations/ranges.
