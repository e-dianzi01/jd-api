from dao import BaseDao

class GoodsDao(BaseDao):
    def query(self, sql):
        return super(GoodsDao, self).query(sql)