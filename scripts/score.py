"""Score WorldGacha GT paths vs arms (C crossfade, D depth-warp, A/B Veo if present). Pre-registered in DESIGN.md.
usage: score.py [scenes...]   (default: every scene with 25 GT frames)"""
import json, os, sys, glob, subprocess, time
from pathlib import Path
import numpy as np, cv2, torch
from PIL import Image
ROOT = Path("/workspace/new-exp/worldgacha"); B = ROOT / "browser"; GT = ROOT / "gt"; FLOW = ROOT / "flow"
OUT = ROOT / ("results_fullres" if os.environ.get("WG_FULL") else "results"); CACHE = ROOT / ("cache_fullres" if os.environ.get("WG_FULL") else "cache"); OUT.mkdir(exist_ok=True); CACHE.mkdir(exist_ok=True)
W, H = 1280, 720; NA = 9; LW, LH = 320, 180; DA_IN = 182; GT_STEP = 2  # Clarification 6 (CPU budget)
if os.environ.get("WG_FULL"): NA, DA_IN, GT_STEP = 33, 518, 1  # robustness: the original pre-registered density
torch.set_num_threads(3)
_pipe = None


def mask_lowres():
    m = np.ones((LH, LW), bool)
    f = ROOT / "mask.json"  # {"rects": [[x0,y0,x1,y1] in 1280x720 px]}
    if f.exists():
        for x0, y0, x1, y1 in json.load(open(f))["rects"]:
            m[int(y0 * LH / H):int(np.ceil(y1 * LH / H)), int(x0 * LW / W):int(np.ceil(x1 * LW / W))] = False
    return m


def grey_mask(a):
    """Amendment 1: the watermark rectangle is set to mean grey in EVERY frame (GT and all arms) before any metric."""
    a = a.copy()
    for x0, y0, x1, y1 in json.load(open(ROOT / "mask.json"))["rects"]:
        a[int(y0):int(y1), int(x0):int(x1)] = 128
    return a


def crop169(im):
    im = im.convert("RGB"); w, h = im.size; nh = round(w * 9 / 16)
    if nh <= h:
        top = (h - nh) // 2; im = im.crop((0, top, w, top + nh))
    else:
        nw = round(h * 16 / 9); l = (w - nw) // 2; im = im.crop((l, 0, l + nw, h))
    return im.resize((W, H), Image.LANCZOS)


def disparity(img):
    global _pipe
    if _pipe is None:
        from transformers import pipeline
        _pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device="cpu")
        _pipe.image_processor.size = {"height": DA_IN, "width": DA_IN}  # Clarification 6: short side 182 px (default 518) for CPU time
    d = _pipe(Image.fromarray(img))["predicted_depth"].float().numpy()
    return cv2.resize(d, (W, H), interpolation=cv2.INTER_LINEAR)


def disp_cached(key, img):
    f = CACHE / f"{key}.npy"
    if f.exists(): return np.load(f)
    d = disparity(img); np.save(f, d.astype(np.float32)); return d


def absrel_aligned(pred, gt, m):
    p, g = pred[m].astype(np.float64), gt[m].astype(np.float64)
    A = np.stack([p, np.ones_like(p)], 1); s, t = np.linalg.lstsq(A, g, rcond=None)[0]
    pa = s * p + t; ok = g > 1e-3 * g.max()
    return float(np.mean(np.abs(pa[ok] - g[ok]) / g[ok]))


def edge_f1(a, b, m, tol):
    ea = cv2.Canny(cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), 100, 200) > 0
    eb = cv2.Canny(cv2.cvtColor(b, cv2.COLOR_RGB2GRAY), 100, 200) > 0
    ea &= m; eb &= m
    if ea.sum() == 0 or eb.sum() == 0: return 0.0
    da = cv2.distanceTransform((~ea).astype(np.uint8), cv2.DIST_L2, 3)
    db = cv2.distanceTransform((~eb).astype(np.uint8), cv2.DIST_L2, 3)
    prec = (db[ea] <= tol).mean(); rec = (da[eb] <= tol).mean()
    return float(2 * prec * rec / (prec + rec + 1e-12))


def dtw_score(C):
    """C [NA, K] costs; monotone DTW, endpoints pinned; mean over interior arm frames of matched (min) cost."""
    n, k = C.shape; D = np.full((n, k), np.inf); D[0, 0] = C[0, 0]; P = {}
    for i in range(n):
        for j in range(k):
            if i == 0 and j == 0: continue
            best = min([(D[i-1, j], (i-1, j)) if i else (np.inf, None), (D[i, j-1], (i, j-1)) if j else (np.inf, None),
                        (D[i-1, j-1], (i-1, j-1)) if i and j else (np.inf, None)], key=lambda x: x[0])
            D[i, j] = C[i, j] + best[0]; P[(i, j)] = best[1]
    path = [(n-1, k-1)]
    while path[-1] != (0, 0): path.append(P[path[-1]])
    match = {}
    for i, j in path: match[i] = min(match.get(i, np.inf), C[i, j])
    interior = [match[i] for i in range(1, n-1)]
    return float(np.mean(interior)), sorted(path)


def lookat(pos, tgt):
    f = np.asarray(tgt) - np.asarray(pos); f /= np.linalg.norm(f)
    r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    return np.stack([r, u, -f])  # rows: camera x,y,z axes in world (three.js looks down -z)


def warp(img, z, K, pos0, tgt0, pos1, tgt1, out_hw=(H, W)):
    h, w = z.shape; fx, cx, cy = K
    v, u = np.mgrid[0:h, 0:w].astype(np.float64)
    X = np.stack([(u - cx) / fx * z, -(v - cy) / fx * z, -z], -1).reshape(-1, 3)
    R0, R1 = lookat(pos0, tgt0), lookat(pos1, tgt1)
    Pw = X @ R0 + np.asarray(pos0)
    Pc = (Pw - np.asarray(pos1)) @ R1.T
    zz = -Pc[:, 2]; ok = zz > 0.05
    uu = np.round(Pc[:, 0] / zz * fx + cx).astype(int); vv = np.round(-Pc[:, 1] / zz * fx + cy).astype(int)
    ok &= (uu >= 0) & (uu < w) & (vv >= 0) & (vv < h)
    idx = np.where(ok)[0]; order = idx[np.argsort(-zz[idx])]  # far first, near overwrites
    out = np.zeros((h, w, 3), np.uint8); hole = np.ones((h, w), np.uint8)
    col = img.reshape(-1, 3)
    # 2x2 splat footprint (fixes pinhole grid from forward splatting when the view zooms in)
    for du in (0, 1):
        for dv in (0, 1):
            u2 = np.clip(uu[order] + du, 0, w - 1); v2 = np.clip(vv[order] + dv, 0, h - 1)
            sel = hole[v2, u2] == 1 if (du or dv) else np.ones(len(order), bool)
            out[v2[sel], u2[sel]] = col[order][sel]; hole[v2[sel], u2[sel]] = 0
    return out, hole


def arm_D(start, end, d0, cam0, cam1, fov_v, aspect_full):
    hf = 2 * np.arctan(np.tan(np.radians(fov_v) / 2) * aspect_full)
    dn = (d0 - d0.min()) / (d0.max() - d0.min() + 1e-9)
    small = lambda a: cv2.resize(a, (LW, LH), interpolation=cv2.INTER_AREA)
    Ks = ((LW / 2) / np.tan(hf / 2), LW / 2, LH / 2)
    s_start, s_end, s_dn = small(start), small(end).astype(float), small(dn)
    best = (np.inf, None)
    for zn in np.geomspace(1.5, 60, 14):
        for zf in np.geomspace(60, 3000, 10):
            t = 1 / zf; s = 1 / zn - t
            z = 1 / (s * s_dn + t)
            o, hole = warp(s_start, z, Ks, cam0[:3], cam0[3:6], cam1[:3], cam1[3:6])
            o = cv2.inpaint(o, hole, 3, cv2.INPAINT_TELEA)
            e = np.abs(o.astype(float) - s_end).mean()
            if e < best[0]: best = (e, (zn, zf))
    zn, zf = best[1]; t = 1 / zf; s = 1 / zn - t; z = 1 / (s * dn + t)
    Kf = ((W / 2) / np.tan(hf / 2), W / 2, H / 2)
    frames = []
    for i in range(NA):
        a = i / (NA - 1); c = [x0 + a * (x1 - x0) for x0, x1 in zip(cam0, cam1)]
        o, hole = warp(start, z, Kf, cam0[:3], cam0[3:6], c[:3], c[3:6])
        o = cv2.inpaint(o, hole, 3, cv2.INPAINT_TELEA)
        frames.append(o)
    return frames, {"z_near": float(zn), "z_far": float(zf), "end_fit_mad": float(best[0])}


def video_frames(mp4):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)]))
    fr = []
    for i in range(NA):
        t = min(i / (NA - 1) * dur, dur - 0.05)
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"])
        fr.append(np.asarray(crop169(Image.open(__import__("io").BytesIO(raw)))))
    return fr, dur


def score_scene(sc):
    log = json.load(open(GT / f"scene{sc}" / "capture_log.json"))
    gtf = [grey_mask(np.asarray(crop169(Image.open(GT / f"scene{sc}" / f["file"])))) for f in log["frames"][::GT_STEP]]
    K = len(gtf); m = mask_lowres(); mfull = cv2.resize(m.astype(np.uint8), (W, H), interpolation=cv2.INTER_NEAREST) > 0
    tol = 0.01 * np.hypot(W, H)
    start = np.asarray(crop169(Image.open(B / f"scene{sc}_start.png"))); end = np.asarray(crop169(Image.open(B / f"scene{sc}_end.png")))
    lo = lambda d: cv2.resize(d, (LW, LH), interpolation=cv2.INTER_AREA)
    gtd = [lo(disp_cached(f"s{sc}_gt{j:03d}", g)) for j, g in enumerate(gtf)]
    arms = {}
    arms["C"] = [((1 - i / (NA - 1)) * start.astype(float) + i / (NA - 1) * end.astype(float)).astype(np.uint8) for i in range(NA)]
    d0 = disp_cached(f"s{sc}_start", start)
    arms["D"], dinfo = arm_D(start, end, d0, log["c0"], log["c1"], log["fov"][0], log["fov"][1])
    vinfo = {}
    for a in ["A", "B"]:
        mp4 = FLOW / f"scene{sc}_{a}.mp4"
        if mp4.exists(): arms[a], vinfo[a] = video_frames(mp4)
    for a in list(arms): arms[a] = [grey_mask(f) for f in arms[a]]
    if os.environ.get("WG_SELFTEST"):  # sanity: GT resampled to 33 frames must score ~0 against GT
        arms = {"GTself": [gtf[round(i * (K - 1) / (NA - 1))] for i in range(NA)]}
    res = {"scene": sc, "K_gt": K, "D_fit": dinfo, "video_duration_s": vinfo, "arms": {}}
    for a, fr in arms.items():
        ad = [lo(disp_cached(f"s{sc}_{a}{i:03d}", f)) for i, f in enumerate(fr)]
        Cm = np.array([[absrel_aligned(ad[i], gtd[j], m) for j in range(K)] for i in range(NA)])
        sc_d, path = dtw_score(Cm)
        pj = {}
        for i, j in path:
            if i not in pj or Cm[i, j] < Cm[i, pj[i]]: pj[i] = j
        e = float(np.mean([edge_f1(fr[i], gtf[pj[i]], mfull, tol) for i in range(1, NA - 1)]))
        res["arms"][a] = {"depth_absrel_dtw": sc_d, "edge_f1_dtw": e, "matched_gt": [int(pj[i]) for i in range(NA)]}
        np.save(CACHE / f"s{sc}_{a}_cost.npy", Cm)
        fd = OUT / "frames"; fd.mkdir(exist_ok=True)
        for i, f in enumerate(fr): Image.fromarray(f).resize((640, 360), Image.LANCZOS).save(fd / f"s{sc}_{a}_{i:03d}.jpg", quality=92)
        if True:
            Image.fromarray(np.concatenate([fr[0], fr[NA // 2], fr[-1]], 1)).resize((960, 180)).save(OUT / f"strip_s{sc}_{a}.jpg")
    for j, f in enumerate(gtf): Image.fromarray(f).resize((640, 360), Image.LANCZOS).save(OUT / "frames" / f"s{sc}_GT_{j:03d}.jpg", quality=92)
    Image.fromarray(np.concatenate([gtf[0], gtf[K // 2], gtf[-1]], 1)).resize((960, 180)).save(OUT / f"strip_s{sc}_GT.jpg")
    if os.environ.get("WG_SELFTEST"): json.dump(res, open(OUT / f"selftest_scene{sc}.json", "w"), indent=1); return res
    json.dump(res, open(OUT / f"scene{sc}.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    scenes = sys.argv[1:] or sorted(p.name[5:] for p in GT.glob("scene??") if len(list(p.glob("gt_*.png"))) >= 25)
    for sc in scenes:
        if not os.environ.get("WG_SELFTEST") and (OUT / f"scene{sc}.json").exists(): print(sc, "done (checkpoint)"); continue
        t = time.time(); r = score_scene(sc)
        print(sc, {a: round(v["depth_absrel_dtw"], 4) for a, v in r["arms"].items()}, f"{time.time()-t:.0f}s", flush=True)
