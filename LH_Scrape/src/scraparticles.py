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
from lxml import objectify

def startswithArt(element):
    if (str(element).startswith('Art')):
        return True
    return False

def parse_articles(cursor, fullUrl, subCategoryId):
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(fullUrl)  # type: Response
    tree = etree.HTML(item.content, myparser)
    columns = tree.xpath('//table[@class="articles"]/tr[@class="columns"]/th/text()')  # type: object

    # print descriptions
    theOutput = open('output/articles.out', 'a')
    theheading = unquote(fullUrl.split('/')[-2])
    theOutput.write('\n' + fullUrl + '\n' + theheading + '\n')
    # The first column is the category id
    theOutput.write('categoryId;')

    numOfArticleColumns = len(list(filter(startswithArt,columns)))

    numOfNonArticleNumberColumns = len(columns) - numOfArticleColumns
    
    if ( columns.count("Artikelnummer") + columns.count("Art.-Nr.") ) > 1:
        theOutput.write("\nSonderlocke für "+ fullUrl)
        return
    # entry = {'categoryId': str(subCategoryId), 'parentID': mainCategory['categoryId'], 'name': textForCSV,
    #          'active': str(1)}
    #
    # entry = {'categories':str(subCategoryId)}
    # entry = {'ordernumber':str(),'mainnumber','name','description_long','categories','propertyValueName','imageUrl']
    theOutput.write('\nColumns for '+fullUrl+'\n')
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

    # only the none article number elements
    nonArticleNumberElements = tree.xpath('//table[@class="articles"]/tr[starts-with(@class,"stdrow")]/td[position()>'+str(numOfArticleColumns)+']/text()')
    # first all the allElements
    allElements = tree.xpath('//table[@class="articles"]/tr[starts-with(@class,"stdrow")]/td/text()')

    with open(file='csv/article-categories.csv', mode='a', encoding='UTF-8') as csvfile:
        fieldnames = ['ordernumber','mainnumber','categoryId']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';',quotechar='"')


        articlePos = 0
        presentColumn = 0
        description_long = scrapdescription.parse_description(fullUrl,subCategoryId)

        values = {}
        if len(nonArticleNumberElements) > 0:
            # the image is only for the first item on the page
            theOutput.write('\ngetting image for ' + articleNrs[0][:2])
            imageUrl = 'https://www.freyhuus.com/images/marintecShopware/' + articleNrs[0][:2] + '/' + articleNrs[0] + '.jpg'
            if len(nonArticleNumberElements) == numOfNonArticleNumberColumns:
                theOutput.write("\nFound a single item\n")
            else:
                theOutput.write("\nFound multiple items\n")
            presentRow = 0
            # Now going through only the non-article number elements
            for anElement in nonArticleNumberElements:
                theOutput.write('\nprocessing anElement/column <' + str(anElement).strip() + '>/<'+ str(presentColumn) +'>')
                if presentColumn == 0:
#                     print('column 0 trying to get pos ' + str(articlePos) + ' from ' + str(articleNrs) + 'and present column '+ str(presentColumn) +'\n')
#                     theOutput.write('\ntrying to get pos ' + str(articlePos) + ' from ' + str(articleNrs) + 'and present column '+ str(presentColumn) +'\n')
#                     if (articlePos > (len(articleNrs) - 1)):
#                         theOutput.write('too many');
                    articleNumber = articleNrs[articlePos]
#                     articleNumberInt = int(articleNumber)
#                     theOutput.write('\ncolumn 0 getting ' + str(articleNumberInt) + ' at pos '+str(articlePos) + '\n')
#                     theOutput.write('\ncolumn 0 element is <'+anElement + '>')
                    entry = {'ordernumber': articleNumber,'mainnumber': articleNumber,
                             'categoryId': str(subCategoryId/100)} # category from the parent
                    filewriter.writerow(entry)
#                     theOutput.write('\ncolumn 0 subCat '+str(subCategoryId) + '; articleNum ' + articleNumber + ';' )
                    articlePos += 1
                entry['name'] = mainpagename
                entry['description_long'] = description_long
                entry['imageUrl'] = imageUrl
                values[columns[presentColumn+numOfArticleColumns]] = anElement.strip()
                theOutput.write('\nline 97 <'+anElement.strip() + '>; at column '+str(presentColumn) + ' of ' + str(numColumns))
                presentColumn = presentColumn + 1
                if presentColumn == numColumns - 1:
                    entry['values'] = values
                    theOutput.write('\n')
                    writearticlescsv.write_article(cursor,entry)
                    presentColumn = 0
        else:
            theOutput.write("\nFound no item\n")
           
                

