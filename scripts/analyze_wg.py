"""Aggregate WorldGacha scene scores: bootstrap over scenes (10k, seed 0), verdicts H1-H4 per DESIGN.md, figures + tables."""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import os
R = Path("/workspace/new-exp/worldgacha"); OUT = R / ("results_fullres" if os.environ.get("WG_FULL") else "results"); FIG = R / ("figures/fullres" if os.environ.get("WG_FULL") else "figures"); FIG.mkdir(exist_ok=True, parents=True)
S = {p.stem[5:]: json.load(open(p)) for p in sorted(OUT.glob("scene??.json"))}
sc = sorted(S); n = len(sc); rng = np.random.default_rng(0)
get = lambda a, k="depth_absrel_dtw": np.array([S[s]["arms"][a][k] if a in S[s]["arms"] else np.nan for s in sc])
def boot(r):
    idx = rng.integers(0, len(r), (10000, len(r))); return np.percentile(r[idx].mean(1), [2.5, 97.5]).tolist()
def ratio(worse, better, k="depth_absrel_dtw", higher_better=False):
    W, Bv = get(worse, k), get(better, k)
    r = (Bv - W) / W if higher_better else (W - Bv) / W
    return {"mean": float(np.mean(r)), "ci95": boot(r), "per_scene": dict(zip(sc, r.tolist())), "wins": int(np.sum(r > 0))}
H = {}
H["H1"] = ratio("B", "A"); H["H1"]["verdict"] = "PROVEN" if H["H1"]["ci95"][0] >= 0.10 else "DISPROVEN" if H["H1"]["ci95"][1] < 0.10 else "INCONCLUSIVE"
for h, (w, b) in {"H2": ("C", "A"), "H3": ("D", "B"), "H4": ("C", "D")}.items():
    H[h] = ratio(w, b); H[h]["verdict"] = "PROVEN" if H[h]["ci95"][0] > 0 else "DISPROVEN" if H[h]["ci95"][1] <= 0 else "INCONCLUSIVE"
sec = {h: ratio(w, b, "edge_f1_dtw", higher_better=True) for h, (w, b) in {"H1": ("B", "A"), "H2": ("C", "A"), "H3": ("D", "B"), "H4": ("C", "D")}.items()}
arms = ["A", "B", "C", "D"]
tab = {s: {a: S[s]["arms"][a]["depth_absrel_dtw"] for a in arms} | {a + "_edge": S[s]["arms"][a]["edge_f1_dtw"] for a in arms} for s in sc}
out = {"n": n, "scenes": sc, "hypotheses": H, "secondary_edge_f1": sec, "table": tab,
       "means": {a: float(get(a).mean()) for a in arms}, "edge_means": {a: float(get(a, "edge_f1_dtw").mean()) for a in arms},
       "D_fits": {s: S[s]["D_fit"] for s in sc}}
json.dump(out, open(OUT / "summary.json", "w"), indent=1)
names = {"A": "A: Veo start+end", "B": "B: Veo start only", "C": "C: crossfade", "D": "D: 2.5D depth warp"}
cols = {"A": "#2b6cb0", "B": "#63b3ed", "C": "#a0aec0", "D": "#dd6b20"}
for k, lab, fn in [("depth_absrel_dtw", "Depth AbsRel vs GT path (lower = better)", "depth_by_scene.png"), ("edge_f1_dtw", "Edge F1 vs GT path (higher = better)", "edge_by_scene.png")]:
    fig, ax = plt.subplots(figsize=(14, 5), dpi=150); x = np.arange(n); w = 0.2
    for i, a in enumerate(arms): ax.bar(x + (i - 1.5) * w, get(a, k), w, label=names[a], color=cols[a])
    lbl = {"01": "01 Riverside", "02": "02 Castle", "03": "03 Seaside hill", "04": "04 Downtown", "05": "05 Skyscrapers", "06": "06 Farming village"}
    ax.set_xticks(x); ax.set_xticklabels([lbl.get(s, s) for s in sc]); ax.set_ylabel(lab); ax.legend(ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    ax.spines[["top", "right"]].set_visible(False); fig.tight_layout(); fig.savefig(FIG / fn); plt.close(fig)
fig, ax = plt.subplots(figsize=(15, 5), dpi=150); fig.subplots_adjust(right=0.8)
desc = {"H1": "H1: A vs B (keyframe helps), bar = +10%", "H2": "H2: A vs crossfade C", "H3": "H3: B vs depth-warp D", "H4": "H4: depth-warp D vs crossfade C"}
for i, h in enumerate(["H1", "H2", "H3", "H4"]):
    m, (lo, hi) = H[h]["mean"], H[h]["ci95"]
    ax.errorbar(m * 100, i, xerr=[[(m - lo) * 100], [(hi - m) * 100]], fmt="o", color="#2b6cb0", capsize=6, ms=8)
    ax.scatter(np.array(list(H[h]["per_scene"].values())) * 100, [i] * n, color="#a0aec0", s=18, zorder=0)
    ax.text(1.02, i, f'{H[h]["verdict"]}\n{m*100:+.0f}% [{lo*100:+.0f}, {hi*100:+.0f}]', transform=__import__('matplotlib.transforms', fromlist=['x']).blended_transform_factory(ax.transAxes, ax.transData), va="center", fontsize=11, weight="bold")
ax.axvline(0, color="k", lw=0.8); ax.axvline(10, color="#e53e3e", lw=0.8, ls="--", ymin=0.78)
ax.set_yticks(range(4)); ax.set_yticklabels([desc[h] for h in ["H1", "H2", "H3", "H4"]]); ax.invert_yaxis()
ax.set_xlabel("Relative depth-error reduction, % (mean over scenes, 95% bootstrap CI; grey = single scenes)")
ax.spines[["top", "right"]].set_visible(False); fig.tight_layout(rect=(0, 0, 0.84, 1)); fig.savefig(FIG / "hypotheses_ci.png"); plt.close(fig)
for h in H: print(h, round(H[h]["mean"], 4), [round(x, 4) for x in H[h]["ci95"]], H[h]["verdict"], "wins", H[h]["wins"], "/", n)
print("means", out["means"]); print("edge", out["edge_means"])
