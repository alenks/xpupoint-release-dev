#!/bin/bash
rm scan.out
for t in T.*.bb
do
 echo -n "$t ' ::' " >> scan.out
 grep -c -e ' ::' $t >> scan.out
 echo -n "$t ':[0-9][0-9]*: ' " >> scan.out
 grep -c -e ':[0-9][0-9]*: ' $t >> scan.out
 tail -2 scan.out
done
cat scan.out | awk '{if ($NF) print $0}'

