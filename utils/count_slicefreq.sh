#!/bin/bash
#set -x
IFS="\n"
for s in `grep "^T:" $1`
do
echo $s | sed '/^T/s///' | awk '
  { for (i=1; i<=NF; i++) { split($i,a,":"); fcount+=a[3]}}
  END {print "FCOUNT ", fcount}
  '
done
