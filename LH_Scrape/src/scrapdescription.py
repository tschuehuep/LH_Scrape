#!/usr/bin/python
# coding: utf-8

import requests
from lxml import etree
from requests import Response

def parse_description(fullUrl, categoryId):
    completeDescription = ""
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(
        fullUrl)  # type: Response
    tree = etree.HTML(item.content, myparser)
    # html.fromstring(kocher.content)
    descriptions = tree.xpath('//div[@id="descriptioncontent"]/text()')  # type: object

    # print descriptions
    theOutput = open('description.out', 'a')
    if descriptions:
        theOutput.write(fullUrl + "\nDescription for "+str(categoryId)+"\n")
        for description in descriptions:
            #    sDesc = description.decode('UTF-8')
            #    theOutput.write(sDesc)
            completeDescription = completeDescription + description.strip() + "<br>"
        theOutput.write(completeDescription)
    return completeDescription
