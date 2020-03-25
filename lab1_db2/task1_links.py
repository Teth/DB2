import requests
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import requests
import re
from lxml import html
baseUrl = 'https://www.ukraine-is.com/uk/'
pageContent=requests.get(baseUrl)
tree = html.fromstring(pageContent.content)

root = ET.Element('data')
pageUrl = ET.SubElement(root, 'page')
fragment = ET.SubElement(pageUrl, 'fragment')
fragment.set('type', 'text')
pageUrl.set('url', baseUrl)
next_links = tree.xpath('//a[@href]/@href')
fragment.text = str(next_links)
pagesAnalyzed = 1
for link in next_links:
    if re.match('^(http|https)://', link):
        resp = requests.get(link)
        if resp.status_code == 200:
            subPageUrl = ET.SubElement(root, 'page')
            subFragment = ET.SubElement(subPageUrl, 'fragment')
            subFragment.set('type', 'text')
            subPageUrl.set('url', link)
            sub_next_links = tree.xpath('//a[@href]/@href')
            subFragment.text = str(sub_next_links)
            pagesAnalyzed = pagesAnalyzed + 1
        if pagesAnalyzed >= 20:
            break

tree = ET.ElementTree(root)


tree.write(open('data.xml', 'w'), encoding='unicode')