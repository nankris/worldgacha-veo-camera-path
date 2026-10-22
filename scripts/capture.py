"""Headless GT capture: load a scene's start_url once, set interpolated cameras, export PNG via the app's own exporter.
usage: capture.py SCENE K OUTDIR [VIEWPORT_W VIEWPORT_H]"""
import csv, json, sys, time, urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright
scene, K, outdir = sys.argv[1], int(sys.argv[2]), Path(sys.argv[3])
vw, vh = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (1600, 1100)
outdir.mkdir(parents=True, exist_ok=True)
rows = {r["scene"]: r for r in csv.DictReader(open("/workspace/new-exp/worldgacha/browser/links.tsv"), delimiter="\t")}
r = rows[scene]
cam = lambda u: [float(x) for x in urllib.parse.parse_qs(u.split("#", 1)[1])["c"][0].split(",")]
c0, c1 = cam(r["start_url"]), cam(r["end_url"])
_gl = Path("/workspace/new-exp/worldgacha/browser/headless_gen_log.json")
if _gl.exists() and scene in json.load(open(_gl)):  # headless-generated scenes: use the exact (unrounded) cameras the start/end PNGs used
    _g = json.load(open(_gl))[scene]; c0, c1 = _g["c0"], _g["c1"]
log = {"scene": scene, "c0": c0, "c1": c1, "K": K, "viewport": [vw, vh], "frames": []}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
                          args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": vw, "height": vh}, accept_downloads=True)
    pg.set_default_timeout(600000)
    t = time.time(); pg.goto(r["start_url"], wait_until="load", timeout=180000)
    time.sleep(20)
    import wgpage; wgpage.apply_style(pg)  # colour + straight verticals ON (matches the browser operator's settings)
    log["load_s"] = time.time() - t
    log["fov"] = pg.evaluate("[VIEW.camera.fov, VIEW.camera.aspect, VIEW.lens, VIEW.camera.filmGauge, VIEW.camera.near, VIEW.camera.far]")
    log["build"] = pg.evaluate("window.WG_WORKER_V || null")
    for i in range(K):
        a = i / (K - 1)
        c = [x0 + a * (x1 - x0) for x0, x1 in zip(c0, c1)]
        wgpage.set_cam(pg, c)
        f = outdir / f"gt_{i:03d}.png"
        if f.exists():  # resume
            log["frames"].append({"i": i, "alpha": a, "cam": c, "export_s": None, "file": f.name, "resumed": True}); continue
        time.sleep(3)
        t1 = time.time()
        with pg.expect_download(timeout=600000) as dl:
            pg.evaluate("document.getElementById('png').click()")
        dl.value.save_as(f)
        log["frames"].append({"i": i, "alpha": a, "cam": c, "export_s": time.time() - t1, "file": f.name})
        print(i, round(time.time() - t1, 1), flush=True)
        json.dump(log, open(outdir / "capture_log.json", "w"), indent=1)
    b.close()
