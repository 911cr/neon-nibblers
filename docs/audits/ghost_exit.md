# Ghost house exit and return audit — 2026-11-08

## Verified code behavior

Current initial four ghosts are placed inside the house at (24,17), (26,17), (28,17), (30,17). They wait .9 + .6*i seconds, converge horizontally on x27, move upward to (27,13), then enter roaming mode. A local 40-step check at dt=.16 confirmed all four reach roaming. The shared exit cell belongs to all four current map graphs (root checked this).

A concrete visual bug was reproduced: set ghost0 to (27,13) in eyes mode, call update_foes(.16); it immediately appears at (24,17) in house mode. The return skips the doorway and inside path entirely. Add an entering state that travels down the same doorway to y17, then moves horizontally to its home location, then reforms and waits. Keep eyes rendering until arrival. Every successive position should be adjacent except the existing deliberate wrap edges.

Other recommendations:
- Derive house mouth, exit path and home positions from Arena metadata rather than repeating literals in movement and rendering. This prevents later visual/map updates from silently breaking exits.
- Add full lifecycle checks on all maps: house -> leaving -> roaming -> eyes -> entering -> house, valid movement in lanes or designated house-only path, and a bounded eventual return for every roam location.
- Current house/leaving/eyes states bypass quake and lightning slow/stun checks. That may be a useful game rule but has not been verified against CHOMPionship.
- Current .16s step, .9/.6s stagger, 1.2s recovery, protected doorway and exact home ordering are adaptation values, not measured original values.
- Eyes should move visibly through the door before body regeneration; avoid a direct distant teleport. A clear state transition also prevents accidental collisions/eating while reforming.

## Reference evidence and limits

The actual 2022 CHOMPionship Deluxe manufacturer-authored manual was successfully read at this distributor mirror:
https://www.bmigaming.com/Games/Manuals/namco/Pac-Man-Battle-Royale-Chompionship-Deluxe-Video-Arcade-Game-Manual-Bandai-Namco.pdf
It is 28 pages of installation, service and operator settings; it does not specify ghost-house release order, return timing or state protections. It is not evidence for exact lifecycle timings.

Developer Cosmodog's own history identifies CHOMPionship and describes characters/items bouncing in time to music, but does not specify ghost return/release rules:
https://www.cosmodog.com/
Search indexing returned that description; live page timed out. This supports animated presentation only, not exact movement constants.

Known footage references already inspected by parent/other agents: https://www.youtube.com/watch?v=GhSV1oQVA6g&t=57s and https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s . This audit did not independently measure a complete exit/return sequence from that footage. Do not claim it did, nor call the proposed enter/return behavior an exact measured commercial reproduction.

No shared game code edited.

## QA1 — verify the reported return teleport fix

Tested source snapshot SHA256 prefix 8c5e3f1f4d92 using Python + work/deps. All 16 cases (four ghosts on four maps) passed. Each starts in eyes mode at (27,13), stays there while changing to entering, passes through (27,14), (27,15), (27,16), reaches y17, then moves laterally to its own home. Every update moves at most one cell. House mode begins only at the home cell. The original doorway-to-home teleport is fixed. Rendering also keeps entering ghosts eyes-only, as confirmed in the renderer call.

## QA2 — adversarial complete cycles

All 48 repeated lifecycle cases passed (four maps x four ghosts x three return starts: left tunnel mouth, right tunnel mouth, farthest walkable cell). Tests validate eyes -> entering -> house -> leaving -> roaming, adjacent movement including valid wrap adjacency, outside movement staying on lanes, and house movement staying on the dedicated entrance/home path. Every case reached roaming within the bounded loop.

Each repeated cycle also ran under long quake, smoke, global stun and individual zap. Returning/house/leaving movement remains protected from these effects by design; after reaching roaming the active stun correctly holds position. Exact commercial protection behavior is still unverified, so these passes establish internal consistency, not original-game identity.

No additional concrete lifecycle defect found in these passes. There is no persisted/external ghost-state input to justify injecting arbitrary impossible entering coordinates; such malformed internal states were not counted as gameplay bugs. Existing reset_foe(False) remains a teleport helper, but the ordinary returning-eyes path no longer calls it. Avoid reintroducing that helper into visible return transitions.

Reproducible test script: work/qa_ghost_exit.py. Machine-readable results: work/ghost_exit_qa.json. No shared source edits.
