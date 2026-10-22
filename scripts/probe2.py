import json, sys, time, urllib.parse
from playwright.sync_api import sync_playwright
rec = json.load(open("/workspace/new-exp/worldgacha/browser/scene01_recipe.json"))
cam = rec["cam"]
c = ",".join(str(v) for v in cam["pos"] + cam["target"]) + "," + str(cam["lens"])
url = "https://tools.oyasumi-gamedev.com/worldgacha/?lang=en#" + urllib.parse.urlencode({"r": json.dumps(rec, separators=(",", ":")), "c": c})
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
                          args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1600, "height": 1000}, accept_downloads=True)
    pg.set_default_timeout(300000)
    t = time.time(); pg.goto(url, wait_until="load", timeout=180000)
    print("loaded", round(time.time()-t), pg.evaluate("(()=>{const c=document.createElement('canvas');const g=c.getContext('webgl2');return g?g.getParameter(g.RENDERER):null})()"), flush=True)
    time.sleep(30)
    print("cam", pg.evaluate("location.hash.slice(-80)"), flush=True)
    with pg.expect_download(timeout=300000) as dl:
        pg.evaluate("document.getElementById('png').click()")
    dl.value.save_as("/tmp/wg_probe_export.png"); print("export", round(time.time()-t), flush=True)
    b.close()
