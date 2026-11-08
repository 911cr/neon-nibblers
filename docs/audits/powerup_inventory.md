# Power-up inventory audit — 2026-11-08

All eleven publicly listed power-up categories have an entry and an independently drawn icon in this game. No inventory slot is missing. This does NOT mean the implemented effects are faithful.

| Reference category | Game analog | Current icon | Inventory verdict |
|---|---|---|---|
| Gold Power Pellet | Crown | gold orb | Present |
| Green Super Pellet | Titan | green orb | Present |
| Caffeine | Rush | drink can | Present |
| Smoke Bomb | Mist | smoking bomb | Present |
| Banana Peel | Slick | yellow peel | Present |
| Lightning | Spark | lightning bolt | Present |
| Ghost Sheet | Veil | pale sheet with eyes | Present |
| Chili Pepper | Flare | red pepper | Present |
| Earthquake | Quake | seismic rings/wave | Present |
| 1UP | Heart | green 1UP badge | Present; Heart name is misleading |
| Ghost Magnet | Lure | horseshoe magnet | Present; Lure name implies the wrong behavior |

Verified in code: game.py ITEMS has11 entries. arcade_art.py power_icon has corresponding drawn branches (magnet is final fallback). Art was independently authored. Exact commercial icon shapes/colors/animation were NOT verified by this inventory audit; semantic recognizable silhouettes alone do not establish a visual match. Recommend rename Heart to Extra Life and Lure to Ghost Grab/Magnet in displayed labels, keeping internal keys for compatibility if desired. Rename Crown to Gold Orb for clarity if original parody naming is unnecessary.

Critical semantic mismatches for effect audit: current Mist ignores foes rather than slowing them with smoke; Slick creates an opponent trap rather than causing uncontrolled skidding on pickup; Spark affects all instead of nearby targets; Veil grants blanket combat immunity rather than just hiding from ghosts; Quake stuns rivals/scatters foes rather than slowing everyone; Lure attracts foes and changes points rather than carrying a ghost as a weapon. Do not declare the inventory 'complete and correct' until those are fixed/tested. These effect descriptions are corroborated by two distributor listings below, not inferred from names.

Sources:
- PrimeTime Amusements product description, complete11 list: https://primetimeamusements.com/product/pac-man-battle-royale-chompionship/
- Pinballs.com distributor, same complete11 list: https://pinballs.com/product/namco-pac-man-battle-royale-chompionship/
- Manufacturer current DX product/parts page: https://bandainamco-am.com/collections/pac-man-battle-royale-deluxe (confirms model, but current page does not expose the11-item details).
- Manufacturer historical DX manual search index exists, but live PDF returned404 from both www and non-www URLs. Do not cite it as successfully read: https://www.bandainamco-am.com/Ecommerce/Site/Content/PDFs/Pac-Man%20Battle%20Royale%20Chompionship%20DX%20Manual_5_12_revise_Edit.pdf

Remaining unknowns: exact icon animation and size; probabilities, timers, spawn eligibility; item placement; effect duration/range/stacking. These require the other targeted audits or measured footage.

## QA pass 1 — correction verification (same inventory agent)
Reviewed current game.py ITEMS, collection/movement/ghost logic and arcade_art.py again after root implementation. All11 dictionary entries, pickup branches and icons remain. Six previously wrong effect descriptions now name the intended class of effect: smoke slowing, forced skid, nearby zap, ghost invisibility, everyone slowed, carrying ghosts. Exact duration/range/stacking remain custom/unverified.

FAIL to fix: Titan field-guide description still says slower, but current movement uses normal .10 seconds per tile for Titan (Rush .065; Slick .055; quake doubles). Remove slower from description.

FAIL to fix before packaging: README still describes the old effects (Mist ignores foes, Slick trap, global Spark, Veil universal immunity, Quake stun/teleport, Lure attraction/400-point bonus). It also says normal players overlap. Documentation no longer matches updated code.

Naming recommendation remains: displayed Heart should say Extra Life, displayed Lure should say Ghost Magnet/Ghost Grab. Internal compatibility keys can remain unchanged. This is clarity, not an omitted inventory item.

## QA pass 2 — adversarial inventory/render/label consistency
Executed work/inventory_render_qa.py headlessly and visually inspected work/inventory-guide-qa.png. Result:11 distinct nonempty icon images, all11 entries visible in F1 guide without clipping/overlap; measured longest description386px fits easily. All11 categories remain selectable by randomized spawn_item; fixed gold/green and nine other types retain distinct matching art branches. No missing icon, duplicate icon or missing guide row found.

The rendering check DOES NOT establish original-art identity. Exact commercial silhouettes, per-icon animation, palette and sizes remain unverified. Heart/Lure labels remain misleading but descriptive guide text identifies their effects. power_icon uses its final else as the Lure icon; unknown future keys would silently draw a magnet, so an explicit Lure branch plus rejection/fallback for unknown keys would be a defensive improvement, not a current missing-item failure.

Two QA passes complete; inventory coverage passes, guide/README accuracy requires the concrete fixes above. Root notified directly.

## Resolution recheck — same inventory agent
Re-read latest source and README after fixes. RESOLVED: Titan description no longer claims slower movement. RESOLVED: DISPLAY_NAMES covers exactly all11 internal keys; F1 guide uses the display map, including Extra Life and Ghost Magnet. RESOLVED: README rule/power table now describes smoke trails, forced skid, nearby zap, ghost-only hiding, slowing everyone, ghost carrying, bumping and200-point ghost reward accurately instead of the obsolete behaviors. Exact timings/stacking/art remain explicitly unverified custom choices.

Executed focused headless assertions: inventory/display key sets equal; Titan has no stale slower text; all expanded label+description lines fit the guide width. Regenerated work/inventory-guide-qa-resolved.png. Inventory/label/documentation findings are now closed. Exact reference artwork is still unknown, not certified identical.

## Poster-based artwork QA — same inventory agent
New supplied evidence inspected directly: work/chomp-power-poster-reference.png, a CHOMPionship promotional power-up poster. Rendered latest F1 screen to work/inventory-poster-qa.png and inspected it visually alongside that poster. This improves the earlier appearance evidence from name-only inference to direct object/silhouette comparison.

Confirmed corrections: Caffeine now has a handled coffee mug with a visible beverage surface rather than a can; Earthquake now has a red box and silver T plunger rather than abstract seismic rings; Ghost Magnet now uses a blue sideways C silhouette with pale metal tips rather than an upright pink horseshoe; Chili Pepper includes a flame; Extra Life uses white 1UP text rather than a green framed badge; Giant Orb no longer has the invented triangle/crown marker. These are materially closer category silhouettes/palettes. All11 remain legible, distinct and correctly paired with labels in F1.

Remaining visible differences (do not call exact art): the original 1UP has an oversized1 and smaller raisedUP, ours uses same-baseline lettering; original smoke bomb has wrapped/segmented shading that our simple sphere lacks; our pepper has a steeper curved orientation; our mug carries an original lightning emblem instead of commercial logo art; our icons have uniform round halos/backgrounds and simplified procedural shading. Gold/green orbs in the poster have smoother broad highlights. These observations do not undermine the confirmed corrections, but prevent a pixel-identical claim. No game code edited by this audit.

## Targeted final icon follow-up
Rendered current F1 guide once to work/inventory-poster-qa-final.png and inspected it. Confirmed tall1/raisedUP, wrapped smoke-bomb seams, diagonal flaming pepper, removal of generic blue disks, and shaded spherical gold/green orbs. All11 shapes remain recognizable and distinct; no visible clipping, overlap or misleading substituted object was found. Guide text still fits.

Remaining differences are fine artwork/proportion details: procedural icons are flatter/simpler and sharper-edged than the poster's smooth 3D illustrations; the mug intentionally uses a different emblem; exact highlights, outline thickness, wrapper geometry, lettering and per-item animation are not matched or certified. This targeted pass closes the previously identified silhouette issues without claiming identical art. No code edits.
