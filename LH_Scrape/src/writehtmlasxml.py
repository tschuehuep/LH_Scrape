# from lxml import html, etree
#
# doc = html.fromstring(open('a.html').read())
# out = open('a.xhtml', 'wb')
# out.write(etree.tostring(doc))


import requests
from lxml import html, etree
from requests import Response

myparser = etree.HTMLParser(encoding="utf-8")
item = requests.get(
#    'https://www.lankhorst-hohorst.de/Katalog/Kochen+und+K%c3%bchlen/Gaskocher/Eno/Bootskocher+Atoll/Produkt.aspx')  # type: Response
    'https://www.lankhorst-hohorst.de/Katalog/Wasser+und+Tanksysteme/Kraftstoffpumpen/Marco/Dieselpumpen/Produkt.aspx')  # type: Response
tree = etree.HTML(item.content, myparser)
out = open('pump.xhtml','wb')
out.write(etree.tostring(tree))
