# Revision 15 — yellow threshold and wall-lighting evidence

Reviewer: dx_research, 2026-11-09. Reference: user-supplied `work/user-gate-reference-r14.png`, a static DX spectator-screen photograph. Related source family D was independently observed in revision14 footage `qcO9tzgsdjo` at5:05/5:15. No claim that the user photograph itself has a verified video timestamp.

## Initial independent photo pass

The yellow-green threshold at each of the eight bay mouths has a thin continuous bright horizontal lip, with diagonal dark gaps descending below it. The lower-left threshold is enlarged without invention in `work/r15-reference-yellow-gate-crop.png`. It clearly separates the horizontal lip from the diagonal hatch treatment. The revision14 renderer painted dark diagonal strokes through the full10-pixel stripe, interrupting both edges; this is a concrete visible difference supporting an intact bright edge.

All eight thresholds are present while multiple players are in the maze. However, a still photo cannot establish the exact open/crossing animation or prove that a stripe survives every opening frame. The gameplay state should not be inferred solely from the presence of an active player elsewhere in the maze. Gate behavior and the visible closed-band correction are separate evidence questions.

The photo's maze contours have a consistent blue core and surrounding glow away from reflections. Large white bright spots overlap walls, dots and background and are camera/room reflections; they must not be treated as intentional wall-lighting variation. Apparent size and intensity vary with camera perspective, compression and glare, so exact photometric equality to the photo cannot be certified. The useful target is internally uniform edge construction along equivalent straight segments, curves, narrow stems and bay/house joins.

The underlying family D topology remains identifiable: long upper and upper-middle horizontal islands, tiny central top/bottom capsules, single side tunnel row, offset hooked branches and pairs of vertical islands beside the house. No new missing route is demonstrated by the supplied photo compared with the revision14 trace. This audit does not propose geometry changes based only on blur or glow width.

## Fresh continuous color investigation — two passes

Source: Harold Zheng, *Pac-Man Battle Royale Chompionship arcade gameplay*, https://www.youtube.com/watch?v=qcO9tzgsdjo . Native Chrome playback at 0.25x; no media download. Captures are research-only files outside the distributable. Video timestamps are whole-second UI readings, not frame-accurate measurements.

Pass 1, approximately 5:00–5:05: family C is almost empty; the wall layout morphs into family D and dots refill while the same spectator monitor remains amber/gold. Files `work/r15-transition-before.png`, `-middle.png`, `-preclear.png`, `-after.png` preserve that sequence. The `preclear` filename is misleading: it shows the walls already morphing. The last individual dot is not causally isolated because actors obscure the last cluster. This proves a topology transition does not necessarily change the wall hue; it supports dot-clear progression, but does not establish the exact remaining-dot threshold.

At 5:06–5:07 the new D maze remains amber, with a normal red player moving in the upper-left region. By 5:08 the red player is enlarged, walls are red and physical cabinet chase lights are red. Nearby actors/effects obscure the precise pickup. Files `r15-color-onset-a.png` (5:06), `-b.png` (5:07), `-c.png` (5:08). This is strong observed association between enlargement and player-colored wall illumination, independent of layout. It is not proof of the exact pickup timing or an exclusive single-player priority rule.

Pass 2 replayed 5:07–5:17 to challenge a naive last-pickup explanation. `r15-multi-color-1.png` at5:08 is red. `-2.png` at5:10 is blue with BOTH red and blue enlarged players visible. `-3.png` at5:11 shows purple/red wall transition and red cabinet lights, both enlarged players remaining. `-4.png` at5:13 is blue with both giants still present. `-5.png` at5:14 moves the camera to the tabletop, still blue and both giants visible. `-6.png` at5:15 has blue tabletop walls and red external perimeter lights; the earlier revision14 5:15 capture has red walls. These alternating observations support cycling among concurrently enlarged player colors. They contradict a rule that merely retains the last pickup color until another pickup. Exact dwell/transition duration, eligible power states, ordering with three or more giants, and expiry/reversion remain unmeasured. Physical and screen lights need not have identical phase. No exact period should be promoted from these whole-second samples.

## Broad visual inventory and limits

| Category | Reference and conclusion | Remaining comparison limit |
|---|---|---|
| Maze topology | Four traced families; C→D transition freshly observed above | Glare-hidden endpoints, exact widths and full layout inventory remain uncertain |
| Wall core/glow | User photo supports continuous uniform strokes; white hot spots cross background and dots and are reflections | Do not reproduce camera glare as a wall feature; absolute brightness cannot be calibrated |
| Wall hue behavior | Enlargement-associated colors, multiple giant color cycling observed | Exact cycle and expiry policy not established |
| Bay thresholds | Continuous bright lip with hatch cuts beneath; current closed after-render visually preserves it | Static photo does not prove persistent lip during opening; open after-render remains a custom choice |
| Ghost house | Two contours and doorway observed in prior reference; current house follows this | Exact thickness, door animation timing unmeasured |
| Normal players | Colored shaded spheres with opening mouths, larger powered forms; fresh5:14/5:15 frames | Our eye shape, cutout mouth and sphere lighting are original approximations, not pixel matches |
| Normal ghosts | Fresh5:14/5:15 show domed bodies and conspicuous white directional eyes | Current procedural body/feet and shading remain approximations |
| Frightened ghosts | Code currently changes body blue but retains normal large eyes | No newly isolated close frightened face; do not claim exact facial match or invent a fix based only on legacy Pac-Man |
| Returning eyes | Fresh5:15 right-side passage contains eyes-only sprite; implementation has eyes-only state | Return animation and speed not measured |
| Dots and yellow/green pellets | Direct HOW TO PLAY10/100/1000 evidence retained from revision14 | Visual scale/gloss estimated from camera images |
| Eleven pickups | Coverage exists in code; earlier sources support categories | No clean reference atlas of all eleven icons/states; count alone does not establish effect fidelity |
| Smoke, fire, zap and explosions | Fresh5:07–5:08 cyan jagged effect visible around upper-left actors | Attribution/extent obscured; particles, layering, cadence not certified |
| Scores/lives/HUD | Colored station scores and CONTINUE countdown observed; original block glyphs implemented | Exact font shapes, lives icon spacing and full prompt set not reproduced |
| Start/join/locator | Prior station evidence retained | Full continuous all-eight joining and locator animation not newly established |
| Continue/end | Recorded countdown and AI continuation, revision14 | Paid continuation resume not observed; custom results/operator screens are not replicas |
| Operator/help/highscores | Functional implementation and automated QA | No source visual parity claim; independent app UI |

## Adversarial collision review

Quarter-speed footage around4:50–5:15 was examined, but distant spectator sprites, nearby ghosts and camera movement prevented isolating a normal equal-size player bump with a defensible displacement or timing measurement. Larger red and blue players coexist and move; this does not quantify equal-giant bounce. Do not describe application regression tests as verification of DX impulse physics. Fixing repeated pushes/jitter is internally justified, while exact DX contact response remains a separate evidence gap.

## Independent post-fix gate check

Viewed `work/gates-r15-after-closed.png` and `work/gates-r15-after-open.png` directly. Closed bands now retain a bright unbroken horizontal lip, addressing the concrete photo discrepancy. Open bands disappear in the after-render; that behavior is not verified by the static photo. Render previews still show procedural actor, HUD and power styles; this review approves the specific lip correction, not blanket visual identity.

Native UI is released after the second replay. Video ended into a paused post-roll advertisement; the main video's speed had been set to0.25x and the ad does not expose a playback-speed control. No external state was posted and no commercial media is bundled into the game.

Research figure: outputs/DX-wall-color-evidence-r15.png, four actual cropped frames. The 5:07 label intentionally says before red hue, not before enlargement: the onset effect obscures the precise growth boundary.
