# I gave Veo two frames of a 3D town, then checked its video against the real street

*6 free WorldGacha towns, 12 Veo clips, ground truth rendered from the same 3D scene. Veo looked best on edges, but a free crossfade and a depth warp matched its street geometry.*

![](../figures/compare_scene04_small.gif)
*Downtown, a 40 m walk forward. Top left: the true path, rendered from the 3D town. Top right: Veo given the start and end frame. Bottom left: Veo given only the start. Bottom right: a free 2.5D depth warp of the start frame.*

## The short version

- **The idea:** [WorldGacha](https://tools.oyasumi-gamedev.com/worldgacha/?lang=en) is a free in-browser generator of Japanese towns, and the towns are real 3D scenes. I could export a start and an end frame, ask Veo to fill the 8 seconds between them, then render the *actual* camera path and compare.
- **Setup:**
  - 6 towns, 4 methods:
    - Veo with start+end frames
    - Veo with the start frame only
    - a plain crossfade
    - a 2.5D depth warp
  - Depth error is measured with Depth Anything V2.
  - Everything was pre-registered, and the Veo watermark was masked identically everywhere.
- **Giving Veo the end frame:** depth error fell by **13%** on average, and edge match improved by **14%** (CI +7 to +21%). The depth result is too noisy to call (**inconclusive**).
- **Veo start-only vs a free depth warp:** Veo was **worse** on 5 of 6 towns, with 65% more depth error. That one is **disproven**: start-only Veo did not beat a 50-line warp.
- **Veo start+end vs a crossfade:** a tie on depth (−21%, CI −86% to +30%). Veo looks far better, but its geometry wasn't measurably closer to the real street. Veo also invents trees and buildings that aren't there.
- **WorldGacha as a test bench:** excellent. Share links rebuild the town byte-for-byte, headless rendering matches the desktop browser to 0.03/255, and it exports GLB.
- **Cost:** 190 Google Flow credits for 12 clips, plus a CPU box. No GPU.

Thanks for reading Tech in General! Subscribe for free to receive new posts and support my work.

