from flask import Blueprint, request, jsonify

from dao.cart_order import cart_orderDao
from libs import cache

cart_order_blue = Blueprint('cart_order_blue', __name__)


@cart_order_blue.route('/cart/paycart/', methods=('POST', ))
def paycart():
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        user_id = cache.get_token_user_id(token)
        goods_list = request.get_json().get('goodsList', None)
        dao = cart_orderDao()
        cart_orderlist = []
        unable_list = []
        for i in range(len(goods_list)):
            goods_id = goods_list[i].keys()
            goods_cart_num = goods_list[i].values()
            resp = dao.check_stock(user_id,goods_id)
            cart_orderlist.append(resp[0])
            if goods_cart_num <= resp[0]['goods_num']:
                unable_list.append({"productID":goods_id,"productstock":resp[0]['goods_num']})
        if len(unable_list)>0:
            return jsonify({
                "code": 400,
                "msg":"商品库存不足，请减少购买数量或改天再来",
                "goodslist":unable_list
            })
        cart_cal_list = []
        for i in range(len(goods_list)):
            goods_id = goods_list[i].keys()
            goods_cart_num = goods_list[i].values()
            resp = dao.check_seckill(user_id, goods_id)
            if resp:
                goods_cal_price = cart_orderlist[i]['kill_prices']
                cart_cal_list.append([goods_id,goods_cart_num,goods_cal_price])
            else:
                goods_cal_price = cart_orderlist[i]['goods_prices']
                cart_cal_list.append([goods_id, goods_cart_num, goods_cal_price])















        # 查询地址，返回默认地址

        data = {

        }

        return jsonify({
            'code': 200,
            'msg': '已支付订单查询成功',
            'data':data
        })

    else:
        return jsonify({
            'code': 400,
            'msg': '您还未登陆，请先登录'
        })



@cart_order_blue.route('/cart/crtord/', methods=('POST', ))
def create_order():
    pass


@cart_order_blue.route('/cart/payord/', methods=('POST', ))
def payorder():
    pass