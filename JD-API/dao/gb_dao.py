from dao import BaseDao


class gbDao(BaseDao):

    def check(self,sql,num):
        with self.db as c:
            c.execute(sql)
            data = c.fetchmany(num)
            if data:
                data = list(data)
        return data

# if __name__ == '__main__':
#     g=gbDao()
#     gBC_sql = "select img_urls,page_text from nav limit 5,10"
#     # g.query(gBe_sql,5)
#     print( g.query(gBC_sql,5))