# coding: utf-8
import requests
import re
import os
from utils import parse_url, get_urls
from Search import Search

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/536.36',
}
re_words = re.compile(u"[\u4e00-\u9fa5]+")


def save_pdf(s, html, login=False):
    """
    保存pdf到本地
    @params s: requests的session
    @params html: 请求到的网页
    @params login: 是否连接到校园网，默认未连接

    @return 保存pdf的名字
    """
    url_lst = re.findall(r'<a target="_blank" href="&#xA;(.+)">', html)
    name = re.findall(r'id="chTitle">(.+)</span>', html)

    if name:
        res = re.findall(re_words, name[0])
        name = ''.join(s for s in res)

    for url in url_lst:
        if 'pdfdown' in url:
            pdf_url = parse_url(url)
            if name + '.pdf' not in os.listdir():
                print('Download ing')
                if login:
                    url = 'http://gb.oversea.cnki.net'
                else:
                    url = 'http://gb-oversea-cnki-net.wvpn.ncu.edu.cn'
                response = s.get(url + pdf_url, stream=True)
                with open(name + '.pdf', 'wb') as file:
                    for data in response.iter_content(chunk_size=1024):
                        file.write(data)
                print('success')
                return name + '.pdf'
            else:
                print('{} have been in directory'.format(name + '.pdf'))
                return ''


def login_download(username, password, url_lst):
    """
    @params username: 学号
    @params password: 密码
    @params url_lst: 需要下载论文的海外知网的链接

    @return None
    """
    data = {
        'utf8': '✓',
        'user[login]': username,
        'user[password]': password,
        'user[dymatice_code]': 'unknown',
        'commit': '登录 Login',
    }
    login_url = 'http://wvpn.ncu.edu.cn/users/sign_in'

    with requests.Session() as s:
        html = s.get(login_url).text
        token = re.findall(r'name="csrf-token" content="(.+)" />', html)
        data['authenticity_token'] = token,
        s.post(login_url, data=data, headers=headers)

        for url in url_lst:
            # 海外知网下载页面 origin_url = 'http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=1016156901.nh&DbName=CMFD201602&DbCode=CMFD'
            # 不确定无线网络登陆情况下，是否需要替换网址，若需要可以根据自己机构的网址来替换。
            if url:
                # 替换
                new_url = url.replace('gb.oversea.cnki.net',
                                      'gb-oversea-cnki-net.wvpn.ncu.edu.cn')
                print(new_url)
                html = s.get(new_url, headers=headers).text

                fname = save_pdf(s, html)


def download(url_lst):
    """
    @params url_lst: 需要下载论文的海外知网的链接
    
    @return None
    """
    with requests.Session() as s:
        for url in url_lst:
            html = s.get(url, headers=headers).text
            save_pdf(s, html, login=True)


if __name__ == '__main__':
    username = ''
    password = ''

    # 搜索得到url
    # text = 'TEST'
    # search = Search(method='Title', category='result', batch=False)
    # url_lst = [search.run(text)]

    # 根据CNKI导出的endnote文件（txt），解析标题，并搜索url，可能搜索不到标题
    # endnote = ''
    # with open('{}.txt'.format(endnote), 'r', encoding='utf-8') as f:
    #     data = f.read()
    # title_lst = re.findall(r'%T (.+)\n', data)
    # search = Search(method='Title', category='result', batch=False)
    # url_lst = [
    #     search.run(text) for title in title_lst
    # ]

    # 手动设定
    # url_lst = [
    #   'http://gb.oversea.cnki.net/kcms/detail/detail.aspx?recid=&FileName=JDEW603.003&DbName=CJFD9697&DbCode=CJFD',
    # ]

    # 批量获取论文
    # fname = '中国学术文献网络出版总库_files'
    # url_lst = get_urls(fname)

    # 未连接校园网的情况
    # login_download(username, password, url_lst)

    # 连接校园网的情况
    # download(url_lst)
