# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 19:18:46 2022

@author: Angelo
"""

import sqlite3

class DataBase:

    __db_name = ""
    __conn = None

    def __init__(self,db_name:str):
        DataBase.__db_name = db_name

    def connect(self):
        try:
            DataBase.__conn = sqlite3.connect(DataBase.__db_name)
            return True
        except:
            return False

    def disconnect(self):
        DataBase.__conn.close()

    #Usar para INSERT, UPDATE, DELETE

    def execSql(self, _sql, _tupla=()):

        try:
            _cursor = DataBase.__conn.cursor()
            if _tupla == ():
                _cursor.execute( _sql )
            else:
                _cursor.execute( _sql, _tupla )
            DataBase.__conn.commit()
        finally:
            _cursor.close()

    #Todas las ocurrencias
    def selectAllSql(self, _sql ):
        #print ( f"SQL: {_sql}" )
        _rows = None
        try:
            _cursor = DataBase.__conn.cursor()
            _cursor.execute( _sql )
            _rows = _cursor.fetchall()
        finally:
            _cursor.close()
            return _rows

    #Primera ocurrencia
    def selectOneSql(self, _sql):
        _row = None
        try:
            _cursor = DataBase.__conn.cursor()
            _cursor.execute( _sql )
            _row = _cursor.fetchone()
        finally:
            _cursor.close()
            return _row

    #SELECT MAX (id) FROM table        colation

    '''
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            results = cursor.execute(query, parameters)
            conn.commit()
            conn.close()
        return results


    def get_orders(self):
        query = 'SELECT * FROM orders ORDER BY id DESC'
        db_rows = self.run_query(query)
        print(db_rows)
    '''
    '''
    def insert(self, _sql:str):
        try:
            _cursor = DataBase.__conn.cursor()
            _cursor.execute(_sql)
        finally:
            DataBase.__conn.commit()
            _cursor.close()
    '''

'''
conexion = DataBase("./database.db")
print("\nConexion establecida:", conexion.connect(), "\n")

table = "orders"
s=1
sql = f"SELECT * FROM {table} WHERE service = {s}"

rows=conexion.selectAllSql(sql)
print(rows)

table = "orders"
s=2
sql = f"SELECT elements FROM {table} WHERE service = {s}"

rows=conexion.selectAllSql(sql)
print(rows)
'''

