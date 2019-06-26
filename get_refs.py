# coding: utf-8
import requests
import grequests
from bs4 import BeautifulSoup as soup
import re
import math
from functools import reduce
from utils import parse_url


class CNKI_refs(object):
    def __init__(self, url, CurDBCode='CRLDENG'):
        """
        CRLDENG: 外文参考文献
        SSJD: 国际期刊数据库
        """
        self.url = 'http://gb.oversea.cnki.net/kcms/detail/frame/list.aspx'
        params = self.get_params(url)
        # print(params)
        self.params = {
            'dbcode': params['dbcode'],
            'filename': params['filename'],
            'dbname': params['dbname'],
            'RefType': '1',
            'CurDBCode': CurDBCode,
            # 'page': str(page_num)
        }

    def get_params(self, url):

        params_lst = url.lower().split('?')[-1].split('&')
        params_dict = {}

        for params in params_lst:
            kv = params.split('=')
            if len(kv) == 2:
                params_dict[kv[0]] = kv[1]
            else:
                params_dict[kv[0]] = ''

        return params_dict

    def get_li_lst(self, text):
        html = soup(text, 'lxml')
        li_lst = html.find_all('li')
        page_li = [li.text for li in li_lst]
        return page_li

    def get_page_num(self):
        s = requests.get(self.url, params=self.params)
        num = re.findall(r'共找到 (\w+) 条', s.text)[0]
        num = math.ceil(int(num) / 10)
        return num

    def get_text(self, page_num):
        self.params['page'] = page_num
        s = requests.get(self.url, params=self.params)
        return self.get_li_lst(s.text)

    def main(self):
        num = self.get_page_num()
        url_lst = map(self.get_text, list(range(1, num + 1)))
        # print(url_lst)
        try:
            res = reduce(lambda x, y: x + y, url_lst)
            return list(res)
        except:
            return []


def get_urls(fname):
    # 获取关键词的所有的论文，需要页面上手动保存到本地
    with open('{}/brief.html'.format(fname), 'r', encoding='utf8') as f:
        html = f.read()

    matchs = re.findall(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')', html)

    urls = [parse_url(url) for url in matchs if 'detail' in url]

    return urls[::2]


if __name__ == '__main__':

    # url = 'http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=1017296391.nh&DbName=CDFDLAST2018&DbCode=CDFD'
    # url = 'http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=1019008016.nh&DbName=CDFDTEMP&DbCode=CDFD'
    # url_lst_1 = get_urls('博士')
    # url_lst_2 = get_urls('硕士')
    import pickle
    # CRLDENG: 外文参考文献
    # SSJD: 国际期刊数据库
    url_lst = get_urls(fname)
    url_lst_all = []
    for url in url_lst:
        ref = CNKI_refs(url, CurDBCode=dbcode)
        ref_lst = ref.main()
        url_lst_all.append(ref_lst)
    with open(f'{dbcode}{fname}.pkl', 'wb') as f:
        pickle.dump(url_lst_all, f)
