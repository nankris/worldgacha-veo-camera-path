"""Blog visuals: per-scene contact sheets (GT|A|B|C|D x 5 path positions), 2x2 GIFs (GT|A|B|D, 25 steps), start/end gallery.
Scored arm frames come from results/frames (9 per arm). GIFs re-sample the clips/warp at all 25 GT positions (no depth inference)."""
import json, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
import score as S0
R = Path("/workspace/new-exp/worldgacha"); F = R / "results" / "frames"; FIG = R / "figures"; FIG.mkdir(exist_ok=True)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26); fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
NAME = {"01": "Riverside country town", "02": "Castle town", "03": "Seaside hill town", "04": "Downtown", "05": "Skyscrapers", "06": "Farming village"}
LAB = {"GT": "Ground truth (3D re-render)", "A": "A  Veo, start+end", "B": "B  Veo, start only", "C": "C  Crossfade", "D": "D  2.5D depth warp"}
SUM = json.load(open(R / "results" / "summary.json"))
gtimg = lambda sc, j: Image.fromarray(S0.grey_mask(np.asarray(S0.crop169(Image.open(R / "gt" / f"scene{sc}" / f"gt_{j:03d}.png"))))).resize((640, 360), Image.LANCZOS)
for sc in SUM["scenes"]:
    W, Hh, LW = 400, 225, 330
    sheet = Image.new("RGB", (LW + 5 * W, 60 + 5 * Hh), "white"); d = ImageDraw.Draw(sheet)
    d.text((10, 14), f"Scene {sc} · {NAME[sc]}: frames at 0, 25, 50, 75, 100% of the move", font=font, fill="black")
    for r, a in enumerate(["GT", "A", "B", "C", "D"]):
        y = 60 + r * Hh; d.text((10, y + 80), LAB[a], font=fs, fill="black")
        if a != "GT": d.text((10, y + 112), f"depth err {SUM['table'][sc][a]:.3f}", font=fs, fill="#555")
        for c, t in enumerate([0, .25, .5, .75, 1]):
            im = gtimg(sc, round(t * 24)) if a == "GT" else Image.open(F / f"s{sc}_{a}_{round(t * 8):03d}.jpg")
            sheet.paste(im.resize((W - 4, Hh - 4), Image.LANCZOS), (LW + c * W, y))
    sheet.save(FIG / f"sheet_scene{sc}.png")
    # GIF at 25 positions
    log = json.load(open(R / "gt" / f"scene{sc}" / "capture_log.json"))
    vids = {}
    for a in "AB":
        S0.NA = 25; vids[a], _ = S0.video_frames(R / "flow" / f"scene{sc}_{a}.mp4")
    start = np.asarray(S0.crop169(Image.open(R / "browser" / f"scene{sc}_start.png")))
    d0 = np.load(R / "cache" / f"s{sc}_start.npy"); fit = SUM["D_fits"][sc]; zn, zf = fit["z_near"], fit["z_far"]
    dn = (d0 - d0.min()) / (d0.max() - d0.min() + 1e-9); t_ = 1 / zf; s_ = 1 / zn - t_; z = 1 / (s_ * dn + t_)
    hf = 2 * np.arctan(np.tan(np.radians(log["fov"][0]) / 2) * log["fov"][1]); Kf = ((S0.W / 2) / np.tan(hf / 2), S0.W / 2, S0.H / 2)
    c0, c1 = log["c0"], log["c1"]; gif = []
    for j in range(25):
        a_ = j / 24; c = [x0 + a_ * (x1 - x0) for x0, x1 in zip(c0, c1)]
        o, hole = S0.warp(start, z, Kf, c0[:3], c0[3:6], c[:3], c[3:6]); o = cv2.inpaint(o, hole, 3, cv2.INPAINT_TELEA)
        panes = {"GT": gtimg(sc, j), "A": Image.fromarray(S0.grey_mask(vids["A"][j])).resize((640, 360)), "B": Image.fromarray(S0.grey_mask(vids["B"][j])).resize((640, 360)),
                 "D": Image.fromarray(S0.grey_mask(o)).resize((640, 360))}
        g = Image.new("RGB", (1280, 760), "white"); dd = ImageDraw.Draw(g)
        for k, a in enumerate(["GT", "A", "B", "D"]):
            x, y = (k % 2) * 640, 40 + (k // 2) * 360; g.paste(panes[a], (x, y)); dd.rectangle([x, y, x + 360, y + 34], fill="black"); dd.text((x + 8, y + 5), LAB[a], font=fs, fill="white")
        dd.text((10, 6), f"Scene {sc} · {NAME[sc]}  (watermark corner greyed in all panes)", font=fs, fill="black")
        gif.append(g.quantize(colors=200, method=Image.Quantize.MEDIANCUT))
    gif[0].save(FIG / f"compare_scene{sc}.gif", save_all=True, append_images=gif[1:], duration=320, loop=0, optimize=True)
    print(sc, flush=True)
B = R / "browser"; W, Hh = 960, 540
gal = Image.new("RGB", (2 * W + 30, 50 + len(SUM["scenes"]) * (Hh + 46)), "white"); d = ImageDraw.Draw(gal)
d.text((10, 10), "Start (left) and end (right, 35–40 m further along the street): the two Veo keyframes", font=font, fill="black")
for r, sc in enumerate(SUM["scenes"]):
    y = 50 + r * (Hh + 46); d.text((10, y + 6), f"{sc} {NAME[sc]}", font=fs, fill="black")
    for c, e in enumerate(["start", "end"]):
        gal.paste(Image.open(R / "flow_inputs" / f"scene{sc}_{e}_16x9.png").resize((W, Hh), Image.LANCZOS), (c * (W + 30), y + 40))
gal.save(FIG / "gallery_start_end.png"); print("ok")
