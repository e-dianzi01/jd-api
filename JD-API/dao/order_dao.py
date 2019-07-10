from dao import BaseDao
from logger import api_logger


class OrderDao(BaseDao):
    def get_order_all(self, user_id_id):
        orderList = []
        dict2 = {}
        api_logger.info('db insert jd_user: <%s>' % user_id_id)

        sql = "select * from o_detail " \
              "where o_user_id=%s and o_status !=5 limit 20 "
        order_info = self.query(sql, user_id_id)

        for i in range(len(order_info)):
            dict_goods = {}
            # 查询商家名称
            m_id= order_info[i]['o_shopper_id']
            sql1 = "select m_name from jd_shopper " \
                   "where m_id=%s"
            shop_info = self.query(sql1, m_id)
            if not shop_info:
                shop_info = [{'m_name': '无'}]
            orderID = order_info[i]['o_num']

            sql2 = "select * from order_list " \
                   "where o_num_id=%s"
            goods_info1 = self.query(sql2,orderID)

            for j in range(len(goods_info1)):
                goods_id = goods_info1[j]['o_goods_id']
                sql3 = "select goods_img,goods_name from goods_details " \
                       "where goods_id=%s"
                goods_info2 = self.query(sql3, goods_id)[0]
                dict_goods = {
                    "img": goods_info2['goods_img'],
                    "describe": goods_info2['goods_name'],
                    "ProductNum": goods_info1[j]['g_num'],
                    "productPrice": goods_info1[j]['g_price']
                }

            dict2 = {
                "orderstatus": order_info[i]['o_status'],
                "orderID": order_info[i]['o_num'],
                "shopID": m_id,
                "shopname": shop_info[0]['m_name'],
                "orderasset": order_info[0]['o_total'],
                "orderProductList": [dict_goods]
            }
            orderList.append(dict2)

        return orderList

    def get_order_sts(self ,user_id ,o_status):
        orderList = []
        dict2 = {}
        api_logger.info('db insert jd_user: <%s>' % user_id)
        sql = "select * from o_detail " \
              "where o_user_id=%s and o_status=%s limit 20"
        order_info = self.query(sql, user_id, o_status)
        for i in range(len(order_info)):
            dict_goods = {}
            #查询商家名称
            m_id = order_info[i]['o_shopper_id']


            sql1 = "select m_name from jd_shopper " \
                  "where m_id=%s"
            shop_info = self.query(sql1, m_id)

            orderID = order_info[i]['o_num']
            sql2 = "select * from order_list " \
                  "where o_num_id=%s"
            goods_info1=self.query(sql2, orderID)
            for j in range(len(goods_info1)):
                goods_id = goods_info1[j]['o_goods_id']
                sql3 = "select goods_img,goods_name from goods_details " \
                      "where goods_id=%s"
                goods_info2= self.query(sql3,goods_id)[0]
                dict_goods = {
                    "img": goods_info2['goods_img'],
                    "describe": goods_info2['goods_name'],
                    "ProductNum":goods_info1[j]['g_num'],
                    "productPrice":goods_info1[j]['g_price']
                }
            if not shop_info:
                shop_info = [{'m_name': '无'}]
            dict2 = {
                     "orderstatus":order_info[i]['o_status'],
                     "orderID":order_info[i]['o_num'],
                     "shopID":m_id,
                     "shopname":shop_info[0]['m_name'],
                     "orderasset":order_info[0]['o_total'],
                     "orderProductList":[dict_goods]
                     }
            orderList.append(dict2)

        return orderList



    def UpdateOrder(self,user_id,state,o_num):
        api_logger.info('db update o_detail: <%s>' % user_id)
        sql = "update o_detail set o_status=%s " \
              "where o_num=%s"%(state,o_num)
        succuss = False
        with self.db as c:
            c.execute(sql)
            api_logger.info('%s ok!' % sql)
            succuss = True
        return succuss





    def get_oreder_info(self,o_num):
        sql = "select * from o_detail " \
              "where o_user_id=%s"
        order_info = self.query(sql,o_num)
        if order_info:
            return order_info



