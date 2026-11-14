# Production readiness, November 13, 2026

The Windows/Linux package is ready for another local playtest. Physical cabinet acceptance and sustained performance checks are still open.

## Player contact

Holding two players into each other used to make them turn their faces away, pause, retreat one cell and immediately repeat. Equal-size players now approach the contact point along their incoming lanes, keep facing the direction they were moving, slide back once, and settle if both keep pressing. Either player can steer away. A fresh collision is possible after they disengage. The particular recoil timing is our design choice.

The video uses the same scripted inputs in both builds. Its head-on encounter produced three bump events before the change and one afterward. The eight-player convergence went from 43 to seven. Each scene lasts 4.5 seconds. These are controlled encounters with ghosts and pickups removed. [Watch the comparison](images/contact-comparison.mp4).

On Golden Rails the previous giant bite missed a vulnerable rival at (14,1) and (16,2). Their centers were 44.72 pixels apart and a fully grown 36-pixel body plus a normal 17-pixel body reach 53 pixels. The old rule allowed only two corridor steps and this corner took three. Player centers and growth now advance on the simulation clock. The renderer uses those same poses. A bite requires touching circular bodies with an unobstructed line between their centers. Tunnel distance wraps, solid walls and private bays block hits, and active respawn protection still prevents damage. The mouth opening is part of the body silhouette, so its animation cannot make prey temporarily inedible. The game awards one hit per loss of life. Tests cover 52.99, 53.00 and 53.01 pixels, all four tunnel maps and the same growth-contact tick under 30, 60 and 144 Hz draws. [Watch three bite scenarios](images/giant-bites.mp4).

## Reliability

- The previous build crashed on discovering an SDL joystick because the Python joystick object lacked a method provided by the old test double. The game now enumerates current device handles and processes changes while the operator or initials screen is open. The updated input path passed an eight-device virtual test with independent button joins, opposing directions and disconnect warnings. The packaged hardware diagnostic reported zero devices and a failed hardware check on the development machine, as expected.
- Two game processes sharing one save folder could both spend its last credit. One could replace the other process's saved score. The game launcher now obtains a Windows or Linux operating-system lock before loading the profile. A two-process regression verifies refusal of a second writer, independent profiles, recovery after forced termination and retention of saved credit.
- The archive includes the production controller checker alongside the game and keyboard drill. The normal launchers enable real hardware detection. The keyboard playtest launchers use the explicitly simulated controller preset. First installation requires Python and a connection for the pinned Pygame dependency.

## Measured frame times

Each Windows sample used 1,200 frame intervals at 1280 × 720, an actual SDL display, automated movement, the corresponding number of active players with no extra bots, and a fresh process reading the extracted ZIP. Times below are between consecutive frame draws. Cold application startup and maze preparation are measured separately. These desktop samples do not measure button-to-screen latency.

| Windows players | Previous worst frame | After graphics fix, worst frame | After graphics fix, average FPS |
| --- | ---: | ---: | ---: |
| 1 | 92 ms | 19 ms | 60.7 |
| 2 | 102 ms | 19 ms | 60.6 |
| 8 | 301 ms | 30 ms | 60.7 |

The initial frame was calculating shaded sphere textures in Python. The loading screen now prepares the character lighting, pickup sprites and base gate graphics. The renderer also skips a full-frame scale and fill at native resolution. With both the bounce and giant-bite changes, a further eight-player Windows run measured 60.4 FPS, a 21.2 ms 99th-percentile frame and a 24.5 ms worst frame. Cold startup took 7.5 s. No frames in that run exceeded two 60 Hz refresh periods.

On Ubuntu through WSLg, an eight-player run after the graphics fix had one 154 ms interval. A 3,600-interval repeat had one 66 ms interval, on the opening draw, and a 20.0 ms 99th percentile. That repeat reached the second stage. Host load, window composition and the operating system can affect these measurements. A standalone production Linux machine has yet to be measured.

## Release acceptance still open

1. On the intended hardware, do a clean Windows and Linux installation with an ordinary player account. Run the normal launcher and confirm eight real USB devices can join, steer together and reconnect to the correct seats. Check the missing-device warning, keyboard fallback and speaker output.
2. Run consecutive full matches, rematches and continues for a cabinet-length session. Include stage changes, powers, high scores, restart and the actual production screen resolution. Record frame times, memory use, any input stalls and whether saved scores survive relaunch. The acceptance criterion for an eight-hour session and a visible hitch threshold should be agreed for the target hardware.
3. Confirm the intended fidelity claim. Four maze families, the gate details, the eleven power categories and three pellet scores have reference evidence. The graphics and sound are original. Exact collision impulse, ghost priorities and release timing, most pickup probabilities and timing, stage order and paid continue rules remain partially inferred. [DX comparisons and evidence](DX_RELEASE_STATUS.md).
