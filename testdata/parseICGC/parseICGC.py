#!python
#Chr    Start   End     Ref     Alt     ICGC_Id ICGC_Occurrence
# 1       10002   10002   A       T       MU43280717      MELA-AU|1|183|0.00546

#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
# 1       1000000 MU88749506      T       .       .       .       CONSEQUENCE=.;OCCURRENCE=NKTL-SG|23|23|1.00000;affected_donors=23;mutation=T>T;project_count=1;studies=.;tested_donors=12198

import sys
# def extend_pos(pos,ref,alt):
#     #
#     length_ref = len(ref) 
#     length_alt = len(alt)
#     pos = int(pos)
#     # insert
#     if length_ref==0:
#         start = pos
#         end = pos
#         ref = '-'
#         return ((start,end,ref,alt))

#     # del
#     if length_alt ==0:
#         start = pos
#         end = pos+length_ref-1
#         alt='-'
#         return ((start,end,ref,alt))
#     # snp and mnp
#     if length_alt == length_ref:
#         start = pos
#         end = pos+length_alt-1
#         return ((start,end,ref,alt))
#     # mnp length not equal
#     if length_alt!=le

def format_pos(pos,ref,alt):
    pass
    return(start,end,ref,alt)


def main(raw_file,output_file):
    #raw_file = sys.argv[1]
    #output_file = sys.argv[2]

    r = open(raw_file)
    o = open(output_file,'w')
    o.write('#Chr\tStart\tEnd\tRef\tAlt\tICGC_Id\tICGC_Occurrence\n')
    o.flush()

    while(True):
        line = r.readline()
        if line == '':
            break
        if '#' in line:
            continue
        (chr,pos,id,ref,alt,qual,filter,info)=line.split()
        print (chr,pos,id,ref,alt,qual,filter,info)
        occur = info.split(';')[1].split('=')[1]
        print (occur)
        #
        if ref == '.':
            ref = '-'
        if alt == '.':
            alt = '-'
        start = pos
        end = int(pos)+len(ref)-1

        output_str = '\t'.join([chr,start,str(end),ref,alt,id,occur])+'\n'
        o.write(output_str)
        o.flush()
    o.close()
    r.close()

if __name__ == '__main__':
    if len(sys.argv)<3:
        print("Usage: python {0} <raw_file> <output_file>".format(sys.argv[0]))
        sys.exit()
    raw_file = sys.argv[1]
    output_file = sys.argv[2]
    main(raw_file,output_file)



