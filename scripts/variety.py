"""Descriptive variety across the 6 region types (pre-registered as descriptive only): edge density, colourfulness,
sky fraction proxy, and pairwise depth-histogram distance (Jensen-Shannon) between start frames. LPIPS not computed (not installed)."""
import json, itertools
from pathlib import Path
import numpy as np, cv2
from PIL import Image
R = Path("/workspace/new-exp/worldgacha"); C = R / "cache"
sc = ["01", "02", "03", "04", "05", "06"]; out = {}; H = {}
for s in sc:
    im = np.asarray(Image.open(R / "flow_inputs" / f"scene{s}_start_16x9.png").convert("RGB").resize((1280, 720)))
    e = (cv2.Canny(cv2.cvtColor(im, cv2.COLOR_RGB2GRAY), 100, 200) > 0).mean()
    rg = im[..., 0].astype(float) - im[..., 1]; yb = 0.5 * (im[..., 0].astype(float) + im[..., 1]) - im[..., 2]
    col = np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    d = np.load(C / f"s{s}_start.npy"); dn = (d - d.min()) / (d.max() - d.min() + 1e-9)
    h, _ = np.histogram(dn, bins=32, range=(0, 1)); H[s] = h / h.sum()
    out[s] = {"edge_density": float(e), "colourfulness": float(col)}
js = lambda p, q: float(0.5 * sum(a * np.log((a + 1e-12) / ((a + b) / 2 + 1e-12)) + b * np.log((b + 1e-12) / ((a + b) / 2 + 1e-12)) for a, b in zip(p, q)))
pair = {f"{a}-{b}": js(H[a], H[b]) for a, b in itertools.combinations(sc, 2)}
json.dump({"per_scene": out, "depth_hist_js": pair, "mean_pairwise_js": float(np.mean(list(pair.values())))}, open(R / "results" / "variety.json", "w"), indent=1)
for s in sc: print(s, {k: round(v, 3) for k, v in out[s].items()})
print("mean JS", round(np.mean(list(pair.values())), 3), "min", min(pair, key=pair.get), round(min(pair.values()), 3), "max", max(pair, key=pair.get), round(max(pair.values()), 3))
