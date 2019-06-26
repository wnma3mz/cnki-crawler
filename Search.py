# coding: utf-8

import re

import requests


class Search(object):
    def __init__(self,
                 method='Theme',
                 order=str(1),
                 category='index',
                 batch=False):
        """
        @params method: 搜索方法        
            'Content': 全文
            'Title': 标题
            'Theme': 主题
            'KeyWord': 关键词
            'Author': 作者
            。。。
        @params order: 搜索结果排序
            '1': 相关度排序，
            '2': 发表时间，
            '3': 下载次数，
            '4': 被引次数
        @params category: 搜索类别 
            'index': 学位论文
            'result': 全部
            。。。
        @params batch: 是否批量下载，默认否
        """
        self.method = method
        self.order = order
        self.category = category

        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }
        self.caj_url = re.compile(
            r'href="(.+)" target="_blank" .+ data-dflag="cajdown"')

    def yuanjian_search(self):
        """
        @params None

        @return 返回搜索结果页
        """
        data = {
            'searchType': 'MulityTermsSearch',
            self.method: self.text,
            'Order': self.order,
        }
        url = 'http://yuanjian.cnki.net/Search/Result'

        if self.category == 'index':
            url = 'http://yuanjian.cnki.net/cdmd/Search/index'
            data['ArticleType'] = '14'
            data['Type'] = '14'
            print(1)

        response = requests.post(url, headers=self.headers, data=data)
        return response

    def run(self, text):
        """
        @params text: 搜索的文本

        @return 需要下载的海外知网的链接
        """
        self.text = text

        res = self.yuanjian_search()

        url_lst = re.findall(
            r'<a href="(.+)" target="_blank" class="left" title="', res.text)

        try:
            cnki_url = self.cnki_detail(url_lst[0])
            oversea_url = self.cnki2oversea(cnki_url)
            print(cnki_url, oversea_url)

            if batch:
                return [
                    self.cnki2oversea(self.cnki_detail(url)) for url in url_lst
                ]
            else:
                return oversea_url
        except:
            print(self.text, 'not found!')
            return ''

    def cnki2oversea(self, cnki_url):
        """
        @params cnki_url: 知网caj的下载链接

        @return oversea_url: 海外知网的详情页链接
        """
        params_lst = cnki_url.split('?')[-1].split('&')
        dbcode, dbname, year, filename = '', '', '', ''
        for param in params_lst:
            if 'filename' in param.lower():
                filename = param.split('=')[-1]
            if 'dbcode' in param.lower():
                dbcode = param.split('=')[-1]
            if 'year' in param.lower():
                year = param.split('=')[-1]
        url = 'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&'
        if dbcode == 'CJFD':
            dbname = 'CAPJLAST'
        if dbcode == 'CMFD' or 'CDFD':
            dbname = dbcode + year

        oversea_url = url + f"FileName={filename}&DbName={dbname}&DbCode={dbcode}"
        return oversea_url

    def cnki_detail(self, url):
        """
        @params url: 论文详情页的url

        @return cnki_url: caj下载的url
        """
        response = requests.get(url).text
        try:
            cajdownload_url = caj_url.findall(response)[0]
        except:
            return 'Failed'
        return cajdownload_url
