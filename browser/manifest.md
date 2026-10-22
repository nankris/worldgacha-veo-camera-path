# WorldGacha browser run — PARTIAL (3 of 12 scenes complete)

Site: https://tools.oyasumi-gamedev.com/worldgacha/?lang=en (opened in its own new tab; Colab tab untouched; no login/pay/forms).
Build id: not shown in UI (page source had WG_WORKER_V="2d68c99a" per task; not re-verified).

## Display
- Browser window maximised on the 1280x800 desktop (not resized). 3D view ~632 x 505 CSS px. 
- PNG export: "PNG (current view)", long side 2400 px -> 2400 x 1919 px.

## Settings (same for scenes done)
Render style Color; People & cars = None; time of day Day (default); lens 24 mm (set via slider after each preset, presets reset it to ~28-30 mm); "Straight verticals" ON; Shadows/Distant windows left at default (on); Light display and Low-poly view OFF (defaults); Season Summer.
### Settings changed (page was too slow: box load average ~30, other jobs running)
- Area (Size / 広さ) 4 km -> 2 km and Near area size 600 m -> 300 m, for ALL scenes (k=300 and size=2000 in every link).

## Scenes completed
01 Riverside country town seed 361462237; 02 Castle town seed 468998665; 03 Seaside hill town seed 485980239. Each: start PNG, end PNG, recipe JSON, links in links.tsv. 01 also has start_reload PNG and scene01.glb (49,759,476 bytes = 47.5 MB, "Include the surroundings" OFF).
Gacha presses: 1 each (scene 01: the page's default seed 581477794 on first load was replaced by the first press -> 361462237).
Camera: "In town (shopping street)" for all three ('Central street · eye level' was tried first for 01/02/03 but a tree/trunk or wall blocked the view). Scene 03 start is under a covered arcade (street, buildings both sides, but roofed).
End camera = start + 40 m (01,02) / 35 m (03) along the same horizontal heading, y/target-y unchanged, same lens, via editing c in the URL and reloading (style Color + Straight verticals re-applied after reload because they are not stored in the link).

## Reload check (scene 01)
start_url opened in a fresh tab -> same view; scene01_start_reload.png is byte-identical to scene01_start.png (cmp: identical). Reload checks for 05 and 12: NOT DONE.

## Oddities
- Link/recipe: "Copy link" only includes c= once the camera is "(Moved camera)". Scene 01's start c came after a stray click that nudged the camera; 02 after one mouse-wheel tick; for 03 start c was taken from the recipe JSON "cam" (pos/target/lens) which gives the preset camera exactly (scene03_recipe.json). 
- Start PNG of scene 03 was first exported blank (WebGL context lost) and re-exported; the blank one was discarded.
- Link style/lens/people are not in the URL; the hash holds r= (type,seed,size,res...), c= camera, k=300 near-area.
- Colour/straight-verticals toggles need re-applying after each page reload; UI lags 10-30 s per action.
- WebGL context lost several times (GPU process crash count 1); at scene 04 (Mountain hot-spring seed 553968321, 1 press) the page stopped initialising after a reload (stays unhydrated in Japanese UI, no gacha button) for >8 minutes while box load avg ~30 (llama-server, eval_sequence jobs of other agents).
## Stop point
Scene 04 gacha pressed (seed 553968321, type onsen, 1 press) but NO scene 04 files exported. Scenes 04-12 not done.

## Run 2 (scenes 04-06) - STOPPED, page did not start
2026-10-22 12:56-13:06 IST: closed crashed + extra Flow tabs (Colab kept), opened WorldGacha in new tab; stayed unhydrated (Japanese static UI, no World Gacha button, empty seed) for 10 min incl. one reload at ~13:03. Box load avg 18-32. No scenes 04-06 produced; links.tsv unchanged.

## Scenes 04–06, generated headless by the experiment agent (13:10–13:16 IST)
The desktop browser could not start WorldGacha (box load), so I made these headless with `scripts/gen_scenes.py`: Chrome + SwiftShader via Playwright, viewport 1600x1100, exported at 2400 px with the app's own PNG exporter.
- Settings: Colour; People & cars None; lens 24 mm (set after the preset); Straight verticals ON; Area 2 km; Near 300 m.
- Types and seeds: 04 `downtown` seed 20261004; 05 `skyscraper` seed 20261005; 06 `rural` (Farming village) seed 20261006. I fixed the seeds up front (date-based) instead of pressing gacha. Every first draw was usable, so none were re-rolled.
- Camera preset: "Central street · eye level" (`center`). "In town (shopping street)", used for 01–03, exists only for `rural`, so I used `center` (available for all three) to keep 04–06 consistent. This is a deviation from 01–03 and is disclosed.
- End: start + 40.0 m along the horizontal heading, with the target shifted by the same offset (same heading, same height).
- Files: scene0{4,5,6}_{start,end}.png (2400x1919), scene0{4,5,6}_recipe.json (the app's "Save recipe"), headless_gen_log.json (exact cameras, preset lists, timings), plus rows in links.tsv.
- Reload check (06): a fresh browser opening start_url renders slightly differently from the original start PNG (mean |Δ| 2.37/255; 4.4% of pixels differ by more than 8). The reason is that the share link rounds the camera to 0.1 m (−7.427 → −7.4). Two independent reloads of the same link were **byte-identical**, so the town itself is deterministic. GT capture for 04–06 uses the exact unrounded cameras, so frame 0 matches the Flow start image.
