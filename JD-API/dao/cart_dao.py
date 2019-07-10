from dao import BaseDao


class CartDao(BaseDao):

    # 购物车的数据查询
    def query(self,sql):
        return super(CartDao,self).query(sql)

    def update(self,table_name,goodnum,newnum,goodid,newid):
        sql = "update %s set %s=%d where  %s=%d"%(table_name,goodnum,int(newnum),goodid,int(newid))
        with self.db as c:
            c.execute(sql)
        return int(newnum)
    def delete(self, table_name,id,by_id):
        sql = "delete from %s where %s = %s" % (table_name, id, by_id)
        with self.db as c:
            c.execute(sql)
        return True
