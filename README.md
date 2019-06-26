## CNKI-Crawler

### get_refs.py

根据[海外知网](<http://gb.oversea.cnki.net/kns55/default.aspx>)的论文链接，来获取文章的参考文献。比如输入`<http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=1017296391.nh&DbName=CDFDLAST2018&DbCode=CDFD>`的链接，返回它的英文的引用文献。具体见代码注释。

我自己的使用习惯是，查看博士学位论文与硕士学位论文，分别保存他们的搜索结果表格，再解析出他们的`url`，进一步获取他们的外文参考文献。

### download_pdf.py

关于下载知网论文，由于学校购买的知网的数据库，连校园网或者远程登陆即可下载。

获取url方式:
1. 根据信息直接搜索得到url
2. 根据cnki的endnote文件得到url
3. 手动输入url
4. 手动保存海外知网的表格，得到url_lst

这里有"远程登陆本校校园网下载"与"连接校园网下载"的两种下载方式。

### Search.py

根据关键信息（标题，主题等）搜索结果并返回海外知网的url。根据知网的[远见搜索](http://yuanjian.cnki.net/Search/Result)的搜索结果，实验发现，部分论文可能存在搜索不到的情况。
