#!/usr/bin/python
# coding: utf-8

import csv
import dbutils

def parseAllPrices():
    '''
    Sets up the database table for the prices and then reads cvs
    files containing page number, ordernumber, description, quantity, price
    Only the ordernumber and price are now stored in the database
    :return:
    '''
    conn, cursor = dbutils.create_connection()
    dbutils.create_price_table(cursor)

    with open(file='SicherheitUndFlaggenPreise.csv',encoding='iso-8859-1') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
            print(row)
            print(row[0])
            print(row[0],row[1],row[2],row[3],row[4],)
            dbutils.insert_price(cursor,{'ordernumber': row[1], 'price': row[4]})
    dbutils.commit(conn)

parseAllPrices()
conn,cursor = dbutils.create_connection()
dbutils.get_price(cursor,'28311030')