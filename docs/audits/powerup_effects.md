# Power-up effects audit — 2026-11-08

## Evidence and confidence

The strongest accessible CHOMPionship DX-specific product description is PrimeTime Amusements [S1]. The eleven-category effects are independently repeated by Game Room Guys [S2] and MobyGames [S3]. These descriptions establish effect categories, not exact timings, ranges, damage resolution or stacking. Some dealer paragraphs incorrectly recycle the predecessor's rounds/last-player-standing text; avoid using those paragraphs for sequel rules.

## All eleven mappings and required corrections

| Analog | Supported behavior | Audit / correction |
|---|---|---|
| Crown / gold pellet | Enables ghost eating [S1] | Correct basic category. Do not grant rival-eating power. Whether global ghost vulnerability applies to unpowered players is unverified. |
| Titan / green pellet | Enlarges player; permits eating ghosts and regular-sized rivals [S2] | Correct basic category. Current slowdown and immunity against every attack are not established by the sources. Equal-large interaction needs its own audit. |
| Rush / caffeine | Increases movement speed [S2] | Correct category. Current speed multiplier and seven seconds are custom. |
| Mist / smoke bomb | Leaves smoke that impedes ghosts [S1] | Current removal of the player from ghost targeting is wrong. Create visible smoke along travelled cells; ghosts entering it move more slowly. Smoke should not itself mean invulnerability. |
| Slick / banana | Makes the affected player skid with impaired control [S2] | Current rival-only trap and stationary stun are wrong. On pickup apply a short forced-direction slide; at obstruction stop/rebound along legal routes. Exact turning/rebound behavior is custom pending footage. |
| Spark / lightning | Electrical effect against nearby ghosts and rivals [S1] | Current global two-second stun is unsupported. Restrict to nearby actors and render visible arcs. Sources say zap, not whether it kills or stuns; choose and label a provisional outcome. |
| Veil / sheet | Conceals player from ghosts [S1] | Remove universal immunity against rival bites, pepper or electricity. Suppress ghost targeting. Whether incidental ghost contact becomes harmless is not documented; must be called custom. |
| Flare / pepper | Burns nearby foes and opponents [S2] | Current local effect matches category, but Manhattan radius4, through-wall reach and instant death are unverified. Add visible flames to explain hits. |
| Quake / earthquake | Slows all players [S2] | Replace global stun of rivals and random relocation of ghosts with a temporary movement slowdown including the collector. Source does not establish house growth or teleporting. |
| Heart / 1UP | Adds a life [S3] | Correct category. Life cap5 is custom, not source-confirmed. |
| Lure / magnet | Allows carrying a ghost as an offensive object [S1] | Attraction plus double score is wrong. Attach a contacted ghost to holder, visibly carry it, use carried contact against rivals, then release on timer expiry/death. Capture count, position, protection and damage rules remain custom. |

## Recommended tests

Test each category separately; test near/far targets for lightning/pepper, smoke-local slowdown with outside ghost unaffected, banana input suppression without wall traversal, quake affecting collector too, Veil still vulnerable to a powered rival, magnet attach/carry/release plus rival contact, and gold not eating rivals. Mark provisional damage/immunity decisions in README so test success does not imply original-rule verification.

## Sources

- [S1] https://primetimeamusements.com/product/pac-man-battle-royale-chompionship-dx/ — DX-specific list and lives/points premise, retrieved through web search full page text.
- [S2] https://www.gameroomguys.com/Namco-Pac-Man-Battle-Royale-Chompionship — complete effects list.
- [S3] https://www.mobygames.com/game/198053/pac-man-battle-royale-chompionship/ — eleven powers and bouncing pickups.

No shared source code edited. There is insufficient evidence here to claim exact lightning lethality, sheet collision immunity, immunity precedence, durations, power combinations, or effect range.

## QA1 — same-agent correction review
Latest implementation reviewed after parent changes. Smoke creates local lingering trails; skidding suppresses buffered turn control; lightning affects nearby actors; sheet suppresses ghost target acquisition without rival immunity; pepper projects fire through legal corridor cells; earthquake slows collector and other players; magnet captures a ghost and carries it offensively. These correct the six principal category mismatches found above. Gold remains ghost-only; green consumes regular rivals; speed and extra life categories remain present. Exact commercial stun/damage/range/timer behavior is still NOT established by accessible descriptions.

## QA2 — adversarial runtime review
Ran work/qa_powerup_effects.py against local pygame-ce through PYTHONPATH work/deps. Fourteen focused checks exercised near/far zap targets, local smoke placement, skid ignoring turn input, sheet vulnerability to Titan, directional fire damage, magnet capture/weapon contact/expiry, gold not consuming rivals, expired flame no damage, and stage transition clearing stun.

Found a reproducible bug: p.stun survived new_arena, so a player zapped before a clear entered the next arena with 1.99 seconds of stale stun. Reported to parent. Parent reset stun and movement clock in new_arena and hurt. Re-ran all14 cases: ALL PASS, including original failure (stun now0).

Ran additional work/qa_powerup_slowdowns.py checks: smoke ghost remains still at0.16s while outside ghost moves, affected ghost moves at0.32s; earthquake slows collector and other players; Rush+Quake uses combined cadence. ALL PASS.

No additional confirmed implementation defects found in this focused pass. This is not certification of perfect commercial fidelity: exact zap lethality, carried-ghost immunity/expiry semantics, power stacking and numerical parameters remain custom/unverified.

## Issue4 targeted evidence continuation — poster inspected

Retrieved the full promotional power-up poster from the Game Room Shop product image into work/chomp-power-poster-reference.png and visually read it at full resolution. Source asset: https://www.gameroomshop.com/cdn/shop/files/namco-pac-man-battle-royale-chompionship-home-version-3.png?v=1701789284&width=2242 . Product source: https://www.gameroomshop.com/products/namco-pac-man-battle-royale-chompionship . This is a promotional graphic, not measured gameplay, and must not be labeled a video timestamp observation.

New directly observed visual corrections: caffeine is depicted as a handled coffee mug with brown liquid, rather than a drink can; earthquake is a red plunger/detonator box with a gray T-handle, rather than seismic rings; magnet is a blue C/U form with silver tips, rather than a two-color pink/blue magnet; chili includes a flame; extra life uses white block typography. The artwork should be reauthored to these generic recognizable silhouettes, retaining original code and avoiding logo copying.

The poster confirms the same high-level categories already corrected. It does NOT specify lightning kill versus stun, incidental collision under sheet, giant immunity to attacks, or what happens when magnet expires. Therefore it does not justify changing those four runtime choices or certifying them exact.

A new dealer page explicitly describes lightning as stationary stun: https://themancaveauthority.com/products/pacman-battle-royale-arcade . However it also mixes last-survivor text and says earthquake affects only others, contrary to the poster's all-players description. Treat the stun sentence as weak corroboration of current provisional stun behavior, not definitive evidence. Do not import immunity or expiry from predecessor/other Pac-Man games.

Footage access attempted at https://www.youtube.com/watch?v=GhSV1oQVA6g&t=100s . No event was viewed: IAB was unavailable and browser inventory empty; shared native Chrome was reserved by the gate/spawn agents, so no concurrent input was attempted. No video timestamps are asserted as observations. A fresh Deluxe candidate reported by gate agent, https://www.youtube.com/watch?v=efLgejKG_ls , also remains uninspected here.

Actionable result: correct four object silhouettes and pepper flame using the actual inspected poster. Remaining behavior questions are still open; closing them requires an observable before/after collision or expiry sequence, rather than another copy of the same marketing list.
