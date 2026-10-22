"""Centre-crop browser PNGs to 16:9 (full width) for Flow inputs and GT alignment."""
import sys, glob, os
from PIL import Image
src = "/workspace/new-exp/worldgacha/browser"; dst = "/workspace/new-exp/worldgacha/flow_inputs"
for p in sorted(glob.glob(f"{src}/scene??_start.png") + glob.glob(f"{src}/scene??_end.png")):
    o = os.path.join(dst, os.path.basename(p).replace(".png", "_16x9.png"))
    if os.path.exists(o): continue
    im = Image.open(p).convert("RGB"); w, h = im.size
    nh = round(w * 9 / 16); top = (h - nh) // 2
    if nh > h: nw = round(h * 16 / 9); left = (w - nw) // 2; im = im.crop((left, 0, left + nw, h))
    else: im = im.crop((0, top, w, top + nh))
    im.save(o); print(o, im.size)
