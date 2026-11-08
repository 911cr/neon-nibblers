# Controller development/production mode QA — 2026-11-08

No shared game files changed. Local checks use work/deps; mocked device counts are explicitly test doubles, not physical controller evidence.

## PASS 1 — implementation and intended mode separation

Read App initialization, refresh_pads/controller_status/events/inputs, CLI and both development/production launchers. Executed the two new controller mode tests: both pass.

- App defaults simulate_controllers=False; ordinary launchers do not add the flag.
- Explicit --simulate-controllers sets an availability assumption, with an unmistakable DEV / SIMULATED label.
- Development launchers forward the explicit flag. Windows quotes its launcher path; Linux resolves and quotes its directory and forwards arguments.
- Development actual count remains the observed pad count. effective is the requested player count, missing is zero, but no fabricated joystick objects or directional input are created.
- Production zero/partial counts generate a missing-device message and retain keyboard input; disconnect events refresh device inventory and give a visible notice.

## PASS 2 — adversarial matrix and layout

Executed work/controller_mode_qa.py: both modes x requested1/2/8 x actual0/1/2/8, checking actual/effective/missing, lobby rendering, in-game footer width/height, and keyboard KEYDOWN fallback. All matrix checks passed. Both lobby and gameplay screenshots were visually inspected; status text fits inside1280x720 and does not overlap major controls or score panels.

Injected real pygame event objects with patched joystick enumeration to test remove then immediate add, without resetting app state:
- Removal: actual1, expected2, missing1, disconnectedTrue, correct message.
- Immediate recovery: actual2, expected2, missing0, but **disconnected remainsTrue** and UI still says `Controller disconnected | 2/2 connected | keyboard fallback available` until its five-second timer expires.

This is a minor but confirmed recovery UI bug. The existing test manually clears controller_notice_until after reconnect and therefore masks it. Automatically clear the warning once expected controllers are restored, or explicitly say `Recently disconnected` if retaining a historical notice. Add a replug assertion without modifying the notice timer.

No fabricated hardware report was found. Physical USB hotplug/input and Linux hardware remain untested; these are software-level mocks plus real event handling/render checks.

## Targeted recovery fix recheck — CLOSED

Reran the same adversarial matrix and immediate remove/replug reproduction against the updated file. Recovery now reports actual2/effective2/missing0/disconnectedFalse and `2 controllers connected | 2 players`, with no manual notice reset. The revised production hotplug regression also passes. Original controller-mode QA finding is resolved; zero/partial/full mode separation, keyboard fallback and layout checks still pass. This remains software-level validation, not physical USB certification.
