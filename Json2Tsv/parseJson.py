#!python
import json
import sys
import re


def parsejson(jsonf,tsv_outputf):
    jsonfile = jsonf
    output = tsv_outputf
    print("Reading files...")
    f = open(jsonfile)
    w = open(output,'w')
    print("Loading....")
    js =json.load(f)
    count=0   # count line output
    for item in js:
        count+=1
        print("Processing "+str(count)+" line")
        dna_change = item['genomic_dna_change']
        ssm_id = item['ssm_id']
        mutation_subtype = item['mutation_subtype']
        consequences = []
        for cons in item['consequence']:
            transcript = cons["transcript"]
            # 1
            if ("is_canonical" in transcript):
                is_canonical = str(transcript['is_canonical'])
            else:
                is_canonical = 'null'
            # 2
            if ("gene" in transcript):
                if ('symbol' in transcript['gene']):
                    genesymbol = transcript['gene']['symbol']
                else:
                    genesymbol = 'null'
                if ('gene_id' in transcript['gene']):
                    gene_id = transcript['gene']['gene_id']
                else:
                    gene_id = 'null'
                
            else:
                genesymbol = 'null'
                geneid = 'null'
            # 3
            if ("annotation" in transcript):
                if ("impact" in transcript['annotation']):
                    impact = transcript['annotation']['impact']
                else:
                    impact = 'null'
            else:
                impact = 'null'

            # 4
            if ("aa_change" in transcript):
                aa_change = transcript["aa_change"]
                if (aa_change is None):
                    aa_change = 'null'
            else:
                aa_change = 'null'

            # 5
            if("consequence_type" in transcript):
                consequence_type = transcript["consequence_type"]
            else:
                consequence_type = 'null'

            # sumup
            trans_str = '|'.join([genesymbol,gene_id,aa_change,impact,consequence_type,is_canonical])
            consequences.append(trans_str)
        consequences_str = ','.join(consequences)

        # parse dna change 
        # m = re.search('chr([0-9XYxy]{1,2}):g\.([0-9]+)([ACTG])>([ACTG])',dna_change)
        # Chr = m.group(1)
        # Pos = m.group(2)
        # Ref = m.group(3)
        # Alt = m.group(4)
        #item_elm = [Chr, Pos, Ref, Alt, consequences_str, ssm_id, mutation_subtype]
        Chr,Pos,Ref,Alt = parseDnaChange(dna_change)
        item_elm = [Chr,Pos,Ref,Alt, consequences_str, ssm_id, mutation_subtype]
        itemstr = '\t'.join(item_elm)

        w.write(itemstr)
        w.write('\n')
        w.flush()
    w.close()
    f.close()

def parseDnaChange(s):
    if '>' in s:
        m = re.search('chr([0-9XYxy]{1,2}):g\.([0-9]+)([ACTG]+)>([ACTG]+)',s)
        Chr = m.group(1)
        Pos = m.group(2)
        Ref = m.group(3)
        Alt = m.group(4)
        #Type = 'snp'
    if 'ins' in s:
        m = re.search('chr([0-9XYxy]{1,2}):g\.[0-9]+_([0-9]+)ins([ACTG]+)',s)
        Chr = m.group(1)
        Pos = m.group(2)
        Ref = '.'
        Alt = m.group(3)
        #Type = 'ins'
    if 'del' in s:
        m = re.search('chr([0-9XYxy]{1,2}):g\.([0-9]+)del([ATCG]+)',s)
        Chr = m.group(1)
        Pos = m.group(2)
        Ref = m.group(3)
        Alt = '.'
        #Type = 'del'
    return (Chr,Pos,Ref,Alt)

if __name__ == "__main__":
    if len(sys.argv)<3:
        print("Usage: python {0} <json file> <output file>".format(sys.argv[0]))
        sys.exit()

    inputf = sys.argv[1]
    outputf = sys.argv[2]
    parsejson(inputf,outputf)
    print("Done!")

