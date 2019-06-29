import pymysql
from pymysql.cursors import DictCursor

from logger import api_logger

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'jd_api_db',
    'charset': 'utf8'
}


class DB:
    def __init__(self):
        self.conn = pymysql.Connect(**DB_CONFIG)
        # 如果上传的code中包含更新sql语句，如何自动创建(在服务器端)

    def __enter__(self):
        if self.conn is None:
            # 考虑数据库连接是断开的情况
            self.conn = pymysql.Connect(**DB_CONFIG)

        return self.conn.cursor(cursor=DictCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            api_logger.error(exc_val)
            self.conn.rollback()

        return True  # 异常不会继续向外抛出


class BaseDao():
    def __init__(self):
        self.db = DB()

    def save(self, table_name, **values):
        # insert or update
        # values['id'] 如果ID值是存在的，则是更新, 反之是插入
        sql = 'insert into %s(%s) values(%s)' % \
              (table_name,
               ','.join(values.keys()),
               ','.join([ '%%(%s)s' % key for key in values.keys() ])
               )

        success = False
        with self.db as c:
            c.execute(sql, args=values)
            api_logger.info('insert %s ok!' % sql)
            success = True

        return success

    def delete(self, talbe_name, by_id):
        pass

    def list(self, table_name,
             *fields, where=None, args=None,
             page=1, page_size=20):
        pass

    def count(self, table_name):
        pass

    def query(self, sql, *args):
        with self.db as c:
            c.execute(sql, args=args)
            data = c.fetchall()
            if data:
                data = list(data)
            return data



