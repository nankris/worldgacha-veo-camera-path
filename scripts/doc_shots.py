"""Blog UI screenshots at a 1920x1200 viewport (parent request 13:07). Headless Chrome + SwiftShader; nothing is clicked except UI toggles."""
import json, time
from playwright.sync_api import sync_playwright
import wgpage as W
D = "/workspace/new-exp/worldgacha/browser/doc"; L = json.load(open("/workspace/new-exp/worldgacha/browser/headless_gen_log.json"))
SHOT = dict(timeout=300000, animations="disabled", caret="hide")
def card(pg, sel, path):
    h = pg.evaluate_handle(f"document.querySelector('{sel}').closest('.card,.box,.gbar')")
    h.as_element().screenshot(path=path, **SHOT); print(path, flush=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, args=W.ARGS)
    ctx = b.new_context(viewport={"width": 1920, "height": 1200}, device_scale_factor=2, accept_downloads=True)
    ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin="https://tools.oyasumi-gamedev.com")
    pg = ctx.new_page(); pg.set_default_timeout(600000)
    pg.goto(W.BASE, wait_until="load", timeout=180000); W.settle(pg, 25)
    pg.screenshot(path=f"{D}/h01_landing_full.png", full_page=True, **SHOT); print("landing", flush=True)
    pg.goto(L["04"]["start_url"], wait_until="load", timeout=180000); pg.reload(wait_until="load"); W.settle(pg, 25); W.apply_style(pg)
    W.set_cam(pg, L["04"]["c0"]); time.sleep(5)
    pg.screenshot(path=f"{D}/h02_town_loaded_full.png", full_page=True, **SHOT)
    card(pg, "#types", f"{D}/h03_region_picker.png")
    card(pg, "#size", f"{D}/h04_settings_panel.png")
    card(pg, "#twopt", f"{D}/h05_view_bar_straight_verticals.png")
    pg.evaluate("(()=>{const s=document.getElementById('cams'); s.size=s.options.length;})()"); time.sleep(2)
    card(pg, "#cams", f"{D}/h06_camera_presets_expanded.png")
    pg.evaluate("(()=>{const s=document.getElementById('cams'); s.size=0;})()")
    card(pg, "#png", f"{D}/h07_export_card.png")
    pg.evaluate("document.getElementById('link').click()"); time.sleep(1.5)
    pg.screenshot(path=f"{D}/h08_after_copy_link.png", **SHOT)
    try: txt = pg.evaluate("navigator.clipboard.readText()")
    except Exception as e: txt = "ERR " + str(e)
    open(f"{D}/h08_copied_link.txt", "w").write(txt + "\n"); print("link", txt[:120], flush=True)
    b.close()
