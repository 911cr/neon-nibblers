# Gate detail and operation review

Reference: user-supplied codex-clipboard-714bc97c-aa0c-455f-9d0f-49a30fab812d.png, viewed directly. The photo supports continuous double U-shaped bay walls, pale bright edges with blue glow, and a yellow threshold band crossed by dark diagonal stripes. It is static evidence: it does not prove opening/closing timing, collision ownership, AI spawn positions, or continue mechanics.

## Reproduced operation defect

The previous App renderer used joined-only occupant selection for both HUD and physical gate opening. AI actors are alive with bot=true/joined=false, so their hatches stayed closed during initial departure and owner return. Actual render tests found119 yellow hatch pixels at the AI P2 mouth during both scenarios. Human HUD eligibility should remain joined-only, while physical gate opening must consider a living bot too.

An initial code-review concern about y-only interpolation proximity was not reproduced during normal far-border movement: the entry center was26 pixels from the mouth, outside the22-pixel crossing threshold. The far-border test already passed. Horizontal proximity is a sensible defensive guard, but this audit does not label it an observed normal-play defect.

## Static art test design

The visible stripes contain legitimate dark pixels, so the test does not demand a uniformly bright filled rectangle. Instead each interior row must retain substantial yellow-band coverage, distinguishing a filled striped band from a single line plus sparse diagonal marks. The open throat must clear its central path. Geometry/glow checks use the root renderer's declared geometry, rather than inventing pixel-perfect source dimensions from a perspective photograph.

Initial actual-render matrix covers four profiles and eight stations in initial departure, far-border travel, owner return, empty/unjoined, eliminated and pending-continue states. Actor artwork is suppressed only for hatch-pixel inspection so an overlapping body cannot hide a closed gate.


## Second critical pass and fixes

The final gate helper exposes outer/hatch/clear rectangles. Tests use its outer rectangle explicitly, not an assumed return type. Normal radius17 bodies now fit the outside64x48 pocket at their actual rendered center, and an actual muncher draw-call check verifies an unclipped own-bay pass. Departure testing checks the hatch stays open until the body's trailing edge clears the mouth. AI initial release and return now open the physical hatch; HUD eligibility stays human-only.

Two further real defects were reproduced during the art review. First, blurred gate/house layers were added with RGB-only blending onto transparent surfaces, leaving halo alpha zero and making the supposed glow invisible on an opaque canvas. Sampling four pixels beyond the core returned exact background. Root switched these layers to alpha-aware RGBA addition; tests now verify visible soft halo outside both gate and house cores, two distinct bright parallel gate edges and a dimmer gap. The wall renderer uses an opaque result and did not have this alpha defect.

Second, moving the house inner contour to inset10 left it crossing the doorway: the old cut stopped at top+8, while pixels at offsets10/11/12 were bright wall colors. Root extended the opening cut through the inner contour and its glow. The updated legacy house test counts two bright contour bands (including pale highlights) and checks the entire intended inner-door opening at offsets2..14, rather than incorrectly counting exact-accent fragments of one highlighted stroke.

The gate/art matrix covers all four profiles and all eight stations: human/AI initial release, far-border travel, owner return, empty slots, eliminated humans and pending continuation; central filled-striped-band coverage and cleared open paths; physical body fit and actual clip pass; normal/six/nine-digit HUD clearance; and visible halo/parallel borders for all five palettes. The conservative pocket halo rectangle clears score/life rectangles and screen edges. Additional actual footer blit checks verify its reserved central gap at720p and1080p, for1/2/8 humans. Independent palette cycling now covers all five palettes and still leaves simulation digests unchanged.

Legacy fixtures were updated honestly: the hatch-color test disables AI so its unused bay is truly closed and inspects the whole striped band; respawn/stage-cache checks use the new true center(spawn); house tests use the new contour inset and opening; footer checks intercept actual surface blits instead of an obsolete text helper; palette tests cycle the actual palette list.

Final combined targeted run:24 tests passed in48.940s. This includes11 new gate-detail tests,11 rendering tests, the hatch-color fixture and the house-door fixture. Actual scripted gate-state contact sheets were regenerated for four profiles plus the blue photo palette. They show actual App rendering, not commercial footage or proof of measured timing. Root separately corrected stripe orientation to keep the same slash direction at both upper/lower bays.

Disposition: approved for the assigned geometry, art-compositing, body placement, opening/closing state and HUD bounds scope. Static reference agreement does not certify cabinet gate timing, unpublished collision rules, physical controls or perfect source identity. Final full Windows/Linux discovery and gameplay recordings remain root-owned.
