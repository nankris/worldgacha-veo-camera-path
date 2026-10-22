"""Combine the small UI element screenshots (browser/doc/h03-h07) into one full-width blog image."""
from PIL import Image, ImageDraw, ImageFont
D = "/workspace/new-exp/worldgacha/browser/doc/"
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
items = [("h03_region_picker.png", "1  Pick a region type, roll a seed"), ("h05_view_bar_straight_verticals.png", "2  View bar: Straight verticals (not stored in the share link!)"),
         ("h04_settings_panel.png", "3  The generator's node chain (Blueprint → Terrain → Town → Streets → Buildings), Size 2 km"),
         ("h06_camera_presets_expanded.png", "4  Camera presets (dropdown expanded for the screenshot)"), ("h07_export_card.png", "5  Export: PNG at 2400 px, GLB/FBX/OBJ, Copy link, Save recipe")]
W = 2000; pad = 30; rows = []
for fn, lab in items:
    im = Image.open(D + fn).convert("RGB"); s = min(1.0, (W - 2 * pad) / im.size[0])
    if im.size[0] < 900: s = min(1.6, (W / 2) / im.size[0])
    rows.append((im.resize((int(im.size[0] * s), int(im.size[1] * s)), Image.LANCZOS), lab))
c = Image.new("RGB", (W, sum(r[0].size[1] + 70 for r in rows) + pad), "white"); d = ImageDraw.Draw(c); y = pad
for im, lab in rows:
    d.text((pad, y), lab, font=f, fill="black"); y += 50; c.paste(im, (pad, y)); d.rectangle([pad - 1, y - 1, pad + im.size[0], y + im.size[1]], outline="#cbd5e0", width=2); y += im.size[1] + 20
c.save(D + "ui_panels_composite.png"); print(c.size)
