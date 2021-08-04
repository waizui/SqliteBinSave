import os
import sqlite3


class SBSSqlite(object):
    def __init__(self, db_name=None, pwd=None):
        self._db_name = db_name
        self._db_pwd = pwd

    def get_sqlite_connection(self):
        path = self._get_sqlte_path()
        create = False
        if not os.path.exists(path):
            create = True

        con = sqlite3.connect(path, )

        if create == True:
            self._create_sqlite_table(connection=con)

        return con

    def _sqlite_insert(self, con: sqlite3.Connection, data: dict, table: str):
        if not data:
            return
        cur = con.cursor()
        keys = ",".join(data.keys())
        values = ",".join(['?'] * len(data))
        sql = """INSERT OR REPLACE INTO {table}({keys}) VALUES({values})
                """.format(table=table, keys=keys, values=values)
        cur.execute(sql, list(data.values()))
        con.commit()

    def sqlite_insert_bin(self, con: sqlite3.Connection, data: dict):
        self._sqlite_insert(con, data, "bins")

    def _create_sqlite_table(self, connection: sqlite3.Connection):
        sql = self._get_sqlite_create_sql()
        cur = connection.cursor()
        cur.executescript(sql)
        connection.commit()

    def _get_sqlte_path(self):
        if not self._db_name:
            return "./SBSData.db"
        else:
            return "./{name}.db".format(name=self._db_name)

    def _get_sqlite_create_sql(self):
        create_sql = """
                CREATE TABLE IF NOT EXISTS bins (
                    id integer PRIMARY KEY AUTOINCREMENT
                    ,name varchar(32) NOT NULL /*file name*/
                    ,ext varchar(10) NOT NULL /*file extension*/
                    ,data blob NOT NULL
                    ,create_date varchar(16)
                );
                 """
        return create_sql
