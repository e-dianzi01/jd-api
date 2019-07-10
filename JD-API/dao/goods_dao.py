from dao import BaseDao


class GoodsDao(BaseDao):

    def search_goods(self, clt_id):
        # 获取商品的详细信息
        sql = "select goods_id, good_img, goods_name, goods_prices, remark from goods_details " \
              "where goods_id=%s"
        user_profile = self.query(sql, clt_id)
        return user_profile

    def search_shop(self, clt_id):
        # 获取商铺的详细信息
        sql = "select m_id, m_img, m_name from jd_shopper " \
              "where m_id=%s"
        user_profile = self.query(sql, clt_id)
        return user_profile

    def check_collect_goods(self, user_id):
        # 根据type_id查询收藏商品信息
        sql = "select user_id_id, clt_id, type_id from u_clt " \
              "where type_id=0 and user_id_id=%s"
        with self.db as c:
            c.execute(sql, user_id)
            data = c.fetchall()
            if data:
                data = list(data)
            return data

    def check_collect_shops(self, user_id):
        # 根据type_id查询收藏商铺信息
        sql = "select user_id_id, clt_id, type_id from u_clt " \
              "where type_id=1 and user_id_id=%s"
        with self.db as c:
            c.execute(sql, user_id)
            data = c.fetchall()
            if data:
                data = list(data)
            return data

    def check_goods(self):
        # 查询商品详情表
        sql = "select goods_id as productID, goods_img as img, goods_name as title, goods_prices as price from goods_details"
        user_profile = self.query(sql)
        return user_profile

    def del_collect(self, clt_id):
        sql = "delete from u_clt where clt_id=%s"
        success = False
        with self.db as c:
            c.execute(sql, args=clt_id)
            success = True
        return success

    def check_goods2(self, clt_id):
        # 查询商品详情表
        sql = "select goods_id, goods_img, goods_name, goods_prices from goods_details where goods_id=%s"
        user_profile = self.query(sql, clt_id)
        return user_profile
