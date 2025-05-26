import json
import requests
from bs4 import BeautifulSoup
keyword = 'python'
url = 'https://www.huibo.com/cq/jobs/all/?key='+keyword
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 SE 2.x MetaSr 1.0'}
response = requests.get(url,headers=headers)
with open('.\webpage\kanzhun.html','wb')as writer:
    writer.write(response.content)
if response:
    data = response.content
    soup = BeautifulSoup(data.decode('utf-8'),'html.parser')
    print(soup)
    div_list = soup.find_all('div',class_="postIntro")
    print(div_list)
    content = []
    for div in div_list:
        try:
            #查找工作名称
            job_name = div.find('div',class_="name").find('a').get('title')
            #获取超级链接
            link = div.find('a',class_='des_title job_item_exposure_statistics').get('href')
            #获取公司名称
            company = div.find('div',class_='company_name').string
            #获取薪水
            salary = div.find('div',class_='money').find('span').string


        except Exception as e:
            continue
