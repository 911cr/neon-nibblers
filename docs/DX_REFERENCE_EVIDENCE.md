# DX reference evidence register

Research updated2026-11-08. Baseline audited:0f9c3c98e097d2fb16b058896ba872b31783d2ed,29 headless checks passing. This register separates primary documentation, direct observations, inherited observations, and unresolved questions. A URL or search result alone is not a watched gameplay sequence.

## Status vocabulary

**VERIFIED DX** means manufacturer/developer evidence establishes that specific DX fact. **OBSERVED DX** means visible behavior in identified DX footage, limited to the sample. **HISTORICAL ONLY** cannot establish DX behavior. **INFERRED** names an interpretation. **UNKNOWN** means not recovered. **IMPLEMENTED AND TESTED** describes Neon Nibblers only. **BLOCKED** applies to a specific missing evidence/resource, not the whole project.

## Primary sources freshly checked

| ID | Source/version/location | Observation | Confidence/status and limit |
|---|---|---|---|
| D01 | [2022 DX operation manual, manufacturer-authored BMI mirror](https://www.bmigaming.com/Games/Manuals/namco/Pac-Man-Battle-Royale-Chompionship-Deluxe-Video-Arcade-Game-Manual-Bandai-Namco.pdf), PDF page14 (one-based), rendered and visually inspected | Adjustments include starting lives, bonus-life threshold, long high-score names, attract sounds, audio, rotation and coinage/free play. Example values3 lives/10,000 bonus. | High, **VERIFIED DX** configurable entries and shown examples. Does not prove all cabinets use these, bonus repeats/once-only, or life cap5. |
| D02 | Same manual p13 | Menu includes high-score/credit clearing, software update, system info and diagnostics. | High, **VERIFIED DX** facilities, not exact results UI or update history. |
| D03 | Same manual p15 | I/O diagram has independent joystick/button stations, top4/8/7/3, bottom1/5/6/2. | High, **VERIFIED DX** station numbering. Not USB enumeration or join policy. |
| D04 | Same manual parts table | 75-inch main panel and43-inch panel listed. | High, **VERIFIED DX** hardware; state-specific overhead content remains unmeasured. |
| D05 | [Manufacturer purple Find My Pac/Start decal](https://bandainamco-am.com/products/bc40-20692-06); [DX parts collection](https://bandainamco-am.com/collections/pac-man-battle-royale-deluxe), BC40-20692 series | Dual-purpose locator/start labeling is explicitly DX-compatible. | High, **VERIFIED DX** existence of station action. Exact graphic, duration, retrigger policy and available game states remain **UNKNOWN**. |
| D06 | [Manufacturer SD page](https://bandainamco-am.com/collections/pac-man-battle-royale-standard) | Four-player cabinet links with a second for eight players; new powers attack ghosts/rivals. | High for SD capabilities. Not proof of identical stage/join logic in DX. |
| D07 | [Cosmodog developer timeline](https://www.cosmodog.com/),2022 entry | Developer identifies its CHOMPionship work and describes eight-player maze action and movement/bouncing coordinated with music. | Primary developer account; high for family feature, **UNKNOWN** exact BPM, synchronization and DX-specific settings. Current site accessed through indexed text when direct open timed out. |

Manual retrieval notes: the supplied ftp manufacturer URL returned502; the current manufacturer CDN URL was inaccessible to the web tool. The BMI mirror was readable, then downloaded solely for research and rendered locally. Research-only PDF/page images remain under work/dx-manual*, not bundled in game assets. No commercial game software was accessed.

## Recorded footage observations inherited from earlier agent passes

These are preserved rather than misrepresented as newly watched this cycle. Full original audit narratives live under docs/audits.

| ID | URL and sample | Version/observation | Limit/status |
|---|---|---|---|
| V01 | [Seals on the Move released cabinet](https://www.youtube.com/watch?v=efLgejKG_ls&t=75s),75,90,120s | Identified Deluxe footage: cyan walls/pockets with yellow gate hatches. | **OBSERVED DX**, high for color relationship. Cuts/camera prevent complete entry/death/reentry timing. |
| V02 | [JurassicVerse64](https://www.youtube.com/watch?v=GhSV1oQVA6g&t=95s),95–101s | Moving peel in right interior lane; gold/green-like round items in interior lanes. | CHOMP cabinet identity not conclusively DX; medium for movement, not exact spawn origins/count/cadence. Do not elevate to VERIFIED DX. |
| V03 | [Arcade Heroes mobile/projector](https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s),94s | Clearer maze, thin outlined walls, border pockets, occupied house. | CHOMP mobile/projector. Useful proportional reference; surrounding UI, rules and map equivalence to DX **UNKNOWN**. |
| V04 | [Deluxe cabinet sample](https://www.youtube.com/watch?v=-cNOhumVZ74&t=49s),49s | Cabinet cross-check from earlier visual revision. | Limited angled sample; not a full-session state trace. |

No new continuous full DX session was viewed in this research pass. No new frame-perfect visual/score/timing claims are made. Reference frame reuse in a distributable artifact needs separate consideration; no external video/audio/sprites are bundled.

## Historical and conflicting material

- [Original manufacturer product page](https://bandainamco-am.com/collections/pac-man-battle-royale) describes last-survivor rounds, enlarged/faster hunters, equal-size bumps, fruit/dot refills and statistics. **HISTORICAL ONLY**.
- [Original Deluxe manual](https://wwyss.ch/Arcades_Manuals/Manuals/Arcades/Pac-Man%20Battle%20Royale%20DX%20Manual.pdf),section7-3-4 p20: join waits for next group round, with solo/final-round exclusions. **HISTORICAL ONLY**. The word Deluxe in its title does not make it CHOMPionship.
- [2013 hands-on prototype report](https://arcadeheroes.com/2013/05/01/pac-man-battle-royale-unboxing-and-review/) directly supports configurable CPUs/tournament placement in that prototype, not released DX.
- [2021 first-hand preview](https://arcadeheroes.com/2021/11/15/bandai-namco-to-launch-pac-man-battle-royale-chompionship-to-arcades/) discusses score/leaderboard and eight players but also predecessor-like winning language. It is pre-release evidence, not authority for today's end condition.
- [Rental page](https://phoenixamusements.com/product/4-player-pac-man-battle-royale/) explicitly mentions using Start to locate a player but mixes old round/fruit descriptions with CHOMPionship. Locator is independently supported by D05; other copied rules are not accepted.
- [2022 shipping report](https://arcadeheroes.com/2022/05/12/pac-man-battle-royale-chompionship-update/) describes overhead screens showing play. This does not establish that startup, results, advertising and transitions always mirror the main screen.

## Actionable unknowns and discriminating observations

| Question | Current evidence gap | Next useful observation |
|---|---|---|
| Immediate vs queued late joining | No released-DX join sequence | Continuous shot showing available station, button press, bay appearance and active play; repeat in final moments and solo/multiplayer. |
| Find visual/timing/retrigger | Label only, no measurable sequence | Record button visible and player highlight from onset to disappearance; press twice, test during respawn/results. |
| Scoring | None of10/75/200/300/500 recovered from primary DX evidence | Before/after digits around one isolated pellet/pickup/ghost/rival event, with all concurrent events excluded; repeat. |
| Life bonus policy | Example threshold only | Score crossing10,000 and20,000; inspect lives before/after and operator settings. |
| Map transitions | No complete multi-stage sessions cataloged | Two continuous DX sessions with dot counts, items, clock and all player lives visible through transitions. |
| Latest software | No official changelog/version sequence found | System Info screen matching a dated gameplay run; public manufacturer release notes. |
| Spectator content | Active-play mirroring reported | Simultaneous main/overhead shot through startup, play, stage, results and idle. |

## Two-pass research QA

Pass1 checked manufacturer pages, current parts labels, DX manual imagery, first-hand historical reporting and developer history. Pass2 challenged version confusion, date ambiguity, cached access, example settings versus universal defaults, and cause versus coincidence. Corrections: bonus-at10,000 does not establish a once-only grant; prototype CPU behavior is not DX behavior; a physical Start/Find label does not prove immediate late joining; overhead gameplay mirroring does not prove universal mirroring. No exact-duration, scoring or full-lifecycle claims survived without direct evidence.

## V05 — fresh released-DX inspection in revision8

Actual native Chrome playback of [efLgejKG_ls](https://www.youtube.com/watch?v=efLgejKG_ls) inspected2026-11-08, with seek-slider timestamps confirmed and post-seek frames refreshed before comparison. At15s the cabinet presents a POWERUPS/EARTHQUAKE instruction over title artwork;15–32s contains camera/edit discontinuities before gameplay. At75/90/120s cyan walls have yellow hatch gates. At75/120s house border has double rectangular contours with central doorway; this motivated a rendering-layer audit. Baseline already showed two overlapping-layer contours; an initial extra-line patch caused three and was rejected. Final revision8 clears the background edge, draws two explicit contours and checks the doorway.500 text is visible at120s, but no isolated scoring cause was recovered. Details and limitations: audits/revision8_stations.md. Research comparison screenshot kept at work/dx-reference-120s.png, excluded from playable assets. This updates the earlier no-new-footage statement for the initial research pass, without claiming a complete uncut session.

Analytical comparison artifact: outputs/DX-house-comparison-r8.png is outside the playable ZIP. It compares the actual120s research crop (rotated180 degrees, perspective/glare retained) to baseline/current house renders. This is a limited enclosure comparison, not a full-board or animation parity proof.


## Revision 11 — animation, proportions and fresh DX reference review

Fresh real DX footage was viewed safely through normal browser navigation after using a new tab with a verified address. New60/65/124/135second research captures and the report are recorded in audits/revision11_reference.md; camera edits/glare prevent exact cycle timing and a complete commercial map catalog. Distinct house-side geometry appears with the same cyan palette. Palette selection is now independent of layout: F12 cycles wall colors during play, or use `--palette 0..3`. This changes presentation only, not match logic or routes; default progression remains our approximation.

Fixed the left-facing eye/light flip, missing individual ghost stun feedback and tunnel copies, sorted-item animation identity jumps, short respawn/stage cache slides, and animation continuing during pause/guide/results. All11 power icons now use cached3x procedural artwork and position-independent bob phase. Fire is a continuous layered animated plume with a pale core, clipped to reachable corridor endpoints and split correctly at tunnels. Lightning arcs animate. Exact DX art proportions and timing are still unverified.

110 tests cover artwork/time samples, direction, icon sizes16–96px, ghost states, HUD/tunnels, effects, pause/results, respawn, item tracking,720/1080 resizing and palette changes without logic mutation. Two agent QA passes included discovered clipping and freeze regressions followed by corrections. Native1/2/8 render samples cover every map on Windows and Ubuntu/WSLg. These are short graphics checks, not hardware or performance certification; the final plume styling is also checked by the final render suite and recordings. Physical controllers remain deferred to production.

Each1/2/8-player GIF tours four separate6-second map scenarios (24seconds,288frames). New `gameplay_1_player.mp4`, `gameplay_2_player.mp4` and `gameplay_8_player.mp4` show the same tour at1280x720/60fps with original event audio, avoiding GIF color/frame-rate limits. They are actual computer-controlled game simulations. They do not prove a commercial stage sequence or physical-input compatibility.

Optional recording tools: `python -m pip install -r requirements-capture.txt`, then `python record_video.py --players 8 --seconds 6`. They are unnecessary for playing. Native Windows encoding was tested; playback files can be viewed on Windows/Linux with an H.264/AAC player. The game remains Python/Pygame source, not a standalone executable.

See animation_contact_r11.png, animation_review_r11.gif, fire_animation_r11.png and animation_world_effects.png for tested frame sequences and sizes. The matrices document finite reviewed cases; no exhaustive or perfect-commercial-match claim is made. Full DX topology, scoring/timing/AI, death/growth transitions and operator/spectator/attract systems remain unfinished.
