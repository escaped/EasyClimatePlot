#!/bin/bash
#
# calculate the mean of a column
#

if [ $# -eq 2 ]
then
FILENAME=$1
COL=$2

# else: read from stdin
else
  COL=$1
fi

SUM=0
INPUTLENGTH=0
cat $FILENAME > tmp
for val in $(awk '{print $ARGV[2];}' tmp $COL)
do
  SUM=$(echo "$SUM + $val" | bc)
  INPUTLENGTH=$(echo "$INPUTLENGTH+1" | bc)
done

echo "scale=5;$SUM/($INPUTLENGTH)" | bc
