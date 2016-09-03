import sqlite3, sys

log = __import__("logging").getLogger(__name__)


class DB(object):
    name = None

    @property
    def cur(self):
        return self.connect().cursor()

    def __init__(self, name):
        self.name = name
        con = None
        try:
            con = sqlite3.connect(name)
            cur = con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
            log.debug("SQLite version: %s" % data)
        except sqlite3.Error, e:
            log.error("Error %s:" % e.args[0])
            sys.exit(1)
        finally:
            if con:
                con.close()

    def connect(self):
        if self.name:
            return sqlite3.connect(self.name)
        raise Exception('No database name declared')

    def execute(self, sql):
        log.debug("Running SQL statement %s" % sql)
        self.cur.execute(sql)
        log.debug("Row count %s" % self.cur.rowcount)

    def executemany(self, sql):
        log.debug("Running SQL statements %s" % sql)
        self.cur.executemany(sql)
        log.debug("Row count %s" % self.cur.rowcount)

    def executescript(self, sql):
        log.debug("Running SQL script %s" % sql)
        self.cur.executescript(sql)
        log.debug("Row count %s" % self.cur.rowcount)


if __name__ == "__main__":
    from log import setup_logging
    setup_logging()
    db = DB('test.sqlite')
    list_tables_sql = "SELECT * FROM sqlite_master WHERE type='table'"
    db.cur.execute(list_tables_sql)
    rows = db.cur.fetchall()
    print db.cur.rowcount
    for row in rows:
        print row
    create_table = 'CREATE TABLE dup(id INT PRIMARY KEY)'
