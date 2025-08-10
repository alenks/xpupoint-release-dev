#!/bin/bash
ERROR()
{
  echo "Usage : $0 slice.trace.txt t.simpoints"
  exit
}
if  [ $# -ne 2 ];  then
    echo "args " $#
    ERROR
fi

SLFILE=$1
TSIMFILE=$2

IFS=$'\n'
for rec in `cat $TSIMFILE`
do
  cl=`echo $rec | awk '{print $2}'`
  echo "cluster = $cl"
    #cat slice.trace.txt | awk '{print $1,$2,$3,$4,$5}' |  sort -n -t "," -k 3 | grep -e ", $cl" > cluster.$cl.txt
    cat $SLFILE | awk -v CL=$cl '{if ($5==CL"") print $0}' > cluster.$cl.txt
done
