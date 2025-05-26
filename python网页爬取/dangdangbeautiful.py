import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from tqdm import tqdm


def get_total_pages():

    url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'gb2312'

        soup = BeautifulSoup(response.text, 'html.parser')
        page_div = soup.find('div', class_='paging')
        if page_div:
            last_page = page_div.find_all('li')[-2].text
            return int(last_page)
        return 20
    except:
        return 20


def scrape_dangdang_bestsellers(page_count=None):
    all_books = []
    base_url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    total_pages = get_total_pages() if page_count is None else page_count
    print(f"开始爬取当当网畅销书排行榜，共{total_pages}页...")

    for page in tqdm(range(1, total_pages + 1)):
        url = base_url + str(page)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = 'gb2312'

            soup = BeautifulSoup(response.text, 'html.parser')
            book_list = soup.find('ul', class_='bang_list')

            if not book_list:
                print(f"第{page}页未找到书籍列表，跳过...")
                continue

            for li in book_list.find_all('li'):
                try:
                    rank = li.find('div', class_='list_num').text.strip()
                    name = li.find('div', class_='name').text.strip()

                    pub_info = li.find('div', class_='publisher_info')
                    authors = [a.text.strip() for a in pub_info.find_all('a')] if pub_info else []
                    author = authors[0] if authors else "未知"
                    publisher = authors[-1] if len(authors) > 1 else "未知"

                    price_div = li.find('div', class_='price')
                    price = price_div.find('span', class_='price_n').text.strip() if price_div else "未知"

                    star_div = li.find('div', class_='star')
                    comments = star_div.find('a').text.strip() if star_div and star_div.find('a') else "0"

                    all_books.append({
                        '排名': rank,
                        '书名': name,
                        '作者': author,
                        '出版社': publisher,
                        '价格': price,
                        '评论数': comments,
                        '页码': page
                    })
                except Exception as e:
                    print(f"第{page}页书籍信息提取出错: {e}")
                    continue

            time.sleep(1 + 2 * random.random())

        except requests.RequestException as e:
            print(f"第{page}页请求失败: {e}")
            continue
        except Exception as e:
            print(f"第{page}页处理出错: {e}")
            continue

    df = pd.DataFrame(all_books)
    df['排名'] = df['排名'].str.replace('.', '').astype(int)
    df['评论数'] = df['评论数'].str.extract(r'(\d+)').fillna('0').astype(int)

    return df


def save_to_txt(dataframe, folder='webpage', filename='dangbeautiful.txt'):

    if not os.path.exists(folder):
        os.makedirs(folder)


    filepath = os.path.join(folder, filename)


    with open(filepath, 'w', encoding='utf-8') as f:
        # 写入表头
        f.write("当当网畅销书排行榜数据\n\n")
        f.write(f"共爬取 {len(dataframe)} 条记录\n")
        f.write(f"页码范围: 第1页到第{dataframe['页码'].max()}页\n\n")


        columns = ['排名', '书名', '作者', '出版社', '价格', '评论数', '页码']
        f.write("\t".join(columns) + "\n")


        for _, row in dataframe.iterrows():
            line = "\t".join([str(row[col]) for col in columns]) + "\n"
            f.write(line)


        f.write("\n各页数据统计:\n")
        page_stats = dataframe['页码'].value_counts().sort_index()
        for page, count in page_stats.items():
            f.write(f"第{page}页: {count}条记录\n")


if __name__ == "__main__":

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)


    print("正在获取总页数...")
    books_df = scrape_dangdang_bestsellers()

    if books_df is not None and not books_df.empty:
        print("\n爬取结果预览:")
        print(books_df.head(10))


        save_to_txt(books_df)
        print("\n数据已保存到 webpage/dangbeautiful.txt")


        print(f"\n共爬取 {len(books_df)} 本书籍信息")
        print(f"页码范围: 第1页到第{books_df['页码'].max()}页")
        print("\n各页书籍数量统计:")
        print(books_df['页码'].value_counts().sort_index())
    else:
        print("未能爬取到任何数据")