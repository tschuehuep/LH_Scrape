#!/usr/bin/python
# coding: utf-8

import sqlite3

def create_connection():
    try:
        conn = sqlite3.connect('data/mydb')
        c = conn.cursor()
        return conn, c
    except Exception as e:
        print(e)

    return None

def commit(conn):
    conn.commit()

def close_connection(conn):
    conn.commit()
    conn.close()

def create_categories_table(cursor):
    cursor.execute('''DROP TABLE IF EXISTS categories''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories(categoryId INTEGER PRIMARY KEY, name TEXT,
                           parentID INTEGER)
    ''')

def print_categories(cursor):
    cursor.execute('''SELECT categoryId, parentId, name FROM categories''')
    for row in cursor:
        # row[0] returns the first column in the query (categoryId), row[1] returns parentID column.
        print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))

def insert_category(cursor,category):
    cursor.execute('''INSERT INTO categories(categoryId, parentID, name)
                  VALUES(:categoryId,:parentID, :name)''',
                   # {'categoryId': subCategoryId, 'parentID': mainCategory['categoryId'], 'name': textForCSV})
                   category)

def create_price_table(cursor):
    cursor.execute('''DROP TABLE IF EXISTS price''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price(ordernumber INTEGER PRIMARY KEY, price TEXT)
    ''')

def insert_price(cursor, price):
    cursor.execute('''INSERT INTO price(ordernumber, price)
                  VALUES(:ordernumber,:price)''',
                   price)

def get_price(cursor,ordernumber):
    print('getting price for ' + ordernumber)
    cursor.execute('''SELECT price FROM price WHERE ordernumber = ?''',(ordernumber,))
    for row in cursor:
        # row[0] returns the first column in the query (categoryId), row[1] returns parentID column.
        print('{0}'.format(row[0]))
        return row[0]
