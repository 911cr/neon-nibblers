# Neon Nibblers

**Current build: Keyboard Playtest 5 with turn diagnostics.** [Download the Windows/Linux playtest](dist/NeonNibblers-keyboard-playtest-5.zip). Extract it and run `playtest_windows.bat` or `sh playtest_linux.sh`. The playtest launchers select the two-person keyboard setup. Movement, ghost speed, one-way gates and the experimental manual gate exit follow local playtest feedback. [Current DX comparison](docs/DX_RELEASE_STATUS.md).

Original-code Windows/Linux local arcade maze battle inspired by PAC-MAN Battle Royale CHOMPionship Deluxe. Up to8 human stations, USB gamepad/joystick support, keyboard fallback and AI opponents. No commercial sprites, ROMs, source code, logos or recordings are included.

Revision18 updates the provisional Giant duration from fresh footage, fixes simultaneous fire and carried-ghost cleanup, and aligns ghost eyes, house colors and fire effects with rendered motion. Four observed maze reconstructions and per-station continuation remain available. This is not an exact replica: graphical details, power timing/interactions, ghost AI, map morphing/progression, remaining scoring and paid continuation still have documented differences. See docs/DX_CURRENT_GAP_AUDIT.md.

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

AI fills vacant stations by default:1human+7AI,2+6,8+0. F11 can disable fill. Human input/rankings/controller requirements exclude bots. `--demo` steers every actor for demonstrations. AI routes and difficulty are independently authored. Normal travel uses the keyboard playtest setting of about 6.45 dot spacings per second. Use --tuning tuning.fast.json to compare the former10dot/second profile. Holding two keyboard directions now prioritizes the newer press. A short Preparing mazes screen moves geometry setup before play.

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
| Giant Orb | Grow/eat smaller rivals and ghosts10s;1000points |
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

The revision 18 suite had 363 checks covering all1–8 counts/maps,11powers, ledger/replay, AI, continuous house return, rendered routes, HUD, operator/storage failures, continuation/initials and spectator feeds. Windows and Ubuntu/WSLg native checks include1/2/8 per maze and full continue acceptance/timeout/name entry. Tests and screenshots are automated; physical controllers, eight-human acceptance, speaker audibility and standalone Linux hardware remain production checks.

Three revision 18 MP4s are104seconds each,1280x720/60fps with original AAC event audio:64seconds touring all four mazes, an8-second labelled controlled C-to-D maze change, then two16-second labelled controlled tests of continue acceptance and expiry/initials. All actors are automated. Logical1/2/8 human stations have7/6/0AI. Controlled final-life setup is explicitly labelled, not presented as unassisted human gameplay. GIF previews are24-second silent map tours and may be provided alongside the ZIP.

Optional capture dependencies: `python -m pip install -r requirements-capture.txt`; then `python record_video.py --players 1 --seconds 16 --untimed --continue-showcase --transition-showcase`. The revision 18 ZIP includes its source/tests/docs and three HD videos; historical captures stay in workspace/history. Commercial reference comparisons are separate research artifacts.

See docs/DX_RELEASE_STATUS.md and revision18 audits for evidence boundaries. Repository: https://github.com/911cr/neon-nibblers


## Map from the clearer photo

Yes: the photo is our Golden Rails / observed family D. Double-click `photo_map_windows.bat`, or run `sh photo_map_linux.sh`, to open it in the fifth blue palette and untimed mode with the visibly labelled development controller stub. Manual equivalent: `python game.py --arena 0 --palette 4 --untimed --simulate-controllers`.

The current build has larger glowing64x48 gate pockets, filled striped48x10 thresholds, visible bodies inside their pockets, corrected AI opening, bright wall cores/halos and rounded outer corners. Gate/border graphics remain independently drawn. Desktop scores stay upright. The photo is retained only as separate research evidence and is excluded from the runnable ZIP. F12 cycles all five palettes without changing the maze.

## Revision 18 — power timing, ghost presentation and simultaneous attacks

Fresh DX footage, Harold Zheng's qcO9tzgsdjo, was replayed continuously and critically checked around4:09–4:20. Orange is normal at4:09, enlarged by4:11, still large at4:19 and normal by4:20 while remaining on the field. Passing a green pellet and the approximate score change support Giant identification. No second green pickup was visible on the tracked route, but occlusion, whole-second timestamps and growth/shrink animation leave uncertainty. The narrow estimate is roughly9–11seconds, conservatively8–12. The new default Giant duration is a provisional10seconds, replacing7; other power durations, generation rates and speed ratios remain unchanged. This single sequence does not certify an exact cabinet timer. tuning.example.json follows the default; tuning.fast.json deliberately preserves the entire former fast profile, including7-second Giant.

Blue ghost bodies are visibly present inside the house in the same4:19/4:20 footage. The renderer now includes housed/leaving ghosts in the existing global blue presentation while a hunter effect is active. Returning eyes/carried state treatment and protected house/release collision rules are unchanged. Color alone does not establish whether ghosts can damage or be eaten. Ghost eyes now face the actual rendered corridor segment, including short tunnel crossings, retain facing during stops, and reset on relocation. They no longer face backwards through a tunnel or diagonally toward a future corner waypoint.

The contact reviewers reproduced a dead owner retaining a carried ghost after fire damage until the next update. Damage now releases every owned ghost immediately into returning-eyes state, preserving its location. A second defect gave lower-numbered stations automatic victory in simultaneous fire exchanges because damage deleted the other outgoing attack. Fire emitters, targets and source positions are now snapshotted before damage: both already-emitted attacks resolve, victims take damage at most once, and score popups remain at the original battle location even if an emitter has respawned. When several emitters hit one shared victim, existing first-effective-hit attribution remains an explicit adaptation choice; no recovered DX kill-credit rule is claimed.

At the slower pace, fire began up to18.7pixels ahead of its visible owner. Player poses are now sampled once before effects/gates and reused for the body. Fire connects the visible mouth to its existing logical ray along known corridor waypoints, splitting corners/tunnels and rejecting walls/private bays/diagonal shortcuts. A separate authorized vertical connection through the owner gate is clipped to its pocket and the public field, preserving score clearance. This short connecting tail is presentation compensation only; damage range remains fire_cells. Independent helper and actual-App checks cover all four maps, fractional positions, seams, pauses and concurrent contacts.

All363 checks pass on Windows and Ubuntu/WSLg. New checks cover complete ghost leave/roam/return/release cycles,30/60/144Hz scheduling, smoke/quake/stun combinations, hidden-player targeting, same-tick power expiry/refresh/contact, immediate weapon release, mutual attacks, protected states, actual rendered face/tint/fire paths and1/2/8-player crowds. The configured11-power timing sweep verifies refresh, exact60Hz expiration and pause behavior; Extra Life is instantaneous. No new ghost routing or equal-size bump defect justified changing those algorithms. Natural continue replay uses seed1 because seed0's one-human actor now survives the60-second test; continuation/replay assertions are unchanged.

Native checks cover all four maps at1/2/8 human-designated stations on Windows and Ubuntu/WSLg, plus six maze-transition runs. Twelve full automated matches reconcile score accounts; deterministic replay, stress and extracted-package checks are recorded separately. Updated104-second720p60AAC videos show all four maps, a labelled controlled transition and labelled continue acceptance/expiry. All actors are automated;1/2/8 human-designated stations have7/6/0AI opponents. These are not human playtest recordings or proof of equal fun.

Three agents completed initial and deeper reviews with independent cross-checks. The sole task-owned research Chrome window was closed and its removal verified; preexisting user windows were preserved. Physical controllers remain deferred to production. Exact remaining power timings/ranges/stacking, ghost targeting/release, global vulnerability, collision impulses, kill credit and subjective fun remain unverified. Original code, artwork, sounds and branding remain independently authored. Reference screenshots stay outside the playable ZIP.
