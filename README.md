# Neon Nibblers — local arcade maze battle

A playable 1–8 player Windows/Linux Python game, inspired by PAC-MAN Battle Royale CHOMPionship Deluxe. Independently authored code, procedural artwork, sounds and branding; no commercial sprites, logos, ROMs or source code are included. Maze routes, scoring, timings and several power effects are custom. This is an adaptation, not a certified identical reproduction.

## Install and run

Requires Python 3.10+ (64-bit recommended), a graphical desktop, and internet for the initial dependency installation. Python 3.14.2 / pygame-ce 2.5.8 were tested on Windows. Python and pygame-ce are not bundled in the ZIP.

**Windows:** extract the entire ZIP. Install Python with its `py` launcher enabled. Double-click `run_windows.bat`. It creates `.venv`, installs pygame-ce and launches the lobby. Double-click `watch_windows.bat` to watch eight computer-controlled players instead.

**Linux:** install Python 3, pip and venv through your distribution's package manager, extract the ZIP, and run `sh run_linux.sh` in its folder. Debian/Ubuntu may require `python3-venv`. SDL-compatible display/audio drivers are needed. Ubuntu under WSLg has been tested with X11 graphics and audio initialization; standalone Linux hardware remains untested.

**Manual setup:**

```text
python -m venv .venv
```

Activate with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on Linux, then:

```text
python -m pip install -r requirements.txt
python game.py
```

After installation the game runs offline: `.venv\Scripts\python game.py` on Windows, or `.venv/bin/python game.py` on Linux. Convenience launchers check dependencies online each time.

## Watch the moving game

With the environment activated:

```text
python game.py --demo --players 1
python game.py --demo --players 2
python game.py --demo --players 8
```

On Windows, `run_windows.bat --demo --players 2` also works. On Linux, use `sh run_linux.sh --demo --players 2`. `--demo` enables computer-controlled navigation using the actual game rules. Normal launches are human-controlled. These demonstrations do not represent physical USB/controller testing.

Three separate silent 24-second all-map tours are included:

- `gameplay_1_player.gif`
- `gameplay_2_player.gif`
- `gameplay_8_player.gif`

`gameplay_preview.gif` duplicates the eight-player clip. `gameplay.gif` is a 72-second montage: 1, 2, 8 players on Golden Junction, then Violet Switchback, Ember Crossroads and Cyan Circuit, six seconds per scenario. `arena_checks.png` shows all twelve map/player-count views.

## Controls

Lobby: **1–8** chooses player count, **Tab** changes the starting arena, **Enter** starts the quick-play preset. Select the number of actual players; unoccupied selected player slots remain stationary in human-controlled mode.

During play: **P** pauses, **F1** opens/closes the power guide and pauses play, **F2** toggles sound, **Esc** returns to the lobby. At match end, Enter restarts the preset; a station Start begins a new session for that station. Esc from the lobby exits. Resizing preserves the 16:9 image with black bars when necessary.

**Independent stations:** F3 through F10 are Start/Find for P1 through P8. Controller button 1 starts only its assigned station. An unused station can join active play; a living joined player gets a two-second locator ring, arrow and player number. Eliminated players cannot buy a free life by pressing Start. Pause/guide blocks joining and freezes the locator. These joining windows and locator timing are configurable adaptation choices: the DX Start/Find button is documented, but its detailed behavior is not yet measured.

**Controller ownership:** connected controllers initially occupy free station slots. Unplugging one never shifts another controller's station. A unique model GUID can reclaim its reserved station; identical models are ambiguous and require explicit pairing. In the lobby press **Shift+F3..F10**, then the desired controller's button 1 to assign that station. An occupied station cannot be stolen; move its controller to a free station first. Assignments last for this app session, not across launches. USB enumeration is not a persistent physical identity. Production warnings check coverage of joined stations, not just total device count.

Use the main stick (axes0/1) or D-pad hat; dead zone0.35. Movement continues until a wall or buffered turn. D-pads exposed only as buttons may need OS-level remapping.

| Player/color | Up | Left | Down | Right |
|---|---|---|---|---|
| 1 yellow | Up arrow | Left arrow | Down arrow | Right arrow |
| 2 pink | W | A | S | D |
| 3 cyan | I | J | K | L |
| 4 red | Numpad 8 | Numpad 4 | Numpad 2 | Numpad 6 |
| 5 green | T | F | G | H |
| 6 orange | E | X | C | V |
| 7 purple | Y | B | M | N |
| 8 blue | 8 | 4 | 5 | 6 |

Keyboards can block many simultaneous keys (ghosting); eight USB controllers are preferable for full multiplayer. Numpad behavior depends on Num Lock. Physical USB devices and eight simultaneous human players remain untested.

## Game rules

Three starting lives; one score bonus life at 10,000, and Extra Life pickups (cap 5). Highest score after 180 seconds wins; the match ends early if everyone is eliminated. The timed score-attack format, scores, durations and interaction ranges are adaptation choices, not verified commercial values.

Dots give 10 points; pickups 75; foes 200; biting/burning a rival or hitting them with a carried ghost gives 300. Clearing dots awards 500 to survivors and advances through four themed maps, retaining lives, score and time. Scores are not persisted.

Walls, navigation and dots share one corridor graph. Thin rounded outlines, two side tunnels, double border contours and gated player bays replace the earlier wide/open-looking areas. Station order follows the manufacturer control-panel diagram: top 4/8/7/3, bottom 1/5/6/2. Each owner can enter their own bay; start/respawn releases them after 0.8 seconds. Gate ownership, voluntary return and release timing remain custom/unverified.

Four ghosts begin inside the central house and move through its doorway in sequence. Eaten ghosts return as eyes, enter through the door, reform and leave again. The exact starting arrangement and release delays are not recovered commercial settings. Normal/equal-size players bump apart; giant players can eat smaller rivals. Exact bump displacement and cooldown are custom. Respawn safety prevents damage for 3 seconds but does not prevent collecting powers or eating ghosts.

| Display name / internal key | Implemented effect |
|---|---|
| Gold Orb / Crown | Eat ghosts for 7 seconds; does not eat rivals |
| Giant Orb / Titan | Grow and eat ghosts/smaller rivals for 7 seconds; physical damage immunity |
| Caffeine / Rush | Faster movement for 7 seconds |
| Smoke Bomb / Mist | Leave a smoke trail for 7 seconds; each cloud lasts 2.5 seconds and slows nearby ghosts |
| Banana Peel / Slick | Skid quickly without turn control for 2 seconds |
| Lightning / Spark | Zap nearby rivals/ghosts, stunning them for 2 seconds; radius 8 cells |
| Ghost Sheet / Veil | Hide from ghost targeting for 7 seconds; does not protect from rival attacks or incidental ghost contact |
| Chili Pepper / Flare | Breathe fire up to 5 corridor cells ahead for 3 seconds, stopped by walls |
| Earthquake / Quake | Slow everyone, including collector and ghosts, for 5 seconds |
| Extra Life / Heart | Gain one life, up to 5 |
| Ghost Magnet / Lure | Capture contacted ghosts and carry them ahead as weapons for 7 seconds; expired/dead-owner weapons cannot attack |

The basic power categories are supported by published CHOMPionship descriptions. Exact duration, range, immunity, stacking, lightning stun-versus-kill, flame shape, sheet contact behavior and magnet release behavior are **not** verified. Those are explicit implementation choices. Powers can stack; identical powers refresh. Damage clears effects. Expired captured ghosts return home harmlessly as eyes.

Spawning remains configurable custom tuning: four gold corner anchors, two green central anchors, three other initial pickups; a new random pickup every 3 seconds, cap 12. Non-orb items roam every 0.24 seconds. `SPAWN_INTERVAL`, `MAX_ITEMS` and `ITEM_STEP_INTERVAL` are in game.py. Exact commercial locations/probabilities/frequency are unknown. Arena transitions reset spawn/movement clocks. Foes and pickups never enter player bays.

## Verification and ongoing QA

Run `python -m unittest discover -p "test*.py" -v` to include all suites; `test_smoke.py` alone runs the original29 checks. The revision-8 headless suite covers 110 tests, including complete 1/2/8-player simulations on four maps, all 11 powers, combat/crossings, bumping, ghost house departure/continuous return, carried-ghost expiry/death, smoke/skid/speed/quake, gate launch/return/respawn, one-line corridors, every movement edge against wall pixels, tunnels, arena transitions, menu/pause/rematch, resize and simulated eight-controller assignment.

Ten topic agents reviewed player interactions, gates, inventory, effects, spawn policy, edges, walls, ghost starts, ghost exits and player/ghost/power interactions. Review findings distinguish code defects from unverified reference details. Follow-up QA findings are retained under docs/audits in the repository. No review consensus is a substitute for evidence of visual/mechanical identity.

Native Windows autoplay runs render 1,800 frames per count. See NATIVE_TEST_RESULTS.json and TEST_RESULTS.txt. Recordings are actual computer-controlled game runs. Ubuntu/WSLg native graphics and audio initialization passed 1/2/8-player runs. Physical USB controllers, eight humans, standalone Linux hardware and audible sound quality remain unverified. Desktop-injected keys were inconclusive; direct game-event keyboard checks pass.

For captures, install Pillow and run `python record_demo.py --players 1` (or 2/8); `python record_demo.py` records all maps; `python visual_check.py` makes a contact sheet. Captures are generated deliverables, not committed to source history. Pillow is unnecessary for playing.

## Visual references and source

The visual revision was compared against [active CHOMPionship gameplay](https://www.youtube.com/watch?v=GhSV1oQVA6g&t=57s), [Deluxe cabinet footage](https://www.youtube.com/watch?v=-cNOhumVZ74&t=49s), and a clearer [front-facing CHOMPionship playfield](https://www.youtube.com/watch?v=JSp72DKyW5U&t=91s). The last reference is the mobile/projector presentation; its surrounding interface is not assumed identical to the Deluxe cabinet.

Source files: `game.py` (rules, controls and flow), `arcade_art.py` (new procedural artwork), `test_smoke.py` (checks). pygame-ce is distributed separately under its own license. No commercial art/code was extracted. Remaining deliberate differences include authored maze routes, branding, several power effects, timing and scoring. This ZIP is runnable source, not a standalone executable.

## Development

Repository: https://github.com/911cr/neon-nibblers . The revision-4 tag preserves the imported baseline; later commits track fixes. GitHub Actions runs smoke checks on Windows and Linux. Open issues record unresolved reference fidelity and hardware testing.

## Controller verification

Run `python check_controllers.py --expected 8` after connecting controllers. Move each stick/D-pad in all four directions and press a button; Escape saves `controller_check_results.json`. For fewer devices set `--expected` to the connected count. The report records observed input and hotplug events; zero devices can never pass. This is an input check, not proof of eight-person gameplay. Current local discovery found zero controllers, so physical verification is pending connected hardware.

## Additional Linux evidence

`LINUX_NATIVE_TEST_RESULTS.json` records real local Ubuntu with Python3.12/pygame-ce2.5.8 runs using X11 through WSLg, with audio initialized at44.1kHz stereo. 1/2/8-player runs each rendered1800frames; observed averages52.85/38.16/59.72FPS. These are samples under concurrent desktop load, not a guaranteed framerate. Hardware audibility still needs a listener to confirm.

## Development controller stub versus production detection

For development now, launch `dev_windows.bat` or `sh dev_linux.sh`. These enable `--simulate-controllers`: the availability check assumes enough controllers for the selected1–8players and displays **DEV ... SIMULATED**. It does not invent device input: use the keyboard or add `--demo` for computer-controlled gameplay. For example: `dev_windows.bat --demo --players 8`.

Normal `run_windows.bat` / `run_linux.sh` launches use real device detection. Missing controllers produce a persistent warning in the lobby and gameplay footer; a disconnect triggers a five-second notice, followed by any remaining missing-controller warning. Keyboard fallback remains available. Physical controller compatibility is deferred to production verification by user direction; simulated availability is not recorded as physical testing. `check_controllers.py` always observes real devices independently of this development option.


## Revision 8: evidence, stations and replay

The four arenas now have explicit versioned geometry in `maps.json`. Their routes are unchanged from revision7 and still authored, not recovered DX layouts. Each can be edited independently. `map_library.py` rejects disconnected paths, undeclared exits and multiple dot lanes. Default dot-clear transitions remain custom; `--progression cycle`, `repeat` or `random` selects an explicit policy.

Every scoring event records simulation time, tick, player, stage, points, resulting score and context. The HUD and score popups use those events; tied scores receive equal ranks in the new results table. `score_ledger.py` centralizes the still-unverified10/75/200/300/500 values. There is no claim those match DX.

```text
python game.py --demo --players 8 --seed 42 --event-log match-events.json
python game.py --locator-seconds 2 --progression repeat
python replay.py record replay.json --players 8 --seconds 20 --seed 42
python replay.py verify replay.json
python replay.py verify replay_sample.json
```

Replay checks input commands, state fingerprints, score events and movement traces. It covers simulation joins/movement; it is not a recording of physical controllers or every UI action. Native play advances logic at60Hz independently of rendering; animation interpolation follows elapsed render time. A pre-existing autoplay bug that silently removed the current dot without scoring was fixed.

`docs/DX_FEATURE_PARITY.md` separates verified DX facts, observed footage, historical-only rules, unknowns and implemented tests. The six companion DX documents record history, references, maps, scoring, visuals and verification. No complete commercial map reconstruction or aligned full-field comparison is claimed. A separate research-only house crop comparison was made from released DX footage at2:00; it is not bundled as a game asset. `station_before_after_r8.png` compares our previous and current builds, not commercial footage. Separate1/2/4/8-player clips show actual computer-controlled gameplay; a locator is triggered during the1/2/8 clips.

The formal application states are attract/lobby, playing, paused, guide and results (`stations.Phase`). The state table and remaining gaps are in `docs/DX_TEST_REPORT.md`. Credits, persistent high scores, a full animated attract demonstration, layered audio and a separate spectator-display mode remain unfinished. The existing three synthesized sounds and single-monitor mode remain usable.


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
