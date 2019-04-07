# coding: utf8

import re


def parse_url(url):
    return url.replace('amp;', '').replace(' ', '')


def replace_name(name):
    return name.replace('<sub>', '').replace(
        '</sub>', '').replace('/', '-')


def get_urls(fname):
    # 获取关键词的所有的论文，需要页面上手动保存到本地
    with open('{}/brief.html'.format(fname), 'r', encoding='utf8') as f:
        html = f.read()

    matchs = re.findall(
        r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')', html)

    urls = [parse_url(url) for url in matchs if 'detail' in url]

    return urls[::2]
