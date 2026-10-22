# WorldGacha → Veo: can Veo fly a camera through a real 3D town? (design v1, pre-registration draft)

Status: DESIGN ONLY, written 2026-10-22 ~12:15 IST. Nothing has been generated and no credits have been spent.

## Question
If Veo 3.1 is given the **first and last frames of a known camera move** rendered from a procedural 3D town (WorldGacha), does the in-between video follow the real 3D geometry? Or does it just morph/crossfade, or invent a different street?
WorldGacha gives exact ground truth: the camera is in the share-link hash (`c=x,y,z,tx,ty,tz,lens`), and the same page renders any interpolated camera.

## Arms (per scene; 12 scenes from BROWSER_BRIEF.md)
| Arm | Input | Source |
|---|---|---|
| A: Veo keyframes | start PNG + end PNG + fixed prompt | Veo 3.1 Lite, 8 s, 720p, 16:9, no audio |
| B: Veo start-only | start PNG + same prompt with an explicit "camera dollies forward ~40 m down the street" | Veo 3.1 Lite, same settings |
| C: Crossfade (trivial floor) | linear blend start→end | box, free |
| D: 2.5D parallax (cheap geometry floor) | Depth Anything V2 Small depth of start PNG, forward dolly warp to the same displacement | box, free (`social-plans/ai-metro-character/tools/parallax25d.py`) |

Fixed prompt (A/B): "Smooth steady forward dolly at eye level down this street in a quiet town. No people, no cars, no cuts, buildings stay solid, daylight." (B adds the distance sentence.)

## Ground truth and metric
- GT path: about 33 frames per scene along a linear interpolation of position/target (lens fixed at 24 mm) between `start_url` and `end_url`. They're captured from the same WorldGacha page via headless Playwright on the box; the fallback is phase-2 browser capture of 9 frames.
- Gate before any credits: re-render the start camera headlessly and compare it with the browser's `sceneNN_start.png`. Edge-F1 must be ≥ 0.9 at 2 px tolerance, otherwise fix the capture first.
- Everything is resized/cropped to 1280×720 (centre crop to 16:9).
- Veo/arm frames are sampled at 4 fps (33 frames over 8 s). Timing may ease in/out, so each arm's frames are aligned to the GT path with **monotone DTW**, with endpoints pinned.
- **Primary metric:** mean scale-invariant log depth error (SI-log) between arm frame and aligned GT frame, using Depth Anything V2 Small on both (so GT is "depth-of-render", the same estimator for both, which removes estimator bias). Averaged over interior frames.
- Secondary: Canny edge F1 at 1% of the image diagonal; LPIPS; "geometry hallucination" rated blind (shuffled, arm-masked) on a 0–2 scale for building permanence and street layout.
- Veo may add its own watermark/SynthID; this route is the Magnific API, where none is visible. Google Flow free is **not** used because it forces a visible watermark in India, and free personal access is unverified.

## Pre-registered hypotheses (n = 12 scenes, paired; scene-level bootstrap, 10,000 resamples, 95% CI)
- **H1 (keyframes help):** relative SI-log reduction of A vs B, r1 = mean_s (B−A)/B.
  PROVEN if LB(r1) ≥ 0.10. DISPROVEN if UB(r1) < 0.10. Otherwise INCONCLUSIVE.
- **H2 (Veo beats a crossfade):** r2 = mean_s (C−A)/C. PROVEN if LB(r2) > 0. DISPROVEN if UB(r2) ≤ 0.
- **H3 (Veo beats the cheap 2.5D warp, start-only):** r3 = mean_s (D−B)/D. PROVEN if LB(r3) > 0. DISPROVEN if UB(r3) ≤ 0.
- Power caveat: n = 12 is a small pilot-scale sample. Effects under about 15% will likely come out INCONCLUSIVE; the post must say so.
- Exclusion rule, fixed now: a scene is dropped only if the GT gate fails or a Veo job errors twice. Content-based exclusion isn't allowed. All drops are reported.

## Cost
*[Redacted for publication on 2026-10-22: an internal paid-API cost estimate for the Veo arms, which was not used. The unredacted file is kept privately. No pre-registered rule depended on it.]*

## Steps
1. Browser: BROWSER_BRIEF.md (12 scenes, start/end PNGs, links, recipes).
2. Box: headless GT capture + gate; build arms C/D; metric code tested on C/D, with an A/B dry run using GT itself, which must score ≈ 0.
3. User OK → pilot scene 01 (2 clips). Check the frame count, the DTW sanity and whether Veo honours the end frame.
4. Full 24 clips → analysis → post + figures (side-by-side strips: GT | A | B | C | D).

---
## AMENDMENT 1: pre-registration of the arms actually run (written 2026-10-22 12:01 IST, BEFORE any GT capture, generation or scoring)
- **Magnific is not used.** The cost section above is superseded, internal only, and redacted.
- Veo arms A and B run on **Google Flow credits only** (user approval 2026-10-22 ~12:00 IST). Model: Veo 3.1 Fast (or Lite if Fast is unavailable), the same for all clips, 8 s, 16:9, 720p, 1 output per prompt. Prompts are exactly as in FLOW_BRIEF.md. 12 scenes × 2 arms = 24 clips including the 2-clip pilot (scene 01).
- **Watermark handling:** Flow puts a visible watermark on videos in India. Its region, plus a margin of 2% of width and height, is located once from the pilot clips. That **same fixed rectangle is masked (set to mean grey, depth/edge metrics ignore masked pixels) in every arm's frames AND in the GT frames**, including the C/D baselines. If Flow crops/reframes the input, GT and baselines get the identical crop. Both are disclosed in the post.
- **Free arms (C crossfade, D 2.5D depth-warp) and the GT capture are scored regardless of Veo.** If the Veo arms don't complete, H1/H2/H3 are reported INCONCLUSIVE (not run), and the Veo-free analysis below stands alone.
- **Veo-free hypotheses (H4, H5), fixed now:**
  - H4 (cheap geometry beats a crossfade): r4 = mean_s (C−D)/C on the primary DTW SI-log depth metric. PROVEN if LB(r4) > 0. DISPROVEN if UB(r4) ≤ 0.
  - H5 (WorldGacha is deterministic): a scene reloaded from its share link reproduces its exported PNG. Gate: edge-F1 ≥ 0.95 at 2 px **and** mean absolute pixel difference ≤ 2/255 on all reload checks, which are the 3 browser reloads plus a headless re-render of every scene's start and end camera.
    - PROVEN if all checks pass.
    - DISPROVEN if any browser reload fails both thresholds.
    - Otherwise INCONCLUSIVE, for example when only the headless rendering differs, which points to a renderer difference rather than non-determinism.
- **Descriptive only (no verdict):** variety across the 9 types (pairwise LPIPS and edge-density/depth-histogram distance between scene start frames, within type vs across type), GLB size, load time and mesh/material counts (trimesh), and time per scene for the browser operator.

## CLARIFICATION 2 (2026-10-22 12:17 IST, before any scoring; tooling tested only on scene 01 capture/visual checks)
- **GT capture works headless:** Chrome + SwiftShader, the page's own "PNG (current view)" exporter at 2400 px, viewport 1600×1100. That gives the same canvas aspect (1.2507) as the browser PNGs (2400×1919). The camera is set by `VIEW.camera.position/controls.target` along a linear interpolation of the share-link `c` values. The colour mode is clicked explicitly, because the link doesn't carry the render mode. About 25 s per frame.
- **GT density:** K = 25 frames per scene (alpha = 0, 1/24, …, 1) instead of about 33, because of capture time. Arms are sampled at 33 frames (4 fps over 8 s; crossfade/warp also generate 33).
- **Common frame:** every image (GT, arms, browser PNGs) is centre-cropped to 16:9 at full width (2400×1350), then resized to 1280×720. The Flow inputs are exactly these crops (`flow_inputs/*_16x9.png`). The watermark mask from Amendment 1 is applied to all arms and the GT.
- **Primary depth metric, made precise:** Depth Anything V2 Small outputs *relative inverse depth* (it's affine-invariant), so a log-depth SI error isn't well defined. Primary metric = **AbsRel of the arm's disparity after least-squares scale+shift alignment to the GT frame's disparity** (MiDaS protocol), over unmasked pixels. Lower is better. The hypotheses' r-ratios use this metric unchanged.
- **DTW:** cost(i,j) = the primary metric between arm frame i and GT frame j. Monotone DTW with both endpoints pinned. The scene score = mean over interior arm frames (i = 1..31) of the cost of the GT frame matched to it, taking the minimum if several are matched.
- **Arm D, made precise (cheap geometry):** the start frame is forward-warped (z-buffered splat) along the true interpolated camera path. Intrinsics come from the page's camera (`VIEW.camera.fov`, recorded at capture). Depth = 1/(s·disparity + t), where DA-V2 disparity is on the start frame and (s, t) is a 2-parameter grid/LS fit that best predicts the **end frame** when warped by the full move. So D uses the same two images as C/A. Holes are filled with cv2.inpaint (Telea, radius 3).
- **Arm C:** linear RGB crossfade start→end, 33 frames.
- **Secondary edge metric:** Canny (thresholds 100/200 on grayscale) F1 at a tolerance of 1% of the image diagonal, on unmasked pixels.
- **H5 measurement details:**
  - Browser reload PNG vs browser original PNG, at full 2400 px resolution: mean absolute difference (MAD) and edge-F1 at 2 px.
  - Headless frame 0 / frame K−1 vs the browser start/end PNGs, same metrics.

## CLARIFICATION 3 (2026-10-22 12:52 IST, after the pilot clips were downloaded, before any Veo frame was scored)
- Watermark mask fixed as `mask.json`: rectangle x 1200–1280, y 670–720 in 1280×720 coordinates. It was found by eye on one pilot frame and covers the "Veo" mark with at least a 2% margin.
- Pilot facts: Veo 3.1 Fast, 720p, 8 s, x1, 20 credits per clip; Flow showed no crop box.
- The scene 01 debug scoring run (12:45 IST) scored only arms C and D, the code check. Its numbers are kept as computed. It ran with no mask, so scene 01 will be re-scored with the mask together with A and B.
- **If fewer than 12 scenes are available today, the result is reported as a pilot (n = the scenes available), with that disclosed.** The decision rules stay unchanged; with n ≤ 3 they will almost surely give INCONCLUSIVE, and the post must say so.

## AMENDMENT 2: scope cut to 6 scenes (2026-10-22 12:54 IST, before any Veo frame was scored)
- **The user cut the scope** to 6 scenes because the box is CPU-saturated (load about 30) and the browser capture had stalled. The scenes are 01 Riverside country town, 02 Castle town, 03 Seaside hill town, 04 Downtown, 05 Skyscrapers and 06 Farming village. They are renumbered consecutively by the browser operator (correction noted 12:55 IST). There are 12 Veo clips in total (A+B per scene, Veo 3.1 Fast, 20 Flow credits each).
- n = 6 replaces n = 12 everywhere. The decision rules for H1–H5 are unchanged; with n = 6 the bootstrap CIs will be wide. The post reports this as a **6-scene study**, with that disclosed. If fewer than 6 scenes finish, it becomes a pilot with n = the scenes completed (Clarification 3).
- H5 reload checks: the browser reloads that exist (scene01 is byte-identical per the operator), plus headless re-renders of every scene's start and end frames.

## CLARIFICATION 4 (2026-10-22 12:54 IST): arm-D bug fix before final scoring
- The 12:45 debug run on scene 01 showed a **pinhole-grid artifact**: forward splatting with a 1-pixel footprint leaves gaps when the view zooms in. The D-fit also hit the edge of its grid (z_near = 60 m), because the fit required at least 30% non-hole coverage and so rewarded depths that barely move the image.
- Fix: a 2×2 splat footprint. The (z_near, z_far) fit now minimises the end-frame MAD over **all** pixels after the same Telea inpainting the arm uses, with the coverage filter removed.
- Disclosure: I saw scene 01's debug numbers (unmasked: C 0.152, D 0.189 depth AbsRel) before this fix. The fix is a correctness fix that was visible in the warped images, not tuning against the metric. Every scene, including 01, is re-scored with the fixed code and the mask.

### Clarification 5 (2026-10-22 13:22 IST, before any final scoring)
- Scenes 04–06 were generated headless (gen_scenes.py) with fixed seeds 20261004/5/6, preset "Central street · eye level" (01–03 used "In town (shopping street)", which downtown/skyscraper lack) and end = +40 m. Same render settings as 01–03.
- Ground truth for all 6 scenes is re-captured with Straight verticals ON (issues-found/05). The earlier 01–03 captures are superseded and not scored.
- H5 determinism, refined: (a) link reload vs link reload must be byte-identical; (b) headless frame 0 vs the start PNG is reported as mean |Δ| and percentage of pixels with |Δ| > 8. For 01–03 that is across machines/GPUs (browser vs SwiftShader); for 04–06 it is within headless. Camera rounding in links (0.1 m) is disclosed as a source of difference.

### Clarification 6 (2026-10-22 15:52 IST), before any final scoring: CPU budget
- **Why:** timing tests on the shared box (load 20–30) gave 13 s for a bare Depth Anything V2 Small forward pass at a 266 px input, and 26–33 s at the default 518 px. The pre-registered density (25 GT + 4 × 33 arm frames per scene, 942 inferences) would need about 4–7 h, which isn't feasible today.
- **Changes, identical for GT and every arm, all decided before any score was computed:**
  1. Depth-model input short side is **182 px** (default 518). Same model and weights, aspect kept, multiple of 14. All metrics were already computed on 320×180 maps, so this matches the metric's own resolution.
  2. Arms are sampled at **9 frames** (every 1 s of the 8 s clip, endpoints included) instead of 33. C and D are generated at the same 9 path positions.
  3. GT uses **13 of the 25** captured frames (every 2nd: alpha = 0, 1/12, …, 1).
  4. DTW, the AbsRel alignment, the edge F1, the mask and all decision rules are unchanged. The scene score is the mean over the **7 interior** arm frames.
- **Consequence:** coarser time sampling makes DTW matching less fine-grained, and the depth maps are coarser. Both affect every arm equally. Disclosed in the post.
- Figures and GIFs use all 25 GT frames, since they need no depth inference.
