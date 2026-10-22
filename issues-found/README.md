# Issues found (WorldGacha × Veo camera-path test)

| # | Issue | Status |
|---|---|---|
| 01 | Scope cut 12 → 6 scenes (user, CPU saturation) | accepted, disclosed |
| 02 | GT capture timeout at 24/25 frames under load | fixed (resume + longer timeout) |
| 03 | Depth-warp pinholes and degenerate scale fit | fixed before final scoring |
| 04 | Flow credits: 4 clips cost 30 instead of 80 | observation |
| 05 | First GT captures lacked straight-verticals (not in link) | fixed, re-captured |
| 06 | Depth scoring too slow on the loaded CPU box | protocol cut before scoring; original density re-run as robustness, same verdicts |
| 07 | Share links round the camera (0.1 m), causing sub-pixel H5 mismatches | disclosed; H5 INCONCLUSIVE |
