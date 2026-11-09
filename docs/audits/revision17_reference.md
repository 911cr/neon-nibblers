# Revision17 — movement and encounter pacing reference

Source: Harold Zheng, *Pac-Man Battle Royale Chompionship arcade gameplay*, https://www.youtube.com/watch?v=qcO9tzgsdjo . Released eight-station DX footage. Native Chrome playback at0.25x; timestamps below are SOURCE-video time, not wall-clock playback time. Captures are research-only outside the package. UI released paused4:23, speed restored1x.

## Pass1: continuous movement sample

The4:09→4:13 interval shows two normal-sized player sprites traveling left on long straight routes of familyC. Blue moves along the bottom corridor; purple along the top. Neither shows an obvious trail or enlargement. Orange on the right becomes enlarged during the same interval; orange is therefore excluded from the normal-speed estimate.

| Source time | Capture | Blue approximate screen center | Purple approximate screen center |
|---|---|---|---|
|4:09|work/r17-speed-249.png|790,440|900,303|
|4:11|work/r17-speed-a.png|670,420|807,284|
|4:13|work/r17-speed-b.png|605,411|760,274|

Both tracked actors move monotonically left, staying near their respective long perimeter rows. Camera orientation remains similar, but slight camera movement and perspective must be accounted for using nearby wall junctions and dots. Pixel distances alone cannot become world-speed measurements.

## Pass2: adversarial measurement check

The lower row's nearby dots are approximately13–15screen pixels apart; upper-row dots approximately9–11px apart. Blue travels about185horizontal pixels and purple about140, yielding broadly12–15dot spacings for each over the nominal4seconds. Because each displayed timestamp truncates to a whole second, the true interval is roughly3–5seconds; dot counting also has perspective/occlusion uncertainty. A defensible coarse observed band is approximately **2.4–5dot spacings per source second**, with midrange around3–4. This is a calibration clue, not a recovered exact base constant.

The second actor/row agrees with the first and therefore weakens the explanation that the low displacement is only camera drift. No turn or reversal appears in these captured subintervals. The review does not establish joystick input, hidden status, brief between-capture interactions, or a cabinet difficulty setting. Blue player identity is based on its colored mouth-bearing sprite and continuous route, distinct from nearby white returning ghost eyes. The annotated figure preserves these identity choices for independent review.

Root reported the revision16 application default as10logical dot cells/second (20pixel cells at.10s). If each app cell corresponds to one depicted source dot interval, that default is materially faster than this sample, roughly2–4times the coarse observed range. **Do not confuse source dot spacing with the implementation's navigation grid before changing the constant.** A trial reduction with timing tests and human/visual review is justified; declaring one exact DX speed is not.

## Encounters, collisions and fun

The same interval contains orange growth near cyan on the right and green activity near returning ghost eyes on the left. By4:22 actors have reached the house/central loops and multiple ghosts are near the house. This confirms an active shared field with meaningful nearby encounters; it does not yield a pickup generation interval or encounter-rate statistic from one camera sample. Growth onset is not equivalent to the item spawn time.

No clean isolated equal-size head-on collision was recovered in this pass. Exact recoil distance/duration, held-input behavior and multi-contact priority remain open. Camera-distant mixed actors and effects must not be turned into invented bounce measurements. Likewise, whether an AI intended to chase a rival cannot be inferred from a single shared direction. Internal regression tests can verify that the parody does not repeatedly push/jitter under held controls; they do not certify DX contact physics or prove that the game is fun.

## Deliverable and action

`outputs/DX-movement-evidence-r17.png` shows actual crops at4:09/4:11/4:13 with circles marking the two tracked players. No synthetic reference art or commercial media is included in the runnable package. Confidence: medium for slower movement than the reported10-dot/s app default; low for an exact base speed; insufficient for exact collision or spawn rules. Both passes concern this one continuous interval, not independent cabinet sessions.

Recommended next software check: report actual dot cells per second for normal/Rush/giant movement and time a fixed straight run; compare the normal run visually against this source interval. Keep responsive buffered turns separate from travel speed. Preserve explicit tuning provenance and evaluate1/2/8-station pacing after any adjustment.

## Independent motion integration QA

Two code-review/test passes added `test_motion_integration_r17.py`: all nine checks pass using real App drawing with SDL dummy display/audio and temporary cabinet stores. Coverage includes axis-aligned rendered turns without changing scores/lives/dots/ledger, pause/resume, short tunnel wrapping, death relocation, restart track cleanup, externally replaced visual positions, fifty-pixel gate traversal in one logical movement interval, ghost/item pause, removed-item track cleanup, and reversals at 1/2/8 players. The actual App motion adapter travels 400 pixels over five seconds at 30/60/144Hz without a growing waypoint backlog.

These verify internal presentation behavior, not exact DX motion. A long frame that advances logical simulation through multiple turns supplies only its final target to drawing; diagonal relocation deliberately snaps rather than inventing a route through walls. Normal tested frame rates at four dots per second avoid that case. No physical-controller claim is implied.
