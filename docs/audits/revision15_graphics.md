# Revision 15 graphics audit

## Evidence and limits
All four independently authored reconstructions reviewed: A at https://www.youtube.com/watch?v=-cNOhumVZ74&t=68s ; B same source73s; C at https://www.youtube.com/watch?v=qcO9tzgsdjo&t=250s (complements270/293/299); D same source305/315s and user photo work/user-gate-reference-r14.png. This is not a certified complete commercial catalog. Coordinates, endpoint widths and occluded details remain estimated. No topology changed this revision.

Fresh actor frame work/r15-multi-color-5.png (Harold Zheng5:14) was inspected: red/blue giants, red normal ghost with large white eyes and cyan house ghost. Perspective, motion blur and camera bloom prevent pixel-exact sprite/light measurements. Reference-containing figures remain outside playable assets.

## Diagnosed defect and fix
Old peak RGB was equal but stroke coverage/energy varied: binary native edges and cardinal erosion produced direction-dependent thickness. Three-times supersampling, circular erosion, a fixed1px pale core and consistent premultiplied neon composition correct this. An intermediate upscaling phase error between opposing edges was caught and fixed with nearest upscaling plus symmetric softening. Geometry masks and20px body clearance are retained.

Quarter-pixel bilinear luminance integration across7px normal windows on all four rendered maps, fixed blue(74,91,255): old curve energy CV14.6-15.0%; final1.62-2.38%. Old curves averaged8.1-8.7% below horizontal strokes; final mean difference0.07-0.34%. Vertical/horizontal residual max3.37% (nearby narrow-wall halo overlap); frame residual below4.6%. This measures renderer consistency, not photographed-monitor photometric parity. Raw stats: work/wall_quality_metrics_r15.json.

Color-independent premultiplied band/core basis caches now avoid morphology and blur on hue changes. Measured initial geometry0.966s, subsequent uncached hues0.00645s, against root's earlier0.475s. Bounded8 geometry bases and20 backgrounds; public results return copies. Initial load cost remains. Shared gate/house compositor integration belongs to gate agent.

## Broader graphics matrix
| Area | Actual checks | Reference and uncertainty |
|---|---|---|
| Munchers |4 directions,8 colors, mouth phases, normal/giant sizing, stable light | Shaded round/open-mouth language supported; eye geometry and proportions remain original |
| Ghosts | Normal, edible, eyes-only, feet animation, stun stars | Colored domes/white eyes supported; exact frightened/stun art unverified |
|11 power icons |32/64/96px sizes, all phases, stable bob | Original readable icons; exact commercial artwork is not reproduced |
| Fire | Animated continuous plume, clipping/bounds regression | Broad flame supported by earlier135s frame; exact particles unknown |
| Smoke | Flat-circle quality defect corrected with cached soft layered smoke_cloud | Original quality improvement, no exact commercial particle claim |
| Zap/magnet/locator/feedback | Actual App state frames0/.2/.4/.6s across4 maps | Readable in sequence; exact commercial effect timing/strokes unknown |
| HUD/lifecycle | Existing desktop-facing layout; parent owns continue/hue changes | Desktop labels/menu and original title differ from cabinet orientation |

Artifacts: outputs/NeonNibblers/animation_contact_r15.png, animation_review_r15.gif, animation_world_effects_r15.png. World sheet is scripted state/effect demonstration, not an earned completed match; root refreshes after integrating new smoke. Research figures: outputs/DX-wall-comparison-r15.png and DX-wall-traces-r15.png show source/baseline/final all-map and enlarged Dcorner/L, BcentralT, Aarch comparisons.

## Critical passes and verification
Pass1 diagnosed stroke variation, built shader, caught/fixed phase asymmetry, inspected enlarged traces/all4 maps. Pass2 measured all contours, added mutation-safe bounded caching, resolved dynamic-hue stall, inspected actual actors/effects and fresh source. Soft smoke fixes a separate visible quality issue.

Final source checks:19 map tests PASS (all1-8 counts/maps, sparse bays, transitions, every route20px body clearance, ghost doorway, exactly2 house contours);5 wall tests PASS (orientation/curve energy, cache safety/reuse, premultiplied halo and soft smoke phase/bounds);8 animation tests PASS (directions, bounds, feet/stars, icons,30/60/144Hz time behavior, fire). Independent agent and full-platform checks are reported separately, not presumed here.

Wall hue does not identify topology. Fresh source retains amber through C-to-D then red/blue while giants are active. Exact simultaneous-giant priority/cycle period remains uncertain; parent owns that rule and documentation. No perfect-match, exhaustive catalog or physical-controller certification is made.

Independent second reviewer (dx_ledger): all5 wall-quality tests passed in4.873s and all4 final backgrounds plus baseline0 visually inspected; no new background geometry/brightness defect found. Its gate integration13 tests passed. Reviewer found App portal-neck flat1px accent lines bypassing shared shader and reported to root; background approval does not certify those separately owned scene connectors.
