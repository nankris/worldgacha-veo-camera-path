# 02: GT capture for scene 01 stopped at 24/25 frames
- **Symptom:** `gt/scene01` had gt_000..gt_023. capture.py was killed by its 1500 s `timeout` while exporting the last frame.
- **Root cause:** SwiftShader exports slowed from about 17 s to about 110 s per frame as box load rose to about 30.
- **Fix:** capture.py now resumes, skipping frames that already exist. The per-scene timeout was raised to 3600 s, and the queue restarted (it waits for any running capture before starting another).
- **Status:** fixed; scene 01's last frame is re-captured by the queue.
