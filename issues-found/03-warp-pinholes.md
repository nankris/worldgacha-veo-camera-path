# 03: Arm D (2.5D depth warp) pinhole artifact and degenerate depth fit
- **Symptom:** in the debug run, the warped frames showed a regular grid of black pinholes, and the depth-scale fit picked z_near = 60 m, the edge of its grid.
- **Root cause:** forward splatting with a 1-pixel footprint, plus a fit that only scored non-hole pixels with a ≥30% coverage filter. That favoured depths that barely move the image.
- **Fix:** a 2×2 splat footprint, and a fit on all pixels after Telea inpainting. Recorded in DESIGN.md Clarification 4.
- **Status:** fixed before final scoring. The scene 01 debug numbers (seen) are disclosed.
