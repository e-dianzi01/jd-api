import datetime

from dao import BaseDao
from logger import api_logger


class cart_orderDao(BaseDao):
    def save(self, **values):
        api_logger.info('db insert order: <%s>'%values['o_num_id'])
        # values['login_auth_str'] = make_password(values['login_auth_str'])
        return super(cart_orderDao, self).save('order_list', **values)

    def save_detail(self, **values):
        api_logger.info('db insert order: <%s>'%values['o_num'])
        # values['login_auth_str'] = make_password(values['login_auth_str'])
        return super(cart_orderDao,self).save('o_detail', **values)


    def check_stock(self,user_id_id,goods_id):
        api_logger.info('db insert jd_user: <%s>' % user_id_id)
        sql = "select * from goods_details " \
              "where goods_id=%s"
        stock_info = self.query(sql, goods_id)
        return stock_info

    # def check_seckill(self,user_id_id,goods_id):
    #     #判断是否秒杀
    #     api_logger.info('db insert jd_user: <%s>' % user_id_id)
    #     sql = "select kill_time from goods_seckill " \
    #           "where goods_id=%s"
    #     seckill_info = self.query(sql, goods_id)
    #     seckill_time = datetime.datetime(2019,1,1,0,0,0)
    #     if seckill_info:
    #         seckill_time = seckill_info[0]['kill_time']
    #     # 判断时间
    #     currtime = datetime.datetime.now()
    #     timestep = currtime - seckill_time
    #     timeday = timestep.days
    #     if timeday != 0:
    #         return
    #     timeseconds = timestep.seconds/3600
    #     if (seckill_time.hour == 22 and timeseconds <2 ) or (timeseconds < 4):
    #         return True

    def get_addr(self,user_id_id):
        api_logger.info('db insert jd_user: <%s>' % user_id_id)
        sql = "select * from u_address " \
              "where user_id_id=%s"
        resp = self.query(sql, user_id_id)
        if resp:
            return resp[0]["user_address"]
        else:
            return "北京"


    def get_vou_list(self,user_id):
        api_logger.info('db insert jd_user: <%s>' % user_id)
        sql = "select * from jd_coupon " \
              "where user_id=%s"
        return self.query(sql, user_id)

    #校验优惠券
    def check_vou(self,user_id_id,cop_id):
        api_logger.info('db insert jd_user: <%s>' % user_id_id)
        sql = "select minusprice,vuc from jd_coupon " \
              "where cop_id=%s"
        return self.query(sql, cop_id)

    def delete_vou(self,user_id_id,cop_id):
        api_logger.info('db insert jd_user: <%s>' % user_id_id)
        resp_vou = self.del_vou(cop_id,user_id_id)
        if resp_vou:
            return True

    def update(self,user_id_id,goods_id,goods_cart_num):
        api_logger.info('db insert goods_details: <%s>' % user_id_id)
        sql = "update goods_details set goods_num=goods_num-%s"\
              "where goods_id=%s"
        success = False
        with self.db as c:
            c.execute(sql,goods_cart_num,goods_id)
            success = True
        return success

    def get_tel(self,user_id_id):
        sql = "select tel from jd_user " \
              "where user_id=%s"
        resp = self.query(sql, user_id_id)
        if resp:
            return resp[0]
        else:return resp["tel":"无"]

    def get_shopname(self,m_id_id):
        sql = "select m_username from jd_shopper " \
              "where m_id=%s"
        resp = self.query(sql, m_id_id)
        if resp:
            print(resp[0],'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            return resp[0]

    def get_std(self,goods_id):
        sql = "select properties from goods_sku " \
              "where goods_id=%s"
        resp = self.query(sql, goods_id)
        if resp:
            print(resp[0], 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            return resp[0]
        else:return resp[{"properties":"无"}]



