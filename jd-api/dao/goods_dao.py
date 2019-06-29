
from dao import BaseDao


class GoodsDao(BaseDao):
    # 商品首页的数据查询

    def query(self,sql):
        return super(GoodsDao,self).query(sql)







