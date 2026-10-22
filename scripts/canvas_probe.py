import csv,time,sys
from playwright.sync_api import sync_playwright
r=list(csv.DictReader(open("/workspace/new-exp/worldgacha/browser/links.tsv"),delimiter="\t"))[0]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",headless=True,args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg=b.new_page(viewport={"width":1600,"height":1000}); pg.goto(r["start_url"],wait_until="load",timeout=180000); time.sleep(10)
    for w,h in [(1600,1000),(1600,1100),(1600,1200),(1920,1080),(1400,1100)]:
        pg.set_viewport_size({"width":w,"height":h}); time.sleep(2)
        print(w,h,pg.evaluate("(()=>{const c=VIEW.renderer.domElement;const r=c.getBoundingClientRect();return [r.width,r.height,r.width/r.height]})()"),flush=True)
    b.close()
