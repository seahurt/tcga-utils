#!/bin/sh

extractExon="perl /lustre/project/og03/Public/Pipe/Tumor/DataBase/Reference/gff2exon_bed.pl"
sortPos="sh /lustre/project/og03/Public/Pipe/Tumor/DataBase/Reference/sortByChr.sh"
addSN="python /lustre/project/og03/Public/Pipe/Tumor/DataBase/Reference/sortBed.py"
if [ ! $1 ] || [ ! $2 ];then
    echo "sh $0 <input.gff> <output.bed>"
    exit
fi
gff=$1
bed=$2

echo "Extract exon info from gff file"
$extractExon $gff oooooootmp
echo "Sort exon and rm dump"
$sortPos oooooootmp oooooootmp2
echo "Add exon SN"
$addSN oooooootmp2 oooooootmp3
echo "Sort again"
$sortPos oooooootmp3 $bed
echo "rm tmp file"
rm oooooootmp
rm oooooootmp2
rm oooooootmp3
echo "Done"


