import json, sys, time, urllib.parse
from playwright.sync_api import sync_playwright
rec = json.load(open("/workspace/new-exp/worldgacha/browser/scene01_recipe.json"))
cam = rec["cam"]
c = ",".join(str(v) for v in cam["pos"] + cam["target"]) + "," + str(cam["lens"])
url = "https://tools.oyasumi-gamedev.com/worldgacha/?lang=en#" + urllib.parse.urlencode({"r": json.dumps(rec, separators=(",", ":")), "c": c})
print(len(url))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
                          args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1600, "height": 1000}, accept_downloads=True)
    logs = []
    pg.on("console", lambda m: logs.append(m.text))
    t = time.time(); pg.goto(url, wait_until="load", timeout=120000)
    print("webgl", pg.evaluate("(()=>{const c=document.createElement('canvas');const g=c.getContext('webgl2');return g?g.getParameter(g.RENDERER):null})()"))
    time.sleep(25)
    pg.screenshot(path="/tmp/wg_probe.png")
    btns = pg.evaluate("Array.from(document.querySelectorAll('button')).map(b=>(b.id||'')+'|'+b.innerText.trim()).filter(s=>s.length>1).slice(0,120)")
    print(btns)
    print("hash_len", len(pg.evaluate("location.hash")), time.time() - t)
    print(logs[-10:])
    b.close()
