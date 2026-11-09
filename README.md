# Neon Nibblers

Original-code Windows/Linux local arcade maze battle inspired by PAC-MAN Battle Royale CHOMPionship Deluxe. Up to8 human stations, USB gamepad/joystick support, keyboard fallback and AI opponents. No commercial sprites, ROMs, source code, logos or recordings are included.

Revision17 fixes missed keyboard turns, introduces continuous corridor motion, improves bot power/rival decisions and uses a slower provisional pace informed by DX footage. Four observed maze reconstructions and per-station continuation remain available. This is not an exact replica: graphical details, power timing/interactions, ghost AI, map morphing/progression, remaining scoring and paid continuation still have documented differences. See docs/DX_CURRENT_GAP_AUDIT.md.

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

AI fills vacant stations by default:1human+7AI,2+6,8+0. F11 can disable fill. Human input/rankings/controller requirements exclude bots. `--demo` steers every actor for demonstrations. AI routes and difficulty are independently authored. Normal travel now uses an estimated4dot-spacings/second, with continuous visual movement. Use --tuning tuning.fast.json to compare the former10dot/second profile. Holding two keyboard directions now prioritizes the newer press. A short Preparing mazes screen moves geometry setup before play.

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

These are independently reconstructed observed topologies with original names/palettes. Perspective, hidden endpoints and20px coordinate quantization remain estimates. Four observed families do not prove the complete catalog. Dot-clear transitions and cycle/repeat/random order remain adaptation policies, preserving scores/lives/effects and legal actor positions. Disappearing cells move to the nearest free public lane; this relocation policy is an approximation. Maze changes have a1.1-second visual pulse and staggered collectible-dot refill. Default starts on Cyan.

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

328 checks cover all1–8 counts/maps,11powers, ledger/replay, AI, continuous house return, rendered routes, HUD, operator/storage failures, continuation/initials and spectator feeds. Windows and Ubuntu/WSLg native checks include1/2/8 per maze and full continue acceptance/timeout/name entry. Tests and screenshots are automated; physical controllers, eight-human acceptance, speaker audibility and standalone Linux hardware remain production checks.

Three current MP4s are104seconds each,1280x720/60fps with original AAC event audio:64seconds touring all four mazes, an8-second labelled controlled C-to-D maze change, then two16-second labelled controlled tests of continue acceptance and expiry/initials. All actors are automated. Logical1/2/8 human stations have7/6/0AI. Controlled final-life setup is explicitly labelled, not presented as unassisted human gameplay. GIF previews are24-second silent map tours and may be provided alongside the ZIP.

Optional capture dependencies: `python -m pip install -r requirements-capture.txt`; then `python record_video.py --players 1 --seconds 16 --untimed --continue-showcase --transition-showcase`. The ZIP includes current source/tests/docs and three HD videos; historical captures stay in workspace/history. Commercial reference comparisons are separate research artifacts.

See docs/DX_RELEASE_STATUS.md and revision17 audits for evidence boundaries. Repository: https://github.com/911cr/neon-nibblers


## Map from the clearer photo

Yes: the photo is our Golden Rails / observed family D. Double-click `photo_map_windows.bat`, or run `sh photo_map_linux.sh`, to open it in the fifth blue palette and untimed mode with the visibly labelled development controller stub. Manual equivalent: `python game.py --arena 0 --palette 4 --untimed --simulate-controllers`.

The current build has larger glowing64x48 gate pockets, filled striped48x10 thresholds, visible bodies inside their pockets, corrected AI opening, bright wall cores/halos and rounded outer corners. Gate/border graphics remain independently drawn. Desktop scores stay upright. The photo is retained only as separate research evidence and is excluded from the runnable ZIP. F12 cycles all five palettes without changing the maze.

## Revision 17 — responsive input, continuous motion and reference-informed pace

Two normal-looking actors in real DX footage qcO9tzgsdjo4:09/4:11/4:13 cover approximately12–15 dot spacings in nominal4seconds. Whole-second timestamps and camera perspective leave a conservative2.4–5dots/second range; hidden power status is not fully excluded. Our previous10dots/second was likely materially faster. The new provisional default is4dots/second (.25s per20px cell). Rush/Slick/ghost/item intervals are.1625/.1375/.40/.60s, preserving earlier authored relative speeds; those ratios are not recovered DX facts. The old fast profile remains selectable with --tuning tuning.fast.json. Power durations, probabilities, spawn interval and collision impulse constants were not guessed from this footage.

Fixed a concrete keyboard bug: held Up overwrote a freshly pressed Right in the next input poll. Every station now uses its most recently pressed held direction; releases fall back to remaining held keys, and no-key state retains buffered intent. Legal facing/reversals update without granting distance or resetting movement clocks. Invalid turns stay buffered until a junction. Slick/recoil remain in control during their effects. Discrete travel decisions still occur on the movement cadence; immediate facing does not eliminate the possible250ms positional wait or constitute a continuous subcell physics model.

Replaced exponential visual easing with constant-speed axis-aligned waypoint motion for players, ghosts and moving items. This avoids bursts/holds at the slower cadence and prevents rounded diagonal cuts through corners. Logical reversals cancel abandoned forward waypoints, tunnel coordinates wrap, damage/restart reset tracks, and50px gate movement receives its own distance scaling. Pause/help/results freeze motion; rendering changes no Match state. Very long frames crossing multiple unseen turns can snap to the final cell rather than inventing a route. Normal30/60/144Hz default-speed tests do not encounter that case.

Bot navigation now recognizes nearby powers across tunnel connections, prioritizes vulnerable rivals while giant even when ghosts are in their house, and chooses a legal safer fallback when goals disappear during refill. Six adversarial/navigation tests and independent review cover these fixes. No new collision-resolver defect was reproduced; all-map crowds recover, retain controls and avoid overlaps/extra-cell jumps. With slower speed, densely packed eight-player crowd recovery takes longer in wall-clock time; this tradeoff remains documented.

Paired90-second eight-actor simulations isolate pace from the bot changes: death events140→54, rival hits93→30, pickups298→285 and mean stage4.75→2.25. Near-rival proximity rises.190→.227, but it is a Manhattan-distance proxy, not a collision measurement. Separate1/2-actor experiments do not include the application's vacant-station bots. These metrics show less rapid churn and fewer attacks, not greater enjoyment. All90s observations are censored for finish time; no survival-length conclusion. No human multiplayer fun-equivalence test has been completed.

Maze geometry is now prepared before play. One local dummy-render comparison moved first-layout-change rendering from.9999s to.0084s, with3.5794s spent preparing four mazes before play; this is a measured cold-start comparison, not a guaranteed native FPS claim. The game shows Preparing mazes during that work. Actual four-map slow tour review found zero off-centerline positions across17,117 player samples, and straight/tunnel motion at60Hz consistently1.333333px per moving frame.

All328 checks pass Windows and Ubuntu/WSLg. Native runs cover all four maps with1/2/8 human-designated stations plus six transition runs, using7/6/0AI fill; audio initializes, physical input/audibility remains uncertified. Twelve full automated matches reconcile scores and rankings; deterministic replay, stress checks and extracted-package validation are recorded separately. Updated104-second720p60AAC videos show64seconds of four-map play,8seconds of labelled controlled C-to-D transition and32seconds of labelled continue scenarios. All capture actors are automated.

Agents completed initial and deeper passes, with targeted fixes/rechecks. The task-owned research YouTube tab/window was closed and its removal verified; other user applications were left untouched. Physical controllers remain deferred to production. Exact DX power timing, ghost rules, collision physics, scoring, artwork and subjective fun are not certified. Original assets/code/audio remain independently authored.
