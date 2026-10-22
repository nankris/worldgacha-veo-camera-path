| Question | What I measured |
|---|---|
| Does a share link rebuild the same town? | **Yes.** Reloading a link gave byte-identical PNGs, in the desktop browser (scene 01) and headless (scene 06, twice). |
| Same image on a different machine and renderer? | Nearly. Desktop Chrome (GPU) vs headless Chrome (software SwiftShader) differed by a mean of 0.03–0.80 / 255 per pixel at the start and end frames. |
| What the link does **not** store | Render style (colour / line art), Straight verticals, People & cars, and camera precision beyond 0.1 m. Re-apply them after every load. |
| 3D export (GLB, scene 01) | 49.8 MB, 0.90 M triangles, 1.15 M vertices, 48 meshes, ~23 materials. Covers the 316 × 323 m near area. Loads in trimesh in seconds. |
| Rendering on a CPU-only box | Page load 47–300 s. One 2400 px PNG takes 25–70 s on software WebGL. A 25-frame camera path took 12–40 min per town. |
| Veo in Google Flow | Veo 3.1 Fast, 720p, 8 s: 55–90 s per clip, 20 credits each. 190 credits for all 12 clips. A small "Veo" watermark is forced in my region. |
| Variety across region types | Six types gave visibly different streets. Edge density ranged 1.7–5.8%, and the pairwise depth-histogram distance (JS) was 0.04–0.21. Riverside vs Castle were most alike; Castle vs Downtown least. |
