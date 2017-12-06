# TCGA Mutation Downloader

## Functions
* 整体思路通过提交查询POST数据获取json数据，然后解析数据，写入文件
* getHash(oldhash)
  - 生成新的hash,与BaseURL生成新的url，避免单个URL获取数据太多被中断
* getOption(url)
  - 用Option方法获取允许的数据提交方法，模拟浏览器访问网页时的操作
* getData(url,size,offset)
  -  用POST方法获取服务器数据
* parseData(inJson,size,offset)
  - 将获取的数据解析成列表返回
* writeOutFormat(outlist,fp)
  - 把解析后的数据输出到文件
* singleThreadRun()
  -  单进程获取数据的流程
* run(url,size,offset,filep)
  - 一次数据并解析输出
* multiRun(url,size,offset,basedir)
  - 多进程的方式获取数据并解析

