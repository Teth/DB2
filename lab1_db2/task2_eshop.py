from lxml import etree
import requests
import re
from lxml import html, etree
from lxml.etree import Element, SubElement, ElementTree, parse

baseUrl = 'https://instrument.in.ua'
catalogUrl = 'https://instrument.in.ua/katalog/'
pageContent=requests.get(baseUrl)
tree = html.fromstring(pageContent.content)

productNodes = tree.xpath('//div[@class=\'catalogCard-main\']')

root = Element('root')

for index, pnode in enumerate(productNodes):
    product = SubElement(root, 'product')
    imgSrc = pnode.xpath('.//div[@class=\'catalogCard-image-i\']/img/@src')[0]
    pName = pnode.xpath('.//div[@class=\'catalogCard-title\']/a/@title')[0]
    pPrice = pnode.xpath('.//div[@class=\'catalogCard-price\']/text()')[0]
    name = SubElement(product, 'name')
    name.text = pName
    price = SubElement(product, 'price')
    price.text = pPrice
    img = SubElement(product, 'img')
    img.text = baseUrl + imgSrc
    if index >= 20:
        break

tree = ElementTree(root)
print(tree)
tree.write('task2_products_data.xml', encoding='utf8')
xslt = etree.parse('template.xslt')
xml = parse('task2_products_data.xml')
print(xml)
transform = etree.XSLT(xslt)
result = transform(xml)
f = open("task2_prettyProducts.html", "a")
f.write(str(result))
f.close()