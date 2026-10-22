"""H5 determinism checks (Amendment 1 + Clarification 2/5). Full-resolution MAD (0-255), share of pixels with |d|>8, edge-F1 at 2 px."""
import json
from pathlib import Path
import numpy as np, cv2
from PIL import Image
R = Path("/workspace/new-exp/worldgacha"); B = R / "browser"; G = R / "gt"
def load(p): return np.asarray(Image.open(p).convert("RGB"))
def f1(a, b, tol=2):
    ea = cv2.Canny(cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), 100, 200) > 0; eb = cv2.Canny(cv2.cvtColor(b, cv2.COLOR_RGB2GRAY), 100, 200) > 0
    da = cv2.distanceTransform((~ea).astype(np.uint8), cv2.DIST_L2, 3); db = cv2.distanceTransform((~eb).astype(np.uint8), cv2.DIST_L2, 3)
    p = (db[ea] <= tol).mean(); r = (da[eb] <= tol).mean(); return float(2 * p * r / (p + r + 1e-12))
def cmp(kind, a, b):
    A, Bm = load(a), load(b); d = np.abs(A.astype(int) - Bm.astype(int))
    mad = float(d.mean()); e = f1(A, Bm)
    return {"kind": kind, "a": str(a.relative_to(R)), "b": str(b.relative_to(R)), "identical_bytes": a.read_bytes() == b.read_bytes(),
            "mad": mad, "frac_gt8": float((d.max(2) > 8).mean()), "edge_f1_2px": e, "pass": bool(mad <= 2 and e >= 0.95)}
checks = []
for r in sorted(B.glob("scene??_start_reload.png")):
    sc = r.name[5:7]
    checks.append(cmp("browser_reload" if sc in ("01", "02", "03") else "headless_link_reload_vs_exact_cam", B / f"scene{sc}_start.png", r))
if (B / "scene06_start_reload2.png").exists(): checks.append(cmp("headless_link_reload_vs_link_reload", B / "scene06_start_reload.png", B / "scene06_start_reload2.png"))
for sc in ["01", "02", "03", "04", "05", "06"]:
    fr = sorted((G / f"scene{sc}").glob("gt_*.png"))
    if len(fr) < 25: continue
    kind = "headless_vs_browser" if sc in ("01", "02", "03") else "headless_vs_headless_gen"
    checks.append(cmp(kind + "_start", B / f"scene{sc}_start.png", fr[0])); checks.append(cmp(kind + "_end", B / f"scene{sc}_end.png", fr[-1]))
br = [c for c in checks if c["kind"] == "browser_reload"]
allpass = all(c["pass"] for c in checks)
verdict = "PROVEN" if allpass else ("DISPROVEN" if any((c["mad"] > 2 and c["edge_f1_2px"] < 0.95) for c in br) else "INCONCLUSIVE")
json.dump({"checks": checks, "verdict_H5": verdict}, open(R / "results" / "h5_determinism.json", "w"), indent=1)
for c in checks: print(f'{c["kind"]:42s} {c["b"]:40s} mad={c["mad"]:.3f} >8={c["frac_gt8"]*100:.2f}% f1={c["edge_f1_2px"]:.3f} {"PASS" if c["pass"] else "fail"}')
print("H5", verdict)
