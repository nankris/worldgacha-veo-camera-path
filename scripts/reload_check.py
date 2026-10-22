"""Reload check: open the saved start link in a fresh browser, re-apply the non-link settings, export, and diff against the original."""
import sys, json, time
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import wgpage as W
B = "/workspace/new-exp/worldgacha/browser"; sc = sys.argv[1]; suf = sys.argv[2] if len(sys.argv) > 2 else ""
d = json.load(open(f"{B}/headless_gen_log.json"))[sc]
with sync_playwright() as p:
    b, pg = W.launch(p); pg.goto(d["start_url"], wait_until="load", timeout=180000); W.settle(pg); W.apply_style(pg)
    cam = W.cam_now(pg); W.export(pg, f"{B}/scene{sc}_start_reload{suf}.png"); b.close()
a = np.asarray(Image.open(f"{B}/scene{sc}_start.png").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{B}/scene{sc}_start_reload{suf}.png").convert("RGB")).astype(int)
diff = np.abs(a - r)
res = {"scene": sc, "cam_original": d["c0"], "cam_from_link": cam, "identical_bytes": open(f"{B}/scene{sc}_start.png", "rb").read() == open(f"{B}/scene{sc}_start_reload{suf}.png", "rb").read(),
       "mean_abs_diff": float(diff.mean()), "frac_pixels_diff_gt8": float((diff.max(2) > 8).mean())}
json.dump(res, open(f"{B}/scene{sc}_reload_check{suf}.json", "w"), indent=1); print(res)
