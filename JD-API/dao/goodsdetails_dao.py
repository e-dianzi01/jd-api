from dao import BaseDao
from logger import api_logger


class GoodsDetailsDao(BaseDao):
    # 商品首页的数据查询

    def query(self, sql):
        return super(GoodsDetailsDao, self).query(sql)

    # def count(self,table_name):

    def add(self, a, b, c, d):
        add_sql = "insert into jd_cart(c_goods_num,c_freight,c_goods_id,c_shopper_id,c_user_id) " \
                  "values('{}',10,'{}','{}','{}')".format(a, b, c, d)
        with self.db as c:
            c.execute(add_sql)
            # api_logger.info('%s ok!' % add_sql)
        return True

    def change(self,num,a,b):
        change_sql = "update jd_cart set c_goods_num='{}' where c_goods_id='{}' and c_user_id='{}'".format(num, a, b)
        with self.db as c:
            c.execute(change_sql)
            # api_logger.info('%s ok!' % add_sql)
        return True