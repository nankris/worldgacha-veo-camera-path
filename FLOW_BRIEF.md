# FLOW_BRIEF (pilot): 2 Veo clips for WorldGacha scene 01, Google Flow credits ONLY

Written 2026-10-22 12:05 IST. The user approved Flow credits only (account [account redacted], flow.google.com/, about 1,050+ credits, +50/day).
**No Magnific, no other paid tool, no purchases.** A second brief for the other 22 clips follows after the pilot costs are reported.

## Preconditions
- Use the **16:9 pre-cropped inputs**: `/workspace/new-exp/worldgacha/flow_inputs/scene01_start_16x9.png` and `scene01_end_16x9.png` (2400×1350). The originals are 2400×1919, so Flow would crop them unpredictably. Use exactly these files. Don't use screenshots and don't re-export them. If they're missing, run `python3 /workspace/new-exp/worldgacha/scripts/crop16x9.py` first.
- Open Flow in a new tab as [account redacted]. Leave the other tabs alone (Colab, Substack, WorldGacha).

## Settings (identical for both clips; write down what the UI actually shows)
- Model: **Veo 3.1 Fast**. If Fast isn't offered, use **Veo 3.1 Lite**, and use that same model for all 24 clips later. Never mix models.
- Duration **8 s**. If 8 s isn't offered, use the longest available and note it.
- Aspect **16:9 (landscape)**. Resolution **720p** (the default). Don't upscale.
- **Outputs per prompt: 1**. Set this in the settings so each generation makes one video and costs credits once.
- Audio: off if there's a toggle, otherwise leave the default and note it.

## Clips
1. **Arm A, scene 01, start+end frames** (Flow mode "Frames to Video": first frame = `scene01_start_16x9.png`, last frame = `scene01_end_16x9.png`). Prompt, verbatim:
   `Smooth steady forward dolly at eye level down this street in a quiet town. No people, no cars, no cuts, buildings stay solid, daylight.`
2. **Arm B, scene 01, start frame only** (same mode with only the first frame, or "Image to Video" if that's what Flow calls it). Prompt, verbatim:
   `Smooth steady forward dolly at eye level down this street in a quiet town. The camera moves about 40 metres straight ahead. No people, no cars, no cuts, buildings stay solid, daylight.`
   - If Flow has no start-only option, skip clip 2 and report that.

If Flow crops or reframes the uploaded image (it may show a crop box), choose **no crop / fit** if available. Otherwise accept the default centre crop and **say so**, because the ground truth must be cropped the same way.

## For each clip, record
- Credits shown **before** clicking Generate and **after** the clip finishes.
- Exact model/duration/aspect/resolution/outputs labels as shown in the UI.
- Any prompt rewrite or "enhance prompt" Flow applied. Turn prompt enhancement **off** if there's a toggle.
- Whether the visible watermark appears, and where (corner, approximate size).
- Generation time, plus any errors or retries (a failed generation that still costs credits counts).

## Downloads → `/workspace/new-exp/worldgacha/flow/`
- Download the original MP4 (720p, not GIF, not upscaled): `scene01_A.mp4`, `scene01_B.mp4`.
- `pilot_log.md`: for each clip, the arm, model, settings, prompt, credits before/after/cost, watermark position, timings and notes. Also the credits shown at the end.

## Stop conditions (stop and report; don't work around them)
- If any generation would leave fewer than **200 credits**, stop before generating.
- Stop on anything asking for payment, an upgrade, a trial, card details or a subscription.
- Stop if a generation is refused or blocked by policy, or the account isn't [account redacted].
- Don't generate more than these 2 clips. Retry a failed generation only once, and only if no credits were charged.
