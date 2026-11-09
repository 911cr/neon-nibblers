# Revision15 power and ghost parity: current evidence, not an exact-replica certificate

All11 categories have original icons and implemented effects. That establishes inventory coverage, not behavioral equivalence. This review directly inspected the CHOMP promotional poster in work/chomp-power-poster-reference.png, the current collection/combat/ghost/render paths, and the revision13/14 reference audits. The poster establishes broad effects; it does not specify ranges, duration, stacking, immunity, targeting or spawn cadence. Released-DX instruction-screen evidence independently supports ordinarydot10, Gold100 and Giant1000 awards. Other pickup/combat awards remain estimates.

| Category / internal name | Supported broad effect | Current implementation | Still unverified or different |
|---|---|---|---|
| Gold / Crown | Ghosts become edible | Collector can eat roaming ghosts;100 pickup points |7s estimate; all ghosts visually blue when any hunter exists, but unpowered players still die on contact. Whether edibility is global or collector-specific is unresolved. |
| Green / Titan | Grow; eat ghosts and regular rivals | Giant render, active wall-color cycling, ghost/rival eating;1000 pickup points |7s and wall-cycle cadence remain estimates; blanket hurt immunity also blocks fire and carried weapons; equal-giant rules, hit radius and exact size unknown. |
| Caffeine / Rush | Faster movement | Shorter movement interval |7s, speed ratio, stacking and effect on contact response unknown. |
| Smoke / Mist | Smoke explosion slows ghosts | Immediate pickup cloud now slows nearby roaming ghosts; movement also leaves a trail |The missing stationary pickup cloud was a definite omission and is fixed. Persistent trail,7s emission,2.5s cloud, radius2 and slowdown ratio lack positive evidence. Burst-only would be a literal-poster interpretation, not proof the trail never exists. |
| Banana / Slick | Uncontrolled skid | Ignores wanted turns, keeps direction until blocked, then selects a legal random direction; faster movement |2s, increased speed, random-turn policy and interaction with other powers unknown. |
| Lightning / Spark | Zaps nearby ghosts or rivals | Nearby living rivals and ghosts receive stun |Radius8 Manhattan distance,2s stun, wall/portal propagation and contact immunity during stun unknown. |
| Ghost sheet / Veil | Hidden from ghosts | Ghost targeting ignores collector; translucent player art |Ghost physical collision remains dangerous. Whether source invisibility also prevents collision, exact appearance and7s duration unknown. |
| Chili / Flare | Burns nearby ghosts or rivals | Forward corridor flame, stopped by walls and split at tunnels; ghost/rival damage |Forward-only five-cell reach, no flame when direction is zero,3s duration, victim immunity and scoring are assumptions; broad poster wording does not resolve the area shape. |
| Earthquake / Quake | Everyone slows | Global player/roaming-ghost slowdown |5s and2x interval; eyes/house movement exceptions, source shake and stacking unknown. |
| Extra life / Heart | Adds a life | Adds one up to5, with positive-gain cue |Five-life cap and pickup75 unverified. At cap it grants no life; do not present that cap as source-certified. |
| Magnet / Lure | Capture/carry ghosts as a weapon | Contact captures ghosts, held ahead of owner; carried ghost can hurt another rival |7s, capture radius/count, held position, release/expiry behavior, Giant immunity and priority over Gold/Giant unknown. |

## Ghost and interaction assumptions needing controlled footage

Four ghosts, staggered house release, fixed base speed, return-as-eyes route, chase probability, weighted bot decisions and nonreversal policy remain independently authored rules. The newer legal-distance routing removes wall-trap oscillation in our simulation; it is not recovered DX AI. Global blue appearance versus player-specific eating needs resolution before calling the power presentation accurate. Contact now also checks radius-aware approach using bounded legal-corridor distances (normal17/giant36), alongside coincidence/head-on swaps. This removes inline adjacent-body penetration during approach, but remains a grid approximation rather than continuous Euclidean disc contact. Equal bodies at unchanged following separation do not repeatedly bump; private bay endpoints are excluded because their visual centers have different spacing. Giant growth beside a smaller body can create a hazard without movement. Recoil magnitude, timing and collision-group policy remain custom even when internally consistent.

## Disposition

No exact-replica approval. The stationary Smoke omission and recovered Gold/Giant scoring are concrete evidence-driven corrections. Other rows contain implemented broad analogues with material unresolved rules. Keep these uncertainties visible; names, icons and passing tests do not certify each power's real-game correctness. Physical controller and cabinet verification remain deferred.
