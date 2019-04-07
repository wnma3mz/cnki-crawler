## CNKI-Crawler

### get_refs.py

根据[海外知网](<http://gb.oversea.cnki.net/kns55/default.aspx>)的论文链接，来获取文章的参考文献。比如输入`<http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=1017296391.nh&DbName=CDFDLAST2018&DbCode=CDFD>`的链接，返回它的英文的引用文献。具体见代码注释。

我自己的使用习惯是，查看博士学位论文与硕士学位论文，分别保存他们的搜索结果表格，再解析出他们的`url`，进一步获取他们的外文参考文献。

### download_pdf.py

关于下载知网论文，由于学校购买的知网的数据库，连校园网或者远程登陆即可下载。

但由于各个学校/机构远程登陆方式不一样，登陆代码就不放出来。若有需要，请提issue。这里放出的是，连接网络可直接批量下载的方式。

目前还是无法根据标题/关键字来搜索获取论文的链接。所以目前的方式是保存搜索结果至本地，然后解析url。

