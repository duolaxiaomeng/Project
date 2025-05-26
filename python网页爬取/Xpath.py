from lxml import etree

with open('lianxi.txt','rb') as reader:
    text = reader.read()

    html=etree.HTML(text,parser=etree.HTMLParser(encoding='utf-8'))
    print(html.xpath('//a[position()<3]/text()'))