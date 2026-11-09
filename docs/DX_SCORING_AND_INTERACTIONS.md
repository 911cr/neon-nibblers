> Current status: see DX_RELEASE_STATUS.md. Earlier revision sections are historical.

# Scoring, event attribution and interactions

Revision 8, 2026-11-08. Status **IMPLEMENTED AND TESTED** describes Neon Nibblers software; it does not mean **VERIFIED DX**. No scoring amount below has been recovered from an unambiguous DX scoring sequence in this cycle. Existing values are preserved as configurable adaptation settings in `score_ledger.DEFAULT_SCORES` / `Match(score_values=...)`.

## Score event audit

| Event | Current points / recipient | Exact trigger | DX value evidence | Next evidence needed |
|---|---|---|---|---|
| `dot` | 10 / collector | Successful movement step ends on an unconsumed dot | UNKNOWN | Isolated before/after score digits during one pellet pickup |
| `pickup` | 75 / collector | Any of all 11 power categories collected | UNKNOWN | Each category in isolation; identify whether item points differ |
| `ghost_eaten` | 200 / Crown or Titan holder | Roaming ghost contact or edge crossing | UNKNOWN | Single and consecutive ghost eats; possible escalating multiplier |
| `ghost_burned` | 200 / flame owner | Roaming ghost inside wall-bounded flame cells | UNKNOWN | Score before/after pepper attack |
| `rival_eaten` | 300 / giant attacker | Smaller rival takes damage on contact or crossing | UNKNOWN | Attacker and victim score indicators simultaneously |
| `rival_burned` | 300 / flame owner | Rival actually loses life to flame | UNKNOWN | Pepper hit with score and life indicators visible |
| `carried_ghost_hit` | 300 / living magnet owner | Carried ghost actually damages another player | UNKNOWN | Ownership and score attribution during carried attack |
| `stage_clear` | 500 / each surviving player | No dots remain, time remains, at least one survivor | UNKNOWN | Continuous DX transition sequence with all scores visible |
| Bonus life | 0 score / eligible player | First crossing of 10,000; up to five lives, no revival | Manual example supports 10,000 threshold; cap/once-only semantics UNKNOWN | Operator setting variants and repeat threshold crossing |
| Extra life item | Pickup points above, life +1 capped at five | Heart pickup | Basic extra-life category supported; cap and pickup points UNKNOWN | At-cap pickup and score before/after |
| Bump, death, survive, capture | No points | These events do not currently award score | UNKNOWN | Establish whether real game awards survival/capture or subtracts score |

No combo multiplier, separate special-food class, persistent high-score table or configurable credit accounting is implemented. These remain gaps, not evidence that DX lacks them. The three-minute timer, highest-score victory and early all-eliminated ending remain adaptation choices. Equal totals share a competition rank; station number only stabilizes row ordering and never breaks a tie. Eliminated joined players remain in rankings. Unjoined stations do not.

## Event ledger and replay

Every live score mutation now passes through `Match.award`. The same `Player.score` supplies the HUD and ranking values. Ledger records are deep-copied at event time and contain sequence, simulation timestamp, tick, event, one-based player ID, stage, score delta, resulting score and collision/power context. Zero-point records include match start/end, station joining, damage, extra life, threshold bonus, ghost capture and stage start. `ledger.totals()` independently reconstructs points awarded per player; gameplay tests assert equality with model totals.

`python replay.py record sample.json --players 8 --seconds 20 --seed 42` stores seed, settings, progression policy, fixed 1/60-second inputs, per-second state/event fingerprints, 10 Hz player/ghost movement traces and the complete ledger. `python replay.py verify sample.json` reconstructs the actual Match logic and rejects changed input, changed seed, changed events or divergent state. `Match.snapshot()` includes all logic timers, actors, effects, items, dots, ghost states, map ID/revision and random-generator state. This is a reproducible regression format for this game version, not a promise of replay compatibility after future rule changes. Versioned replays should retain the producing commit. It covers logic direction/join commands, not raw physical-device or operating-system events.

`FixedStepper` provides a 60 Hz accumulator so the same input schedule produces the same state at 30, 60 and 144 render updates per second. This is separately tested. Calling `Match.update` directly with arbitrary large deltas is **not** frame-rate independent: movement currently processes at most one cell per call. Use the accumulator or the fixed-step replay tool for timing comparisons.

## Interaction matrix: implemented approximation

The category-level reference is the [DX distributor description](https://primetimeamusements.com/product/pac-man-battle-royale-chompionship-dx/), plus the promotional poster reviewed in the preceding audit. These establish categories, not numerical timers, stacking, damage immunity or hit geometry. The [DX operation manual](https://bandainamco-am.com/cdn/shop/files/Pac-Man_Battle_Royale_Chompionship_DX_Manual_5_12_revise_Edit.pdf?v=18440531496271041764) documents operator controls/settings, not this combat matrix. Source details and confidence are tracked in `DX_REFERENCE_EVIDENCE.md`.

| Power | Ghost interaction | Rival interaction | Repeated/combined pickup and expiration | Fidelity status |
|---|---|---|---|---|
| Gold | Eat roaming ghosts, including during respawn safety | Does not eat rivals | Refresh seven seconds; magnet capture takes precedence | Category supported; precedence/timing UNKNOWN |
| Green giant | Eat roaming ghosts | Eat smaller rival; equal giants bump; `hurt` blocks damage | Refresh seven seconds; Rush still speeds giant | Category supported; blanket immunity/stacking UNKNOWN |
| Caffeine | Changes contact cadence through faster player speed | Same damage rules | Refresh seven seconds; quake doubles movement interval | Category supported; combined multiplier UNKNOWN |
| Smoke | Nearby smoke slows roaming ghosts | No direct damage | Trail seven seconds; clouds 2.5 seconds; quake combines | Category supported; range/stacking UNKNOWN |
| Banana | Normal vulnerability | No direct attack | Forced fast slide two seconds; takes precedence over Rush | Category supported; rebound/timing UNKNOWN |
| Lightning | Nearby ghost stun, not kill | Nearby rival stun, including safe/giant actors | Two-second stun overwritten; no persistent player power | Zap category supported; lethality/immunity UNKNOWN |
| Sheet | Removes holder from targeting, not incidental contact | No rival immunity | Refresh seven seconds; translucent rendering | Concealment supported; contact outcome UNKNOWN |
| Pepper | Burns roaming ghosts ahead through legal corridor cells | Damages nonimmune rival | Refresh three seconds; walls stop reach | Category supported; exact shape/range UNKNOWN |
| Earthquake | Doubles roaming ghost movement interval | Doubles all player intervals including collector | Refresh global five seconds; combines with Rush/Smoke | All-player slowdown supported; ghost scope/timing UNKNOWN |
| Extra Life | No direct effect | No direct effect | Immediate life +1, cap five; pickup score remains | Extra life supported; cap/value UNKNOWN |
| Magnet | Multiple contacted ghosts captured, held ahead | Carried ghosts damage rivals and award owner | Refresh seven seconds; death/expiry release harmless returning eyes | Carry weapon supported; count/immunity/release UNKNOWN |

Damage clears player effects and stun/movement clocks. Map transition clears powers, smoke, carriers and stun, preserving lives, score and remaining time. These persistence rules remain UNKNOWN for DX. Existing smoke tests cover local ranges, wall blocking, quake/Rush composition, head-on crossings, equal giants, multi-ghost capture, expired/dead-owner weapons and repeated ghost scoring protection. They prove the stated implementation, not undocumented reference rules.

## Two-pass review of this cycle

Pass 1: all previous 29 smoke tests passed after routing every score path through the ledger. Eight new ledger/replay tests pass, covering all eight reward routes, damage/bonus events, same-tick attribution, immune/repeated attacks, tied ranking, sparse joining, 1/2/4/8 players on four maps, JSON replay and deliberate tampering.

Pass 2: searched the whole game for score assignments; only `award` changes runtime score. Twelve ledger tests now pass, adding seeds 1–8, deterministic cycle/repeat/random progression, sparse P8/P4 joining in the same recorded tick, exact individual score popups, and paused/guide locator timing without catch-up. Tested grouped fixed-step timing at 30/60/144 Hz and score-total reconstruction. Found a pre-existing autoplay defect: selecting `g.dots` directly as a navigation goal set then discarding the current cell could remove an unscored dot. The main developer corrected the alias to copy the set. Recorded and verified the included 12-second eight-player sample: 720 simulation frames, 431 events. Main integration testing separately found a controller-reconnection assertion failure; the main developer fixed same-instance recovery and this reviewer independently reran the original test successfully. Remaining gaps include commercial scoring measurements, custom timer/finish rules, scoring UI comparison, durable high scores and full external-game interaction evidence.


## Revision 10 — all-map review and simultaneous interactions

Reviewed all four authored maps against retained real DX75/120second frames. The footage does not establish four complete DX layouts; a fresh viewing attempt was stopped by browser URL-verification policy. No unsupported geometry changes were made. Every map already has a continuous house perimeter; the catalog now validates those routes and door approaches. Broad wall interiors have an inset contour based on the visible rectangular-island style; application to broad L-shaped walls remains an explicit visual approximation. No floor, frame, gate or house-outline pixels changed in the comparative render QA. See audits/revision10_all_maps.md for the four-row evidence matrix.

Fixed lightning outcomes depending on station order, tiny floating-point power/safety expiration tails, roaming collectibles not collecting on stationary/stunned players, and same-tick bonus credit after that contact. Added ten original layered event cues on separate channels. Mute stops active cues immediately; unavailable audio is handled gracefully. Sounds are synthesized locally, not commercial recordings. Audible speaker quality and physical controllers remain unverified/deferred.

92 automated tests pass locally on Windows and Ubuntu. Actual native1/2/8 rendering runs now cover all four maps (12 short120-frame scenarios on each OS). These are startup/render samples, not benchmarks or human gameplay certification. The supplied1/2/8-player GIFs each show four separate seeded6-second map scenarios (24seconds total); they do not assert that the commercial game uses that stage sequence. All game GIFs are silent. sound_preview.wav demonstrates the original cues.

Source, event replay and captured gameplay were regenerated after the simulation fixes. Complete commercial geometry, exact scoring/timing/AI, stage transitions, joining windows, attract/operator and spectator behavior remain open evidence/work items. Physical controller acceptance stays in production.


## Revision 12 — reconstructed layouts and cabinet lifecycle

Current production routes are independently reconstructed from two full DX spectator views at68/73seconds in the IAAPA2022 source. All four color profiles use these two families; unsupported authored routes are retired. Quantization and glare-hidden endpoints remain approximate; no complete commercial catalog or pixel identity is certified. Ghost house paths, tunnels and bays now derive from each profile's geometry. Actual-width render checks caught and fixed erased wall stems, and new bay positions required a dynamic central HUD clearance fix.

AI actors were observed alongside join prompts. Vacant stations now have configurable AI opponents; human counts, controls, credits and rankings remain distinct. Human takeover resets bot scores, carried weapons and growth; eliminated humans cannot revive through Start. All-human elimination ends a match even if bots survive. Exact DX difficulty/replacement rules remain unknown.

Implemented smooth growth/shrink, death dissolve, bay arrival feedback, saved operator settings, credits/free play, persistent local human scores with failure retry, original idle instructional/high-score attract pages and optional spectator mirrors/ranking windows. Their detailed UI/timing are original adaptations. Native game+spectator pairs ran on Windows and Ubuntu/WSLg.

151 tests pass locally on both OS environments. Twelve complete automated human/AI matches ended with reconciled event totals and human-only rankings; native1/2/8 checks cover all four profiles on both systems. Physical controllers remain deferred to production. Current recordings use1/2/8 logical human slots with7/6/0 AI opponents; all actors are computer-controlled during capture.

Current acceptance/evidence boundaries are in DX_RELEASE_STATUS.md. Software features are implemented and tested; exact commercial score/multiplier values, timings, AI, joining/progression rules, full map inventory and overhead content by state remain unverified. Open evidence issues are not administratively closed to claim completion.


## Revision 13 — source measurements, rounded walls and scoring/AI corrections

Fresh confirmed DX footage43DcDXxEgzk was reviewed at quarter speed and paused positions. At9:22 red144640 has four ordinary dots ahead; at9:23 the corridor is cleared and score144680. This OBSERVED DX aggregate supports10 per ordinary dot; it does not recover other score awards or multipliers. At9:23–9:34 the final-life station displays CONTINUE/COIN while AI moves, followed by alphabet/name entry by9:45. No purchased continue, restored-life policy or score retention was observed. The fresh red full-board9:34 is independently identified as existing family A, corroborating color/layout independence, not adding a third maze. Candidate power sequences were rejected as exact duration measurements because of refreshes, occlusion and transition ambiguity. See audits/revision13_reference.md.

Rounded capsule ends and convex branch corners now retain narrow stems and the same validated corridor graph. Removed a faint third house underlay contour; actual-App scans require exactly two house borders on all four profiles. New comparison research images remain outside the runnable package. Exact20px quantization/hidden endpoints, source widths, full commercial catalog and progression remain unverified.

Corrected ledger totals after bot-to-human takeover: historical bot awards remain recorded, while station_join starts the new score account at zero. HUD, spectator rankings and ledger agree. Tested simultaneous dot/power/ghost/rival/bonus awards, duplicate fire attackers, expiry contact, carried ownership and same-tick damage. Bot routing now uses deterministic weighted legal paths, avoiding nearby lethal ghosts/giants/carried rival weapons and actively seeking capturable ghosts with Magnet. This improves our original strategy; exact DX difficulty/targeting remains unknown.

Power durations, movement intervals, ranges, slowdown multipliers and item cadence/cap are now validated per-Match tuning settings, loadable with --tuning tuning.example.json. Complete effective values and pickup duration/nominal expiry are captured in event logs/replays; quickstart and station START honor the same settings. Existing numerical defaults remain explicitly approximate. The on-screen guide reflects effective durations.

Added optional --untimed life-survival mode, also operator time limit0. Default180s remains an explicit custom score-attack mode, not a certified DX limit. Untimed progression, pause, elimination, spectator labels and replay are covered; CLI mode overrides do not silently rewrite saved operator settings. Exact final-life continue interval and background AI before original name entry remain a known presentation/behavior difference; no invented paid-continue policy is claimed.

Results now offer N for original three-letter initials for this session's qualifying top20 human rows. Atomic renaming uses session/player identity, protecting ties and historical/legacy rows. Failed writes roll back; cancelling discards only the active draft. Immediate replay and pending score-save retries remain intact. Exact cabinet entry UI, timeout and physical-controller entry are not reproduced or certified.

Final validation:187 tests passed on Windows and Ubuntu/WSLg, with source-frozen extracted-ZIP verification recorded separately. Native1/2/8 runs cover every profile on both systems, plus actual game/spectator pairs with audio initialization. Twelve complete automated human/AI matches reconcile ledger totals and rankings. Three48-second1280x720/60fps MP4s with original AAC event audio fully decode;24-second GIF previews and12-frame profile/count contact sheet were checked. All recording actors are automated; logical1/2/8 human stations have7/6/0 AI. Physical controllers, human multiplayer acceptance and audible speaker assessment stay in production.

Agent reviews ran initial and deeper passes with targeted fixes/rechecks. Their approval covers tested implementation scope, not undocumented original rules. Remaining exact scoring/power/AI/map/continue questions are tracked honestly; no perfect-match or zero-issues claim.


## Revision 14 — four observed layouts, recovered pellet awards and station continues

Fresh confirmed eight-station DX footage qcO9tzgsdjo at0:01/0:03 displays HOW TO PLAY awards: ordinary dot10, yellow pellet100, green pellet1000. These are OBSERVED DX for the pictured build, independently read by root and mechanics reviewer. Gold/Giant no longer receive the generic75 pickup award; other items, ghost/rival awards and combos remain explicitly unrecovered estimates. Pickup events retain their event identity and now identify the score rule. Repeat-pickup and same-tick tests use the newly observed values.

The same source at4:10/4:53 and5:05/5:15 shows two more distinct mazes. The runtime catalog now has four independently reconstructed observed families:0 Golden Rails/D569cells,1 Violet Crosscurrent/B569,2 Ember Courtyard/C585,3 Cyan Archway/A582. C was traced by the map reviewer and independently checked by the research reviewer; D was independently traced by research and critically reviewed by maps. Isolated narrow wall bars were widened from8 to16px, while every route retains20px normal-body clearance. Seventeen map checks cover all1-8 counts, edges, tunnels, gates, house contours, landmarks and no unintended open2x2/dead ends. Coordinates and hidden endpoints remain approximations; four observed families do not prove the complete commercial catalog or stage order.

Source43DcDXxEgzk brackets CONTINUE near9:25–9:35; qcO9tzgsdjo shows CONTINUE6 at5:11 and2 at5:15. A source-informed10-second station offer now follows a custom1-second reveal delay after final human death. AI/ghost simulation continues; all-human elimination is deferred until offers expire. Living humans keep playing while another station has an offer. Start redeems a valid offer after atomic software-credit/free-play authorization; failure/pending/paused/repeated inputs never debit incorrectly. The independent restoration policy preserves score and earned-bonus flag and restores configured starting lives. Actual paid source continuation and its score/life policy remain unobserved. Timed expiration overrides offers. Last-offer timeout settles scores once and automatically opens qualifying initials; other results retain optionalN entry.

Continuation state is deterministic, snapshot/replay-visible and pause/guide-safe. Raw Match defaults disable offers for explicit legacy/timed scenarios; normal App defaults enable10seconds. --continue-seconds0 disables; --continue-delay adjusts the explicitly custom reveal. INSERT supplies development credits during an offer; C remains lobby credit/P6-down during active play. Continue text was moved to clear the lower footer. Tests found and fixed that input conflict and footer overlap, and verify pending score-write retry, no duplicate charge, simultaneous/staggered stations and automatic name-entry recovery.

Ghost navigation now uses legal corridor distance rather than Manhattan shortcuts through walls or across the long side of a tunnel. It avoids immediate reversal when another exit exists. Five navigation checks cover a formerly oscillating U-shaped wall trap, all-map shortest tunnel routes, frightened retreat, normal wandering and dead-end return. Bot risk weights, ghost target choices and difficulty remain original, not recovered cabinet AI.

Actual extra-life and score-threshold events now trigger the original bonus cue; capped/eliminated zero-gain events do not falsely celebrate a life. Continue uses the original join cue. A spectator export check uncovered an image-save exception; pygame image I/O errors now leave play running with a visible message. Native test feed paths were also separated by platform to avoid two test writers sharing one file. The corrected game/viewer pairs passed on both systems.

Final source-frozen verification:238 tests passed on Windows and Ubuntu/WSLg; extracted-ZIP verification is recorded separately. Twelve complete automated matches reconcile score accounts and human rankings. Native1/2/8 checks cover every map on both systems; native final-life/countdown/accept/expiry/automatic-initials sequences pass Windows and Ubuntu. Three80-second1280x720/60fps AAC recordings fully decode:48seconds of four-map gameplay plus two16-second clearly labelled controlled continue scenarios. All actors are automated;1/2/8 logical human stations have7/6/0 AI opponents. Twenty-one decoded frames cover all maps and continue states. GIF previews show24seconds of map gameplay. No physical controllers, eight-human acceptance, audible speaker assessment or standalone Linux hardware are certified.

Two-pass map/reference/mechanics reviews and targeted fix/retests are documented in revision14 audits. Exact power durations/stacking, remaining award/combo values, complete map inventory/order, paid source continuation and original AI remain unresolved. Candidate stage-during-continue evidence was specifically falsified: the new maze already existed before the source offer. No fabricated certainty or perfect-match claim is made.


## Clearer user photo — gates and wall rendering

The supplied higher-quality photo independently matches family D / Golden Rails at all visible major junctions; no new topology was needed. Added a fifth selectable luminous blue palette (`--palette 4`) independent of all four maps. New `photo_map_windows.bat` and `photo_map_linux.sh` launch that map/color in development simulation and untimed mode.

The image exposed undersized, weakly lit pockets and sparse line hatches. New independently drawn64x48 continuous double-U bays have48x10 filled lemon-yellow strips with dark diagonal slashes, pale cores and real alpha-aware glow. Upper/lower stripe directions match. The outer field corners are rounded, walls have soft halos and pale inner ink, and the house has clearly separated double contours with an open inner doorway. Source dimensions and camera bloom remain estimates; no commercial bitmap enters the game.

Normal actors now sit at the actual outside-pocket center; their dedicated bounded render pass lets them enter/leave through the mouth while protecting score/life text. AI occupancy opens its physical gate even though its human HUD remains unjoined. The enlarged bays fit a720p canvas after a5px field shift; lower HUD stays fixed and the controller/simulation footer occupies a reserved central gap. Full save-error messages use a bounded toast. Desktop score orientation remains upright, while the photo's opposite-side cabinet prompts are rotated.

Critical QA found and fixed invisible transparent-surface halos, stale spawn-center rendering, AI hatches staying shut, and a widened house inner line crossing its door. Eleven new gate checks and19 map checks cover actual pixels, soft glow, parallel borders, body fit, departure/return, all8stations/all4profiles, empty/dead/continue states, five palettes, score/life/footer clearance and the full house opening. Combined targeted24 checks passed, followed by full238-check Windows/Ubuntu runs. The final recordings and native checks were regenerated after these fixes, with Golden Rails in blue.

The static photo improves visual evidence; it does not measure original gate release timing, paid-continuation restoration or physical-controller behavior. Controllers remain deferred to production.


## Revision 15 — reference audit, uniform graphics and player contact

Fresh continuous DX footage qcO9tzgsdjo around5:00–5:05 shows C morphing into D while walls remain amber. At5:07–5:08 red enlargement accompanies red walls; by5:10/5:13 red and blue giants coexist and walls alternate their colors. The build now retains its base hue through map changes and cycles active giant colors. The1.25-second interval, station order and expiry fallback remain explicit approximations; exact commercial blending/priority is unresolved. Map morphing itself is still not implemented: our stage changes/reset policy remains different.

Native-resolution cardinal outlining made curved wall strokes8.1–8.7% dimmer than horizontal sections. Supersampled circular outlines and a shared premultiplied material reduce the sampled mean difference to0.07–0.34% across four blue maps. Gates, house and tunnel extensions now share luminous stroke construction. Closed gate hatching has the continuous yellow upper lip from the user's photo. All11 pickup icons, eight player colors/directions/sizes, ghost states and world effects were inspected in animation/contact sheets; this does not certify identical commercial assets. Smoke now has soft animated shading and appears immediately on stationary pickup, while the retained trail remains unverified against DX.

The collision report exposed multiple-cell instantaneous shoves and a cooldown that did not prevent repeated impulses. Contact resolution now rolls back the complete group and affected followers, then takes one outward step at normal movement cadence while retaining buffered input. Radius-aware bounded corridor checks reduce visible interpenetration, including tunnels and stationary giant growth. Separate QA caught stationary recoil in the wrong direction and rollback after a later giant hit; both were corrected. This remains a discrete corridor approximation, not recovered continuous DX physics.

HUD scores now show their actual digits, removing the invented six-digit leading-zero padding absent in the user's photo (1760/9460/13530). Existing gate clearance and long-score fitting remain tested. Desktop orientation and the remaining typography/life indicators are still different or unresolved.

Full final source: 271 checks pass on Windows and Ubuntu/WSLg. These include all1–8 rosters/maps and11power categories; no physical-controller certification. A natural continuation replay fixture needed seed0 because the former seed1 survives the60-second window under corrected contact rules; its continuation, score and replay assertions are unchanged. Native1/2/8 runs cover every map; regenerated actual automated gameplay videos include labelled continue scenarios. Source/package tests and decoded media are recorded in current reports.

The full current comparison is DX_CURRENT_GAP_AUDIT.md. All11 categories exist, but numerical power rules, global ghost vulnerability, blanket giant immunity, ghost AI/count/order, attack/combo scoring, spawn distribution, map catalog/progression, paid continuation and several graphical states remain unverified. Agent approval covers stated test scopes only. Controllers remain deferred to production. No exact-match claim.


## Revision 16 — exterior spacing and continuous maze changes

The user's annotated image exposed a real mismatch: exterior wall cores were3px apart while bay cores were6px apart. The exterior now has the same6px separation, concentric corner curves, aligned gate shoulders and continuous tunnel joins. A second review found and fixed lower gates being dimmer due to inconsistent supersampling phase. All four maps/five palettes/eight station joins were checked, with unchanged public lanes and body clearance.

Two fresh passes through Harold Zheng's DX footage (qcO9tzgsdjo,5:02–5:04) show actors staying on the field, maze compression/change, temporary enlargement of both players and ghosts, and scattered dot refill. The game now preserves actors across stage changes instead of resetting everybody to bays/house. Legal actor and item positions are reserved before displaced objects get the nearest free lane. Ghost release/return/carrier state, scores, lives, ongoing effects and continue timers persist. Exact relocation and power persistence remain our stated policy, not recovered source rules. The initial/new-match reset is unchanged.

An original1.1-second shrink/blend/expand animation replaces the instant layout swap. Actor enlargement is visual only; it never changes combat size or grants a power. Dots refill visibly and become collectible together between0.6 and1.1 seconds, with no accidental second stage-clear during refill. HUD scores stay stationary and pause/help/results freeze the animation. The0.90 maze scale,1.35 actor pulse, short midpoint overlap, timing and trajectories remain approximations; source footage does not establish an exact curve or whether movement pauses.

The deeper transition review caught a moving item stealing an already-valid static pellet position; the reservation fix is covered by a regression. Legacy tests that required a global respawn were updated to require continuous legal placement. The independent transition tests cover all16 ordered map changes, eight-player conflicts, private bays, inactive stations, continuation, carried/returning/releasing ghosts, refill and render immutability.

All288 checks pass on Windows and Ubuntu/WSLg. Native checks cover1/2/8 on all four maps (24 cases), plus actual transition runs for those counts on both systems (six cases). Twelve complete simulated matches reconcile scoring/rankings, and a720-frame472-event replay verifies deterministically. Audio initialized; physical input and audibility are not certified. Initial geometry construction still causes a first-use render delay; short native startup-inclusive figures are not steady-state performance claims.

Three new88-second1280x720/60fps recordings contain48seconds of all-map gameplay, an8-second labelled controlled C-to-D transition, and32seconds of labelled continue acceptance/expiry. All actors are automated;1/2/8 human-designated stations have7/6/0AI. Fresh24-second GIF map tours, all11-power/player/ghost animation sheets and actual transition frame sequences accompany review.

The source clearly shows a3000 popup associated with this transition; its universal award/recipient/scaling rules remain unknown, so the configurable500 simulation clear award is not promoted as authentic. All11 power categories are present and tested internally, but exact durations/spawn rates/stacking, global ghost vulnerability, ghost targeting/release and several source artwork details remain unresolved. Original sprites/audio/branding are retained. Controllers remain deferred to production; no perfect-match or zero-issue claim.
