# How to reproduce

Everything except the Veo clips runs on a CPU-only Linux box with no GPU. All times below were measured on a shared 16 GB box under heavy load (load average 15–38).

## 1. Environment
```bash
python3 -m venv env && . env/bin/activate
pip install playwright numpy pillow opencv-python-headless torch transformers trimesh matplotlib
# Google Chrome stable at /usr/bin/google-chrome (Playwright drives it; WebGL via SwiftShader, no GPU needed)
```

## 2. Towns: start/end keyframes
- Scenes 01–03 were made by hand in a desktop browser. `browser/links.tsv` has the share links, and `browser/*_recipe.json` has the app's own "Save recipe" files.
- Scenes 04–06 were made headless:
```bash
cd scripts && python gen_scenes.py            # -> browser/scene0{4,5,6}_{start,end}.png, recipes, headless_gen_log.json
python crop16x9.py                            # -> flow_inputs/*_16x9.png (2400x1350), the exact Veo keyframes
```
- Settings that the share link does **not** carry have to be set again after every load. `scripts/wgpage.py: apply_style()` does it:
  - Colour render mode
  - Straight verticals ON
  - People & cars = None
  - PNG long side 2400 px
- Area 2 km and Near 300 m are in the link (`size`, `k`).

## 3. Veo clips (manual, Google Flow)
- Settings: Veo 3.1 Fast, Frames mode, 16:9, 720p, 8 s, 1 output.
- Arm A: start + end frame. Arm B: start frame only.
- The prompts are verbatim in `FLOW_BRIEF.md`, and credits per clip are in `flow/pilot_log.md`.
- Download the "Original size 720p" file as `flow/sceneNN_{A,B}.mp4`.

## 4. Ground-truth camera path
```bash
python capture.py 01 25 ../gt/scene01        # 25 frames along the linear start->end camera path, via the app's PNG exporter
bash capture_queue.sh                         # all scenes, memory-gated, resumable
```
About 25–45 s per frame on SwiftShader, so roughly 12–20 min per scene.

## 5. Scoring and analysis
```bash
WG_SELFTEST=1 python score.py 01              # sanity: GT vs itself must score ~0 (got 0.000)
python score.py                               # all scenes -> results/sceneNN.json (+ frames for figures)
python analyze_wg.py                          # bootstrap CIs, verdicts -> results/summary.json, figures/
python h5_determinism.py                      # reload/re-render checks -> results/h5_determinism.json
python make_visuals.py                        # contact sheets, GIFs, gallery
python variety.py                             # descriptive variety
WG_FULL=1 python score.py && WG_FULL=1 python analyze_wg.py   # robustness at the original density
```
- Metric: Depth Anything V2 Small disparity, AbsRel after scale+shift alignment, monotone DTW against the GT path.
- The watermark rectangle in `mask.json` is greyed in every frame of every arm and in the GT.
