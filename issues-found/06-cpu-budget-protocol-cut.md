# 06: Depth scoring too slow on the loaded box, so the protocol was cut down before scoring
- **Symptom:** at 15:45 IST (load average 20–30 from other tenants), one Depth Anything V2 Small pass took 18–46 s through the HF pipeline, and a bare forward pass took 13 s at 266 px and 26–33 s at 518 px. The pre-registered density needs 942 passes, so 4–7 h.
- **Decision (DESIGN.md Clarification 6, 15:52 IST, before any score):** 9 clip frames instead of 33, 13 GT frames instead of 25, and a 182 px depth input instead of 518. Identical for every arm and the GT.
- **What happened next:** the box load dropped to about 3 at 16:00, and scoring took about 18 s per scene. I then also ran the **original** density (WG_FULL=1, 33/25/518 px) as a robustness check. It gives the same verdicts (results_fullres/summary.json, figures/table_robustness.png).
- **Status:** primary = the cut-down protocol (fixed before scoring); the original protocol is reported as robustness.
