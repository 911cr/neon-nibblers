# Ghost appearance and starts audit — 2026-11-08

Scope: CHOMPionship, not classic Pac-Man or 2011 Battle Royale. Read current game.py and arcade_art.py; no shared game files changed.

Direct observation: https://www.youtube.com/watch?v=JSp72DKyW5U&t=94s, Arcade Heroes mobile-control CHOMPionship footage. Inspected paused1:34 and1:38. Center house is visibly occupied during play: three adjacent ghost bodies at1:34, two at1:38, with other actors outside. This supports a real holding/return area instead of placing every ghost outside at initialization or respawn. It does NOT by itself prove the exact initial arrangement for Deluxe, nor the initial release schedule. This is mobile/projector footage and should be cross-checked with the Deluxe cabinet before claiming identity.

Appearance observed: rounded domed silhouettes, flowing/scalloped lower edges, conspicuous pale eyes; bodies in the holding box nearly fill its height and are closely spaced. Colored rendering is heavily affected by projection bloom and powered state; do not extract exact RGB values. The new renderer broadly follows those features. It currently gives edible ghosts the same white oval eyes and blue pupils as normal ghosts, merely changing body color: inspect a clear close-up before asserting that is the correct frightened face. Four red/pink/cyan/orange bodies is a reasonable series-consistent default, but this audit cannot certify exact initial order or count from these sampled frames alone.

Current initial positions are x24/26/28/30,y17, all inside house; releases0.9/1.5/2.1/2.7s. These are author-selected, not measured reference values. Label them custom. Do not import classic Pac-Man's red-ghost-outside/three-inside starting rule without CHOMP evidence.

Concrete code finding: body centers are40px apart, rendered ghost body is about36px wide (58px canvas). This gives close but distinct occupancy matching observed house density better than prior outside starts. Ensure the house interior black rectangle does not cover ghosts after they render and doorway/path remain visible. Ghost release paths and eaten return behavior belong to separate audit.

Recommended regression: initialization bodies inside den bounds; each releases through the door, not through side walls; no ordinary player can enter den; house ghosts cannot damage outsiders; captured/returning ghosts preserve identity; no additional ghost duplication on repeated resets.

Search results on classic Pac-Man/Dossier and original BattleRoyale were excluded as evidence of sequel-specific starting behavior.

## QA1 — implementation verification
Read revised current game.py and arcade_art.py. Four ghosts now initialize inside the den (24/26/28/30,17), with separate house/leaving/roaming/eyes/entering/carried states. The prior outside-only start is fixed. Rendering draws all four colored bodies inside the outlined house; verified at work/ghost_initial_qa.png. Bodies are not clipped or painted over by the house. Door opening is centered above them. House/releasing/returning actors are excluded from combat.

## QA2 — deeper regression pass
Ran work/ghost_starts_qa.py with locally installed work/deps (pygame-ce2.5.8). PASS across12 combinations:1/2/8 players ×4 maps. Confirmed four distinct initial positions inside den and outside ordinary movement lanes; every release traverses (27,13); release order0/1/2/3; no side-wall escape; all four become roaming; returning/reset cycles keep four identities; arena changes reset house positions, release timers, carriers and stun arrays. Snapshot visually inspected: correct four separate red/pink/cyan/orange bodies, ample fit inside house, no initial overlap with players.

No blocking implementation bug found in this scope. Appearance caveat remains: procedural body has mostly horizontal shading, whereas filmed appearance blooms and seems more volumetric; exact commercial shader/face/count/order/timers still unverified. Ghosts' frightened face currently retains large oval eyes; do not certify it exact without a clearer frightened close-up. All4-in-house startup and timed release are authored defaults, not proven by the sampled midgame footage. The audit establishes functional coherent starting behavior, not original-mechanics identity.
