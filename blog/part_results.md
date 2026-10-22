## Results

![](../figures/table_per_scene.png)
*Depth error per town (AbsRel after scale+shift alignment, mean over the clip's interior frames; lower is better). Bold = best in that town. The bottom row is the secondary edge F1, where higher is better.*

![](../figures/depth_by_scene.png)
*The same numbers as bars. No method wins everywhere. The farming village (06) is hard for all of them, because the camera walks past tree trunks a metre away.*

![](../figures/table_verdicts.png)
*Pre-registered verdicts. Ratios are means over the 6 towns with 95% bootstrap CIs. "Wins" counts towns where the first method had lower error.*

![](../figures/hypotheses_ci.png)
*Each line is one hypothesis. A dot left of zero means the first-named method had more depth error. Grey dots are single towns.*

### Finding 1: the end frame helps Veo stay on the street, but only modestly

With only a start frame, Veo has to guess where "40 m ahead" is. Sometimes it guessed well (castle, skyscrapers). Sometimes it turned or invented a new street: in the seaside town, B's depth error was 0.70 against A's 0.27.

Adding the end frame cut depth error by 13% on average, and edge F1 rose 14% (CI +7 to +21%, 5 of 6 towns). But two towns went the other way, so on the pre-registered depth metric the interval (−23% to +48%) doesn't clear my 10% bar. **Inconclusive**, leaning yes.

### Finding 2: start-only Veo lost to a free depth warp

The depth-warp baseline estimates depth once on the start image and pushes the pixels along the true camera path. It's deliberately naïve: no inpainting model, just OpenCV hole filling. It tears and smears near the end (bottom-right panel in the GIF).

Even so, its *geometry* stays roughly right, because it follows the real camera path. Start-only Veo had more depth error than the warp in 5 of 6 towns (mean +65%, CI +10% to +129%). By my pre-registered rule that's **disproven**: Veo given one frame does not follow the street better than a warp.

That's not entirely fair to Veo. The warp knows the true camera motion and Veo only has a text prompt. But it's the comparison a practitioner would make.

### Finding 3: a crossfade tied Veo start+end on geometry

This surprised me. A crossfade is two still images dissolving into each other, which looks awful (row C in the sheets). Yet its depth error was no worse than Veo's start+end clip.

The reason is visible in the contact sheets. Veo's clips are fluent, but *they wander*:
- In the riverside town it plants a large tree in the middle of the street that isn't in the 3D scene.
- In the skyscraper district its middle frames put the walls and the corner at different distances than the real path.

A crossfade can't invent anything, so its depth is always "somewhere between two correct answers".

Edge F1, which rewards sharp structures in the right places, did favour Veo A slightly (+7%, CI 0 to +14%). Veo is the most *plausible* video. It isn't measurably the most *faithful*.

![](../figures/sheet_scene01.png)
*Riverside (01). Both Veo clips grow a large tree that isn't in the 3D town (rows 2–3). The warp (row 5) stays on the true street but smears at the end.*

![](../figures/sheet_scene03.png)
*Seaside hill town (03). Start-only Veo (row 3) leaves the covered arcade for an open road that doesn't exist. With the end frame (row 2), it stays under the arcade.*

![](../figures/sheet_scene05.png)
*Skyscrapers (05), where the crossfade won. Veo's frames look right, but they put the walls and the corner at different distances than the true path.*

![](../figures/compare_scene03_small.gif)
*Seaside hill town, all four views playing.*

### Robustness: the original, denser protocol gives the same verdicts

Scoring had to be cut down (9 frames per clip, 182 px depth) when the shared box was overloaded. Once it freed up, I re-ran the **original** pre-registered density: 33 frames per clip, all 25 ground-truth frames, and the default 518 px depth input.

Every verdict came out the same. H1 moved to +22% (still inconclusive), and the warp-vs-crossfade comparison went from −3% to +10% (still inconclusive). I report the cut-down run as primary because that protocol was fixed before any score existed.

![](../figures/table_robustness.png)
*Primary vs robustness scoring. The verdicts don't change.*

## Is WorldGacha a good test bench?

![](../figures/table_practical.png)
*Reproducibility and practical value, measured along the way.*

- **Reproducibility is the standout.** The same share link gives a byte-identical image after a reload, and a software renderer on another machine gives an image within 0.03/255 of the desktop GPU's.
  - My one H5 "failure" was self-inflicted. The link rounds the camera to 0.1 m, so re-opening a link isn't the *exact* camera I had exported from. That gives a sub-pixel shift at building edges (scenes 02 and 06).
  - By my strict rule (every check must pass) H5 is therefore **inconclusive**, but the town itself never changed.
- **Watch the settings the link doesn't store.** This bit me once: my first ground truth was rendered without Straight verticals.
- **GLB export works:** a 50 MB, 0.9 M-triangle model of the 300 m near area, usable in Blender or three.js.
- **Variety:** the six types gave clearly different streets (edge density 1.7–5.8%), from low village houses to glass towers. Riverside and Castle towns were the most alike.

## How to reproduce

The repo has everything: [github.com/nankris/worldgacha-veo-camera-path](https://github.com/nankris/worldgacha-veo-camera-path).

```bash
pip install playwright numpy pillow opencv-python-headless torch transformers trimesh matplotlib
cd scripts
python gen_scenes.py                 # headless towns + start/end PNGs (Chrome + SwiftShader, no GPU)
python crop16x9.py                   # the exact 16:9 keyframes given to Veo
# Veo: Google Flow, Frames mode, Veo 3.1 Fast, 16:9, 720p, 8 s, x1. Prompts verbatim in FLOW_BRIEF.md
bash capture_queue.sh                # ground-truth camera path, 25 frames per town
WG_SELFTEST=1 python score.py 01     # sanity: ground truth vs itself = 0.000
python score.py && python analyze_wg.py && python h5_determinism.py && python make_visuals.py
WG_FULL=1 python score.py && WG_FULL=1 python analyze_wg.py   # robustness run
```

Prompt A: *"Smooth steady forward dolly at eye level down this street in a quiet town. No people, no cars, no cuts, buildings stay solid, daylight."* Prompt B adds *"The camera moves about 40 metres straight ahead."*

## Limitations

- **6 towns, one clip each.** The plan was 12. I cut it to 6 because of time and a stalled browser, recorded before any scoring. With one Veo sample per town, the CIs are wide, and three of five verdicts are inconclusive for that reason.
- **The metric is a proxy.** Depth Anything V2 on rendered frames isn't true depth, though the same estimator runs on every arm and on the ground truth. Depth error also doesn't punish a crossfade's ghosting, which is why it scores so well. Edge F1 partly compensates.
- **Protocol cut for CPU time:** coarser frame sampling and depth resolution, decided before scoring. The original density gives the same verdicts.
- **Scenes 04–06 differ slightly from 01–03.** They were made headless with fixed seeds and a different camera preset ("Central street · eye level"). Scene 03 moved 35 m, but its prompt said "about 40 metres".
- **Watermark:** a 80×50 px corner is greyed in every frame of every method.
- **Veo settings:** only Veo 3.1 Fast at 720p was tested. Other models, longer clips or better prompts might do better.
- **One shared, heavily loaded CPU box.** Timings are pessimistic.

## Bottom line

If you want a video *of a place that exists*, Veo's beautiful frames are not evidence it followed the place. With only a start frame it wandered further from the real street than a free depth warp. Giving it the end frame helped, but on geometry it still only tied a crossfade.

WorldGacha turned out to be the real find: a free, deterministic, exportable 3D town generator that makes this kind of test cheap and repeatable. The obvious next step is more towns and several Veo samples per town, so the verdicts can firm up.
