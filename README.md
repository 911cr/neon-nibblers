# Neon Nibblers

Original-code Windows/Linux local arcade maze battle inspired by PAC-MAN Battle Royale CHOMPionship Deluxe. Up to eight human stations, USB joystick/gamepad support, keyboard fallback and AI opponents. Commercial sprites, recordings, logos, ROMs and source code are not included.

Revision 13 uses two independently reconstructed observed DX layouts, offered as four color profiles, with rounded wall ends and preserved narrow passages. It adds AI vacancy filling, lifecycle animation, operator settings, local high scores, credits and spectator windows. Exact commercial scoring, timing, AI difficulty, joining rules and the complete DX map inventory remain unverified. This is an independent adaptation, not a certified exact reproduction.

## Install and play

Requires Python 3.10+ and a graphical desktop. Python and pygame-ce are not bundled.

- Windows: extract the entire ZIP, install Python with the `py` launcher, and double-click `dev_windows.bat` for current development. It creates a virtual environment and installs pygame-ce.
- Linux: install Python 3, pip and venv, extract the ZIP, then run `sh dev_linux.sh`. Debian/Ubuntu may need `python3-venv`.
- Normal `run_windows.bat` / `sh run_linux.sh` use real controller detection. Development launchers visibly label assumed availability SIMULATED. Neither invents physical input.

Manual setup: `python -m venv .venv`, activate it, then `python -m pip install -r requirements.txt` and `python game.py`. After installation, offline play is supported. Convenience launchers check dependencies online.

## Stations and controls

F3–F10 are the independent Start/Find actions for P1–P8. Controller button 1 acts at its assigned station. An unjoined station can replace its AI; a living human gets a locator highlight. Eliminated humans cannot obtain a free life by joining again. Immediate takeover, highlight duration and joining windows are explicitly adaptation rules.

Enter starts the selected quick-play roster; keys 1–8 choose its human count in the lobby. Tab selects a starting visual profile. Default AI fill adds seven opponents for one human, six for two, and none for eight. Bots are marked AI, do not receive human input, require no controller, do not occupy human score/ranking slots and cannot prolong play after all humans are eliminated. F11 can disable AI fill. `--demo` steers every actor for demonstrations; videos are automated gameplay, not human/controller acceptance.

| Station | Color | Movement |
|---|---|---|
| P1 | Yellow | Arrow keys |
| P2 | Pink | WASD |
| P3 | Cyan | IJKL |
| P4 | Red | Numpad 8246 |
| P5 | Green | TFGH |
| P6 | Orange | EXCV |
| P7 | Purple | YBNM |
| P8 | Blue |8456 |

P pauses. F1 opens the power guide and freezes gameplay. F2 mutes immediately. F12 cycles wall colors independently of maze geometry. Escape returns to lobby or exits; from guide/operator it closes that panel. Resizing preserves aspect ratio.

USB directions use axes 0/1 or a D-pad hat, deadzone 0.35. Removing a device never renumbers surviving stations. Unique model GUIDs can reclaim a reserved station; indistinguishable controllers require manual pairing. In the lobby press Shift+F3..F10 then the desired controller's button 1. Occupied live stations cannot be stolen. Bindings are session-local. Missing-controller warnings check the joined human stations, not raw device count. Physical input/latency/mixed-device testing remains for production.

## Operator, credits and scores

F11 in the lobby/results opens original operator controls: starting lives, bonus threshold, match duration, free play, attract sound and AI fill. Up/Down select, Left/Right change, Enter saves, Escape cancels. Changes apply to the next match. Default 3 lives and 10,000 bonus are supported manual examples; exact repeat policy and other durations are our choices.

Default free play needs no credits. With it off, C in the lobby inserts a software credit and each new human station costs one. Find and bot replacement cannot grant free lives to an already joined eliminated human. No real payment hardware is integrated. Failed saves do not debit credits.

H shows the local high-score table. Completed human results are stored once per session, ranked with ties and recorded as P1..P8. On results, N opens optional three-letter initials for qualifying saved rows; type A-Z, use arrows/Backspace, Enter to save each, Escape to cancel the current draft. Names are keyboard-entry in this build; controller acceptance stays in production. Failed score writes remain queued in memory for retry even after leaving results; unsaved data cannot survive closing the program while storage remains unavailable. Corrupt data falls back to defaults with a status message.

Data: `%LOCALAPPDATA%/NeonNibblers` on Windows; `$XDG_DATA_HOME/neon-nibblers` or `~/.local/share/neon-nibblers` on Linux. Override with `--data-dir PATH` or `NEON_NIBBLERS_DATA`. Tests use isolated workspace profiles.

After 12 idle seconds, the original attract sequence cycles power-up instructions and saved scores. Any input returns to the lobby. Attract sound is configurable. This is not extracted commercial attract artwork or a measured copy of its timing.

## Maps, rules and animation

Golden Archway and Cyan Archway share observed layout A; Violet Crosscurrent and Ember Crosscurrent share observed layout B. Both were reconstructed from full DX spectator-screen views at 68/73 seconds in the IAAPA2022 reference. Four profiles do not mean four recovered commercial topologies. Quantization, hidden endpoints, wall widths/rounding and dot placement retain documented approximations. Old unsupported routes remain only in Git history.

Every map supplies its own house, doorway, homes, tunnels, bays and corridor radius. Navigation, dots and wall rendering share a graph. Default dot-clear/profile cycling and 3-minute score attack remain adaptation rules. Humans retain score/lives through transitions; positions/effects reset. Bonus lives are once per human/bot at the configured threshold;0 disables the score bonus. Life cap 5 is custom.

Points remain configurable simulation defaults: dots 10, pickups 75, ghosts 200, rival attacks 300, surviving a dot-clear stage 500. Visible DX800/1600 bursts have not been isolated enough to recover their exact cause or multiplier. `score_ledger.py` centralizes event values; every award carries player/time/stage/context and resulting score. HUD popups consume those same events.

| Power | Implemented behavior |
|---|---|
| Gold Orb | Eat ghosts for 7 s |
| Giant Orb | Grow, eat smaller rivals/ghosts, physical damage immunity for 7 s |
| Caffeine | Faster movement for 7 s |
| Smoke Bomb | Trail slows nearby ghosts |
| Banana Peel | Uncontrolled quick skid for 2 s |
| Lightning | Nearby ghost/human/AI stun for 2 s |
| Ghost Sheet | Ghost targeting invisibility for 7 s; incidental contact still dangerous |
| Chili Pepper |3 s fire along up to 5 reachable corridor cells, stopped by walls and split at tunnels |
| Earthquake | Slow everyone for 5 s |
| Extra Life | Gain one life, cap 5 |
| Ghost Magnet | Carry contacted ghosts as weapons for 7 s |

The 11 categories are documented; ranges, durations, stacking, protection and expiration details are still approximations. Pickup contact works for moving, stationary and stunned actors. Repeated powers refresh; damage clears them. New item cadence 3 s/cap 12, orb anchors and other-item roaming 0.24 s are custom settings. Ghost house release/AI and normal/equal-giant bumps are not measured exact DX rules.

Original growth/shrink tweens, death dissolve at the previous position and bay arrival pulses are presentation-only. They never delay physics or alter scoring. Pause/guide/results freeze world animation. Lighting stays fixed when facing changes; collectible icons are supersampled and cached. Render interpolation, timer boundaries, simultaneous lightning and bot takeover have regressions.

## Spectator displays

Start the game with a local feed:

```text
python game.py --spectator-state live/state.json
python spectator.py --state live/state.json
```

Run the second command in another terminal. Move the spectator window to another monitor; launch it twice for two spectator displays. No network service is needed. `--mode game` mirrors the playfield; `--mode scores` uses an independent original ranking view; default `auto` mirrors active play and shows rankings otherwise. It detects stale/malformed feeds and safely falls back. Exact DX overhead content by state is not established; these modes are configurable adaptations. Actual game/viewer pairs were tested on Windows and Ubuntu/WSLg.

## Verification and recordings

Run `python -m unittest discover -p "test*.py" -v`. Revision 13 has 187 checks, including 1–8 human rosters across every profile, bots/takeover, powers, continuous ghost return, all visible route edges, collisions, replay, credits/storage failures, spectator feeds, lifecycle animation, HUD/tunnel clipping and 720/1080 resizing. Twelve complete automated matches validate event totals and human rankings. Native graphics checks cover 1/2/8 on all profiles on Windows and Ubuntu/WSLg; standalone Linux hardware and audible speaker quality remain unconfirmed.

The three MP4s are 48-second 1280 x 720/60 fps tours with original event audio, one for each 1/2/8 human-station setup. AI fills vacant stations; all actors are computer-controlled during capture. Each tour visits four palette profiles of two layouts. GIFs are silent 12 fps previews. They do not assert the commercial game uses this sequence.

Optional capture tools: `python -m pip install -r requirements-capture.txt`, then `python record_video.py --players 1 --seconds 6` or `python record_demo.py --players 1 --tour --seconds 6 --simulate-controllers`. Optional video encoding was tested on Windows.

Replay and configuration examples:

```text
python game.py --demo --players 1 --arena 3 --seed 42 --event-log events.json
python replay.py record replay.json --players 1 --fill-bots --theme 3 --seconds 20 --seed 42
python replay.py verify replay.json
python replay.py verify replay_sample.json
python check_controllers.py --expected 8
```

Physical controllers are explicitly deferred to production; simulation never counts as physical testing. See docs/DX_RELEASE_STATUS.md and the evidence/audit files for the remaining reference uncertainties. Repository: https://github.com/911cr/neon-nibblers .


## Revision 13 options and evidence

Run `python game.py --untimed` to play until all human lives are exhausted. F11 also permits time limit0; the CLI option affects only the current application run. A fixed180-second limit remains a custom selectable mode. Fresh DX footage supports investigating life-survival and shows a continue interval/name entry, but exact paid-continuation and multiplayer termination rules remain unknown. Our immediate results and optional keyboard initials are documented adaptations.

`python game.py --tuning tuning.example.json` loads partial overrides for power durations, player/ghost/item movement intervals, effect ranges, smoke/quake multipliers, spawn cadence and item cap. The included file lists all current approximate defaults. Invalid/unknown/nonfinite values are rejected. Use `python replay.py record tuned.json --players 1 --fill-bots --tuning tuning.example.json`. Replays and match-start events store the complete effective settings. Recorded pickup expiry is the nominal deadline; refresh, damage or a stage transition may end/replace the effect.

Four ordinary dots producing+40 in fresh footage supports the existing10-point dot value. Other point values and power durations were not changed on ambiguous evidence. Independent AI now avoids lethal routes when alternatives exist; its target costs are original choices.

The ZIP contains current source, launchers, tests, documentation and the three current HD gameplay videos. Larger GIF previews and historical revision captures are provided alongside downloads or retained in the workspace/history. Research screenshots/comparisons of the commercial reference are separate and are not playable game assets.
