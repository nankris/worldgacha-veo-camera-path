#!/bin/bash
# Capture GT for every scene with both URLs in links.tsv; memory-gated; resumable (skips scenes with 25 frames).
cd /workspace/new-exp/worldgacha/scripts
OUT=/workspace/new-exp/worldgacha/gt
while true; do
  pending=0
  while pgrep -f "capture.py" >/dev/null; do sleep 20; done
  for s in $(tail -n +2 ../browser/links.tsv | awk -F'\t' '$6!="" && $7!="" {print $1}'); do
    n=$(ls $OUT/scene$s/gt_*.png 2>/dev/null | wc -l)
    [ "$n" -ge 25 ] && continue
    pending=1
    while [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 2000 ]; do echo "$(date +%T) waiting RAM"; sleep 30; done
    echo "$(date +%T) scene $s start"
    timeout 3600 /workspace/tig-env/bin/python capture.py $s 25 $OUT/scene$s > $OUT/scene$s.log 2>&1; echo "$(date +%T) scene $s exit $?"
  done
  done_n=$(tail -n +2 ../browser/links.tsv | wc -l)
  [ "$pending" = 0 ] && [ "$done_n" -ge 6 ] && [ -f ../browser/manifest.md ] && { echo ALL_DONE; break; }
  sleep 60
done
