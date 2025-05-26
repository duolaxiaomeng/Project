import random
import time
import urllib.error
from lxml import etree
import requests

use_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',]
#下载网页内容
def downloader(url):
    try:
        # headers = {'User-Agent':'Mozilla/5.0'}
 headers = {'User-Agent': random.choice(use_agent_list)}
        response = requests.get(url, headers=headers)
        content = response.text
        return content
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
        time.sleep(2)
    except Exception as e:
        print('exception:',e)
        time.sleep(2)

#获取网页的链接
def getlisturl():
    try:
        urllist = []
        url = 'https://www.ctoutiao.com/'
 content = downloader(url)
        with open('./webpage/ctotiao.html', 'w', encoding='utf-8') as writer:
            writer.write(content)
        html = etree.HTML(content)
        div_list = html.xpath('//div[@class="ctt-home-flow-item"]')
        #print(div_list)
 for div in div_list:
            try:
                link = div.xpath('.//h2/a/@href')
                # print(link)
 urllist.append(link[0])
            except Exception as e:
                continue
        return urllist

    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
        time.sleep(2)
    except Exception as e:
        print('exception:',e)
        time.sleep(2)

#获取每个链接的内容
def getcontent(urllist):
    with  open(r'./webpage/ctoutiao_article.html','wb') as writer:
        html1 = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <title>创头条页面</title>
</head>
<body>'''
 writer.write(html1.encode('utf-8'))
    with open(r'./webpage/ctoutiao_article.html','ab') as writer:
        for i in range(len(urllist)):
            try:
                url = urllist[i]
                new_url = 'https://www.ctoutiao.com'+url #拼接连接地址
 data = downloader(new_url)
                html = etree.HTML(data)
                #标题
 title = html.xpath('//title/text()')
                if title:
                    this_title  =title[0]
                else:
                    this_title = '空标题'
 #获取p标签的内容
 p_list = html.xpath('//div[@class="ctt-details-texts"]/p')
                if p_list:
                   this_content = ''
 for p in p_list:
                       text = p.xpath('./text()')
                       if text:
                           this_content+=text[0]+'\n'
 #构建字符串
 data_str = '<p>标题为：'+this_title+'</p><p>内容为：'+this_content+'</p><br>'
 #写入html文件中
 writer.write(data_str.encode('utf-8'))
            except urllib.error.URLError as e:
                if hasattr(e, 'code'):
                    print(e.code)
                if hasattr(e, 'reason'):
                    print(e.reason)
                time.sleep(2)
            except Exception as e:
                print('exception:', e)
                time.sleep(2)
    #写入结尾
 with   open(r'./webpage/ctoutiao_article.html','ab') as writer:
        html2 = '''</body>
</html>'''
 writer.write(html2.encode('utf-8'))

if __name__ == '__main__':
    urllist = getlisturl()
    content = getcontent(urllist)
    print('爬取完毕！')