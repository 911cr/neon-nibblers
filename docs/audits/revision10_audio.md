# Revision 10 — independent audio QA

Reviewer: dx_research, 2026-11-08. Owns `test_audio.py`; root owns audio implementation. No further browser actions used after the reference-tool stop.

## Pass 1

Reviewed `arcade_audio.py` and the application loop. Ten original synthesized cue patterns map from ledger events to separate playback lanes. Identified two code concerns: mute originally discarded future events without silencing a playing cue; mixer shutdown after initialization could raise during playback. Root fixed both before the tests ran. Therefore these are review-found issues verified after correction, not claimed failing-before automated runs.

Eight first-pass tests passed against actual SDL dummy audio: all PCM cues create real pygame sounds; all ten lanes play; repeated consumption does not replay; new ledger resets cursor; mute stops old playback and discards events without a later burst; initial mixer failure and later shutdown are safe; unsupported sample format stays silent; mono works; simultaneous eight dots plus hurt and bonus preserve event history and independent channels; all1–8 player counts join/find/pause/render/restart correctly.

## Pass 2: stronger integration checks

Added direct F2 handling in the lobby while a finish cue is playing: it stops immediately even without a match. Ran the real App.run loop for three rendered paused frames with8 players, observing one initial join consumption then empty consumption on both later frames. Scores and ledger remain unchanged by audio/rendering. The earlier all-count integration test also checks draw alone does not append or replay events.

Final command: `python outputs/NeonNibblers/test_audio.py`, with `PYTHONPATH=work/deps`, SDL dummy video/audio. **10 tests passed**, Python3.14.2, pygame-ce2.5.8, SDL2.32.10. Tests use actual dummy mixer channels and PCM objects; mock use is limited to forcing initialization failure and observing the App consumer.

## Limits and decisions

Cues are independently composed and are not commercial recordings or claimed exact sound matches. Repeated same-type events within one consumption batch intentionally share one lane; hurt/bonus/finish are not displaced by dot activity. Short already-playing cues may finish while paused; muting explicitly stops them. Hardware speaker quality, audible balance and physical controllers remain unverified. No blocking reproduced audio event/lifecycle bug remains in these tests; this is not a complete DX fidelity certification.
