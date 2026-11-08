# Player gate audit — 2026-11-08

Scope: revision4 game.py/Arena/draw, reference footage and manufacturer-authored 2022 Deluxe manual. No game code edited.

## Evidence
- Cabinet footage inspected directly in browser at 1:08 and 1:23: https://www.youtube.com/watch?v=GhSV1oQVA6g&t=68s and https://www.youtube.com/watch?v=GhSV1oQVA6g&t=83s . Eight small outside-border pockets are present; unused pockets are empty. Pockets use the same yellow wall outline as the maze, with two parallel contours. Closed mouths have a band of short diagonal yellow hatch marks aligned with the border. Score/start/card text sits outside and uses station colors. The footage is camera-perspective, so no pixel-perfect dimensions inferred.
- Earlier front-facing comparison in session notes: https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s . Mobile/projector presentation is useful for shape but not proof of Deluxe timing.
- Manufacturer-authored Deluxe operation manual (2022,28pages), working mirror: https://www.bmigaming.com/Games/Manuals/namco/Pac-Man-Battle-Royale-Chompionship-Deluxe-Video-Arcade-Game-Manual-Bandai-Namco.pdf . It covers hardware/setup/service and has no gate operation or detailed game rules. Original manufacturer URL currently404. Do NOT substitute the 2011 Battle Royale manual as evidence for sequel gate behavior.

## Confirmed visual discrepancies and changes recommended
1. Current pocket has a single2px rectangle; reference has narrow twin contours continuous with the outer maze. Use an outlined U pocket extruded from boundary with matching inner/outer contour separation, not a standalone overlay rectangle.
2. Current closed mouth draws player-color bar plus maze-color hatching. Reference observed hatching/threshold use maze yellow; reserve player colors for score/station labels, not a bright colored physical door.
3. Place mouth flush on the outer boundary and consistently mirror top/bottom. Current upper/bottom rectangles overlap border by different offsets (upper mouth aboutTOP+11, bottom mouthTOP+ROWS*TILE-13). Rendering player centers artificially atTOP-5/bottom+5 can make visual-to-logical transition feel detached. Define bay center, threshold and corridor entry from one geometry description.
4. Current open/closed visual state jumps instantly from gap0 to20. A brief retracting hatch transition would feel better; duration would be a parody tuning choice, not verified original behavior.
5. Keep empty pockets empty. Current revision4 correctly removed the fake duplicate muncher icons that existed before.

## Operation findings / unknowns
- Current implementation gives each owner exclusive bay access, auto-releases after0.8s, permits manual return, and repeats on respawn. None of the inspected sources establishes these exact commercial rules or0.8s timing.
- Current gate opens whenever owner is within Manhattan2, including merely passing alongside the mouth. That is a proximity visualization, not a documented original mechanism. Prefer tying opening to actual queued entry/exit crossing so it does not flap when passing laterally.
- Whether players may voluntarily re-enter bays, whether this grants safety, whether giant players can enter, and whether release requires joystick input remain UNVERIFIED. Do not describe these as matching the original. Need footage of an actual death-to-bay-to-reentry sequence before asserting exact behavior.
- No controlled observation in this review established ghost bay invasion. Excluding foes/pickups is a reasonable current game rule but not certified from sources.

## Tests recommended
- Sample path from bay center through threshold to lane; rendered opening must coincide with logical crossing.
- Assert closed gate remains closed when owner passes laterally without entering.
- Gate animation transition remains continuous on start and respawn and cannot be skipped by large dt.
- Mirror geometry top/bottom; no outward movement beyond bay; no hidden duplicate player icon.
- Check every owner and excluded nonowner on every map; retain current gate gameplay tests but label commercial rule uncertainty.

## QA1 — corrective regression review
Read latest game.py/arcade_art.py/test_smoke.py after parent revisions. Ran `python -m unittest discover -s outputs/NeonNibblers -p test_smoke.py -v` with work/deps: all23 tests passed, including gate launch/return/respawn on all maps. Verified renderer now has twin contour pocket, maze-accent hatch, mirrored border threshold, and opening tied to bay/queued crossing/interpolation instead of raw proximity. Captured and visually inspected work/gates_qa.png: eight actual bay occupants, inward facing, no fake duplicate icons, continuous outer wall pocket connection. This verifies implementation corrections, NOT exact commercial gate rules.

## QA2 — deeper state/input transitions
Ran independent work/gates_qa.py.32 scenarios (4maps x8players) verified pause freezes release, normal0.8-second release reaches lane, and buffered lateral input moves correctly on first movement step. Owner/nonowner and respawn are also covered by existing integration test.

Found reproducible stale-state bug: hurt() and new_arena() do not clear player stun or movement clock. A player dying with stun2 and clock.09 remains inside bay after1second with entry timer still.8 and stun1; new_arena also retains stun/clock. This makes gate release depend on the previous life/stage instead of the stated release delay. Recommend reset both fields in hurt/new_arena and add a stunned-death/stage-reset regression. Parent notified. No shared code edited.

Still unverified: commercial gate release timing, input requirement, re-entry permission, giant entry, safety and exclusion behavior. Visual similarity from camera footage cannot certify exact dimensions or a perfect match. Current binary opening is not a measured reproduction of a door animation.

## QA2 targeted fix recheck — resolved
Reran the identical work/gates_qa.py after parent reset correction. Previously stunned death now releases to(5,29) within1second, entry0 and stun0. new_arena reports stun0.0/clock0.0. All32 pause/release/buffered-input scenarios still pass. The stale-stun gate release defect is resolved. Exact commercial gate rules/timings remain unverified. No shared code edited.

## Follow-up sequence search — actual evidence still required
Found a new released-cabinet candidate via web search: Seals on the Move, `Pac-Man Battle Royale Chompionship Deluxe Arcade Gameplay`, published2024-03-02, https://www.youtube.com/watch?v=efLgejKG_ls . This source has NOT yet been visually inspected; it is only a candidate, not evidence of gate behavior.
Attempted authorized browser review. In-app browser unavailable; inventory showed native Chrome window5901650. Parent granted exclusive native UI, but getApp repeatedly returned `Computer Use helper already has an active request`; subsequent listWindows returned the same lock. No native input was sent and no existing user page was changed. Web open cannot fetch this video's frames. Therefore no new death->bay->release or voluntary-reentry observation was obtained in this attempt, and no gate-operation unknown was closed. Needs a functioning UI session or direct review of accessible footage. Earlier static gate appearance evidence remains valid; exact operation remains unresolved.

## Released-Deluxe footage inspected after UI recovery
Successfully inspected Seals on the Move's released Deluxe cabinet footage https://www.youtube.com/watch?v=efLgejKG_ls using separate native Chrome5771396. Paused/sample-inspected0:27,0:37,0:59,1:15,1:30,1:40,1:45 and2:00, with short continuous playback0:59-1:15. This is visibly a large Deluxe table with eight stations.

NEW CONFIRMED VISUAL CORRECTION: At1:15,1:30 and2:00 the maze and pocket outlines are cyan/blue, while the closed gate threshold hatching remains YELLOW. Thus my earlier generic maze-accent hatch recommendation was wrong for nonyellow themes. Use a stable yellow hatch color independent of wall theme, while pocket contours follow the maze theme. Concrete links: https://www.youtube.com/watch?v=efLgejKG_ls&t=75s and https://www.youtube.com/watch?v=efLgejKG_ls&t=120s . Parent notified immediately.

Operation evidence remains insufficient: the active blue player's station is cropped out in many closeups; around1:40 the edit cuts to joystick/person and1:45 shows an angled wide view. No complete identifiable death->own bay->release sequence was observed and no voluntary re-entry attempt could be identified. Do not infer release timing or reentry permissions from these snapshots. This is an unresolved evidence gap, not a pass. No game code changed.

Useful adjacent evidence for effects reviewer: at1:30 a player is visibly on fire with a long smoke trail; at2:00 there are fire/score effects and ghosts in the central enclosure. These frames alone do not identify life-count outcomes. Native UI released to effects reviewer with2:00 paused fullscreen.

## Targeted hatch-color fix verified
Parent applied constant GATE_HATCH yellow to closed threshold bar/stripes while retaining theme accent on pocket contours. Independently reran `python -m unittest test_smoke.Smoke.test_gate_hatch_color_is_independent_of_maze_theme -v`: passed (all4themes covered by the pixel regression). This resolves the specific visual mismatch supported by released-Deluxe footage efLgejKG_ls1:15 and2:00. It does not resolve the still-unobserved death/bay/release timing or voluntary-return rules. No additional browser work or game edits performed.
