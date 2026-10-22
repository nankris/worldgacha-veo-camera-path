# 07: Share links round the camera, so "reload the link" ≠ "the exported view"
- **Symptom:** H5 checks failed in two places:
  - scene 06: link reload vs the exact-camera PNG, MAD 2.37/255, edge F1 0.79.
  - scene 02: browser start PNG vs headless frame 0, MAD 0.60, F1 0.86.
- **Cause:** the `c=` parameter stores the camera with 0.1 m precision (headless-made links) or 0.01 m (the browser operator's 02 link). The difference images show only sub-pixel edge shifts. Two reloads of the same link were byte-identical, and so was the browser reload of 01.
- **Effect:** H5 is INCONCLUSIVE by the strict pre-registered rule (all checks must pass). The town generation itself was deterministic in every check.
- **Practical advice:** if you need the exact camera, save the recipe JSON (it has full-precision `cam`), or set the camera from code.
