# WorldGacha experiment: process log (IST)

| Time | Step | Commands / files | Outcome |
|---|---|---|---|
| 11:55–12:20 | Scouted the site; wrote DESIGN.md v1 + BROWSER_BRIEF.md | `curl tools.oyasumi-gamedev.com/worldgacha/`, grepped i18n labels | Share link hash carries the camera `c=x,y,z,tx,ty,tz,lens` plus `r` (type, seed, size) and `v` (view). The render mode isn't in the link. |
| 12:05 | Flow brief + Amendment 1 (Veo via Flow, watermark mask, H4/H5) | FLOW_BRIEF.md | User approved Flow credits only |
| 12:08 | Browser PNGs are 2400×1919 (aspect 1.2507), not 16:9 | scripts/crop16x9.py → flow_inputs/*_16x9.png (2400×1350) | Flow gets the same crop as the GT |
| 12:10 | Headless probe 1: page screenshot timed out (SwiftShader busy) | scripts/probe.py | Switched to the app's own PNG exporter |
| 12:12 | Probe 2: exporter works headless (~73 s first frame), but it rendered line+tone, not colour | scripts/probe2.py | Clicking `#modes button[data-k=color]` is required |
| 12:14 | Camera control: set `VIEW.camera.position` / `VIEW.controls.target` in page JS | scripts/capture.py | Interpolated cameras render correctly (visual check) |
| 12:16 | Aspect match: viewport 1600×1000 gives a 1.320 canvas; 1600×1100 gives 1.2507 = browser | scripts/canvas_probe.py | Viewport fixed at 1600×1100 |
| 12:17 | GT queue started (25 frames/scene, memory-gated) | scripts/capture_queue.sh → gt/ | 17–40 s/frame idle, up to ~140 s under load 30 |
| 12:20 | Clarification 2 (metric definitions; Depth Anything V2 Small = relative disparity → aligned AbsRel) | DESIGN.md | — |
| 12:42 | Scene 01 capture ended at 24/25 (timeout) | issues-found/02 | Resume added |
| 12:45 | Debug scoring of scene 01 (C, D only) | scripts/score.py | Found D pinholes (issues-found/03) |
| 12:51 | Flow pilot in (Veo 3.1 Fast, 20 credits/clip); watermark located | mask.json (x1200–1280, y670–720) | Clarification 3 |
| 12:53 | User scope cut to 6 scenes | Amendment 2, issues-found/01 | — |
| 12:58 | D-warp fix (2×2 splat, fit over all pixels after inpaint) | Clarification 4 | — |

| 13:07 | Parent: the desktop browser can't start WorldGacha, so generate 04–06 headless | Killed score.py and capture_queue (no capture during heavy scoring) |
| 13:09 | Found `#twopt` (straight verticals) defaults OFF headless and isn't in the link | GT 01–03 superseded (issues-found/05). `scripts/wgpage.py apply_style()` now sets colour + twopt + crowd 0 |
| 13:10 | `gen_scenes.py 04`: downtown seed 20261004, preset "Central street · eye level", lens 24, end +40 m | 113 s. Visual check OK: street-level, verticals straight |
| 13:11 | `gen_scenes.py 05 06` started in the background | Seeds 20261005 (skyscraper), 20261006 (rural). Seeds fixed before looking (date-based) |
| 13:15 | 05, 06 generated (156 s, 90 s). Visual check: 05 skyscraper street, 06 tree-lined village road | Preset `center` used for all of 04–06 (`street` only exists on rural) |
| 13:16 | `crop16x9.py` → flow_inputs/scene04–06 *_16x9.png (2400x1350); wrote flow_inputs/READY_04_06 | GaussiAnimate mid-run, so marker instead of a turn end |
| 13:18 | Reload check 06: link reload ≠ original (link rounds c to 0.1 m), reload1 == reload2 byte-identical | capture.py uses exact cams from headless_gen_log for 04–06 |
| 13:21 | `doc_shots.py`: 1920x1200 viewport landing/town full page + element shots (region picker, settings, view bar, camera presets expanded via select.size, export card, copied link via clipboard) | First pass at 1x was too small for elements → re-shot at deviceScaleFactor 2 |
| 13:25 | GT queue restarted (after doc shots) for 01–06, K=25, with straight verticals | — |
| 13:30 | Re-captured GT 01 frame 0 (straight verticals ON) vs browser start PNG: mean abs diff 0.028/255, 0% px >8 (old capture without twopt: 0.755, 2.5%) | twopt fix confirmed; also an early H5 cross-machine data point. ~26 s/frame |
| 13:30 | GLB stats scene01: 49.8 MB, 48 meshes, 159 nodes, 0.90 M tris, 1.15 M verts, ~23 materials, extents 316x53x323 m (= near area) | results/glb_stats_scene01.json |
| 13:46 | All 12 Flow clips present (parent). Credits 1,050→860 = 190 total; batch 3 sequential = 20/clip | issues-found/04 updated |
| 13:50 | score.py: grey-mask the watermark rect in every frame (GT + arms) before depth/edges; GT-self sanity mode (WG_SELFTEST=1); saves 640x360 frames for visuals. Cache cleared (old unmasked debug cache) | Amendment 1 compliance |
| 14:14 | h5_determinism.py (partial): browser reload 01 byte-identical; headless vs browser 01 start/end MAD 0.03; 02 start MAD 0.60, F1 0.86 (edge-only sub-pixel shift, see _tmp diff; link c rounded to 0.01 m vs operator's exact camera); 02 end MAD 0.03 | camera precision of share links, not non-determinism |
| 14:50 | Checkpointed nohup `wg_pipeline.sh`: waits for capture, then selftest → score (skips scenes already scored) → analyse → H5 → visuals | Survives agent interruptions |
| 15:10 | Repo hygiene: account e-mail/URL redacted in FLOW_BRIEF/pilot_log (originals in _private/, gitignored); internal paid-API cost estimate redacted from DESIGN.md (user: keep private) | — |
| 15:12 | Flow screenshots for the blog: browser chrome (tabs, project URL) cropped, avatar blurred → flow/doc/blog_*.png | Privacy |
| 15:45 | DA-V2 timing on the loaded box: 18–46 s/frame (pipeline, 518 px); bare forward 13 s @266 px, 26–33 s @518 | 942 inferences = 4–7 h, infeasible |
| 15:52 | Clarification 6 (before scoring): DA input 182 px, 9 arm frames, 13 GT frames; rules unchanged | Same for all arms; disclosed |
