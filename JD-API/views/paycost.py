import datetime

from flask import Blueprint, request, jsonify
from dao.cart_order import cart_orderDao
from libs import cache, rd
from services.order import get_order_num

paycost_blue= Blueprint('paycost_blue', __name__)

@paycost_blue.route('/index/paycost/phone/', methods=('POST', ))
def create_phone_order():
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        #获取请求参数
        user_id_id = cache.get_token_user_id(token)
        req_data = request.get_json()
        payasset = req_data.get('payasset', None)
        tel = req_data.get('tel', None)
        if not all((payasset,tel)):
            return jsonify({
                'code': 401,
                'msg': '手机号和充值金额必须上传',
            })

        dao = cart_orderDao()
        #优惠券ID
        cart_cal_rel = payasset
        voucher_id = request.get_json().get('voucher_id', None)
        vou_resp = dao.check_vou(user_id_id,voucher_id)
        if vou_resp:
            if vou_resp[0]['vuc'] == 0:
                vou_price = vou_resp[0]['minusprice']
                cart_cal_rel = payasset - vou_price

            if vou_resp[0]['vuc'] == 1:
                vou_price = vou_resp[0]['minusprice']
                if payasset > 200 and payasset < 500:
                    cart_cal_rel = payasset - vou_price
                elif payasset >500 and payasset < 1000:
                    cart_cal_rel = payasset - vou_price
                elif payasset > 1000:
                    cart_cal_rel = payasset - vou_price

        #将订单写入数据库
        o_num = get_order_num()
        dict1 = {
            "o_num": o_num,
            "o_addr": '不需要地址',
            "o_conn": tel,
            "o_time": datetime.datetime.now(),
            "o_status": 0,
            "o_total": payasset,
            "o_relpay": cart_cal_rel,
            "o_shopper_id": 'phone bill',
            "o_user_id": user_id_id
        }
        print(dict1)
        dao.save_detail(**dict1)

        rd.set(cart_cal_rel,o_num)
        rd.expire(cart_cal_rel,2*60*60)
        # dao.delete_vou(user_id_id, voucher_id)
        data = {
            "orderID":o_num,
            "total":cart_cal_rel
        }
        return jsonify({
            'code': 200,
            'msg': '订单生成成功',
            'data': data
        })

    else:
        return jsonify({
            'code': 400,
            'msg': '您还未登陆，请先登录'
        })


@paycost_blue.route('/index/paycost/traffic/', methods=('POST',))
def create_traffic_order():
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        # 获取请求参数
        user_id_id = cache.get_token_user_id(token)
        req_data = request.get_json()
        payasset= req_data.get('payasset', None)
        tel = req_data.get('tel', None)
        if not all((payasset, tel)):
            return jsonify({
                'code': 401,
                'msg': '手机号和流量数值必须上传',
            })
        # payasset = get_tra_asset(phonetra)
        dao = cart_orderDao()
        cart_cal_rel = payasset
        # 优惠券ID
        voucher_id = request.get_json().get('voucher_id', None)
        vou_resp = dao.check_vou(user_id_id, voucher_id)
        if vou_resp:
            if vou_resp[0]['vuc'] == 0:
                vou_price = vou_resp[0]['minusprice']
                cart_cal_rel = payasset - vou_price

            if vou_resp[0]['vuc'] == 1:
                vou_price = vou_resp[0]['minusprice']
                if payasset > 200 and payasset < 500:
                    cart_cal_rel = payasset - vou_price
                elif payasset > 500 and payasset < 1000:
                    cart_cal_rel = payasset - vou_price
                elif payasset > 1000:
                    cart_cal_rel = payasset - vou_price

        # 将订单写入数据库
        o_num = get_order_num()
        dict1 = {
            "o_num": o_num,
            "o_addr": '不需要地址',
            "o_conn": tel,
            "o_time": datetime.datetime.now(),
            "o_status": 0,
            "o_total": payasset,
            "o_relpay": cart_cal_rel,
            "o_shopper_id": 'phonetraffic',
            "o_user_id": user_id_id
        }
        print(dict1)
        dao.save_detail(**dict1)

        rd.set(cart_cal_rel, o_num)
        rd.expire(cart_cal_rel, 2 * 60 * 60)
        # dao.delete_vou(user_id_id, voucher_id)
        data = {
            "orderID": o_num,
            "total": cart_cal_rel
        }
        return jsonify({
            'code': 200,
            'msg': '订单生成成功',
            'data': data
        })

    else:
        return jsonify({
            'code': 400,
            'msg': '您还未登陆，请先登录'
        })
