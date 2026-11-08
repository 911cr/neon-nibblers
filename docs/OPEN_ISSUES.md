# Remaining verification work

- [Match maze topology and character artwork against timestamped reference](https://github.com/911cr/neon-nibblers/issues/1)
- [Verify gate operation, permissions and release timing against Deluxe footage](https://github.com/911cr/neon-nibblers/issues/2)
- [Measure power-up spawn locations, probabilities and cadence](https://github.com/911cr/neon-nibblers/issues/3)
- [Verify power timing, damage and stacking interaction matrix](https://github.com/911cr/neon-nibblers/issues/4)
- [Verify ghost starting order, release AI and frightened appearance](https://github.com/911cr/neon-nibblers/issues/5)
- [Playtest physical USB controllers and Linux graphics/audio](https://github.com/911cr/neon-nibblers/issues/6)

Controller hardware testing is deferred to production verification by user direction. Development uses explicit simulated availability; normal launches retain real missing/disconnect detection. No cabinet is available; reference research is online-only. Audibility was not observed by the user.

## Revision 8 evidence gaps

- [Verify DX independent joining and Find My Pac lifecycle](https://github.com/911cr/neon-nibblers/issues/7)
- [Recover DX score values, bonus repetition and final ranking behavior](https://github.com/911cr/neon-nibblers/issues/8)
- [Implement evidence-based attract, operator and spectator display lifecycle](https://github.com/911cr/neon-nibblers/issues/9)

Independent stations, score ledger/replay and explicit map records now work and have tests. Their unknown commercial rules remain open; nine tracked gaps are not a claim of nine reproduced software failures. Revision8 code passed63 tests locally on Windows/Ubuntu,63 tests from the extracted package, and all four Windows/Ubuntu × Python3.11/3.14 CI jobs (run42524739127). See DX_FEATURE_PARITY.md for scope and evidence.
