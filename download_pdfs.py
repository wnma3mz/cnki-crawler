# coding: utf8
import requests
import re
import os

from utils import replace_name, parse_url, get_urls


def save_pdf(s, html):

    url_lst = re.findall(r'<a target="_blank" href="&#xA;(.+)">', html)
    name = re.findall(r'id="chTitle">(.+)</span>', html)

    if name:
        name = replace_name(name[0])

    for url in url_lst:
        if 'pdfdown' in url:
            pdf_url = parse_url(url)

    if (pdf_url) and (name not in os.listdir()):
        response = s.get(
            'http://gb-oversea-cnki-net.wvpn.ncu.edu.cn' + pdf_url, stream=True)
        with open(name + '.pdf', 'wb') as file:
            for data in response.iter_content(chunk_size=64):
                file.write(data)


def download(url_lst):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/536.36',
    }

    with requests.Session() as s:

        for url in url_lst:
            # 海外知网下载页面 origin_url = 'http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=1016156901.nh&DbName=CMFD201602&DbCode=CMFD'
            # 不确定无线网络登陆情况下，是否需要替换网址，若需要可以根据自己机构的网址来替换。
            new_url = url
            # print(new_url)
            html = s.get(new_url, headers=headers).text
            save_pdf(s, html)


if __name__ == '__main__':

    # url_lst = [
    # 'http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=JDEW603.003&DbName=CJFD9697&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=MAZH201814010&DbName=CJFDLASN2018&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=SHKF201801001&DbName=CJFDLAST2018&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=LQXJ201002042&DbName=CJFDLAST2018&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=ZWQY201815168&DbName=CJFDLAST2018&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=CDSY201703024&DbName=CJFDLAST2017&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=SZXY201804012&DbName=CJFDLAST2018&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=BJJJ201601051&DbName=CJFDLAST2016&DbCode=CJFD',
    #     'http://gb.oversea.cnki.net/kns55/detail/detail.aspx?recid=&FileName=HWYY201422063&DbName=CJFDLAST2015&DbCode=CJFD'
    # ]
    # 批量获取论文
    fname = '中国学术文献网络出版总库_files'
    url_lst = get_urls(fname)

    # 连接NCU
    download(url_lst)
