# Revision 5 review and QA status

Ten separate topic agents completed an initial research audit, then the same agents performed two QA passes. Reproducible failures were fixed and the relevant agents rechecked them. No agent certified a perfect commercial match. Final targeted reviews report no remaining reproduced blocking failures in their scopes; reference uncertainties remain open.

| Topic | QA outcome / fixes |
|---|---|
| Player interactions | Fixed head-on crossing, cooldown overlaps, eight-player crowds and delayed bonus life; targeted recheck passed |
| Gates | Twin contours, hatch alignment and crossing state; stale stun/clock cleared; 32 gate scenarios passed |
| Power inventory | All11 categories/icons/labels/guide rows checked; stale descriptions corrected |
| Power effects | 14 focused runtime cases plus slowdown/stacking checks passed; unsupported exact ranges/timings remain open |
| Power placement/cadence | 16 scenario groups and4400 occupied-cell-safe spawn cases; clocks reset; cadence explicitly custom |
| Edges/tunnels | 32 player seam scenarios/512frames and16 collectible scenarios/256frames; opacity/giant thresholds/HUD clipping fixed |
| Walls | All-map connectivity/visible routes and giant/corner stress renders passed; authored topology still differs |
| Ghost starts | 12 count/map configurations checked; staging/reset valid, exact original order unknown |
| Ghost exits | 16 direct cases and48 repeated lifecycle cycles; visible doorway return fixed |
| Player/ghost/powers | Eight scenario groups; expired/dead-owner weapons and safe hunter eating fixed |

The integrated headless suite passes25 tests. Native Windows1/2/8-player autoplay and regenerated recordings use the revised build. Physical USB controllers/eight humans and native Linux graphics/audio remain unverified. Linux CI is a headless software check, not hardware validation.

Detailed audit notes are in docs/audits. Some earlier sections describe old bugs and failed intermediate versions; later QA and resolution sections record the fixes. Open GitHub issues separate remaining evidence gaps from verified implementation behavior.

## Revision 6 follow-up

New promotional-poster evidence corrected coffee-mug, quake-plunger, blue-magnet, flaming-pepper, white1UP and shaded-orb artwork. The inventory reviewer checked all11 guide icons for readability/clipping and confirmed improved silhouettes. A released Deluxe video showed yellow gate hatching on cyan mazes, correcting the earlier theme-color inference; the gate reviewer verified the new four-theme pixel test.

27 tests now pass on local Windows and Ubuntu. Actual Ubuntu X11/audio-initialized1/2/8 runs completed. Physical devices detected:0; controller verification cannot pass without hardware. No agentcertifiedexactcommercialart/rules.

## Revision 7 controller acceptance scope

The user authorizes assumed controller availability during development and requires real missing/disconnect detection in production. App defaults to real detection. Dedicated development launchers pass --simulate-controllers and visibly label the assumed count. No fake input devices are created; keyboard and autoplay remain available. Production hardware validation is deferred, not falsely marked passed.

Two targeted QA passes checked zero/partial/full counts, hotplug, fallback and text layout. Fixed stale reconnect warning and added regression assertion. Current integrated suite:29 tests.


## Revision 8

Three focused agents performed research/code review followed by deeper adversarial passes and fix rechecks.63 total tests cover original rules, explicit maps, score/replay and independent stations. Found/fixed autoplay dot deletion without scoring, wrong-station controller availability, top-bay locator clipping and an intermediate three-outline house rendering mistake. The final house check counts actual visible contours. Source evidence, differences and next actions are maintained in the seven DX documents. Native Windows/WSLg1/2/8 runs completed; updated clips are actual simulated gameplay. No exact-DX or physical-hardware certification.


## Revision 9 — 2026-11-08

Fixed scores/lives/start prompts overlapping gate bounds, including giant locator clearance and long score values. Cyan Circuit map revision2 opens the continuous house perimeter and separates two nearby vertical wall sections, informed by real DX footage at75/120seconds after180-degree orientation normalization. Exact coordinates remain estimated and the full DX topology is still unresolved.

Preserved movement timer remainders and boundary precision: normal movement now10cells/s, caffeine15 and banana18 under the configured approximation, versus8/15/15 previously. Damage cues now follow damage events even when another player earns a life simultaneously. Lightning ignores inactive stations.

72 tests pass locally on Windows and Ubuntu. New native300-frame1/2/8 runs used real Windows/X11 drivers; Windows58.39/60.27/59.93FPS; UbuntuWSLg34.49/33.64/45.20FPS under concurrent capture load. Physical controllers remain deferred. Three agents performed reference/code reviews, deeper QA and rechecks. No perfect-match claim.

The separate1/2/8-player clips now show corrected Cyan Circuit,12seconds each; the montage covers allfourmaps. `hud_before_after_r9.png` and `map_before_after_r9.png` are controlled local before/after comparisons. A new reference-only figure outside the gameZIP records actual footage observations. Replay sample regenerated after timing changes.


## Revision 10 — all-map review and simultaneous interactions

Reviewed all four authored maps against retained real DX75/120second frames. The footage does not establish four complete DX layouts; a fresh viewing attempt was stopped by browser URL-verification policy. No unsupported geometry changes were made. Every map already has a continuous house perimeter; the catalog now validates those routes and door approaches. Broad wall interiors have an inset contour based on the visible rectangular-island style; application to broad L-shaped walls remains an explicit visual approximation. No floor, frame, gate or house-outline pixels changed in the comparative render QA. See audits/revision10_all_maps.md for the four-row evidence matrix.

Fixed lightning outcomes depending on station order, tiny floating-point power/safety expiration tails, roaming collectibles not collecting on stationary/stunned players, and same-tick bonus credit after that contact. Added ten original layered event cues on separate channels. Mute stops active cues immediately; unavailable audio is handled gracefully. Sounds are synthesized locally, not commercial recordings. Audible speaker quality and physical controllers remain unverified/deferred.

92 automated tests pass locally on Windows and Ubuntu. Actual native1/2/8 rendering runs now cover all four maps (12 short120-frame scenarios on each OS). These are startup/render samples, not benchmarks or human gameplay certification. The supplied1/2/8-player GIFs each show four separate seeded6-second map scenarios (24seconds total); they do not assert that the commercial game uses that stage sequence. All game GIFs are silent. sound_preview.wav demonstrates the original cues.

Source, event replay and captured gameplay were regenerated after the simulation fixes. Complete commercial geometry, exact scoring/timing/AI, stage transitions, joining windows, attract/operator and spectator behavior remain open evidence/work items. Physical controller acceptance stays in production.


## Revision 11 — animation, proportions and fresh DX reference review

Fresh real DX footage was viewed safely through normal browser navigation after using a new tab with a verified address. New60/65/124/135second research captures and the report are recorded in audits/revision11_reference.md; camera edits/glare prevent exact cycle timing and a complete commercial map catalog. Distinct house-side geometry appears with the same cyan palette. Palette selection is now independent of layout: F12 cycles wall colors during play, or use `--palette 0..3`. This changes presentation only, not match logic or routes; default progression remains our approximation.

Fixed the left-facing eye/light flip, missing individual ghost stun feedback and tunnel copies, sorted-item animation identity jumps, short respawn/stage cache slides, and animation continuing during pause/guide/results. All11 power icons now use cached3x procedural artwork and position-independent bob phase. Fire is a continuous layered animated plume with a pale core, clipped to reachable corridor endpoints and split correctly at tunnels. Lightning arcs animate. Exact DX art proportions and timing are still unverified.

110 tests cover artwork/time samples, direction, icon sizes16–96px, ghost states, HUD/tunnels, effects, pause/results, respawn, item tracking,720/1080 resizing and palette changes without logic mutation. Two agent QA passes included discovered clipping and freeze regressions followed by corrections. Native1/2/8 render samples cover every map on Windows and Ubuntu/WSLg. These are short graphics checks, not hardware or performance certification; the final plume styling is also checked by the final render suite and recordings. Physical controllers remain deferred to production.

Each1/2/8-player GIF tours four separate6-second map scenarios (24seconds,288frames). New `gameplay_1_player.mp4`, `gameplay_2_player.mp4` and `gameplay_8_player.mp4` show the same tour at1280x720/60fps with original event audio, avoiding GIF color/frame-rate limits. They are actual computer-controlled game simulations. They do not prove a commercial stage sequence or physical-input compatibility.

Optional recording tools: `python -m pip install -r requirements-capture.txt`, then `python record_video.py --players 8 --seconds 6`. They are unnecessary for playing. Native Windows encoding was tested; playback files can be viewed on Windows/Linux with an H.264/AAC player. The game remains Python/Pygame source, not a standalone executable.

See animation_contact_r11.png, animation_review_r11.gif, fire_animation_r11.png and animation_world_effects.png for tested frame sequences and sizes. The matrices document finite reviewed cases; no exhaustive or perfect-commercial-match claim is made. Full DX topology, scoring/timing/AI, death/growth transitions and operator/spectator/attract systems remain unfinished.
