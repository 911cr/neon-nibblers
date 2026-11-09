# Revision16 reference audit — continuous maze transition

Source: Harold Zheng, Pac-Man Battle Royale Chompionship arcade gameplay, https://www.youtube.com/watch?v=qcO9tzgsdjo . Native Chrome, normal YouTube playback at0.25x. Two independent passes through the same C→D event; this is not two different cabinet sessions. Research screenshots stay outside the game ZIP. UI released paused5:14, speed restored1x.

## First pass

At5:01 (`work/r16-morph-a.png`) C is almost empty, score56980. At5:02 (`r16-morph-b.png`) score57,0xx and players/ghosts are dispersed. At5:04 (`r16-morph-c.png`) D has appeared with a scattered/sparkling refill and score60,0xx. Orange player remains in the lower-left corridor; green remains lower-right of the house; red/pink ghosts remain near the left perimeter and cyan remains near the house. No general player-to-bay or ghost-to-house reset occurs. At5:07 (`r16-morph-post.png`) normal gameplay continues on D.

This directly contradicts resetting every player and ghost for each map transition. It supports preserving field actors and fitting them to the new legal route if necessary. The exact remapping algorithm and effects preservation cannot be recovered here. No long-running power was clearly tracked across this particular change.

## Deeper pass: animation and reward

A second replay captures the5:03 midpoint (`work/r16-morph-detail.png`). Players AND normal colored ghosts appear globally enlarged while the maze shrinks/compresses toward its center and changes arrangement. This is a transition animation, not simultaneous acquisition of Giant by all players or giant ghosts. A floating orange **3000** appears above the approximately60,0xx station score. Together with approximately57,0xx immediately before, it strongly associates a3000 award with this clear/transition event. Whether the award scales by stage, player contribution, remaining time or some other factor is unknown; it is not evidence that every map always awards3000.

Whole-second samples bound the visible sequence: oldC5:02, midpoint5:03, newD/refill5:04. This supports a short transition, conservatively within an approximately3-second observation window; it does not measure an exact animation duration. The changing projection and sprite scaling prevent confidently separating physical movement from the animation during the pulse. A brief application freeze or specific easing curve must remain labeled an authored approximation. Do not claim all actor coordinates are numerically unchanged: regions persist, but map-relative projection changes.

Figure `outputs/DX-transition-evidence-r16.png` presents actual source crops, without perspective invention. No second independent transition was established in this bounded pass; the previous C→D observations are corroboration of this event, not a larger sample.

## Critical ghost/power check

Retained `work/r15-multi-color-5.png` at5:14 shows red and blue enlarged players while a normal red ghost with conspicuous white eyes is immediately below the house, and cyan remains inside. This is a useful challenge to an unconditional all-blue artwork rule. However, the red ghost may be exiting/recently respawned, so protected release could explain it. The observation is NOT sufficient to conclude that Giant never makes ghosts edible, or that a normal player can eat any blue ghost. Preserve the uncertainty rather than importing legacy Pac-Man rules.

The fresh5:03 transition gives a clearer normal-ghost visual: round dome, broad white eyes, blue pupils and continuous lower skirt. It does not isolate the frightened face. Smoke/zap overlap around5:07 obscures attribution. There is no new exact duration, global-vulnerability rule, smoke area or AI targeting measurement in this pass. Category coverage remains separate from behavioral fidelity.

## Concrete action and honest boundary

1. Preserve actors across maze progression; avoid unconditional bay/house resets.
2. Show a transition pulse and gradual/scattered dot refill rather than a bare instant map swap. Exact curve/duration is custom.
3. Record the observed3000 clear-associated award; do not extrapolate its schedule without another isolated clear.
4. Keep ghost global-vulnerability and protected-release visual questions open.

Neither reviewer agreement nor internal regression checks establish an exact DX replica. This audit approves only the observed corrections above.

Critical digit correction: magnified score crops (`work/r16-score-check.png`) suggest60020 after, with preclear tens blurred (likely57020). Earlier messages transcribed57030→60030 too confidently. Only the floating3000 is clearly legible; the final audit deliberately uses57,0xx→60,0xx.
