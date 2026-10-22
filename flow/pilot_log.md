# Flow pilot log (Oct 22 2026) — account [account redacted] (PRO tier), https://flow.google.com/
Project: "Oct 22 - 03:13" (new). Agent mode toggled off; Video > Frames mode.
Settings as shown: Video, Frames, 16:9, model "Veo 3.1 - Fast", x1 (outputs), 8s, 720p (summary chip "Video · 720p · 8s · x1"). 4s/6s/8s/10s offered for Omni; Veo chip stayed 8s. No audio toggle, no prompt-enhancement toggle, no crop box shown. Veo 3.1 Fast quoted "Generating will use 20 credits".
Inputs uploaded via dialog: scene01_start_16x9.png, scene01_end_16x9.png.
Credits: before A 1,050 -> after A 1,030 (cost 20) -> after B 1,010 (cost 20). Final 1,010.
## A (start+end frames), prompt: Smooth steady forward dolly at eye level down this street in a quiet town. No people, no cars, no cuts, buildings stay solid, daylight.
Generation time ~65 s (about 07:16:04 -> 07:17:08 UTC). No errors. File scene01_A.mp4 (1280x720, 8.0 s, h264+aac audio track present).
## B (start frame only, same Frames mode), prompt: Smooth steady forward dolly at eye level down this street in a quiet town. The camera moves about 40 metres straight ahead. No people, no cars, no cuts, buildings stay solid, daylight.
Generation time ~ 07:17:59 -> ~07:18:58 UTC, ~60 s. No errors. File scene01_B.mp4 (1280x720, 8.0 s).
## Watermark
Visible watermarking is forced on ("required in your region", toggle locked). Small "Veo" text mark at bottom-right corner of the frame, ~3% of width, in player preview; original-size 720p download used.
Download menu also offered 270p GIF, 1080p upscaled, 4K (Upgrade) - not used.

# Batch 2 (Oct 22 2026, ~07:20-07:24 UTC) — same settings as batch 1 (Veo 3.1 - Fast, Frames, 16:9, 720p, 8s, x1)
Inputs uploaded via the upload dialog from /workspace/new-exp/worldgacha/flow_inputs/. Four generations were queued back to back (up to 3-4 running concurrently), so per-clip times are approximate.
Credits: before batch 1,010. Balance showed 980 immediately after the 4th submit (07:21:55) and stayed 980 on fresh page loads at the end. Net change 30, not the expected 80 (4 x 20) - per-clip before/after not measurable because of queueing; unexplained, worth checking the Flow activity/credit history.
- scene02 A (start+end): submitted 07:20:43 UTC, finished by ~07:22 (<~90 s). Saved scene02_A.mp4 (1280x720, 8.0 s, h264+aac).
- scene02 B (start only): submitted 07:20:57, finished by ~07:22 (<~80 s). Saved scene02_B.mp4.
- scene03 A (start+end): submitted 07:21:41, finished by ~07:23 (~80 s). Saved scene03_A.mp4.
- scene03 B (start only): submitted 07:21:55, finished by ~07:23. Saved scene03_B.mp4.
Notes: no errors/refusals/payment prompts; original 720p download used (no upscale); visible Veo watermark forced on. Flow tab crashed at the end (not needed further); downloads identified by prompt text and verified distinct by md5. Duplicate/mis-picked downloads (a scene01_B copy and repeated scene03_A) remain in /home/box/Downloads only.

## Observation (agent, 12:56 IST)
The scenes 02-03 batch (4 clips) moved the balance 1,010 -> 980 (30 credits), not the 4 x 20 quoted. See issues-found/04. Not a blocker.

# Batch 3 (Oct 22 2026, ~08:01-08:13 UTC) — scenes 04-06, submitted strictly ONE AT A TIME
Settings identical to batches 1-2 (agent off, Video > Frames, Veo 3.1 - Fast, 16:9, 720p, 8s, x1; quoted 20 credits). Inputs uploaded via upload dialog from flow_inputs/. Balance read from Account details popup before and after each submit.
| clip | submitted (UTC) | done (UTC) | gen time | credits before -> after | cost |
|---|---|---|---|---|---|
| scene04_A (start+end) | 08:01:35 | ~08:02:30 | ~55 s | 980 -> 960 | 20 |
| scene04_B (start only) | 08:03:49 | ~08:04:48 | ~60 s | 960 -> 940 | 20 |
| scene05_A | 08:05:36 | ~08:06:47 | ~70 s | 940 -> 920 | 20 |
| scene05_B | 08:08:39 | ~08:09:35 | ~55 s | 920 -> 900 | 20 |
| scene06_A | 08:10:35 | ~08:11:40 | ~65 s | 900 -> 880 | 20 |
| scene06_B | 08:12:15 | ~08:13:15 | ~60 s | 880 -> 860 | 20 |
Total 120 credits for 6 clips (980 -> 860); every clip cost the full quoted 20 when submitted singly. So the batch-2 anomaly (4 clips queued together = 30) did not reproduce with sequential submits; it likely relates to queueing/concurrent submission (or a refund/ledger lag), not per-clip pricing.
Notes: originals via Download > 720p Original size (no upscale); all 1280x720, 8.0 s. Each file verified by prompt text and start/end thumbnails in the detail view, first frame matches the corresponding *_start_16x9.png, and all 12 md5s are distinct (no overlap with scenes 01-03). Flow banner "high demand... credits refunded for failed requests" shown but no failures/refusals/payment prompts. First attempt at a detail click accidentally opened an old clip (nothing submitted). Screenshots in doc/: 02_frames_mode_setup.png (scene04 A, before generating), 03_clip_detail_view.png (scene04_A detail). Account popup closed in both (no email visible).
