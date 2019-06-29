import datetime

from dao import BaseDao
from logger import api_logger


class cart_orderDao(BaseDao):
    def check_stock(self,user_id,goods_id):
        api_logger.info('db insert jd_user: <%s>' % user_id)
        sql = "select m_id, goods_id,goods_num,goods_prices,kill_prices from goods_details " \
              "where goods_id=%s"
        stock_info = self.query(sql, goods_id)
        return stock_info

    def check_seckill(self,user_id,goods_id):
        #判断是否秒杀
        api_logger.info('db insert jd_user: <%s>' % user_id)
        sql = "select kill_time from goods_seckill " \
              "where goods_id=%s"
        seckill_info = self.query(sql, goods_id)
        seckill_time = seckill_info[0]['kill_time']
        # 判断时间
        out_time = 1122
        currtime = datetime.datetime.now()


        return

    def check_order(self):
        pass


