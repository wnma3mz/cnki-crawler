# coding: utf-8

import re


def parse_url(url):
    """
    替换url
    @params url: 需要替换的url
    
    @return 替换后的url
    """
    return url.replace('amp;', '').replace(' ', '')


def get_urls(fname):
    """
    @params fname: 本地保存的文件夹名，默认为"中国学术文献网络出版总库_files"
    
    @return urls: 所有论文页面链接
    """
    # 获取关键词的所有的论文，需要在搜索页面上手动保存到本地
    with open('{}/brief.html'.format(fname), 'r', encoding='utf8') as f:
        html = f.read()

    matchs = re.findall(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')', html)

    urls = [parse_url(url) for url in matchs if 'detail' in url]

    return urls[::2]
