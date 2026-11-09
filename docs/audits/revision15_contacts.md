# Revision15 independent player-contact review

The previous instant push was replaced by root's whole-group rollback, follower reservations and a one-step recoil at normal movement cadence. Buffered wanted input is preserved and repeated contact events are suppressed during the contact cooldown. Damaged actors are excluded from the pending bump group so a later giant hit cannot rewind a respawn.

## Concrete defect found and corrected

A stationary target's away vector was computed against the attacker's post-move position, which coincided with it. The zero vector selected an arbitrary up direction, including in horizontal corridors and tunnel wraps. Root corrected the zero-direction case. Deeper review expanded stationary detection to actors that did not move this tick despite a nonzero buffered heading; these now recoil with the incoming actor's direction rather than back toward that actor. Existing input intent remains unchanged.

## Radius-aware approach addition

Root requested a broader contact threshold to address adjacent normal bodies visually overlapping14px (radius17 each, cellspacing20) before a same-cell test fired. player_contacts.approaching_contact now retains classic coincidence/swap checks and adds bounded legal-corridor distance: normal/normal34px, mixed53px, giant/giant72px. The graph walk accounts for tunnels and does not cross walls. Equal-size radius contacts require shrinking separation, so coasting followers are not repeatedly blocked. A giant and smaller player can contact without movement after growth. Private bay endpoints are excluded from this radius addition because their rendered spacing differs from the tile graph.

This remains a discrete corridor-distance approximation. It is not a continuous Euclidean disc solver, has not recovered DX contact radii or timing, and does not promise no visual overlap for unchanged formations or around corners. Logical giant size changes immediately while its visual growth animation interpolates. These limits must remain explicit.

## Independent tests and second pass

Eleven tests passed in0.085s: stationary receiver recoil; tunnel stationary receiver; head-on tunnel rollback with held input; all four maps with eight held players for360ticks checking unique/legal cells and no per-tick movement beyond one legal step; approaching normal/giant radii across all maps; unchanged follower separation; stationary growth damage; private-bay exclusion; a U-corridor wall separation; cadence-stationary target with nonzero heading; and actual Match integration rolling back before inline visual overlap then applying growth damage. No game.py edits were made by this reviewer; root integrated the hook.

Assigned contact implementation approved against these original rules. Full combined regression, native play and release packaging remain root-owned. No physical USB test or exact commercial-physics certification is implied.
