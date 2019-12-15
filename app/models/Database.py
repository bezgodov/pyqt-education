import os
import sqlite3
from sqlite3 import Error
import re

from app.models.Store import Store

class Database():
    DB_PATH = '../../assets/databases/numeral-gestures/'
    DB_FILENAME = 'database.sqlite'
    ROWS_PER_LOAD = 50

    def __init__(self):
        self.connection = self.init_connection()

    def get_cursor(self):
        return self.connection.cursor()

    def init_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.get_database_path())
        except Error as _e:
            print(_e)
        return conn

    def get_database_path(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        path = cur_dir + '/' + Database.DB_PATH + Database.DB_FILENAME
        return path

    def get_table_data_by_foreign_key(self, table):
        query = "SELECT * FROM %s LIMIT ?" %(table)
        cur = self.get_cursor()
        cur.execute(query, (Database.ROWS_PER_LOAD, ))
        rows = cur.fetchall()
        headers = self.get_table_headers(cur.description)

        return {
            'headers': headers,
            'rows': rows,
        }

    def get_table_data(self, name, start):
        query = "SELECT * FROM %s LIMIT ? OFFSET ?" %(name)
        cur = self.get_cursor()
        cur.execute(query, (Database.ROWS_PER_LOAD, start,))
        rows = cur.fetchall()
        headers = self.get_table_headers(cur.description)

        return {
            'headers': headers,
            'rows': rows,
        }

    def get_foreign_keys(self, table):
        query = "SELECT sql FROM sqlite_master WHERE sql LIKE('%REFERENCES%') and name = ?"
        cur = self.get_cursor()
        cur.execute(query, (table, ))
        queries = cur.fetchall()

        regex = r"FOREIGN KEY[\s]*\(`[\s]*([\w\W]+?)[\s]*`[\s]*\)[\s]*REFERENCES[\s]*`[\s]*([\w\W]+?)[\s]*`[\s]*\([\s]*`[\s]*([\w\W]+?)`[\s]*\)"
        res = {}

        for q in queries:
            matches = re.finditer(regex, q[0])
            for i, match in enumerate(matches):
                _groups = match.groups()
                res[_groups[0]] = {
                    'table': _groups[1],
                    'column': _groups[2],
                }

        return res

    def get_table_columns_names(self, name):
        query = "SELECT * FROM %s" %(name)
        cur = self.get_cursor()
        cur.execute(query)
        headers = self.get_table_headers(cur.description)

        return headers

    def get_table_headers(self, desc):
        return [d[0] for d in desc]

    def get_all_tables(self):
        query = 'SELECT name FROM sqlite_master WHERE type="table"'
        cur = self.get_cursor()
        cur.execute(query)

        return list(map(lambda t: t[0], cur.fetchall()))

    def update_table_column(self, table, pk_id, col, value, pk = None):
        _table = table['title']
        
        if pk == None:
            pk = self.get_table_primary_key(_table)
        query = 'UPDATE %s SET %s = ? WHERE %s = ?' %(_table, col, pk)
        cur = self.get_cursor()
        cur.execute(query, (value, pk_id,))

        self.connection.commit()

    def get_table_primary_key(self, name):
        query = "SELECT * FROM %s" %(name)
        cur = self.get_cursor()
        cur.execute(query)
        table_description = cur.description

        return table_description[0][0]

    def remove_table_row(self, table, pk_id):
        _table = table['title']
        pk = self.get_table_primary_key(_table)
        query = 'DELETE FROM %s WHERE %s = ?' %(_table, pk)
        cur = self.get_cursor()
        cur.execute(query, (pk_id,))

        self.connection.commit()

        message = 'Removed row from table "%s" where "%s" is "%s"' %(_table, pk, pk_id)
        Store.show_message_in_status_bar(message)

    def insert_row_to_table(self, values):
        _table = Store.get_current_tab()['title']
        placeholder = ','.join(['?' for v in values])
        query = 'INSERT INTO %s VALUES (%s)' %(_table, placeholder)
        cur = self.get_cursor()
        cur.execute(query, values)

        self.connection.commit()

        self.insert_row(values)

    def insert_row(self, row):
        cur_tab = Store.get_current_tab()
        _table = cur_tab['table']

        _table.add_row_to_table(row)
