"""Shared headless helpers for WorldGacha (Chrome + SwiftShader)."""
import json, time, urllib.parse
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
BASE = "https://tools.oyasumi-gamedev.com/worldgacha/?lang=en"

def launch(p, vw=1600, vh=1100, scale=1):
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=ARGS)
    pg = b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=scale, accept_downloads=True)
    pg.set_default_timeout(600000)
    return b, pg

def make_url(rtype, seed, cam=None, size=2000):
    r = {"app": "worldgacha", "v": 1, "type": rtype, "seed": seed, "size": size, "res": 512, "town": 1, "nodeSeeds": {}, "num": {}, "paint": []}
    q = {"r": json.dumps(r, separators=(",", ":"))}
    if cam is not None:
        q["c"] = ",".join(f"{round(x, 1):g}" for x in cam[:6]) + f",{int(round(cam[6]))}"
    q["k"] = "300"; q["v"] = json.dumps({"cr": 0}, separators=(",", ":"))
    return BASE + "#" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)

def settle(pg, wait=20):
    pg.wait_for_function("typeof VIEW!=='undefined' && document.getElementById('gacha') && document.getElementById('seed').value!==''", timeout=600000)
    time.sleep(wait)

def apply_style(pg):
    """Color mode + straight verticals ON + people&cars none + 2400 px export (none of these are in the link)."""
    pg.evaluate("""() => {document.querySelector('#modes button[data-k="color"]').click();
      const t=document.getElementById('twopt'); if(!t.checked){t.checked=true; t.dispatchEvent(new Event('change'));}
      const c=document.getElementById('optCrowd'); if(c.value!=='0'){c.value='0'; c.dispatchEvent(new Event('change'));}
      document.getElementById('pngSize').value='2400';}""")
    time.sleep(5)

def set_cam(pg, c):
    pg.evaluate("""c => {VIEW.setLens ? VIEW.setLens(c[6]) : null; VIEW.camera.position.set(c[0],c[1],c[2]);
      VIEW.controls.target.set(c[3],c[4],c[5]); VIEW.controls.update(); VIEW.render();}""", c)
    time.sleep(3)

def cam_now(pg):
    return pg.evaluate("(() => {const c=camNow(); return [...c.pos, ...c.target, c.lens];})()")

def export(pg, path, btn="png"):
    with pg.expect_download(timeout=600000) as dl:
        pg.evaluate(f"document.getElementById('{btn}').click()")
    dl.value.save_as(path)
