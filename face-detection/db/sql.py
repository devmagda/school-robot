import psycopg2 as psycopg2


class Connection:
    def __init__(self, host='localhost', database='dev', username='postgres', password='postgres'):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password)
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def exec(self, statement, values=None, fetch=None):
        self.cur.execute(statement, values)
        if fetch == 'all':
            return self.fetchAll()
        if fetch == 'one':
            return self.fetchOne()

    def commit(self):
        self.conn.commit()

    def fetchOne(self):
        return self.cur.fetchone()

    def fetchAll(self):
        return self.cur.fetchall()


class SqlUtil:
    conn = Connection()

    @staticmethod
    def execute(statement, values=None, fetch=None):
        result = SqlUtil.conn.exec(statement, values=values, fetch=fetch)
        SqlUtil.conn.commit()
        return result
