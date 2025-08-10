#!/bin/bash
set -x
rm -rf workspace
mkdir workspace
set -x
PID=`ls | grep BasicBlocksGPU | awk -F "." '{print $2}'`
echo "PID $PID"
for BB in `find BasicBlocksCPU -name "T.$PID.*.bb"`
do
  echo $BB
  SRC=`readlink -f $BB`
  TMP=`basename $BB`
  DST=`echo $TMP | sed "/\.$PID/s///"`
  ln -sf $SRC workspace/$DST
done
for GBB in `find BasicBlocksGPU.$PID -name "*.bbv"`
do
  echo $GBB
  SRC=`readlink -f $GBB`
  TMP=`basename $GBB`
  DST=`echo $TMP | sed "/\.$PID/s///"`
  ln -sf $SRC workspace/$DST
done
