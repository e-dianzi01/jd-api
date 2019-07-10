import pymysql
from pymysql.cursors import DictCursor

from logger import api_logger

DB_CONFIG = {
    'host': '121.199.63.71',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'jd_api_db',
    'charset': 'utf8',
    'init_command': "SET foreign_key_checks = 0;"
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

    def delete_tab(self, talbe_name, goods_id,user_id):
        sql = "delete from %s where c_goods_id=%s and c_user_id=%s"%(talbe_name,goods_id,user_id)
        success = False
        with self.db as c:
            c.execute(sql)
            api_logger.info('delete %s ok!' % sql)
            success = True
        return success

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


    def del_vou(self,vou_id,user_id):
        sql = "delete from jd_coupon where cop_id=%s and user_id=%s"%(vou_id,user_id)
        with self.db as c:
            resp =c.execute(sql)
            if resp == 0:
                return True



    def update(self, table_name, key, value, where=None, args=None):
        sql = "update {} set {}='{}' where {}='{}' ".format(
            table_name, key, value, where, args
        )
        succuss = False
        with self.db as c:
            c.execute(sql)
            api_logger.info('%s ok!' % sql)
            succuss = True
        return succuss

    def delete(self, table_name, where=None, args=None):
        sql = "delete from {} where {}='{}'".format(table_name, where, args)
        success = False
        with self.db as c:
            c.execute(sql)
            api_logger.info('%s ok!' % sql)
            success = True
        return success

    def list(self, table_name, *fields, where=None, args=None, page=1, page_size=20):
        # if not where:  # 无条件查询
        #     sql = "select {} from {} limit {},{}".\
        #         format(','.join(*fields), table_name, (page - 1) * page_size, page_size)
        # else:  # 条件查询
        sql = "select {} from {} where {}={} limit {},{}".format \
            (','.join(*fields), table_name, where, args, (page - 1) * page_size, page_size)
        with self.db as c:
            c.execute(sql)
            result = c.fetchall()
            api_logger.info('%s ok!' % sql)
            if result:
                result = list(result)
            return result

    def count(self, first_table_name, *fields, arg, alias, second_table_name=None, b_con=None, a_con=None,
              b_arg=None,
              a_arg=None, args):
        if not second_table_name:
            sql = "select {}, count({}) as {} from {} group by {}".format \
                (','.join(*fields), arg, alias, first_table_name, args)

        else:
            sql = "select {}, count({}) as {} from {} join {} on {}={} and {}={} group by {}".format \
                (','.join(*fields), arg, alias, first_table_name, second_table_name, b_con, a_con, b_arg, a_arg, args)

        with self.db as c:
            c.execute(sql)
            data = c.fetchall()
            api_logger.info('%s ok!' % sql)
            if data:
                data = list(data)
        return data
