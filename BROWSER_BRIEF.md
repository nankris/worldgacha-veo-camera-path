# BROWSER_BRIEF: WorldGacha capture for the Veo keyframe experiment

Written 2026-10-22 ~12:10 IST. Read DESIGN.md (same folder) if you need the why.

## Scope and rules
- Site: https://tools.oyasumi-gamedev.com/worldgacha/?lang=en (free, no login, everything runs in the browser, outputs free for any use, no credit required).
- **No login, no accounts, no payments, and no Veo/Magnific/Flow generations in this step.** This step only builds scenes and exports files.
- Work in a new tab and leave any other tabs (Colab, Substack) alone.
- Put every deliverable in **/workspace/new-exp/worldgacha/browser/**. Browser downloads land in ~/Downloads, so move or rename them there afterwards.
- The site is a beta. Record the build id if one is shown; the page source currently has `WG_WORKER_V="2d68c99a"`. Links can drift between versions, so the PNGs are the ground truth.

## Global settings (keep identical for every scene)
- UI language English (`?lang=en`).
- Render style **Color**. Don't use line art, tone or white model.
- **"People & cars": off/none.** They're parked and static, but switching them off removes clutter that Veo would animate.
- Time of day/light: default (day). Don't touch the light/tone panel.
- Lens: **24 mm** (default). **"Keep verticals straight": ON.**
- Maximise the browser window, and don't resize it between start and end captures. Write the 3D view's pixel size in the manifest.
- Leave "light display"/low-poly at defaults unless the page is unusably slow. If you change it, change it for all scenes and note it.

## Scenes (12)
Use each of the 9 region types once, then add 3 extra scenes with new seeds:
These are the exact English UI labels: 01 Riverside country town, 02 Castle town, 03 Seaside hill town, 04 Mountain hot-spring town, 05 Downtown, 06 Skyscrapers, 07 Suburban neighborhood, 08 Farming village, 09 Water city above the falls. For the extras, gacha again: 10 Riverside country town, 11 Castle town, 12 Seaside hill town.

For each scene:
1. Select the region type, then press **🎲 World Gacha** once. If the town is clearly broken or empty, press it again. Record the **seed** from the seed box, plus how many presses it took.
2. **Start camera.** Pick a street-level camera from the camera candidates. Prefer them in this order: "Central street · eye level", "In town (shopping street)", "Eye level (town center)", "Between towers (avenue)", "Station square", "Crossing N", "Narrow lane downtown". Avoid "Overview", "Top", "Whole region", "From the air" and "Lookout". You need a view that **looks down a long, fairly straight street with buildings on both sides**. If no preset gives that, click the map to stand on a straight street. Don't use the 🎲 Camera button; it isn't reproducible.
3. Press **🔗 Copy link** and save the URL as `start_url`. The hash holds the camera as `c=x,y,z,tx,ty,tz,lens`.
4. Export **PNG (current image)** at long edge **2400 px** and save it as `sceneNN_start.png`.
5. **End camera.** Move the camera **forward along the same street, about 30–60 m, keeping the same heading**. A good end view shows buildings that were mid-frame in the start view now near the edges. Don't turn corners or pass through buildings. The camera should only move, with no rotation and no lens change. Either click the map further along the same road and re-aim to the same heading, or edit `c` in the link (add the same offset to x,z and tx,tz) and load it. Then **🔗 Copy link** → `end_url`, and export `sceneNN_end.png` the same way.
6. **Reproducibility check (do this for scenes 1, 5 and 12 only).** Open `start_url` in a fresh tab and check it shows the same view. Export it as `sceneNN_start_reload.png`.
7. **Save recipe** (JSON) → `sceneNN_recipe.json`.
8. **Scene 1 only:** export **GLB** with the near area only ("include distant view" OFF) → `scene01.glb`, and note its file size. It's a fallback for box-side rendering.

## Deliverables in /workspace/new-exp/worldgacha/browser/
- `sceneNN_start.png`, `sceneNN_end.png`, `sceneNN_recipe.json` for NN = 01..12
- `scene01_start_reload.png`, `scene05_start_reload.png`, `scene12_start_reload.png`, `scene01.glb`
- `links.tsv` with columns: `scene  region_type  seed  gacha_presses  camera_preset  start_url  end_url`
- `manifest.md`: build id, window/3D-view size, PNG pixel size, any setting you had to change, whether the reload checks matched, and anything odd (slow, crashes, lens not 24, people/cars toggle not found).

## Stop conditions
- If the site needs a login, shows a paywall, or asks for any submission, stop and report it.
- If it's too slow to use, shrink "Area" (広さ) to 2–4 km and "Near-view area" (近景の広さ) to 300 m for **all** scenes, and note that.
- If you can't remove people/cars, continue and note it. The ground-truth renderer will then be the same page, so they'll match as long as they're static per link.

## What happens next (not your job now)
On the box, I'll interpolate the camera between `start_url` and `end_url` and capture a dense ground-truth path of about 33 frames per scene from the same page, using headless Playwright on the box and these links. If headless WebGL fails, a short phase-2 brief will ask the browser to load about 9 interpolated links per scene and export PNGs.
