# Current DX comparison — 9 November 2026

**Neon Nibblers is not an exact replica.** It is an independently implemented game with broad feature coverage, four observed maze reconstructions, and reference-supported details. Passing its automated tests verifies its own rules, not the commercial game's rules. This assessment supersedes older baseline tables without erasing their history.

## Revision 17 — responsive input, continuous motion and reference-informed pace

Two normal-looking actors in real DX footage qcO9tzgsdjo4:09/4:11/4:13 cover approximately12–15 dot spacings in nominal4seconds. Whole-second timestamps and camera perspective leave a conservative2.4–5dots/second range; hidden power status is not fully excluded. Our previous10dots/second was likely materially faster. The new provisional default is4dots/second (.25s per20px cell). Rush/Slick/ghost/item intervals are.1625/.1375/.40/.60s, preserving earlier authored relative speeds; those ratios are not recovered DX facts. The old fast profile remains selectable with --tuning tuning.fast.json. Power durations, probabilities, spawn interval and collision impulse constants were not guessed from this footage.

Fixed a concrete keyboard bug: held Up overwrote a freshly pressed Right in the next input poll. Every station now uses its most recently pressed held direction; releases fall back to remaining held keys, and no-key state retains buffered intent. Legal facing/reversals update without granting distance or resetting movement clocks. Invalid turns stay buffered until a junction. Slick/recoil remain in control during their effects. Discrete travel decisions still occur on the movement cadence; immediate facing does not eliminate the possible250ms positional wait or constitute a continuous subcell physics model.

Replaced exponential visual easing with constant-speed axis-aligned waypoint motion for players, ghosts and moving items. This avoids bursts/holds at the slower cadence and prevents rounded diagonal cuts through corners. Logical reversals cancel abandoned forward waypoints, tunnel coordinates wrap, damage/restart reset tracks, and50px gate movement receives its own distance scaling. Pause/help/results freeze motion; rendering changes no Match state. Very long frames crossing multiple unseen turns can snap to the final cell rather than inventing a route. Normal30/60/144Hz default-speed tests do not encounter that case.

Bot navigation now recognizes nearby powers across tunnel connections, prioritizes vulnerable rivals while giant even when ghosts are in their house, and chooses a legal safer fallback when goals disappear during refill. Six adversarial/navigation tests and independent review cover these fixes. No new collision-resolver defect was reproduced; all-map crowds recover, retain controls and avoid overlaps/extra-cell jumps. With slower speed, densely packed eight-player crowd recovery takes longer in wall-clock time; this tradeoff remains documented.

Paired90-second eight-actor simulations isolate pace from the bot changes: death events140→54, rival hits93→30, pickups298→285 and mean stage4.75→2.25. Near-rival proximity rises.190→.227, but it is a Manhattan-distance proxy, not a collision measurement. Separate1/2-actor experiments do not include the application's vacant-station bots. These metrics show less rapid churn and fewer attacks, not greater enjoyment. All90s observations are censored for finish time; no survival-length conclusion. No human multiplayer fun-equivalence test has been completed.

Maze geometry is now prepared before play. One local dummy-render comparison moved first-layout-change rendering from.9999s to.0084s, with3.5794s spent preparing four mazes before play; this is a measured cold-start comparison, not a guaranteed native FPS claim. The game shows Preparing mazes during that work. Actual four-map slow tour review found zero off-centerline positions across17,117 player samples, and straight/tunnel motion at60Hz consistently1.333333px per moving frame.

All328 checks pass Windows and Ubuntu/WSLg. Native runs cover all four maps with1/2/8 human-designated stations plus six transition runs, using7/6/0AI fill; audio initializes, physical input/audibility remains uncertified. Twelve full automated matches reconcile scores and rankings; deterministic replay, stress checks and extracted-package validation are recorded separately. Updated104-second720p60AAC videos show64seconds of four-map play,8seconds of labelled controlled C-to-D transition and32seconds of labelled continue scenarios. All capture actors are automated.

Agents completed initial and deeper passes, with targeted fixes/rechecks. The task-owned research YouTube tab/window was closed and its removal verified; other user applications were left untouched. Physical controllers remain deferred to production. Exact DX power timing, ghost rules, collision physics, scoring, artwork and subjective fun are not certified. Original assets/code/audio remain independently authored.

## Revision 16 — exterior spacing and continuous maze changes

The user's annotated image exposed a real mismatch: exterior wall cores were3px apart while bay cores were6px apart. The exterior now has the same6px separation, concentric corner curves, aligned gate shoulders and continuous tunnel joins. A second review found and fixed lower gates being dimmer due to inconsistent supersampling phase. All four maps/five palettes/eight station joins were checked, with unchanged public lanes and body clearance.

Two fresh passes through Harold Zheng's DX footage (qcO9tzgsdjo,5:02–5:04) show actors staying on the field, maze compression/change, temporary enlargement of both players and ghosts, and scattered dot refill. The game now preserves actors across stage changes instead of resetting everybody to bays/house. Legal actor and item positions are reserved before displaced objects get the nearest free lane. Ghost release/return/carrier state, scores, lives, ongoing effects and continue timers persist. Exact relocation and power persistence remain our stated policy, not recovered source rules. The initial/new-match reset is unchanged.

An original1.1-second shrink/blend/expand animation replaces the instant layout swap. Actor enlargement is visual only; it never changes combat size or grants a power. Dots refill visibly and become collectible together between0.6 and1.1 seconds, with no accidental second stage-clear during refill. HUD scores stay stationary and pause/help/results freeze the animation. The0.90 maze scale,1.35 actor pulse, short midpoint overlap, timing and trajectories remain approximations; source footage does not establish an exact curve or whether movement pauses.

The deeper transition review caught a moving item stealing an already-valid static pellet position; the reservation fix is covered by a regression. Legacy tests that required a global respawn were updated to require continuous legal placement. The independent transition tests cover all16 ordered map changes, eight-player conflicts, private bays, inactive stations, continuation, carried/returning/releasing ghosts, refill and render immutability.

All288 checks pass on Windows and Ubuntu/WSLg. Native checks cover1/2/8 on all four maps (24 cases), plus actual transition runs for those counts on both systems (six cases). Twelve complete simulated matches reconcile scoring/rankings, and a720-frame472-event replay verifies deterministically. Audio initialized; physical input and audibility are not certified. Initial geometry construction still causes a first-use render delay; short native startup-inclusive figures are not steady-state performance claims.

Three new88-second1280x720/60fps recordings contain48seconds of all-map gameplay, an8-second labelled controlled C-to-D transition, and32seconds of labelled continue acceptance/expiry. All actors are automated;1/2/8 human-designated stations have7/6/0AI. Fresh24-second GIF map tours, all11-power/player/ghost animation sheets and actual transition frame sequences accompany review.

The source clearly shows a3000 popup associated with this transition; its universal award/recipient/scaling rules remain unknown, so the configurable500 simulation clear award is not promoted as authentic. All11 power categories are present and tested internally, but exact durations/spawn rates/stacking, global ghost vulnerability, ghost targeting/release and several source artwork details remain unresolved. Original sprites/audio/branding are retained. Controllers remain deferred to production; no perfect-match or zero-issue claim.

## Earlier revision15 detailed comparison (updated by revision16 above)

Fresh continuous DX footage separates map transitions from power-related color changes. In [Harold Zheng's DX gameplay](https://www.youtube.com/watch?v=qcO9tzgsdjo), approximately5:00–5:05, nearly cleared family C morphs into family D and dots refill while the same spectator display remains amber. At5:07–5:08 the red player enlarges and the walls/cabinet lights turn red without another layout change. At5:10 both red and blue giants are visible and walls are blue;5:11 shows a red/purple transition;5:13 returns blue with both giants still active. This supports cycling among concurrently enlarged player colors. It does not establish a fixed one-color-per-map rule or a permanently retained last-pickup color.

Revision15 now keeps the base color across stage changes and cycles active giant station colors. Its **1.25-second period and station ordering are authored approximations**, not measured commercial constants. Exact eligible states, three-or-more-player order, transition blend, expiry/reversion and cabinet/display synchronization remain unresolved. The last individual dot and precise pickup contact were obscured, so these observations must not be promoted into a complete trigger specification. Camera glare still explains local brightness variation, not the synchronized global red/blue changes. Research captures and the four-frame figure `outputs/DX-wall-color-evidence-r15.png` are outside the playable package; see `docs/audits/revision15_reference.md` for both critical passes.

The actual revision14 renderer had a separate reproducible quality problem: native-resolution mask outlining with horizontal/vertical erosion made curves thinner and broke the pale core. Revision15 replaces it with a shared supersampled contour/material for walls, house and bays, and restores the continuous yellow edge above gate hatching. Quantized coordinates, inferred curves and exact reference bloom remain limitations.

## Complete subsystem comparison

| Area | What we actually have | What remains different or unverified | Required next evidence/check |
|---|---|---|---|
| Maze catalog | Four traced observed families A/B/C/D | Complete inventory, hidden endpoints, exact coordinates, order and transition trigger | More distinct full-board views and uninterrupted transitions |
| Wall material | Uniform supersampled contours and independent palettes | Exact thickness, bloom and hue policy | Aligned crops and continuous color-event sequences |
| Gates/house/tunnels | Eight double-U bays, yellow lip/hatch, two house contours, doorway and wrap | Release permissions/timing and open stripe persistence | Complete exit/reentry/death sequences including AI stations |
| Players | Eight colors, shaded spheres, mouth, growth, death and arrival | Exact silhouette, eye/mouth/lighting, poses and contact radius | Source direction/state animation strips |
| Ghost artwork | Domes, eyes, blue state, returning eyes, stun stars | Frightened expressions, proportions, state colors and shading | Clear normal/frightened/returning/carry frames |
| Ghost movement | Four fixed ghosts, graph-distance nearest-target chase,70% targeting/30% random, avoids needless reversal | Authored AI; personalities, count/order, speed, chase/flee and difficulty not recovered | Track individual ghosts through intersections and release/return |
| Ghost release | Initial stagger .9/.6s,1.2s recovery, protected house/exit/eyes | All numerical delays and protection are assumptions | Timed startup/eaten-return sequences |
| Player contact | Equal-size bump, giant eats smaller; coordinated rollback and one outward step | DX displacement, recoil, hitboxes and crowd priority | Close controlled contacts and held-input motion checks |
| Power inventory | Eleven categories | Edge cases, damage, timing and artwork not established by count | Per-power interaction evidence |
| Power generation | Initial corner Gold, central Giant,3 other items; every3s, cap12, equal category weights | Positions, weights, cadence, movement and exceptions authored | Multi-session timestamped spawn census |
| Scoring | Dot10/Gold100/Giant1000 observed in instruction legend; shared ledger | Other item75/ghost200/rival300/clear500, combos, bonuses and life cap5 unconfirmed | Isolated pickup/attack score changes |
| Stage progression | Dot-clear advances map; actors/effects persist with nearest-legal relocation, animated refill | No general respawn observed; exact trigger, relocation, power persistence, trajectory and order unknown | Track final dot and actors/effects across transition |
| Joining/Find | Independent stations, identity, locator and bot takeover | Eligibility, locator animation/timer and takeover policy | Cabinet Start/Find in each lifecycle state |
| Continue/end | Approximate10s prompt with AI continuing; original restore/initials policies | Paid score/life restoration, price, reveal delay and ranking UI | Successful paid continue and complete end sequence |
| HUD/screens | Station order/colors, upright scores, original menus/results/operator/attract | Cabinet-side scores rotate; font, spacing, life symbols and transitions differ | Comparable full-state screenshots |
| Audio/spectators | Original synthesized cues; mirror/ranking spectator windows | Audio texture/timing and overhead lifecycle content | Source event sequences and audibility review |
| Controls | Real detection plus visibly simulated development availability | Physical8-controller, mixed-device, latency and human acceptance | Deferred to production by user instruction |

## Visual coverage matrix — independent reference pass

“Implemented” means visible in the app, not an exact graphical match. Latest research used continuous DX frames plus the user photograph; it did not manufacture a commercial sprite atlas.

| Visual category | Direct reference evidence | Implemented treatment | Remaining difference/unknown |
|---|---|---|---|
| Four maze families and tunnels | Full-board A/B/C/D and observed C→D morph | Traced corridor graphs, rounded contours, wrap mouths | Pixel coordinates, hidden endpoints, morph animation and full inventory |
| Wall lighting/colors | Uniform cores; growth-associated red/blue cycling | Supersampled material and giant-color cycling | Photometric match, exact cycle/expiry; glare is not game shading |
| Bays/house | Double contours, hatch with continuous lip, central doorway | Original vector bays, two house contours and lip | Opening stripe persistence, line widths and release animation |
| Normal/giant players | Shaded colored spheres, mouth motion, visibly enlarged red/blue at5:10–5:15 | Original shaded sprites, directional mouths and growth/death effects | Eye/silhouette, interior mouth shading, animation curves and exact scale |
| Normal ghosts | Domes, directional white eyes; close tabletop5:14–5:15 | Original domes, animated feet and eye direction | Surface shading, feet and proportions are approximations |
| Frightened/returning/carried ghosts | Returning eyes visible5:15; no newly isolated close frightened/carry face | Blue body with normal eye structure, eyes-only and carrying states | Frightened facial design and carry visual correspondence not established |
| Dot/pellet visuals | Small white dots; yellow/green spheres in footage and instruction legend | Dots and shaded collectible spheres | Diameter, bloom and bob/rotation phase |
| Eleven pickup icons | Published category poster and scattered footage | Eleven independently drawn icons | No complete clean in-game state atlas; icon coverage is not art identity |
| Power effects | Fire in retained footage; cyan jagged effect5:07–5:08 | Original fire, smoke burst/trail, zap, shake, skid and magnet feedback | Exact geometry, layering, duration and attribution of overlapping effects |
| Contact/death/arrival | Moving/overlapping players and end-of-life presentation | Coordinated contact response and original effects | No isolated measured DX bump; frame-by-frame poses not recovered |
| Scores/lives/locator | Station-colored scores, life/status markings and prompts | Upright desktop HUD, custom glyphs and locator | Cabinet-side rotation, exact glyphs/icons and flash timing differ |
| Join/continue/end/initials | Continue countdown and subsequent initials observed | Functional original screens and persistent records | Paid-resume flow unobserved; composition and transitions remain original |
| Attract/help/operator/spectator | Overhead gameplay and instruction legend available | Original help/operator/attract plus spectator windows | Full original screen inventory and exact lifecycle presentation unavailable |

The strongest remaining visible differences are (1) custom desktop HUD and lifecycle screen composition rather than cabinet-oriented typography/layout, (2) procedural player/ghost surfaces, face geometry and animation poses rather than source-matched sprites, and (3) independently authored power icons/particles rather than a verified eleven-power animation set. Frightened-face correspondence is specifically **unverified**, not a newly proved wrong expression. These are broader gaps than the now-corrected yellow lip and contour defects.

## Eleven powers: present is not the same as exact

The published CHOMPionship poster establishes categories, not numerical duration/range/stacking. Defaults in gameplay_tuning.py are configurable; configurability is not reference verification.

| Reference category | Current behavior | Remaining fidelity gap |
|---|---|---|
| Gold Power Pellet | Holder eats roaming ghosts7s;100points | All ghosts blue globally while unpowered players vulnerable; global-versus-holder rule unresolved |
| Green Super Pellet | Giant7s, eats ghosts/smaller rivals;1000points | Blanket immunity, equal-giant contacts, hitbox and duration |
| Caffeine | Faster cadence7s | Speed multiplier, acceleration, trail and duration |
| Smoke Bomb | Ghost slowdown, immediate stationary pickup cloud and movement trail | Poster says explosion; area, burst/trail and duration unknown |
| Banana Peel | Forced-direction fast skid2s | Speed, collision/rebound and recovery |
| Lightning | Stuns nearby rivals/ghosts2s within8 cells | Kill versus stun, walls, immunity and range |
| Ghost Sheet | Ghosts ignore holder7s; incidental contact hurts | Invisibility appearance and incidental outcome |
| Chili Pepper | Forward wall-bounded fire5 cells3s; damages rivals/ghosts | Poster says nearby burn; direction/radius, reach and lethality |
| Earthquake | Slows players/roaming ghosts5s | Affected set, slowdown, shake and duration |
| Extra Life/1UP | Adds life, cap5 | Original cap and capped-pickup behavior |
| Ghost Magnet | Captures contacted ghosts7s, carries as weapons | Multiple capture, attachment, Gold/Giant precedence, hits and expiry authored |

## Correction order

1. Fix concrete defects: uneven outlines, yellow lip, contact jumps and stationary smoke burst. Retest those cases.
2. Compare all assets/states at equal scale; record unavailable source states as unresolved.
3. Recover global vulnerability, smoke/pepper/lightning, spawn and AI rules from sequences; color cycling is observed but exact cadence/expiry remains unknown.
4. Regenerate1/2/8-station footage from frozen source, verify Windows/Linux and extracted package, preserve open evidence issues. Agent code approval is not a perfect-match certificate.

## Sources and boundaries

- [Manufacturer DX page](https://bandainamco-am.com/collections/pac-man-battle-royale-deluxe): cabinet/station identity, not physics specification.
- [Actual promotional power poster](https://www.gameroomshop.com/cdn/shop/files/namco-pac-man-battle-royale-chompionship-home-version-3.png?v=1701789284&width=2242): categories only. Dealer prose mixing predecessor rules is excluded.
- [DX instruction/gameplay](https://www.youtube.com/watch?v=qcO9tzgsdjo): legend0:01/0:03, C4:10/4:53, D5:05/5:15, continue6→2 at5:11→5:15; fresh color sequence5:07–5:15.
- [DX session](https://www.youtube.com/watch?v=43DcDXxEgzk): dot aggregate9:22→9:23, continue9:25–9:35 and initials.
- [IAAPA DX footage](https://www.youtube.com/watch?v=-cNOhumVZ74): A/B layouts68/73s, AI labels/unjoined stations.
- User blue-maze photograph: familyD wall/gate appearance only; no timing inferred. Research media stays outside playable package.

Original code, art, branding and audio remain explicit project constraints. No commercial sprites/ROM/audio are bundled. Literal asset identity is not achieved or certified.
