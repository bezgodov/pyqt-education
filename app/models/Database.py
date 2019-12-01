import os
import sqlite3
from sqlite3 import Error

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

    def get_table_headers(self, desc):
        return [d[0] for d in desc]

    def get_all_tables(self):
        query = 'SELECT name FROM sqlite_master WHERE type="table"'
        cur = self.get_cursor()
        cur.execute(query)

        return list(map(lambda t: t[0], cur.fetchall()))

    def update_table_column(self, table, pk_id, col, value):
        _table = table['title']
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
