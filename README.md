# Neon Nibblers — local arcade maze battle

A playable 1–8 player Windows/Linux Python game, inspired by PAC-MAN Battle Royale CHOMPionship Deluxe. Independently authored code, procedural artwork, sounds and branding; no commercial sprites, logos, ROMs or source code are included. Maze routes, scoring, timings and several power effects are custom. This is an adaptation, not a certified identical reproduction.

## Install and run

Requires Python 3.10+ (64-bit recommended), a graphical desktop, and internet for the initial dependency installation. Python 3.14.2 / pygame-ce 2.5.8 were tested on Windows. Python and pygame-ce are not bundled in the ZIP.

**Windows:** extract the entire ZIP. Install Python with its `py` launcher enabled. Double-click `run_windows.bat`. It creates `.venv`, installs pygame-ce and launches the lobby. Double-click `watch_windows.bat` to watch eight computer-controlled players instead.

**Linux:** install Python 3, pip and venv through your distribution's package manager, extract the ZIP, and run `sh run_linux.sh` in its folder. Debian/Ubuntu may require `python3-venv`. SDL-compatible display/audio drivers are needed. Linux hardware has not been tested here.

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

Three separate silent 12-second recordings are included:

- `gameplay_1_player.gif`
- `gameplay_2_player.gif`
- `gameplay_8_player.gif`

`gameplay_preview.gif` duplicates the eight-player clip. `gameplay.gif` is a 72-second montage: 1, 2, 8 players on Golden Junction, then Violet Switchback, Ember Crossroads and Cyan Circuit, six seconds per scenario. `arena_checks.png` shows all twelve map/player-count views.

## Controls

Lobby: **1–8** chooses player count, **Tab** changes the starting arena, **Enter** or controller button 1 starts. Select the number of actual players; unoccupied selected player slots remain stationary in human-controlled mode.

During play: **P** pauses, **F1** opens/closes the power guide and pauses play, **F2** toggles sound, **Esc** returns to the lobby. At match end, Enter/button 1 restarts. Esc from the lobby exits. Resizing preserves the 16:9 image with black bars when necessary.

USB controllers map to P1–P8 in connection order. Use the main stick (axes 0/1) or D-pad hat; dead zone 0.35. Movement continues until a wall or buffered turn, like an arcade joystick game. Plug controllers in before starting. Hot-plug is supported, but removing one can shift later assignments; return to the lobby to check. D-pads exposed only as buttons may need OS-level remapping. No buttons are required during play.

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

Start with 3 lives. Highest score after 180 seconds wins; ties share victory. A match ends early if everyone loses all lives. An eliminated player can still win on points.

- Dot: 10 points. Power: 75 points.
- Eat a foe while powered: 200 points (400 with Lure stacked).
- Eat a vulnerable rival using Titan: 300 points.
- Clear all dots: 500 points to survivors and move to the next arena, retaining scores, lives and remaining match time.

Four visually distinct arena variants cycle from the selected starting map. The new scene is 1280×720, with rounded neon walls derived from the movement graph, single-lane dot trails, wrap tunnels, a central foe bay, functional border player gates, shaded directional munchers, animated domed foes, moving collectible icons and floating score bursts.

Four foes chase players, with random wandering and retreat from hunters. Regular players can overlap without damage. Crown hunts foes; Titan also eats rivals. Respawning grants three seconds of safety. Equal Titan powers cannot eat each other.

| Name / icon | Effect |
|---|---|
| Crown / gold orb | Eat foes for 7 seconds |
| Titan / green orb | Giant, slower hunter; eat foes/rivals and block damage for 7 seconds |
| Rush / drink can | Faster movement for 7 seconds |
| Mist / smoke bomb | Foes ignore you for 7 seconds; contact still hurts |
| Slick / peel | Leave a 10-second trap; the next rival touching it is stunned 1.5 seconds |
| Spark / bolt | Stun rivals and foes for 2 seconds |
| Veil / sheet | Ignore combat damage for 7 seconds; translucent appearance |
| Flare / pepper | Hit rivals and foes within Manhattan distance 4, including through walls |
| Quake / seismic pulse | Stun rivals for 2 seconds and relocate foes |
| Heart / 1UP badge | Gain one life, maximum 5 |
| Lure / magnet | Attract foes for 7 seconds; combine with a hunter for bonus foe points |

Powers can stack; collecting the same one refreshes its timer. Damage clears powers. Titan, Veil and respawn safety block damage. Arena changes clear temporary powers and traps. Orbs begin at fixed anchors; other powers roam through corridors. Random powers spawn every three seconds, up to twelve on the field. Scores are per-match and are not saved. Sound is synthesized locally and gracefully disabled if audio initialization fails. There is no network play.

## Verification

Run `python test_smoke.py` after installing requirements. It uses dummy SDL display/audio drivers. The current **16 tests pass**, covering:

- Complete simulated matches for 1/2/8 players on all four maps (12 cases).
- Random movement for 1/2/4/8 players on all maps (16 cases).
- Map reachability, wall blocking, tunnels and roaming collectibles.
- Every movement edge sampled against rendered pixels on all four maps; single-lane graph and no unintended dead ends.
- All eight gate launches, return trips, respawns and owner-only access across all four maps.
- All eleven powers, scoring, respawn safety, elimination and time-out.
- Every ordered attacker/victim pair for 2/8 players across maps, including crossing paths.
- Eight successive arena transitions with score/life/time checks.
- Menu/start/pause/rematch and keyboard events; simulated eight-stick assignment.
- Lobby/help/pause/end rendering and aspect-ratio preservation on resize.

Revision 4 removes the separate invisible movement grid. Walls, corridor dots and movement now share one graph. There are no two-by-two open navigation squares or unintended corridor dead ends. Each player starts inside their own bay and enters after a short 0.8-second release. Their gate opens on approach; they can return through it. Rivals, foes and moving powers cannot enter another player's bay. Respawn uses the same bay/release flow. These timings/access rules are our implementation, not verified exact commercial behavior.

**Native Windows runs:** 900 rendered frames each for 1, 2 and 8 computer-controlled players, approximately 60 FPS in each run. See `NATIVE_TEST_RESULTS.json` and `TEST_RESULTS.txt`. The updated native eight-player window was visually inspected during active play. The recordings show all three counts. Native one/two-player runs were measured but not separately inspected through the desktop screenshot tool in this revision.

Functional tests do not establish identical commercial mechanics, visual identity, human play balance, audible sound quality, Linux hardware behavior or physical controller compatibility. Desktop automation's injected keys did not visibly operate the native game; direct game-event keyboard checks passed.

To regenerate visual captures, additionally install Pillow (`python -m pip install Pillow`) and run `python record_demo.py --players 1`, `--players 2`, or `--players 8`. `python record_demo.py` generates the full montage; `python visual_check.py` generates the contact sheet. Pillow is unnecessary for playing. For a short app check: `python game.py --players 8 --frames 120`.

## Visual references and source

The visual revision was compared against [active CHOMPionship gameplay](https://www.youtube.com/watch?v=GhSV1oQVA6g&t=57s), [Deluxe cabinet footage](https://www.youtube.com/watch?v=-cNOhumVZ74&t=49s), and a clearer [front-facing CHOMPionship playfield](https://www.youtube.com/watch?v=JSp72DKyW5U&t=91s). The last reference is the mobile/projector presentation; its surrounding interface is not assumed identical to the Deluxe cabinet.

Source files: `game.py` (rules, controls and flow), `arcade_art.py` (new procedural artwork), `test_smoke.py` (checks). pygame-ce is distributed separately under its own license. No commercial art/code was extracted. Remaining deliberate differences include authored maze routes, branding, several power effects, timing and scoring. This ZIP is runnable source, not a standalone executable.
