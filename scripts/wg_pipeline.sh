#!/bin/bash
# Checkpointed post-capture pipeline (nohup). Waits for the GT capture queue, then selftest -> score -> analyse -> H5 -> visuals.
cd /workspace/new-exp/worldgacha/scripts; P=/workspace/tig-env/bin/python; L=../results/pipeline.log
while pgrep -f capture_queue.sh >/dev/null || pgrep -f "capture.py" >/dev/null; do sleep 30; done
echo "$(date +%T) capture finished" >> $L
[ -f ../results/selftest_scene01.json ] || { WG_SELFTEST=1 $P score.py 01 >> $L 2>&1; echo "$(date +%T) selftest done" >> $L; }
$P score.py 01 02 03 04 05 06 >> $L 2>&1; echo "$(date +%T) score done" >> $L
$P analyze_wg.py >> $L 2>&1 && $P h5_determinism.py >> $L 2>&1 && $P make_visuals.py >> $L 2>&1; echo "$(date +%T) PIPELINE_DONE" >> $L
