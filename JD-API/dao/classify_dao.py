from dao import BaseDao


class ClassifyDao(BaseDao):
    # 分类页的数据查询

    def query(self,sql):
        return super(ClassifyDao,self).query(sql)

    def check(self,a):
        sql = "select remark from goods_type1 " \
              "where one_type_name = %s" %(a,)
        with self.db as c:
            c.execute(sql)
        data = c.fetchall()
        return data



