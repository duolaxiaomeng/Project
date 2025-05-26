# 获取虎扑社区的内容，保存为csv格式
# 获取文章标题、分类、作者以及文章地址等内容

import requests
from bs4 import BeautifulSoup
import csv


# 下载网页内容
def downloader(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 SE 2.x MetaSr 1.0'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    content = response.text
    return content
    # 获取响应


# 获取链接
def getlisturl(url):
    url = 'https://bbs.hupu.com/'
    content = downloader(url)
    with open(r'./webpage/hupushequ.html', 'w', encoding='utf-8') as writer:
        writer.write(content)
    soup = BeautifulSoup(content, 'html.parser')
    div_list = soup.find_all('div', class_='hu-pc-navigation-topic-type-link')

    urllist = []
    for div in div_list:
        a_list = div.find_all('a')
        for a in a_list:
            link = a.get('href')
            urllist.append(link)
    return urllist


# 获取文章标题、分类、作者以及文章地址等内容
def getcontent(url):
    pass





if __name__ == '__main__':
    urllist = getlisturl('https://bbs.hup.com/')
    print(urllist)