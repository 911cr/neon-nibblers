# Revision 5 review and QA status

Ten separate topic agents completed an initial research audit, then the same agents performed two QA passes. Reproducible failures were fixed and the relevant agents rechecked them. No agent certified a perfect commercial match. Final targeted reviews report no remaining reproduced blocking failures in their scopes; reference uncertainties remain open.

| Topic | QA outcome / fixes |
|---|---|
| Player interactions | Fixed head-on crossing, cooldown overlaps, eight-player crowds and delayed bonus life; targeted recheck passed |
| Gates | Twin contours, hatch alignment and crossing state; stale stun/clock cleared; 32 gate scenarios passed |
| Power inventory | All11 categories/icons/labels/guide rows checked; stale descriptions corrected |
| Power effects | 14 focused runtime cases plus slowdown/stacking checks passed; unsupported exact ranges/timings remain open |
| Power placement/cadence | 16 scenario groups and4400 occupied-cell-safe spawn cases; clocks reset; cadence explicitly custom |
| Edges/tunnels | 32 player seam scenarios/512frames and16 collectible scenarios/256frames; opacity/giant thresholds/HUD clipping fixed |
| Walls | All-map connectivity/visible routes and giant/corner stress renders passed; authored topology still differs |
| Ghost starts | 12 count/map configurations checked; staging/reset valid, exact original order unknown |
| Ghost exits | 16 direct cases and48 repeated lifecycle cycles; visible doorway return fixed |
| Player/ghost/powers | Eight scenario groups; expired/dead-owner weapons and safe hunter eating fixed |

The integrated headless suite passes25 tests. Native Windows1/2/8-player autoplay and regenerated recordings use the revised build. Physical USB controllers/eight humans and native Linux graphics/audio remain unverified. Linux CI is a headless software check, not hardware validation.

Detailed audit notes are in docs/audits. Some earlier sections describe old bugs and failed intermediate versions; later QA and resolution sections record the fixes. Open GitHub issues separate remaining evidence gaps from verified implementation behavior.
