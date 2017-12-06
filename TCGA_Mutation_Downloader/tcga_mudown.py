#!python
import os
import sys
import json
import requests
import time
import re
import random
import hashlib
from multiprocessing import Pool
#global file
total_vars = 3115606
jsonStr = r'''
{
    "query": "query SsmsTable_relayQuery(\n  $ssmTested: FiltersArgument\n  $ssmCaseFilter: FiltersArgument\n  $ssmsTable_size: Int\n  $consequenceFilters: FiltersArgument\n  $ssmsTable_offset: Int\n  $ssmsTable_filters: FiltersArgument\n  $score: String\n  $sort: [Sort]\n) {\n  viewer {\n    explore {\n      cases {\n        hits(first: 0, filters: $ssmTested) {\n          total\n        }\n      }\n      filteredCases: cases {\n        hits(first: 0, filters: $ssmCaseFilter) {\n          total\n        }\n      }\n      ssms {\n        hits(first: $ssmsTable_size, offset: $ssmsTable_offset, filters: $ssmsTable_filters, score: $score, sort: $sort) {\n          total\n          edges {\n            node {\n              id\n              score\n              genomic_dna_change\n              mutation_subtype\n              ssm_id\n              consequence {\n                hits(first: 1, filters: $consequenceFilters) {\n                  edges {\n                    node {\n                      transcript {\n                        is_canonical\n                        annotation {\n                          impact\n                        }\n                        consequence_type\n                        gene {\n                          gene_id\n                          symbol\n                        }\n                        aa_change\n                      }\n                      id\n                    }\n                  }\n                }\n              }\n              filteredOccurences: occurrence {\n                hits(first: 0, filters: $ssmCaseFilter) {\n                  total\n                }\n              }\n              occurrence {\n                hits(first: 0, filters: $ssmTested) {\n                  total\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n",
    "variables": {
        "ssmTested": {
            "op": "and",
            "content": [
                {
                    "op": "in",
                    "content": {
                        "field": "cases.available_variation_data",
                        "value": [
                            "ssm"
                        ]
                    }
                }
            ]
        },
        "ssmCaseFilter": {
            "op": "and",
            "content": [
                {
                    "op": "in",
                    "content": {
                        "field": "available_variation_data",
                        "value": [
                            "ssm"
                        ]
                    }
                }
            ]
        },
        "ssmsTable_size": 10,
        "consequenceFilters": {
            "op": "NOT",
            "content": {
                "field": "consequence.transcript.annotation.impact",
                "value": "missing"
            }
        },
        "ssmsTable_offset": 0,
        "ssmsTable_filters": null,
        "score": "occurrence.case.project.project_id",
        "sort": [
            {
                "field": "_score",
                "order": "desc"
            },
            {
                "field": "_uid",
                "order": "asc"
            }
        ]
    }
}
'''

jsonDict = json.loads(jsonStr)
URL = r'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=2bd1bd20d2e5e00592b69c4625586ea1'
TotalCase= 0
# Total_Mutation_Record = dict() # key:ssid value:{}
BaseURL = r'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash='

def getHash(oldhash):
    # origin_url = r'https://portal.gdc.cancer.gov/exploration?searchTableTab=mutations'
    # TODO
    newhash = hashlib.md5(oldhash.encode('utf-8')).hexdigest()
    return newhash

def getOption(url):
    r = requests.options(url)
    if r.status_code==200:
        return True 
    else:
        print(r.status_code)
        return False

def rmDup(inlist):
    tmp = []
    for x in inlist:
        if x is None:
            x = '.'
        if x not in tmp:
            tmp.append(str(x))
    return tmp

def getData(url,size,offset):
    jsonDict['variables']['ssmsTable_size'] = size
    jsonDict['variables']['ssmsTable_offset'] = offset
    response = requests.post(url,data=json.dumps(jsonDict))
    return response.json()

def parseData(inJson,size,offset):
    try:
        TotalCase = inJson['data']['viewer']['explore']['cases']['hits']['total']
        result_lsit = inJson['data']['viewer']['explore']['ssms']['hits']['edges']
        records = []
        for item in result_lsit:
            ssm_id = item['node']['ssm_id']
            cases = item['node']['score']
            dna_change = item['node']['genomic_dna_change']
            mutation_subtype = item['node']['mutation_subtype']
            gene_id = []
            gene = []
            consequence_type = []
            aa_change = []
            impact = []
            is_canonical = []
            # mutiple trancript
            for x in item['node']['consequence']['hits']['edges']:
                gene_id.append(x['node']['transcript']['gene']['gene_id'])
                gene.append(x['node']['transcript']['gene']['symbol'])
                consequence_type.append(x['node']['transcript']['consequence_type'])
                aa_change.append(x['node']['transcript']['aa_change'])
                impact.append(x['node']['transcript']['annotation']['impact'])
                is_canonical.append(x['node']['transcript']['is_canonical'])
            gene = ','.join(rmDup(gene))
            gene_id = ','.join(rmDup(gene_id))
            consequence_type = ','.join(rmDup(consequence_type))
            aa_change = ','.join(rmDup(aa_change))
            impact = ','.join(rmDup(impact))
            is_canonical = ','.join(rmDup(is_canonical))
            # save 
            record = [ssm_id,str(cases),dna_change,mutation_subtype,gene,gene_id,
                      consequence_type,aa_change,impact,str(is_canonical),TotalCase]
            records.append(record)

        return records
    except KeyError:
        with open('tcga.log','w') as f:
            print((size,offset,'found error'),f)

        # Total_Mutation_Record[ssm_id] = dict()
        # Total_Mutation_Record[ssm_id]['cases'] = cases
        # Total_Mutation_Record[ssm_id]['dna_change'] = dna_change
        # Total_Mutation_Record[ssm_id]['mutation_subtype'] = mutation_subtype
        # Total_Mutation_Record[ssm_id]['gene_id'] = gene_id
        # Total_Mutation_Record[ssm_id]['gene'] = gene
        # Total_Mutation_Record[ssm_id]['consequence_type'] = consequence_type
        # Total_Mutation_Record[ssm_id]['aa_change'] = aa_change
        # Total_Mutation_Record[ssm_id]['impact'] = impact
        # Total_Mutation_Record[ssm_id]['is_canonical'] = is_canonical
def writeOutFormat(outlist,fp):
    #[ssm_id,str(cases),dna_change,mutation_subtype,gene,gene_id,consequence_type,aa_change,impact,str(is_canonical)]
    for item in outlist:
        ssm_id,cases,dna_change,mutation_subtype,gene,gene_id,consequence_type,aa_change,impact,is_canonical,TotalCase= item
        Chr = re.search('(?P<chr>chr[0-9XYMxym]+)',dna_change).group('chr')
        Pos = re.search('g.(?P<pos>[0-9]+)',dna_change).group('pos')
        if '>' in dna_change:
            Ref = re.search('([A-Z]+)>([A-Z]+)',dna_change).group(1)
            Alt = re.search('([A-Z]+)>([A-Z]+)',dna_change).group(2)
            Start = Pos 
            End = Pos
        elif 'del' in dna_change:
            Ref = re.search('del([A-Z])+',dna_change).group(1)
            Alt = '-'
            Start = Pos
            End = str(int(Pos)+len(Ref)-1)
        elif 'ins' in dna_change:
            Ref = '-'
            Alt = re.search('ins([A-Z]+)',dna_change).group(1)
            Start = Pos
            End = str(int(Pos) + len(Alt)-1)
        else:
            print(dna_change)
            Ref = '-'
            Alt = '-'
            Start = Pos
            End = Pos
        VF = '%4f' % (float(cases)/int(TotalCase))
        outstring = '\t'.join([Chr,Start,End,Ref,Alt,gene,aa_change,VF,mutation_subtype, consequence_type, impact])+'\n'
        fp.write(outstring)
        fp.flush()


def singleThreadRun():  
    count = 0
    mutation_size = 0
    url = URL
    size = 100
    while(True):
        offset = count*size
        print(size,offset)
        print("Obtaining data...")
        #r = getOption(url)
        #print(r.status_code)
        try:
            data = getData(url,size,offset)
        except:
            print("Wait for 20s before retry...")
            time.sleep(20)
            url = BaseURL+getHash(url.split('=')[-1])
            r = getOption(url)

        print("Parsing data...")       
        parseData(data,size,offset)
        count+=1
        time.sleep(1)
        if offset + size >total_vars:
            print("Done!")
            break

def run(url,size,offset,filep):
    print(size,offset)
    r = requests.options(url)
    if r.status_code==200:
        print("Fetching...")
        data = getData(url,size,offset)
        print("Parsing...")
        records = parseData(data,size,offset)
        with open(filep,'w') as fp:
            writeOutFormat(records,fp)
    else:
        print("Connection error")
        raise BaseException 

def multiRun(url,size,offset,basedir):
    
    taskPool = []
    Total = 3115606
    while True:
        url = BaseURL+getHash(url.split('=')[-1])
        filep = os.path.join(basedir,str(offset)+'.xls')
        taskPool.append((url,size,offset,filep))
        offset += size
        if offset > Total:
            break
    p = Pool()
    for x in taskPool:
        p.apply_async(run,args=x)
    p.close()
    p.join()


if __name__ == '__main__':
    testdir = os.path.abspath('test')
    if not os.path.exists(testdir):
        os.mkdir(testdir)
    url = BaseURL+getHash(URL.split('=')[-1])
    run(url,1000,0,testdir)
