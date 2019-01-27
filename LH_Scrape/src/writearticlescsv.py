#!/usr/bin/python
# coding: utf-8

import csv
import dbutils

def write_article(cursor, article):

    with open(file='articles.csv', mode='a', encoding='UTF-8') as csvfile:
        fieldnames = ['ordernumber','mainnumber','name','additionalText','supplier','tax',
                        'price_SC','pseudoprice_SC','baseprice_SC','from_SC','to_SC',
                        'price_EK','pseudoprice_EK','baseprice_EK','from_EK','to_EK',
                        'price_H','pseudoprice_H','baseprice_H','from_H','to_H','active',
                        'instock','stockmin','description','description_long','shippingtime',
                        'added','changed','releasedate','shippingfree','topseller','keywords',
                        'minpurchase','purchasesteps','maxpurchase','purchaseunit',
                        'referenceunit','packunit','unitID','pricegroupID','pricegroupActive',
                        'laststock','suppliernumber','weight','width','height','length','ean',
                        'similar','configuratorsetID','configuratortype','configuratorOptions',
                        'categories','propertyGroupName','propertyValueName','accessory',
                        'imageUrl','main','attr1','attr2','attr3','purchasePrice','metatitle']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"')
        fieldsforentry = ['ordernumber','mainnumber','name','additionalText','supplier',
                           'tax','price_EK','pseudoprice_EK','to_EK','active','instock',
                           'stockmin','description_long','topseller','minpurchase',
                           'purchaseunit','referenceunit','categories','propertyGroupName',
                           'propertyValueName','imageUrl']

#       the article looks like this, with values as further dict
        property_and_values = ''
        for k,v in article['values'].items():
            if property_and_values:
                property_and_values += '|'
            property_and_values += k + ':'+ v
        price = dbutils.get_price(cursor,article['ordernumber'])
        rowEntry = {'name':article['name'],'ordernumber':article['ordernumber'],'mainnumber':article['mainnumber'],
                    'categories':article['categoryId'],'propertyValueName':property_and_values,
                    'description_long':article['description_long'],'imageUrl':article['imageUrl'],
                    # default values
                    'supplier': 'supplier', 'tax': '19', 'price_EK': price, 'pseudoprice_EK': '0', 'from_EK': '1',
                    'to_EK': 'beliebig', 'active': '1', 'instock': '50', 'stockmin': '5'}
        filewriter.writerow(rowEntry)

def create_articles_file():
    with open(file='articles.csv', mode='w', encoding='UTF-8') as csvfile:
        fieldnames = ['ordernumber', 'mainnumber', 'name', 'additionalText', 'supplier', 'tax',
                      'price_SC', 'pseudoprice_SC', 'baseprice_SC', 'from_SC', 'to_SC',
                      'price_EK', 'pseudoprice_EK', 'baseprice_EK', 'from_EK', 'to_EK',
                      'price_H', 'pseudoprice_H', 'baseprice_H', 'from_H', 'to_H', 'active',
                      'instock', 'stockmin', 'description', 'description_long', 'shippingtime',
                      'added', 'changed', 'releasedate', 'shippingfree', 'topseller', 'keywords',
                      'minpurchase', 'purchasesteps', 'maxpurchase', 'purchaseunit',
                      'referenceunit', 'packunit', 'unitID', 'pricegroupID', 'pricegroupActive',
                      'laststock', 'suppliernumber', 'weight', 'width', 'height', 'length', 'ean',
                      'similar', 'configuratorsetID', 'configuratortype', 'configuratorOptions',
                      'categories', 'propertyGroupName', 'propertyValueName', 'accessory',
                      'imageUrl', 'main', 'attr1', 'attr2', 'attr3', 'purchasePrice', 'metatitle']
        filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"')
        filewriter.writeheader()
