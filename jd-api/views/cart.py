from flask import Blueprint, request, jsonify

from libs import cache

cart_blue = Blueprint('cart_blue', __name__)

@cart_blue.route('/cart/', methods=('POST', ))
def cart():

    token = request.args.get('token', None)
    if token is None:
        return jsonify({
            'code': 202,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })
    if cache.check_token(token):
        user_id = cache.get_token_user_id(token)

    return jsonify({
        'code': 200,
        'msg': '登陆购物车页面',
        'data': {
            "user_id": user_id,
            'ord_num': '100191919',
            'state': '待支付',
            'price': '2900.00元'
        }
    })


@cart_blue.route('/cart/updata/', methods=('POST', ))
def updata_cart():
    return jsonify({
        "code":200,
        'msg': '增加、减少'
    })

@cart_blue.route('/cart/delete/', methods=('POST', ))
def del_cart():
    return jsonify({
        "code":200,
        'msg': '删除'
    })

@cart_blue.route('/cart/paycart/', methods=('POST', ))
def pay_cart():
    return jsonify({
        "code":200,
        'msg': '结算'
    })
@cart_blue.route('/cart/crtord/', methods=('POST', ))
def crtord_cart():
    return jsonify({
        "code":200,
        'msg': '生成订单提交'
    })

@cart_blue.route('/cart/payord/', methods=('POST', ))
def payord_cart():
    return jsonify({
        "code":200,
        'msg': '支付提交'
    })