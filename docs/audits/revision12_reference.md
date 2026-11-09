# Revision 12 — second-source DX footage, full mazes and critical behavior review

Reviewer: dx_research, 2026-11-08. Source: [Arcade Heroes, The Ultimate Pac Battle Unfolds In Pac-Man Battle Royale Chompionship DX — IAAPA2022](https://www.youtube.com/watch?v=-cNOhumVZ74), published2022-12-08. The source was independently identified in prior web research as primarily DX, then actually viewed this revision. Physical DX tabletop, eight stations and its spectator screen appear in the same footage. Software build/settings beyond visible free-play prompts are unknown.

## Method and actual captures

The previous Chrome window had closed. Refreshed native window inventory, reopened installed Chrome using the documented launcher, selected its returned new-tab window and navigated normally to the known video URL. No safety setting, warning or access check was bypassed. Native CUA fullscreen screenshots were captured and inspected. Captions were turned off through the player's normal control to reveal bottom maze routes. Seek changes sometimes returned stale accessibility positions immediately; final screenshots were checked with a later paused Play-state/time observation. Slider set-value did not reliably seek and was not trusted.

Research captures remain under `work`, outside the playable app:

| File | Paused source position | Useful evidence / limitation |
| --- | --- | --- |
| dx-iaapa-39s-r12.png |0:39|Gold-colored layout, lengthwise table view, sparse dots; player obscures one edge.|
| dx-iaapa-42s-r12.png |0:42|Same golden layout, complementary near-end routes.|
| dx-iaapa-46s-r12.png |0:46|Same golden layout; visible point bursts, causes not isolated.|
| dx-iaapa-48s-clean-r12.png |0:48|Cyan layout and full dot pattern; most tabletop visible, captions off.|
| dx-iaapa-49s-clean-r12.png |0:49|Adjacent continuous-play capture, clearer near short boundary; column still obscures corner.|
| dx-iaapa-68s-r12.png |1:08|Full spectator playfield: all eight bays, both side tunnels, all corners; small central glare spots.|
| dx-iaapa-73s-r12.png |1:13|Second full spectator layout with fresh dots and different topology; same camera direction.|
| dx-iaapa-79s-r12.png |1:19|High-resolution tabletop closeup, three foes in house and one outside; near player encounter.|
| dx-iaapa-79s-encounter-r12.png |Later within1:19|Brief continuous-play follow-up: red/pink separation and starbursts; no frame-accurate duration.|

Additional0:29,0:53 and0:58 snapshots were inspected but not retained: people, marquee/cabinet details or table edge obscure the required playfield. Short continuous intervals were played between paused inspections at39→42→46 and around48→49,68→69, and79. These are sampled sequences, not a claim that every intervening video frame was analyzed. No source video/audio download occurred.

## Pass 1 — actionable findings

**Two complete mazes now available.**1:08 and1:13 show the entire main playfield mirrored on the DX spectator monitor. The house opening faces upward in both raw images, unlike prior upside-down tabletop references. There are eight external bays and side tunnels. All four corners are visible, with only small reflections near the center. Both captures and the supporting tabletop images were sent to the map reviewer immediately.

**A genuine layout/progression difference, not just a palette.**Between1:08 and1:13, wall connectivity/silhouettes change and a fresh dot pattern appears while wall color stays cyan. The small lower-left counter changes8→9. It is reasonable to interpret this as stage progression, but the exact trigger was not isolated: do not claim last-dot clearing or any particular pickup caused it. The counter's formal name is not verified.

**Separate gold/cyan transition sample.**0:39/0:42/0:46 show mostly cleared golden corridors;0:48/0:49 show different cyan routes and replenished dots. Camera view stays broadly consistent, but the video is edited and no exact transition duration or cause can be established from these paused samples.

**Actor/house evidence.**The1:19 closeup visibly contains three differently colored ghosts in the house with a red ghost outside. This supports inside-house clustering during play, not necessarily the exact initial spawn arrangement. The house has a centered doorway on its upper side in this shot. Ghost eyes and mouth opening/closing poses appear in the sequence; no exact animation cadence is certified.

**Encounter appearance.**At1:19, red and pink actors approach near the upper-left corridor; a brief continuous follow-up shows separation and star-shaped spark effects. This supports a collision-feedback visual, but the player's power state is not fully established. Do not certify this as an isolated normal-size bump, a death, or a particular power-up effect.

## Pass 2 — adversarial review

- Compared the1:08/1:13 frames at the same spectator orientation. Bent sections become different connected branches, dots replenish and counter changes. This cannot be explained solely by rotating the camera or changing hue. Still, it establishes two sampled layouts, not an exhaustive original map count or all four home-game counterparts.
- In lengthwise0:48/0:49 views the house doorway faces raw left. Rotate clockwise90 degrees to normalize its doorway upward. Spectator1:08/1:13 already has doorway up. Applying one blanket180-degree rotation to all sources would be wrong.
- Point bursts around0:46 and1:08–1:09 coincide with multiple actors, powers and ghost eyes. Their causes are ambiguous; no exact dot/pickup/rival/ghost score was accepted. Upside-down station numerals also make careless digit reading unsafe.
- The visible stage counter8→9 does not prove a timed progression interval. The same-color route change contradicts assigning one original layout solely by wall hue.
- No clean continuous death→own bay→release sequence was isolated. No exact respawn timer, growth ramp, death duration or gate re-entry rule was accepted. This remains a real evidence gap rather than a passing test.
- A free-play demonstration with multiple players does not establish all operator settings, paid-credit behavior or the shipping build. Existing manufacturer manual evidence remains separate.
- Screenshot UI overlays and stale seek state were excluded from route tracing. The clean48/49 and paused68/73 images are the preferred map evidence.

## Deliverable and outcome

Created and visually inspected `outputs/DX-full-layouts-r12.png`: side-by-side cropped full spectator frames1:08/1:13 with source, orientation and limits. Perspective is retained; no invented pixels or unsupported geometric correction is applied. It is a research figure outside the playable ZIP, not a game asset.

This pass materially improves map evidence and provides sampled progression/encounter observations. It does not resolve the isolated scoring, death/respawn and animation timing gaps. Physical controller testing remains deferred by the user. Native UI is released, paused near1:09 in the source.


## Focused follow-up: AI participants and scoring evidence

A further native-UI pass revisited the same IAAPA2022 DX source around 1:13–1:15. Paused Play state and time were checked after seeking; the AX seek setter did not actually move playback and was rejected. A frame initially named74s was corrected to73s after the final player readout. Advertisements were skipped using the normal visible Skip control. No media downloader or undocumented frame extraction was used.

- `work/dx-score-73s-r12.png`: bottom orange station reads250. Yellow/green/white bottom station prompts readFREE PLAY, yet matching colored muncher actors appear inside the maze. A vulnerable blue ghost is near the orange actor at the bottom-right interior lane.
- `work/dx-score-75s-r12.png`: bottom orange station reads650, a visible increase of400. Yellow left floating label reads1600; blue floating label near the upper-left-middle reads800. A smallAI label is visible under the yellow actor's floating number. Several events occur elsewhere at once, and the interval is not a clean isolated contact sequence. Therefore400 is a measured station-score difference, NOT a certified universal ghost or pickup award.
- **Actionable observed feature:** AI-labeled munchers can occupy unjoined station colors while join prompts remain visible. The ordinary game should account for this separately from an all-bot demonstration mode if pursuing this source's solo/mixed-session behavior. Exact AI replacement on join, difficulty, lives and score handling were not isolated.
- **Rejected inference:** the colored1600/800 labels are consistent with variable awards, but they do not establish the category or a200/400/800/1600 ghost chain. Do not import the original1980/2011 or Mega Tunnel Battle scoring table. The game's current10/75/200/300/500 values remain custom unless separately supported.

A targeted web search for CHOMPionship AI/scoring returned unrelated Mega Tunnel Battle and classic-game score tables, plus dealers' generic descriptions. These were not used to certify DX values. The search also exposed conflicting dealer statements about score competition versus last-player-standing; primary manual/actual DX footage remain higher priority. Native focus reporting retained the address field despite mouse playback changes, so keyboard frame stepping was not attempted without reliable focus confirmation.
