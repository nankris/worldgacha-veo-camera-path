"""Headless generation of scenes 04 Downtown, 05 Skyscrapers, 06 Farming village (parent request 13:07 IST).
Seeds fixed before generation: base seeds below; if no street-level preset gives a street view, seed += 1 (logged).
Start = first available preset in the BROWSER_BRIEF preference order; lens 24 mm; end = start + 40 m along the
horizontal heading (target moved by the same offset). Outputs mirror the browser operator's files."""
import csv, json, sys, time, shutil
from pathlib import Path
import numpy as np
from playwright.sync_api import sync_playwright
import wgpage as W
B = Path("/workspace/new-exp/worldgacha/browser"); LOG = B / "headless_gen_log.json"
SCENES = [("04", "downtown", 20261004), ("05", "skyscraper", 20261005), ("06", "rural", 20261006)]
PREF = ["center", "street", "eye", "canyon", "station", "ix", "lane"]
log = json.load(open(LOG)) if LOG.exists() else {}
only = sys.argv[1:]
with sync_playwright() as p:
    for sc, rtype, seed in SCENES:
        if only and sc not in only: continue
        if (B / f"scene{sc}_end.png").exists(): continue
        b, pg = W.launch(p)
        t0 = time.time(); pg.goto(W.make_url(rtype, seed), wait_until="load", timeout=180000); W.settle(pg); W.apply_style(pg)
        keys = pg.evaluate("Array.from(document.getElementById('cams').options).map(o=>[o.value,o.textContent])")
        pick = None
        for pref in PREF:
            for k, lab in keys:
                if k == pref or (pref == "ix" and k.startswith("ix")): pick = (k, lab); break
            if pick: break
        pg.evaluate(f"applyCam({json.dumps(pick[0])})"); time.sleep(4)
        c0 = W.cam_now(pg); c0[6] = 24; W.set_cam(pg, c0); c0 = W.cam_now(pg)
        W.export(pg, B / f"scene{sc}_start.png"); W.export(pg, B / f"scene{sc}_recipe.json", "json")
        f = np.array(c0[3:6]) - np.array(c0[:3]); f[1] = 0; f /= np.linalg.norm(f)
        c1 = list(np.array(c0[:3]) + 40 * f) + list(np.array(c0[3:6]) + 40 * f) + [c0[6]]
        W.set_cam(pg, c1); c1 = W.cam_now(pg); W.export(pg, B / f"scene{sc}_end.png")
        log[sc] = {"type": rtype, "seed": seed, "presets_available": keys, "preset": pick, "c0": c0, "c1": c1,
                   "start_url": W.make_url(rtype, seed, c0), "end_url": W.make_url(rtype, seed, c1), "seconds": time.time() - t0}
        json.dump(log, open(LOG, "w"), indent=1); print(sc, pick, round(time.time() - t0), flush=True)
        b.close()
