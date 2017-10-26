# tcga_tools
Some tools to handle tcga data


parseJson.py 可以将tcga partal上下载的变异数据json文件转换成tsv格式

sort_by_chr.sh 可以将首列是染色体编号，第二列是坐标的tsv文件按染色体编号及坐标排序

tsv2vcf.sh 可以为将tsv格式的变异文件（来自于parseJson和sort_by_chr）转换成标准的vcf格式

如果要将vcf的坐标系从GRCh38转换成hg19或其它的坐标系，可以用CrossMap这个软件,使用pip就可以安装