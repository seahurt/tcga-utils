#!/bin/basho
if [ ! $1 ]||[ ! $2 ];then
    echo "Usage: sh $0 <input.bed> <output.bed>"
    exit
fi
read -p "Input the full path of bedtools:" bedtools
inputbed=$1
refbed=genExonRefBed/sorted.exon.bed
outputbed=$2
echo "sorting..."
sh sortByChr.sh $inputbed input.sorted.bed
echo "add exon info"
$bedtools intersect -a input.sorted.bed -b $refbed -wa -wb|cut -f 1,2,3,7,8 >tmp
echo "rm dup info"
perl rmDupinBed.pl tmp $outputbed
echo "rm tmp files"
rm input.sorted.bed
rm tmp
echo "All done!"
