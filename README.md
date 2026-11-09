# Neon Nibblers

Original-code Windows/Linux local arcade maze battle inspired by PAC-MAN Battle Royale CHOMPionship Deluxe. Up to8 human stations, USB gamepad/joystick support, keyboard fallback and AI opponents. No commercial sprites, ROMs, source code, logos or recordings are included.

Revision15 corrects wall brightness, yellow gate lips, tunnel lighting, player contact and smoke, and adds source-observed giant-related wall colors. Four observed maze reconstructions and per-station continuation remain available. This is not an exact replica: graphical details, power timing/interactions, ghost AI, map morphing/progression, remaining scoring and paid continuation still have documented differences. See docs/DX_CURRENT_GAP_AUDIT.md.

## Install and run

Requires Python3.10+ and a graphical desktop. Python/pygame are not bundled.

- Windows: extract the entire ZIP, install Python with the `py` launcher, then double-click `dev_windows.bat`.
- Linux: install Python3, pip and venv, extract, then run `sh dev_linux.sh`. Ubuntu/Debian may need `python3-venv`.
- Development launchers visibly assume controller availability as SIMULATED. They never create physical input. Normal `run_windows.bat` / `sh run_linux.sh` use real controller detection and missing/disconnect warnings.

Manual setup: `python -m venv .venv`, activate it, `python -m pip install -r requirements.txt`, then `python game.py`. Launchers create the environment/install dependencies online; offline play works after setup.

Use `dev_windows.bat --untimed` or `sh dev_linux.sh --untimed` for life-survival without a fixed timer. Default180-second score attack is an explicit adaptation option; F11 time limit0 also enables survival.

## Start, movement and controls

Enter starts the quick-play roster;1–8 select its human count in the lobby. F3–F10 independently Start/Find P1–P8. Controller button1 serves its assigned station. Unjoined stations can replace AI; living humans receive a locator highlight. Stable numbering is top4/8/7/3, bottom1/5/6/2.

| Station/color | Movement |
|---|---|
| P1 Yellow | Arrows |
| P2 Pink | WASD |
| P3 Cyan | IJKL |
| P4 Red | Numpad8246 |
| P5 Green | TFGH |
| P6 Orange | EXCV |
| P7 Purple | YBNM |
| P8 Blue |8456 |

Tab selects a starting maze in the lobby. F12 changes the base wall color. Active giants temporarily color the walls; multiple giants cycle colors every1.25 seconds (an estimated interval). Layout changes alone retain the base hue. P pauses; F1 guide freezes play; F2 mutes immediately. Escape closes guide/editor, returns to lobby or exits. Resize preserves aspect ratio.

AI fills vacant stations by default:1human+7AI,2+6,8+0. F11 can disable fill. Human input/rankings/controller requirements exclude bots. `--demo` steers every actor for demonstrations. AI routes and difficulty are independently authored.

USB uses axes0/1 or D-pad hats, deadzone0.35. Disconnects do not renumber remaining stations. Unique model GUIDs may reclaim a reservation; identical models require explicit pairing: lobby Shift+F3..F10, then that controller's button1. Physical input/latency/mixed-device acceptance remains for production.

## Final life and continue

After a human loses its last life, a custom1-second reveal delay precedes an approximately10-second continue countdown. Other humans, AI and ghosts keep playing. Press that station's Start after the prompt appears. Free play permits it; with free play off, one software credit is required. INSERT adds a development credit while an offer is active. C adds a lobby credit and remains P6 down during play.

An accepted continuation preserves score and the earned bonus flag, restores configured starting lives and releases a fresh avatar from its bay. This restoration policy is our explicit approximation: footage establishes a countdown and continuing AI, but actual paid score/life restoration was not observed. Pending/expired/paused offers and failed payments do not debit. An expired station remains out until a new match. Timed expiration overrides offers.

When the last offer expires, results save once and qualifying scores automatically open original three-letter initials. Other results use N for initials. Type A-Z, use arrows/Backspace, Enter to save each, Escape to discard the current draft. Only current-session qualifying top20 human rows are edited; ties/old entries remain safe. Failed writes roll back and allow retry. Immediate restart preserves queued score saves.

Use `--continue-seconds 0` to disable offers. `--continue-delay 1` changes the custom reveal. Raw Match/replay defaults disable offers unless explicitly configured; normal application default is10seconds.

## Operator, saved data and spectator displays

F11 in lobby/results edits starting lives, bonus threshold, time limit, free play, attract sound and AI fill. Up/Down select; Left/Right change; Enter saves; Escape cancels. Changes apply next match. Default3 lives/10000 bonus are documented manual examples; once-only bonus/life cap5 remain adaptation choices. H shows local scores. Idle12-second original instruction/high-score attraction uses configurable sound.

Data: Windows `%LOCALAPPDATA%/NeonNibblers`; Linux `$XDG_DATA_HOME/neon-nibblers` or `~/.local/share/neon-nibblers`. Override `--data-dir PATH` or `NEON_NIBBLERS_DATA`. Failed result writes retry in memory; unsaved data cannot survive closing while storage is unavailable. Corrupt data falls back to defaults with a message.

```text
python game.py --untimed --spectator-state live/state.json
python spectator.py --state live/state.json
```

Run the second command separately; move its window to another monitor. Two viewers may share a feed. Each running game should use its own feed path. Default auto mirrors active/continue play and shows rankings otherwise; `--mode game` / `--mode scores` select a view. Exact DX overhead behavior by state remains unknown.

## Mazes, points and powers

| Profile | Observed family | Public lane cells |
|---|---|---|
|0 Golden Rails | D |569|
|1 Violet Crosscurrent | B |569|
|2 Ember Courtyard | C |585|
|3 Cyan Archway | A |582|

These are independently reconstructed observed topologies with original names/palettes. Perspective, hidden endpoints and20px coordinate quantization remain estimates. Four observed families do not prove the complete catalog. Dot-clear transitions and cycle/repeat/random order remain adaptation policies, preserving scores/lives while clearing effects and repositioning actors. Default starts on Cyan.

The actual DX instruction legend in `qcO9tzgsdjo` at0:01/0:03 shows dot10, Gold100, Giant1000. These now have separate score rules. Other item75, ghost200, rival300 and stage500 remain configurable simulation estimates in `score_ledger.DEFAULT_SCORES` / Match score_values. All awards share one event ledger used by HUD/ranking/replay.

| Power | Implemented effect (durations are estimates) |
|---|---|
| Gold Orb | Eat ghosts7s;100points |
| Giant Orb | Grow/eat smaller rivals and ghosts7s;1000points |
| Caffeine | Faster movement7s |
| Smoke Bomb | Immediate cloud plus trail slows nearby ghosts7s; clouds2.5s (trail/timers approximate) |
| Banana Peel | Uncontrolled fast skid2s |
| Lightning | Nearby ghost/rival stun2s |
| Ghost Sheet | Ghost target concealment7s; incidental contact still dangerous |
| Chili Pepper |3s wall-bounded fire, up to5 corridor cells |
| Earthquake | Slow everyone5s |
| Extra Life | One life, cap5 |
| Ghost Magnet | Carry contacted ghosts as weapons7s |

`--tuning tuning.example.json` loads validated partial duration/range/speed/cadence/cap overrides. The guide shows effective durations. Defaults do not claim recovered exact timers. Repeated powers refresh; damage clears effects. Stacking, spawn frequencies/probabilities, house release and combat details retain documented approximations.

## Checks and recordings

```text
python -m unittest discover -p "test*.py" -v
python replay.py verify replay_sample.json
python replay.py record continued.json --players 1 --fill-bots --seconds 60 --continue-seconds 10 --auto-continue
python replay.py verify continued.json
python check_controllers.py --expected 8
```

271 checks cover all1–8 counts/maps,11powers, ledger/replay, AI, continuous house return, rendered routes, HUD, operator/storage failures, continuation/initials and spectator feeds. Windows and Ubuntu/WSLg native checks include1/2/8 per maze and full continue acceptance/timeout/name entry. Tests and screenshots are automated; physical controllers, eight-human acceptance, speaker audibility and standalone Linux hardware remain production checks.

Three current MP4s are80seconds each,1280x720/60fps with original AAC event audio:48seconds touring all four mazes, then two16-second labelled controlled tests of continue acceptance and expiry/initials. All actors are automated. Logical1/2/8 human stations have7/6/0AI. Controlled final-life setup is explicitly labelled, not presented as unassisted human gameplay. GIF previews are24-second silent map tours and may be provided alongside the ZIP.

Optional capture dependencies: `python -m pip install -r requirements-capture.txt`; then `python record_video.py --players 1 --seconds 12 --untimed --continue-showcase`. The ZIP includes current source/tests/docs and three HD videos; historical captures stay in workspace/history. Commercial reference comparisons are separate research artifacts.

See docs/DX_RELEASE_STATUS.md and revision15 audits for evidence boundaries. Repository: https://github.com/911cr/neon-nibblers


## Map from the clearer photo

Yes: the photo is our Golden Rails / observed family D. Double-click `photo_map_windows.bat`, or run `sh photo_map_linux.sh`, to open it in the fifth blue palette and untimed mode with the visibly labelled development controller stub. Manual equivalent: `python game.py --arena 0 --palette 4 --untimed --simulate-controllers`.

The current build has larger glowing64x48 gate pockets, filled striped48x10 thresholds, visible bodies inside their pockets, corrected AI opening, bright wall cores/halos and rounded outer corners. Gate/border graphics remain independently drawn. Desktop scores stay upright. The photo is retained only as separate research evidence and is excluded from the runnable ZIP. F12 cycles all five palettes without changing the maze.


## Revision15 visual and contact review

Fresh continuous DX footage qcO9tzgsdjo around5:00–5:05 shows C morphing into D while walls remain amber. At5:07–5:08 red enlargement accompanies red walls; by5:10/5:13 red and blue giants coexist and walls alternate their colors. The build now retains its base hue through map changes and cycles active giant colors. The1.25-second interval, station order and expiry fallback remain explicit approximations; exact commercial blending/priority is unresolved. Map morphing itself is still not implemented: our stage changes/reset policy remains different.

Native-resolution cardinal outlining made curved wall strokes8.1–8.7% dimmer than horizontal sections. Supersampled circular outlines and a shared premultiplied material reduce the sampled mean difference to0.07–0.34% across four blue maps. Gates, house and tunnel extensions now share luminous stroke construction. Closed gate hatching has the continuous yellow upper lip from the user's photo. All11 pickup icons, eight player colors/directions/sizes, ghost states and world effects were inspected in animation/contact sheets; this does not certify identical commercial assets. Smoke now has soft animated shading and appears immediately on stationary pickup, while the retained trail remains unverified against DX.

The collision report exposed multiple-cell instantaneous shoves and a cooldown that did not prevent repeated impulses. Contact resolution now rolls back the complete group and affected followers, then takes one outward step at normal movement cadence while retaining buffered input. Radius-aware bounded corridor checks reduce visible interpenetration, including tunnels and stationary giant growth. Separate QA caught stationary recoil in the wrong direction and rollback after a later giant hit; both were corrected. This remains a discrete corridor approximation, not recovered continuous DX physics.

HUD scores now show their actual digits, removing the invented six-digit leading-zero padding absent in the user's photo (1760/9460/13530). Existing gate clearance and long-score fitting remain tested. Desktop orientation and the remaining typography/life indicators are still different or unresolved.

Full final source: 271 checks pass on Windows and Ubuntu/WSLg. These include all1–8 rosters/maps and11power categories; no physical-controller certification. A natural continuation replay fixture needed seed0 because the former seed1 survives the60-second window under corrected contact rules; its continuation, score and replay assertions are unchanged. Native1/2/8 runs cover every map; regenerated actual automated gameplay videos include labelled continue scenarios. Source/package tests and decoded media are recorded in current reports.

The full current comparison is DX_CURRENT_GAP_AUDIT.md. All11 categories exist, but numerical power rules, global ghost vulnerability, blanket giant immunity, ghost AI/count/order, attack/combo scoring, spawn distribution, map catalog/progression, paid continuation and several graphical states remain unverified. Agent approval covers stated test scopes only. Controllers remain deferred to production. No exact-match claim.
