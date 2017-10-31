#!python
import os
import sys
input = sys.argv[1]
output = sys.argv[2]

f = open(input)
exon_pool=dict()
o = open(output,'w')
for line in f.readlines():
    if('#' in line):
        continue
    if(line==""):
        break
    (chr,start,end,gene)=line.split()
    #print(gene)
    if (gene in exon_pool):
        exon_pool[gene].append((start,end,chr))
    else:
        exon_pool[gene]=[(start,end,chr)]

for gene in exon_pool.keys():
    count=1
    #print(gene)
    #print(exon_pool[gene])
    #exon_pool[gene].sort(key=lambda x:x[0])
    for exon in sorted(exon_pool[gene],key=lambda x: int(x[0])):
        o.write("{chr}\t{start}\t{end}\t{gene}\t{count}\n".format(chr=exon[2],start=exon[0],end=exon[1],gene=gene,count=count))
        o.flush()
        count=count+1
f.close()
o.close()
