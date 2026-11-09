# Revision 14 — continue timing, displayed scoring and third maze source

Reviewer: dx_research, 2026-11-08. Initial and deeper reference passes; actual native Chrome observations. Research screenshots only, no source video download, no game-code edits.

## Pass 1: continue-window boundary

Source [Haid3rs, Playing Pac-Man Battle Royale Chompionship!](https://www.youtube.com/watch?v=43DcDXxEgzk), confirmed eight-station DX. Fine paused seeks refine revision13:

- 9:24: score144680 and shrinking/death presentation remain visible; no CONTINUE yet (`work/dx14-continue-564.png`).
- 9:25: CONTINUE / COIN appears. A numeral resembling9 is partly cropped on the right (`work/dx14-continue-565.png`). Treat digit reading as supportive, not the sole timing evidence.
- 9:28: CONTINUE remains; camera crops its right side (`work/dx14-continue-568.png`).
- 9:34: prior full spectator capture still shows red CONTINUE while other stations are unjoined and actors move (`work/dx13-haid-574-board.png`).
- 9:35: spectator screen has switched to high-score/title presentation (`work/dx14-continue-575.png`).

Onset is bounded between sampled9:24 and9:25; exit between9:34 and9:35. This supports an approximately10-second continue window, conservatively9–11seconds at the sampling resolution. It does not certify frame-exact timing or every operator configuration. A10-second implementation is now source-informed rather than an arbitrary duration. Actual paid continuation and restored score/lives remain unobserved.

## Pass 2: a new primary on-screen scoring legend

New source [Harold Zheng, Pac-Man Battle Royale Chompionship arcade gameplay](https://www.youtube.com/watch?v=qcO9tzgsdjo),5:19long. The opening shows the branded DX cabinet, giant tabletop, eight stations and spectator monitor. Software build/operator settings are unknown. Native YouTube search found this source; its normal advertising Skip control was used before viewing.

At paused0:01 its HOW TO PLAY panel displays:

| Icon | Displayed award | Confidence |
| --- | --- | --- |
| Small ordinary dot |10PTS|High; independently agrees with revision13 four-dot/+40 measurement.|
| Yellow pellet |100PTS|High; enlarged actual crop and adjacent0:03 panel checked.|
| Green pellet |1000PTS|High; same adjacent-frame check.|

Raw `work/dx14-qco-howtoplay.png`; analytical enlargement `work/dx14-score-panel-crop.png`; adjacent raw `work/dx14-qco-howtoplay-3.png`. The0:03 frame also repeats the legend on the tabletop. No generated pixels or external enhancement was used beyond ordinary crop/resize. Both root and mechanics reviewer were asked to independently read the numerical legend before changing awards. These values apply to those icons; they do not establish the award for every other power-up or enemy combo.

At paused4:53 a full spectator view shows a third distinct maze family: broad central enclosure paths around the house and paired lower rectangular islands. Raw `work/dx14-qco-board293.png`; complementary continuous4:59 frame `work/dx14-qco-board-live.png`. House doorway points upward. Map reviewer independently confirmed this is distinct from familiesA/B and is reconstructing it. Low camera angle introduces perspective; exact pixel widths are not certified.

## Deeper falsification and final source checks

The new source also supplies a clear second continue countdown. At paused5:11 orange reads CONTINUE6 / SWIPE (`work/dx14-qco-continue311.png`); at paused5:15 it reads CONTINUE2 / CARD (`work/dx14-qco-continue315.png`). The four-count decrease across four source seconds supports ordinary one-count-per-second behavior. At5:18 the screen shows the publisher logo and0credits (`work/dx14-qco-end318.png`). No actual paid resume occurred in the observed ending, so score/life retention is still unknown.

A potential claim that ambient AI caused a stage change during CONTINUE was explicitly tested and rejected: paused5:05 already shows the new layout and full dots while orange still has score60060 (`work/dx14-qco-transition305.png`). The CONTINUE prompt appears later. Thus the fresh sequence proves continued ambient movement, not an AI-only stage transition. Keep the latter unverified.

The5:05/5:15 layout was independently identified by the map reviewer as a fourth family, distinct from A/B/C. The5:15 tabletop view offers a much larger complementary image with the house opening upward, side tunnels, all eight bays and corners. FamilyC additional captures: `work/dx14-qco-board250.png` at4:10 has many dots still present; `work/dx14-qco-board269.png` is actually4:30/270seconds despite its filename. Both use the same spectator-camera angle. These went directly to map QA; coordinates inferred from perspective remain estimates.

Cross-source web searches for paid-continue retention did not yield a reliable exact rule. Search results about Mega Tunnel Battle or World's Largest Pac-Man were rejected as different games. A venue listing mentioning a continue price cannot establish score/lives behavior. Power duration and AI targeting constants remain unresolved; no numerical substitutions were made from speculative similarity. Native UI was released paused at5:18, normal speed.

## Independent family D trace and artifact verification

Research agent manually traced family D wall polylines from the305-second normalized spectator frame, cross-checked against315-second tabletop, then generated a single-line lane graph using the existing geometry helper. Proposal files: `work/dxD_lanes.json` (569 cells), `work/dxD_metadata.json` (source, orientation, estimated wall coordinates), `work/trace_dxD.py` (reproduction), and `work/dxD_lane_overlay.png` (actual source overlay). Runtime catalog validation passed for connectivity, no open2x2 squares, no unintended dead ends, existing eight stations and required house perimeter. Only proposal files were written; map owner performs separate critical review and runtime merge. This is topology reconstruction with estimated grid coordinates, not recovered commercial data.

`outputs/DX-scoring-continue-evidence-r14.png` combines the real instruction panel and two countdown frames, explicitly outside the game ZIP. The final figure was reopened and visually checked. It does not assert paid continuation or exact power timing.

## Final independent C/D critical review

After the map owner merged both families, the research reviewer independently reopened `work/dxC_lane_overlay.png`, `work/dx250_normalized.png`, the actual updated C render `work/map_r12_2.png`, and `outputs/DX-maze-comparison-r14.png`. Checked corner U walls and inner posts, three offset side capsules, lower rectangular islands, short posts outside the central enclosure, concentric routes and their entrance gaps. No demonstrable missing or added passage, disconnected visible branch, or mirrored orientation was found. The actual D rendering also agrees with this reviewer's independent trace. This approves the visible topology reconstruction; it does not certify exact endpoint coordinates, pixel widths or actor/glare-obscured edges.

Independently reran all17 `test_maps.py` tests on the merged runtime catalog: PASS,14.302seconds, Python3.14.2 / pygame-ce2.5.8, dummy video/audio. No changes were made by this reviewer to the merged maps. D was separately critically reviewed by the map owner, and C by the research reviewer before freeze.
