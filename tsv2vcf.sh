#!/bin/bash
tsv=$1
vcf=$2
mkdir -p tmp
cut -f 1,2 $tsv >tmp/chr_pos
cut -f 3,4 $tsv >tmp/ref_alt
cut -f 5 $tsv >tmp/consequence
cut -f 6 $tsv >tmp/tcga_id
cut -f 7 $tsv >tmp/var_type

sed 's/^/.\t.\tCONSEQUENCE=/' tmp/consequence >tmp/qual_filte_info
paste tmp/chr_pos tmp/tcga_id tmp/ref_alt tmp/qual_filte_info > tmp/tcga_content

echo  "##TCGA SOMATIC MUTATION 20171025" >tmp/header
echo  "##INFO=<ID=CONSEQUENCE,Number=.,Type=String,Description=Mutation consequence (subfields: gene|geneid|aa change|impact|consequence type|is_canonical)" >>tmp/header
echo  "##comment=TCGA json file parsed" >>tmp/header
echo  "##reference=GRCh38" >>tmp/header
echo  "##source=TCGA release 9.0" >>tmp/header
echo  "#CHROM  POS ID  REF ALT QUAL    FILTER  INFO" >>tmp/header

cat tmp/header tmp/tcga_content >$vcf

#rm tmp -r
