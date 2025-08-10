#!/bin/bash
#set -x
TOOLBASE=$HOME/xpupoint-dev/XPU-Profiler/
ulimit -s unlimited
PREFIX=gpu
    if [ -e t.simpoints ]; then
      $TOOLBASE/utils/report.slice-rdtsc.py --rdtsc_file $PREFIX.onkernelperf.out --region_file t.simpoints --label_file t.labels --weights_file t.weights > slice.trace.txt
    fi

