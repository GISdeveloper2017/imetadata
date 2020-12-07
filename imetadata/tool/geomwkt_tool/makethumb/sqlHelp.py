# coding:utf-8
import sys
import psycopg2


class SQLHelp:
    def __init__(self, host, port, metadatabase, metauser, metapsd):
        self.conn = psycopg2.connect(host=host, port=port, database=metadatabase, user=metauser, password=metapsd)
        self.closed = False

    def executeNONQuery(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)

    def commit(self):
        self.conn.commit()

    def getRows(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return rows

    def closeconn(self, success=True):
        if success:
            self.conn.commit()
        self.conn.close()
        self.closed = True