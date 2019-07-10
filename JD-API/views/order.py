"""
订单数据的接口API
"""
from dao import BaseDao
from libs import cache
from flask import Blueprint, request, jsonify
from dao.order_dao import OrderDao

order_blue = Blueprint('order_blue', __name__)

#查询所有订单
@order_blue.route('/mine/order/', methods=('POST', ))
def get_order():
    # 验证用户是否已登录
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        user_id_id = cache.get_token_user_id(token)

        dao = OrderDao()
        order_list = dao.get_order_all(user_id_id)
        return jsonify({
            'code':200,
            'msg':'订单查询成功',
            'order_list':order_list

        })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })

#查询待支付订单
@order_blue.route('/mine/order/01', methods=('POST', ))
def get_order_arrearage():
    # 验证用户是否已登录
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        user_id_id = cache.get_token_user_id(token)
        dao = OrderDao()
        order_list_ara = dao.get_order_sts(user_id_id ,0)
        return jsonify({
            'code': 200,
            'msg': '待支付订单查询成功',
            'order_list': order_list_ara

        })

    return jsonify({
        'code': 400,
        'msg': 'token查询参数必须提供或者登录后获取token'
    })

#查询待收货订单
@order_blue.route('/mine/order/02', methods=('POST', ))
def get_order_received():
    # 验证用户是否已登录
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        user_id_id = cache.get_token_user_id(token)
        dao = OrderDao()
        order_list_rec = dao.get_order_list(user_id_id ,1)
        return jsonify({
            'code': 200,
            'msg': '已支付订单查询成功',
            'order_list': order_list_rec
        })

    else:
        return jsonify({
            'code': 400,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })

#查询已完成订单
@order_blue.route('/mine/order/03', methods=('POST', ))
def get_order_evaluated():
    # 验证用户是否已登录
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        user_id_id = cache.get_token_user_id(token)
        dao = OrderDao()
        order_list_eva = dao.get_order_sts(user_id_id ,2)
        return jsonify({
            'code': 200,
            'msg': '待评价订单查询成功',
            'order_list': order_list_eva
        })

    else:
        return jsonify({
            'code': 400,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })

