#!/usr/bin/python
# coding: utf-8

import requests
import csv
import dbutils

from lxml import etree
from requests import Response

def parse_categories(conn,cursor,domain):
    dbutils.create_categories_table(cursor)

    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(
        'https://' + domain)  # type: Response
    tree = etree.HTML(item.content, myparser)
    # html.fromstring(kocher.content)
    categories = tree.xpath('//ul[@class="menuitems"]/li/p/a') # /li/p/a')  # type: object

    # print descriptions
    theOutput = open('categories.out', 'w')
    allCategories = []
    allCategoriesForCSV = []
    mainCategoryId = 10
    for category in categories:
        #    sDesc = description.decode('UTF-8')
        #    theOutput.write(sDesc)
        link = category.attrib['href']
        text = category.text
        allCategories.append({'link':link, 'text':text, 'categoryId':mainCategoryId, 'parentID':str(3),'name':text})
        allCategoriesForCSV.append(
            {'categoryId': mainCategoryId, 'parentID': str(3), 'name': text, 'active': str(1)})

        theOutput.write("Id <"+ str(mainCategoryId) + "> Remote <"+text + "> with the href: " + link + "\n")

        dbutils.insert_category(conn,{'categoryId': mainCategoryId, 'parentID': 3, 'name': text})
        mainCategoryId = mainCategoryId + 1
    with open(file='categories.csv', mode='w', encoding='UTF-8') as csvfile:
        fieldnames = ['categoryId', 'parentID', 'name', 'position', 'metatitle', 'metakeywords', 'metadescription',
                      'cmsheadline', 'cmstext', 'template', 'active', 'blog', 'external', 'hidefilter',
                      'attribute_attribute1', 'attribute_attribute2', 'attribute_attribute3', 'attribute_attribute4',
                      'attribute_attribute5', 'attribute_attribute6', 'CustomerGroup']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';',quotechar='"')
        filewriter.writeheader()
        filewriter.writerows(allCategoriesForCSV)
    dbutils.commit(conn)
    return allCategories


