#!/usr/bin/python
# coding: utf-8

import csv
import writearticlescsv
import scrapdescription

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

import requests
from lxml import etree
from requests import Response

def parse_articles(cursor, fullUrl, subCategoryId):
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(fullUrl)  # type: Response
    tree = etree.HTML(item.content, myparser)
    columns = tree.xpath('//table[@class="articles"]/tr[@class="columns"]/th/text()')  # type: object

    # print descriptions
    theOutput = open('articles.out', 'a')
    theheading = unquote(fullUrl.split('/')[-2])
    theOutput.write('\n' + fullUrl + '\n' + theheading + '\n')
    # The first column is the category id
    theOutput.write('categoryId;')

    # entry = {'categoryId': str(subCategoryId), 'parentID': mainCategory['categoryId'], 'name': textForCSV,
    #          'active': str(1)}
    #
    # entry = {'categories':str(subCategoryId)}
    # entry = {'ordernumber':str(),'mainnumber','name','description_long','categories','propertyValueName','imageUrl']
    for description in columns:
        #    sDesc = description.decode('UTF-8')
        #    theOutput.write(sDesc)
        theOutput.write(description.strip()+';')

    theOutput.write('\n')
    numColumns = len(columns)
    # root.xpath(
    #     "//*[re:test(local-name(), '^TEXT.*')]",
    #     namespaces={'re': "http://exslt.org/regular-expressions"})

    mainpagename = tree.xpath('//div[@class="mainpagename"]/h1/text()')[0]

    articleNrs = tree.xpath('//table[@class="articles"]/tr[starts-with(@class,"stdrow")]/td/span/text()')

    # articleNr = tree.xpath('//table[@class="articles"]/tr[re:test(local-name(),".*stdrow1.*"])]/td/span/text()',
    #                        namespaces={'re': "http://exslt.org/regular-expressions"})

    # first all the rows
    rows = tree.xpath('//table[@class="articles"]/tr[starts-with(@class,"stdrow")]/td/text()')

    with open(file='article-categories.csv', mode='a', encoding='UTF-8') as csvfile:
        fieldnames = ['ordernumber','mainnumber','categoryId']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';',quotechar='"')


        articlePos = 0
        presentColumn = 0
        description_long = scrapdescription.parse_description(fullUrl,subCategoryId)
        # the image is only for the first item on the page
        imageUrl = 'https://www.freyhuus.com/images/marintecShopware/' + articleNrs[0][:2] + '/' + articleNrs[0] + '.jpg'

        values = {}
        if len(rows) == 1:
            theOutput.write("\nFound a single item\n")
        else:
            theOutput.write("\nFound multiple items\n")
        for row in rows:
            if presentColumn == 0:
                theOutput.write('trying to get pos ' + str(articlePos) + ' from ' + str(articleNrs) + 'and present column '+ str(presentColumn) +'\n')
                articleNumber = articleNrs[articlePos]
                theOutput.write('getting ' + str(articleNumber) + ' at pos '+str(articlePos) + '\n')
                theOutput.write(row)
                entry = {'ordernumber': articleNumber,'mainnumber': articleNumber,
                         'categoryId': str(subCategoryId/100)} # category from the parent
                filewriter.writerow(entry)
                theOutput.write(str(subCategoryId) + ';' + articleNumber + ';' )
                articlePos += 1
            entry['name'] = mainpagename
            entry['description_long'] = description_long
            entry['imageUrl'] = imageUrl
            values[columns[presentColumn+1]] = row.strip()
            theOutput.write(row.strip() + ';')
            presentColumn = presentColumn + 1
            if presentColumn == numColumns - 1:
                entry['values'] = values
                theOutput.write('\n')
                writearticlescsv.write_article(cursor,entry)
                presentColumn = 0


