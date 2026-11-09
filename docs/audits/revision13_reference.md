# Revision 13 — measured scoring and final-life sequence

Reviewer: dx_research, 2026-11-08. Two critical passes performed on fresh footage, independently of the implementation. This audit certifies the specific observations below, not an exact match of all rules.

## Source and method

Fresh source: [Haid3rs, Playing Pac-Man Battle Royale Chompionship!](https://www.youtube.com/watch?v=43DcDXxEgzk), 10:18 long. The eight-station physical cabinet and spectator screen identify the DX configuration at 9:30–9:34. Software build and operator settings remain unknown. Native Chrome playback was inspected normally using the documented computer-use interface. No video/audio was downloaded. Ordinary player controls supplied fullscreen, pause, timeline seeking and quarter-speed playback; playback was restored to 1x and paused at 9:45 when finished.

Immediate accessibility timestamps sometimes lagged playback. Exact timestamps below are from a subsequent paused state, not stale running-player text. Continuous screenshots without a verified paused timestamp are given brackets. We did not use keyboard frame stepping because actual video keyboard focus could not be established confidently.

## Pass 1 — new source, scoring and survival

At 0:39 the red station reads JOINED. At 0:41 its score is zero and two reserve-life icons appear; the player is in a striped bay during the introductory dot/maze animation. At 0:45 it is outside the bay with score zero. Continuous sampled play from approximately 0:45 to 0:50 shows scores 20, 100, 260, 270 and 330 on a dot route. The camera motion prevented exact individual counts here, so these increments alone were not promoted to a measured per-dot constant.

At paused 4:53 red is enlarged, score 61800, with a golden pellet overlapping its mouth. At 4:59 it remains enlarged and has score 63070. This does NOT measure a six-second power duration: a pickup/refresh is visible at 4:53, the onset is not isolated, and the expiry is not observed. No power-duration constant was changed on this evidence.

The source begins its joined session near 0:39 and shows later scoring beyond 4:59. However, the whole intervening interval was not inspected frame by frame and credits/restarts were not ruled out. This supports investigation of an untimed survival option, not an assertion that a precise 180-second rule is disproven solely by two separated frames.

## Pass 2 — counted dots, final death and post-death behavior

The end sequence was first inspected continuously at quarter speed around 9:19–9:27, then rechecked with paused fine seeks:

| Source position | Direct observation | Evidentiary limit |
| --- | --- | --- |
| 9:22 | Red score 144640; exactly four ordinary small white dots remain along its adjacent bottom corridor. Red is normal size; no reserve icons are visible above its score. | Four-dot aggregate, not an isolated single-dot frame. |
| 9:23 | Same corridor is cleared, red score 144680. Red disappears at the orange-ghost encounter; continuous sampling included a thin collapsing arc. | Death animation duration and exact contact boundary are not measured. |
| Within 9:23–9:34 | Red station switches to CONTINUE with alternating COIN/INSERT; other actors keep moving. | Actual continue purchase and respawn were NOT observed. |
| 9:34 | Full spectator board shows red CONTINUE top-left, seven other bays INSERT; normal moving actors remain. House opening faces upward. | Strong support that other actors are AI/unjoined, but no internal controller-state access. |
| By paused 9:45 | Camera returns to a large alphabet/name-entry interface over title artwork. | Exact timeout and transition onset are not established; no complete name was submitted in our interaction. |

**Measured scoring result:** four disappearing ordinary dots correspond to +40 on the same station (144640 → 144680), without a visible other pickup or award on that corridor. This directly supports the implementation's existing 10 points per ordinary dot in this observed situation. It does not certify every possible dot multiplier or hidden bonus. All other award constants remain unverified unless supported by separate evidence.

**Lifecycle result:** a final-life event has a per-station continue interval while AI play continues, followed by name entry in this single-human session. A global immediate-results transition is therefore a custom simplification, and an optional delay/continue presentation is evidence-aligned. Actual purchased continuation, restored lives, score retention, charge count and multiplayer end policy remain unknown. Do not call a no-revival rule a demonstrated contradiction solely from the prompt text.

**Map result:** the 9:34 spectator frame was immediately sent to the map reviewer for independent topology comparison. It is clearer than the earlier 9:30 capture and shows almost all the field, all eight bays and the upper house doorway; a small left screen edge is cropped. No mapping claim is made just from its red wall palette.

## Primary and corroborating sources

- [Bandai Namco DX manual](https://www.bandainamco-am.com/Ecommerce/Site/Content/PDFs/Pac-Man%20Battle%20Royale%20Chompionship%20DX%20Manual_5_12_revise_Edit.pdf): adjustment text lists Deluxe 8-player cabinet, lives-to-start 3, bonus life at 10000, coinage, long high-score names, attract sounds, audio, volume and monitor rotation. The displayed adjustment menu contains no match-timer entry. Absence from this menu alone is not proof that no other timing setting exists.
- [Firsthand comment under confirmed DX IAAPA footage](https://www.youtube.com/watch?v=-cNOhumVZ74&lc=Ugy_gI5m1BqQ_S14t5F4AaABAg): @JohnshiBRPG describes repeated Dave & Buster's play as an endless score chase and requests round limits. This is lower-confidence player testimony, not a manufacturer rule or controlled measurement.
- [Arcade Heroes March 2022 video](https://www.youtube.com/watch?v=CU0WTUkJVW8): description identifies a near-production build and score-before-lives-run-out objective. It cannot establish exact released-DX constants.
- [Arcade Heroes September 2022 availability report](https://arcadeheroes.com/2022/09/09/pac-man-gets-the-spotlight-with-update-to-bandai-namco-amusements-site/): release/version context, not mechanics evidence.

Older Battle Royale and Mega Tunnel Battle score tables were rejected as different games. No exact enemy-eating, power-item, fruit or combo table was established here. AI decision rules, stacking precedence, power spawn intervals and expiration timings remain custom values pending stronger evidence.

## Captured research artifacts and critical verification

Raw PNGs under workspace `work/`: `dx13-haid-39-joined.png`, `dx13-haid-45-score0.png`, `dx13-dot-a.png`, `dx13-dot-b.png`, `dx13-dot-270.png`, `dx13-power-293.png`, `dx13-end-562.png`, `dx13-end-563.png`, `dx13-end-continue.png`, `dx13-haid-574-board.png`, `dx13-haid-name-entry.png`. The exact paused source positions for the last two are 9:34 and 9:45 respectively. Continuous end-a/b/c/d files are supporting samples with bracketed times, not frame-accurate timestamps.

Research figure: `outputs/DX-scoring-lifecycle-r13.png`, outside the distributable game. It uses actual cropped screenshots with explicit aggregate/timing limitations. All three selected images were reopened, checked nonblank and the final figure visually inspected. No commercial reference artwork is included in the playable application's assets.

Review disposition: ordinary-dot scoring and the described final-life sequence are supported; exact power/AI/continue constants are still unresolved. Two review passes do not convert unresolved facts into agreement on a perfect match. Physical controller and cabinet testing remain deferred per the user's instruction.

## Focused follow-up — power-duration falsification pass

After the initial audit, replayed continuous 4:49–5:08 and 8:59–9:18 at normal speed with repeated actual screenshot inspection. In the first interval, red is normal near the green pickup at 4:49, visibly enlarged by 4:53 and still enlarged at 5:00. The known gold pickup overlaps 4:53, and the camera loses red around 5:02–5:08. Thus neither an isolated initial duration nor expiry is available. The second interval shows normal, enlarged and normal states, but intervening pickup/stage activity, actor overlap and camera blur prevent confidently assigning an unrefreshed onset-to-expiry measurement. No numeric duration was promoted. Final paused 9:18 capture: `work/dx13-power-followup-end.png`. UI was released with speed 1x. These attempts narrow why the intervals fail; they do not establish a hidden constant by subtraction.

Independent map-review feedback on `dx13-haid-574-board.png`: the upper arch, two tunnel rows and lower hooks identify reconstructed family A. The red palette therefore supplies additional evidence that palette and layout are independent. It does not establish a third distinct layout or an exact wall-width measurement.
