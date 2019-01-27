#!/usr/bin/python
# coding: utf-8

import csv

import requests
from lxml import etree
from requests import Response

import dbutils
from scraparticles import parse_articles
from scrapcategories import parse_categories
from writearticlescsv import create_articles_file
from parseprices import parseAllPrices

# Finds the subcategories which are found on the relative Url, relative to https://domain
def parse_subcategories(cursor,mainCategory, domain):
    articleCount = 0
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(
        'https://' + domain + mainCategory['link'])  # type: Response
    tree = etree.HTML(item.content, myparser)
    subCategories = tree.xpath('//a[@class="anav"]') # /li/p/a')  # type: object

    theOutput = open('csv/subCategories.out', 'a')
    allSubCategories = []
    allCategoriesForCSV = []
    subCategoryId = int(mainCategory['categoryId']) * 100
    for subCategory in subCategories:
        link = subCategory.attrib['href']
        textForCSV = subCategory.text.strip()
        text = mainCategory['text'] + "/" + textForCSV
        allSubCategories.append({'link':link, 'text':text, 'categoryId':str(subCategoryId)})
        theOutput.write("<" + text  +"> with the href: " + link + "\n")
        entry = {'categoryId': str(subCategoryId), 'parentID': mainCategory['categoryId'], 'name': textForCSV, 'active': str(1)}
        allCategoriesForCSV.append(
            entry)
        dbutils.insert_category(cursor,entry)
        subCategoryId = subCategoryId + 1


    if allSubCategories:
        with open(file='categories.csv', mode='a', encoding='UTF-8') as csvfile:
            fieldnames = ['categoryId', 'parentID', 'name', 'position', 'metatitle', 'metakeywords', 'metadescription',
                          'cmsheadline', 'cmstext', 'template', 'active', 'blog', 'external', 'hidefilter',
                          'attribute_attribute1', 'attribute_attribute2', 'attribute_attribute3', 'attribute_attribute4',
                          'attribute_attribute5', 'attribute_attribute6', 'CustomerGroup']
            filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            filewriter.writerows(allCategoriesForCSV)
        theOutput.write("found subcategories, recursing")
        for subCategory in allSubCategories:
            parse_subcategories(cursor,subCategory,domain)
    else:
        # don't parse articles while testing categories
        articleCount = articleCount + 1
        if(articleCount < 11):
            theOutput.write("<got to the end> with " + str(subCategoryId) + "\n")
            # we dont need to make a category for the leaf
            # theOutput.write("<" + mainCategory['text']  +"> with the href: " + mainCategory['link'] + "\n")
            # completeDescription = parse_description("https://" + domain + mainCategory['link'],mainCategory['categoryId'])
            # with open(file='categories.csv', mode='a', encoding='UTF-8') as csvfile:
            #     fieldnames = ['categoryId', 'parentID', 'name', 'position', 'metatitle', 'metakeywords', 'metadescription',
            #                   'cmsheadline', 'cmstext', 'template', 'active', 'blog', 'external', 'hidefilter',
            #                   'attribute_attribute1', 'attribute_attribute2', 'attribute_attribute3', 'attribute_attribute4',
            #                   'attribute_attribute5', 'attribute_attribute6', 'CustomerGroup']
            #     filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=';',quotechar='"')
            #     singleCategory = {'categoryId': mainCategory['categoryId'], 'parentID':"not known", 'name': mainCategory['text'],
            #                       'active': str(1),'cmstext':completeDescription}
            #     filewriter.writerow(singleCategory)

            parse_articles(cursor,"https://" + domain + mainCategory['link'],subCategoryId)
    theOutput.close()
    return []

theOutput = open('articles.out', 'w')
theOutput.write('Another try\n')
theOutput.close()
theOutput = open('description.out', 'w')
theOutput.write('Another try\n')
theOutput.close()
theOutput = open('subCategories.out', 'w')
theOutput.write('Another try\n')
theOutput.close()
parseAllPrices()
myurl = input("which url?")

with open(file='article-categories.csv', mode='a', encoding='UTF-8') as csvfile:
    fieldnames = ['ordernumber', 'mainnumber', 'categoryId']
    filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"')
    filewriter.writeheader()

create_articles_file()

conn, cursor = dbutils.create_connection()
allMainCategories = parse_categories(conn,cursor,myurl)
#for mainCategory in allMainCategories :
#    allSubCategories = parse_subcategories(mainCategory,myurl)
parse_subcategories(cursor,allMainCategories[0],myurl)
dbutils.print_categories(cursor)
dbutils.close_connection(conn)
#csvfile.close()