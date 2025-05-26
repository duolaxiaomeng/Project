import requests
from bs4 import BeautifulSoup
import os
import time

# 目标网址（这里假设你要抓取的页面就是上述代码对应的页面，如果不是请修改）
url = "https://www.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-1"
# 模拟浏览器请求头
headers = {
    "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
# 存储文件的文件夹名称
folder_name = "webpage"
# 如果文件夹不存在，则创建文件夹
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
file_path = os.path.join(folder_name, "dangdang.txt")

try:
    # 发送GET请求获取网页内容
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果响应状态码不是200，引发HTTPError异常
    response.encoding = response.apparent_encoding  # 设置正确的编码

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有的li标签，每个li标签代表一本图书
    book_items = soup.find_all('li')

    with open(file_path, 'w', encoding='utf-8') as file:
        for item in book_items:
            rank = ""
            title = ""
            author = ""
            publisher = ""
            publish_time = ""
            original_price = ""
            current_price = ""
            discount = ""
            comment_count = ""
            recommend_rate = ""

            # 抓取排名
            rank_div = item.find('div', class_='list_num')
            if rank_div:
                rank = rank_div.text.strip('.')

            # 抓取书名
            name_div = item.find('div', class_='name')
            if name_div:
                title_a = name_div.find('a')
                if title_a:
                    title = title_a.text

            # 抓取作者信息
            author_div = item.find('div', class_='publisher_info')
            if author_div:
                author = author_div.text.strip()

            # 抓取出版社信息
            publisher_divs = item.find_all('div', class_='publisher_info')
            if len(publisher_divs) > 1:
                publisher_a = publisher_divs[1].find('a')
                if publisher_a:
                    publisher = publisher_a.text

            # 抓取出版时间
            if len(publisher_divs) > 1:
                time_span = publisher_divs[1].find('span')
                if time_span:
                    publish_time = time_span.text

            # 抓取原价
            original_price_span = item.find('span', class_='price_r')
            if original_price_span:
                original_price = original_price_span.text

            # 抓取现价
            current_price_span = item.find('span', class_='price_n')
            if current_price_span:
                current_price = current_price_span.text

            # 抓取折扣
            discount_span = item.find('span', class_='price_s')
            if discount_span:
                discount = discount_span.text

            # 抓取评论数量
            star_div = item.find('div', class_='star')
            if star_div:
                comment_a = star_div.find('a', href=lambda href: href and 'comment_point' in href)
                if comment_a:
                    comment_count = comment_a.text.strip('条评论')

            # 抓取推荐率
            if star_div:
                recommend_span = star_div.find('span', class_='tuijian')
                if recommend_span:
                    recommend_rate = recommend_span.text

            info = f"排名: {rank}\n书名: {title}\n作者: {author}\n出版社: {publisher}\n出版时间: {publish_time}\n原价: {original_price}\n现价: {current_price}\n折扣: {discount}\n评论数量: {comment_count}\n推荐率: {recommend_rate}\n{'-' * 50}\n"
            file.write(info)

except requests.RequestException as e:
    print(f"请求发生异常: {e}")
except AttributeError as e:
    print(f"解析数据时发生属性错误: {e}")