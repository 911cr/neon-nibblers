# Revision 12 â€” cabinet, saved results and spectator QA

Reviewer: dx_research, 2026-11-08. Scope: independent code and actual headless App integration review of cabinet.py, spectator.py and App events/render/run. These are original operator and spectator features; this audit does not certify exact DX timing, scoring, high-score presentation or settings equivalence.

## Isolation and method

All tests inject a CabinetStore backed by a temporary directory under the workspace. No real cabinet profile is read or written. SDL dummy video and audio run real Pygame surfaces, event queues, mixer and App loop. Native browser/computer use was not used for this code QA. Physical controllers, speaker audibility, cross-machine spectator transfer and native Linux execution are not certified here.

## First critical pass

Exercised F11 operator navigation/save/cancel, H high scores, C credits, free-play sparse P8 join, paid preset failure/success, Find without charge, eliminated-player Find, every 1â€“8 player preset, configured lives/time/disabled bonus, tied eight-player results and reload/deduplication. Actual App.draw and a three-frame results App.run exercised runtime persistence and spectator publication. Atomic write failures must roll back settings, credits and result tokens.

Found and reported three implementation defects, subsequently fixed by the implementing agent:

- A late malformed saved field left partially loaded settings/credits despite reporting default recovery. Corrupt saves now reset the full loaded state.
- Spectator feeds accepted malformed/nonfinite remaining time and timestamps, which could reach rendering arithmetic. Feed validation now rejects those values and invalid station IDs.
- Results were saved after event processing, allowing immediate restart, station start or Escape to replace the finished match first. App saves before processing those transitions; regression covers all three.

## Second, adversarial pass

Added failure and lifecycle checks: failed operator save must keep the editor open without changing settings; invalid payment counts must not mint credits; attract audio must survive a mixer shut down after initialization; fresh and stale spectator states must actually produce different rendered pixels. The attract path originally bypassed the audio shutdown guard and raised pygame.error. The implementing agent fixed it and the regression passes.

A further persistent-results defect was reproduced: if saving fails while Escape leaves results, a later successful store cannot recover the discarded match. A dedicated regression now requires retry after leaving results. The implementing agent added an in-memory immutable standings queue and a one-second retry throttle. The regression now advances the mocked monotonic clock past that retry boundary and verifies recovery after leaving results. Another regression verifies ten repeated event passes do not hammer the failed store, later score mutation cannot change the queued result, and successful retry records only once. Both pass.

## Practical limits

A passing headless suite establishes internal behavior and safe failure handling, not physical cabinet fidelity. Spectator output is an original independent standings view, not a captured commercial screen. Persistent storage failure cannot guarantee disk survival across process termination; any in-memory retry must be disclosed appropriately. Exact DX defaults/operator behavior remain bounded by the manual and footage evidence in the reference register.

## Final verification

Final command: `PYTHONPATH=work/deps python outputs/NeonNibblers/test_cabinet.py` (PowerShell resolves the dependency directory first). **17/17 tests passed** in 3.094 seconds on Python 3.14.2, pygame-ce 2.5.8 / SDL 2.32.10, Windows dummy video/audio. Both critical passes are complete for this bounded scope; all reproduced failures have passing regressions. No known failing cabinet regression remains. This is not a claim that every original DX behavior or every hardware/environment combination has been verified.
