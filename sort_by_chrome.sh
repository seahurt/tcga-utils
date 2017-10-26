#!/bin/bash
unsort=$1
sorted=$2

grep -v '^[XY]' $unsort |sort -n -t $'\t' -k 1 -k 2 >$sorted
grep '^X' $unsort |sort -n -t $'\t'  -k 2 >>$sorted
grep '^Y' $unsort |sort -n -t $'\t'  -k 2 >>$sorted

echo "Check this order:"
cut -f 1 $sorted|uniq
echo "Done!"
