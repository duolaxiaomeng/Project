import requests
from lxml import etree


def get_game_names():
    try:
        url = "https://www.4399.com/"
        response = requests.get(url)
        response.encoding = 'gbk'
        root = etree.HTML(response.text)

        game_names = root.xpath('//ul[@class="tm_list "]/li/a/text()')

        if game_names:
            with open('game.txt', 'w', encoding='utf-8') as f:
                for name in game_names:
                    f.write(name.strip() + '\n')
                    print(name.strip())
            print("OK")
        else:
            print("未获取到游戏名称")
    except requests.RequestException as e:
        print(f"请求网页时发生错误: {e}")
    except etree.ParserError as e:
        print(f"解析HTML时发生错误: {e}")


if __name__ == "__main__":
    get_game_names()