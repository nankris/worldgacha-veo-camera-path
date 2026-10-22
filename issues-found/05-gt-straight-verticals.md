# 05: First GT captures (scenes 01–03) missed "Straight verticals"
- **Symptom:** the browser operator had "Straight verticals" (2-point perspective, `#twopt`) ON. It isn't stored in the share link, and the headless page defaults to OFF. So the first headless GT renders used 3-point perspective, slightly different from the browser start/end PNGs.
- **Found:** 13:10 IST while reading manifest.md, before any final scoring. The only scoring that had happened was the scene-01 debug run on C/D.
- **Fix:** `scripts/wgpage.apply_style()` sets Colour, straight verticals ON and people & cars none on every headless page. The old captures were moved to `gt_superseded_no_straight_verticals/` (kept for the record), and every scene was re-captured.
- **Status:** fixed.
