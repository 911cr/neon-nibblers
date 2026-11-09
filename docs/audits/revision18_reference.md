# Revision18 — fresh power interval and ghost presentation evidence

Research date:2026-11-09. Source: [Harold Zheng, Pac-Man Battle Royale Chompionship arcade gameplay](https://www.youtube.com/watch?v=qcO9tzgsdjo&t=249s), confirmed released eight-station DX cabinet, spectator display. Native Chrome playback at0.25x; no downloaded video or commercial art enters the game. Original screenshot perspective is retained: house doorway toward the far/top side of the displayed field. Screenshots are camera views, not a lossless framebuffer.

## First pass: continuous interval

Played from4:08 through4:26 with repeated visual observations. Orange starts normal-sized on the right side, moves left through a green pellet position, becomes visibly large, then travels upward beside the house and left above it. The actor remains in the public maze when it shrinks; there is no bay return or whole-stage reset at this transition.

| Timestamp | Actual observation | Retained evidence |
|---|---|---|
|4:09|Normal orange actor right-center; green pellet immediately ahead to its left.|work/r18-orange-249.jpg|
|4:11|Orange enlarged; green pellet no longer visible at its prior location.|work/r18-orange-251.jpg|
|4:15|Orange still large beside the house. Pink body inside house and red body near its upper side.|work/r18-orange-255.jpg|
|4:19|Orange still clearly enlarged above/right of house.|work/r18-orange-259.jpg|
|4:19, later fractional position|Blue ghost bodies outside AND two inside house.|work/r18-ghosts-259b.jpg|
|4:20|Orange normal-sized in upper-central corridor; still on its route.|work/r18-orange-260.jpg|
|4:21/4:22|Orange continues at normal size; blue ghost bodies still visible near/in house.|work/r18-orange-261.jpg; work/r18-orange-262.jpg|

The score readout appears approximately40,730 before and41,760 after growth, compatible with the independently established1000-point green pellet plus dots. This is not an isolated scoring measurement and does not establish additional score rules.

## Second, more critical pass

Replayed onset from4:09 and expiry from4:19, then separately paused at4:20 and4:21 to verify the size change. Distinct wall references and the same orange actor were followed; a change in camera scale cannot explain orange shrinking while the neighboring maze and actors remain similarly sized. No second green pickup is visible along the tracked right-center → house-right → upper-central route. However, point-in-time observations and distant footage do not exclude every brief refresh or hidden status. Replaying one source sequence is not independent confirmation from another cabinet.

Growth onset is bracketed by displayed4:09/4:11; shrink is bracketed by4:19/4:20. Whole-second UI timestamps, fractional seeks and growth/shrink animation imply a conservative duration interval of roughly8–12seconds. A ten-second Giant/Titan duration is a plausible provisional tuning choice, not a recovered exact constant. No evidence here changes the other ten effect durations or establishes a difficulty/stage-dependent schedule.

Ghost presentation has a firmer actionable observation: blue bodies occur inside the house, including both occupants in the4:19 later frame. The old renderer restricted blue presentation to roaming ghosts. Extending the existing blue presentation to housed/leaving bodies is supported visually. It does NOT imply that housed ghosts can collide with or be eaten by players. Protected house-path mechanics must remain separate from sprite coloring.

A tempting but rejected inference was “red/pink ghosts alongside orange growth disprove global vulnerability.” Close review reveals differently colored versus blue bodies across nearby samples, with blue remaining after orange visually shrinks. This could involve flashing, another actor's effect, a visual cycle, or a separate timer. We did not recover the exact trigger or flash period. Do not implement a new vulnerability rule or flashing timer from these observations alone.

## Remaining limits and deliverable

No clean isolated equal-size head-on collision, held-input collision sequence, or measured house release/return delay was recovered in this interval. Nearby colored players and ghosts are too crowded to infer exact impact impulses or AI targets. Existing collision/AI regression checks can establish internal consistency, not DX rule identity.

`outputs/DX-power-timing-evidence-r18.png` is an inspected annotated research figure, outside the runnable game folder/ZIP. It shows normal/enlarged/expiry frames and the blue-house-body crop. Circles identify orange; original camera pixels are retained without perspective reconstruction.

Cleanup verified: Chrome was absent at task start. Task-created research window28642932 contained the single source tab. Closed with Ctrl+W; a fresh native window inventory confirmed no Chrome windows remain. Preexisting other applications were left untouched. No physical controllers were used.
