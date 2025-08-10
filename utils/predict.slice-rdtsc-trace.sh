#!/bin/bash
#set -x
TRACE="slice.trace.txt"
echo "BM, NumSlices, NumRegions, ActualRDTSC, PredictedRDTSC, Error"
    if [ -e $TRACE ]; then
      BM=`pwd`
      BM=`basename $BM`
      WholeRDTSC=`grep WholeProgram $TRACE | awk '{print $NF}'`
      num_slices=`cat $TRACE | grep -v Whole | grep -v Slice | wc -l`
      num_regions=`cat t.simpoints | wc -l`
      BM="PyTorch"
      echo -n "$BM, $num_slices, $num_regions,  $WholeRDTSC, "
      cat $TRACE | grep "\." | sed  '/,/s///g' | awk -v N=$num_slices -v WP=$WholeRDTSC '
      BEGIN {sum=0}
        {mult=$5*N; rdtsc=$2; sum=sum+mult*rdtsc};
      END {printf "%d,%5.2f%\n",sum, (sum-WP)/WP*100 }
      '
    fi
