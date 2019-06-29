from dao import BaseDao
from logger import api_logger


class OrderDao(BaseDao):

    def get_order_all(self ,user_id ):
        orderList = []
        api_logger.info('db insert jd_user: <%s>' % user_id)
        sql = "select o_status,o_num, o_shopper_id,o_total,o_goods_id from o_detail " \
              "where o_user_id=%s"
        order_info = self.query(sql, user_id)
        print(order_info)
        for i in range(len(order_info)):
            shop_info = []
            m_id = order_info[i]['o_shopper_id']

            sql = "select m_name from jd_shopper " \
                  "where id=%s"
            shop_info = self.query(sql, m_id)
            print(shop_info)
            goods_info = []
            # sql = "select o_status,o_num, o_shopper,o_total,goods_id from  " \
            #       "where user_id=%s" % user_id
            # print(order_profile = self.query(sql, user_id)[0])

            dict[i] = {"orderstatus":order_info[i]['o_status'],
                     "orderID":order_info[i]['o_num'],
                     "shopID":m_id,
                     "shopname":shop_info[0]['m_name'],
                     "orderasset":order_info[0]['o_total'],
                     "goodsList":[goods_info[0]]
                     }
            orderList.append(dict[i])
        return orderList

    def get_order_sts(self ,user_id ,o_status):
        orderList = []
        api_logger.info('db insert jd_user: <%s>' % user_id)
        sql = "select o_status,o_num, o_shopper_id,o_total,o_goods_id from o_detail " \
              "where o_user_id=%s and o_status=%s"
        order_info = self.query(sql, user_id, o_status)
        print(order_info)
        for i in range(len(order_info)):
            shop_info = []
            m_id = order_info[i]['o_shopper_id']

            sql = "select m_name from jd_shopper " \
                  "where id=%s"
            shop_info = self.query(sql, m_id)
            print(shop_info)
            goods_info = []
            # sql = "select o_status,o_num, o_shopper,o_total,goods_id from  " \
            #       "where user_id=%s" % user_id
            # print(order_profile = self.query(sql, user_id)[0])

            dict[i] = {"orderstatus": order_info[i]['o_status'],
                       "orderID": order_info[i]['o_num'],
                       "shopID": m_id,
                       "shopname": shop_info[0]['m_name'],
                       "orderasset": order_info[0]['o_total'],
                       "goodsList": [goods_info[0]]
                       }
            orderList = orderList.append(dict[i])

        return orderList



