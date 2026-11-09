# Revision17 bot navigation and pacing audit

## Scope and method
Owned arcade_ai.py and new test_ai_navigation_r17.py only. No game rules, power durations, collision behavior or rendering changed here. Baseline AI preserved in work/arcade_ai_before_r17.py. Reproducible harness work/measure_pacing17.py uses30Hz updates and decisions, seeds17/61,1/2/8 players on every map,90 simulated seconds each. Separate seed17 runs on all12 combinations continued through the180s timer. Automated coverage is not evidence of human enjoyment or exact commercial bot difficulty.

## Concrete defects fixed
1. Nearby collectible detection used Manhattan screen distance, excluding a power one legal step across a tunnel. It now measures up to14 legal corridor steps.
2. Giant rival pursuit only took priority when a roaming ghost also existed. When ghosts were in their house, a nearby dot beat the rival target. Hunt targets now take priority consistently; protected/private-bay rivals are excluded.
3. Empty refill periods retained a blocked or dangerous wanted direction. A deterministic legal least-danger neighbor fallback now keeps movement possible, respecting direction preference when equally safe.
4. An unreachable selected collectible could suppress reachable dots. Local reachability and fallback dot routes prevent this; the adversarial impossible-item test is robustness coverage, not a claimed normal-spawn defect.

All four adversarial cases fail baseline and pass current code. Six tests pass including5 seconds of sustained navigation for every1-8 player count on all four maps. No artificial speed or scoring boosts added to bots.

## AI-only comparison, original speed profile
Eight runs per player-count group. Coverage counts unique(layout,cell) pairs; reversal counts are movement-direction reversals, not proven pathological loops. Idle excludes entry/stun and includes normal movement waits. Pickup/rival totals aggregate all eight runs.

|Players|Mean coverage before/after|Reversals before/after|Pickups before/after|Rival hits before/after|Max idle before/after|Mean stage before/after|
|---|---|---|---|---|---|---|
|1|430.2 /435.0|193 /178|201 /229|0 /0|.17 /.17s|1 /1|
|2|675.1 /687.8|490 /438|278 /278|14 /15|.63 /.17s|1.50 /1.62|
|8|2254.2 /2204.2|4330 /3725|296 /298|79 /93|.77 /.37s|4.62 /4.75|

Not every metric improves: eight-player coverage falls slightly while interaction frequency rises. Normal contested pickups remain competitive; the policy does not reserve goals or remove rivalry. No persistent idle stall occurred in baseline or updated90s runs. All90s observations are right-censored for match finish. All24 full-duration baseline/updated seed17 matches finished at180s by timer, not elimination. Maximum full-duration idle drops.97s to.37s. These runs do not establish untimed survival duration.

Raw metrics: work/pacing_r17_before.json, pacing_r17_after.json, pacing_r17_before_complete.json, pacing_r17_after_complete.json. First pass inspected policy and ran baseline, then fixed demonstrated cases. Deeper pass ran adversarial baseline comparison, allcounts sustained navigation, identical long simulations and completion checks. Separate pressure-profile tests isolate parent's planned speed change with explicit tuning overrides; results appended below when complete.

## Isolated movement-speed pressure comparison

Same updated AI, seeds17/61,24 runs per profile,90s. Fast explicitly sets player/Rush/Slick/ghost/item intervals .10/.065/.055/.16/.24s; proposed slow uses .25/.1625/.1375/.4/.6s. Other timers/spawns unchanged. Near-rival fraction is Manhattan distance<=3, a proximity proxy that can include walls, not legal collision distance. Power fraction counts any active effect among living-player samples.

|Players|Power occupancy fast/slow|Near-rival fraction fast/slow|Death events fast/slow|Rival hits fast/slow|Pickups fast/slow|Mean stage fast/slow|
|---|---|---|---|---|---|---|
|1|0.812 /0.594|0.000 /0.000|3 /5|0 /0|229 /117|1.000 /1.000|
|2|0.648 /0.547|0.034 /0.048|26 /6|15 /5|278 /228|1.625 /1.000|
|8|0.238 /0.218|0.190 /0.227|140 /54|93 /30|298 /285|4.750 /2.250|

Slower movement reduces pickup saturation and total collisions/clears in this fixed-time sample; spatial proximity can rise because actors spend longer near one another. This is a tradeoff measurement, not proof of correct cabinet difficulty. Every90s pressure run remained unfinished; no elimination-time inference. Raw event/death/occupancy counts: work/pacing_r17_after_fast_pressure.json and pacing_r17_after_slow_pressure.json.
Independent reviewer dx_ledger read all updated AI and passed all6 tests in5.358s. No definite policy regression found; danger avoidance remains a softweighted cost, not a guarantee of survival.
## Actual slow-default rendering review
After CorridorTrack integration, recorded10 seconds on each map with8 simulated players, then an explicit C-to-D transition scenario. outputs/NeonNibblers/slow_tour_r17.gif and outputs/DX-slow-tour-r17.png are actual App output; the transition is scripted QA rather than an earned clear. All four scene contact frames inspected: coherent gates/house/tunnel presentation and less ground covered than old fast profile; no confirmed new clipping or corner-cut defect. Numerical review of17,117 interior player samples found zero off-centerline positions. Separate actual App straight/tunnel probes each observed66 moving frames with1.333333px travel per60Hz frame (80px/s), zero off-axis frames, including wrap. Raw checks: work/slow_visual_metrics_r17.json and work/slow_constant_motion_r17.json. This verifies constant rendered motion rather than claiming a subjective feel or exact cabinet animation match. Six AI tests also pass against final slowed defaults (3.955s).
