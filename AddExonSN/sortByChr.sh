#!/bin/bash
if [ ! $1 ]||[ ! $2 ];then
    echo "Usage: sh $0 <unsort> <sorted>"
    exit
fi
unsort=$1
sorted=$2
grep -v '^[XYM]' $unsort |sort -n -t $'\t' -k 1 -k 2 |uniq>$sorted
grep '^X' $unsort |sort -n -t $'\t'  -k 2 |uniq >>$sorted
grep '^Y' $unsort |sort -n -t $'\t'  -k 2 |uniq >>$sorted
grep '^M' $unsort |sort -n -t $'\t'  -k 2 |uniq >>$sorted
echo "Check this order:"
cut -f 1 $sorted|uniq
echo "Done!"
