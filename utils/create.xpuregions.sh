#!/bin/bash
#set -x
TOOLBASE=$HOME/xpupoint-dev/XPU-Profiler
SARGS=" -m 100 -d 96 "
    f0=0
    t0=0
    f1=0
    t0=`find . -name "T.0.bb" | xargs grep "Slice ending" | wc -l `
    f0=`find . -name "summary.bbv" | xargs grep "Total number of kernels" | awk '{print $NF}'`
    f1=`find . -name "global.bbv" | xargs grep "Slice ending" | wc -l`
    if [ $f1  -ne 0 ]; then
      if [ ! -z $f0 ]; then
        echo $d, $f0, $f1, $t0
        nthreads=`ls T.*.bb | wc -l`
        gnthreads=`cat thread.bbv | grep tid | awk '{print $1}' | sort | uniq |wc -l`
set -x
        $TOOLBASE/utils/run-xpupoint.py $SARGS -n $nthreads -w $gnthreads -g . -c . 
set +x
      fi
    fi
