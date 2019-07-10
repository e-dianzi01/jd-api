from flask import Blueprint, request, jsonify
from dao.user_dao import UserDao
from dao.vou_dao import VouDao
from libs.cache import check_token, get_token_user_id

asset_blue = Blueprint('asset_blue', __name__)


@asset_blue.route('/mine/asset/', methods=('POST',))
def search_discount():
    # 查询资产
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        dao = VouDao()
        dis_data = dao.check_vouchers(user_id)
        print(dis_data)
        asset_data = dao.check_asset(user_id)
        print(dis_data, asset_data)
        if all((dis_data, asset_data)):
            data = {
                "assetInfo": {
                    "vouchers": dis_data[0]['cop_id'],
                    "balance": asset_data[0]['asset'],
                    "integral": asset_data[0]['u_intg'],
                }
            }
            return jsonify({
                'code': 200,
                '查询成功！'
                'data': data
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '查询数据库失败！'
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })


@asset_blue.route('/mine/asset/paycost/', methods=('POST',))
def recharge():
    # 余额充值
    req_data = request.get_json()
    token = req_data.get('token')
    amount = req_data.get('amount')  # 获取上传的充值金额
    if check_token(token):
        user_id = get_token_user_id(token)
        ass_data = VouDao().check_asset(user_id)
        balance = int(ass_data[0]['asset'])
        print(balance)
        if balance is not None:  # 查询到金额
            balance += amount
            dao = UserDao()
            dao.update('jd_user', 'asset', balance, 'user_id', user_id)
            return jsonify({
                'code': 200,
                'data': balance
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '查询金额失败！'
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })


@asset_blue.route('/mine/asset/vouchers/', methods=('POST',))
def search_vouch():
    # 查询优惠卷
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        vou_data = VouDao().check_vouchers(user_id)
        if vou_data:
            data = {
                "mineVouchersList": [{
                    "vouchersUseCondition": 500,
                    "minusPrice": vou_data[0]['minusprice'],
                    "title": vou_data[0]['title'],
                    "type": vou_data[0]['vuc']
                    # 没有优惠卷过期时间
                }]
            }
            return jsonify({
                'code': 200,
                'msg': '查询成功！',
                'data': data
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '数据库查询失败！'
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })


@asset_blue.route('/mine/asset/vouchers/asc/', methods=('POST',))
def up_sort():
    # 所有优惠卷按金额升序排列
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        vou_data = VouDao().sort_up()
        if vou_data:
            return jsonify({
                'code': 200,
                'msg': '排序成功！',
                'data': vou_data
            })
        else:
            return jsonify({
                'code': 200,
                'msg': '查询数据库失败！'
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })


@asset_blue.route('/mine/asset/vouchers/desc/', methods=('POST',))
def down_sort():
    # 所有优惠卷按金额降序排列
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        vou_data = VouDao().sort_down()
        if vou_data:
            return jsonify({
                'code': 200,
                'msg': '排序成功！',
                'data': vou_data
            })
        else:
            return jsonify({
                'code': 200,
                'msg': '查询数据库失败！'
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })


@asset_blue.route('/mine/asset/vouchers/type/01/', methods=('POST',))
def vouch_type0():
    # 查询无门槛优惠卷
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        vou_data = VouDao().vouchers_0(user_id)
        print(vou_data)
        if vou_data:
            vouchers = []
            for i in range(len(vou_data)):
                vouchers.append(vou_data[i]['cop_id'])
            return jsonify({
                'code': 200,
                'msg': '查询成功！',
                'data': vouchers
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '查询数据库失败！'
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })


@asset_blue.route('/mine/asset/vouchers/type/02/', methods=('POST',))
def vouch_type1():
    # 查询满减优惠卷
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        vou_data = VouDao().vouchers_1(user_id)
        if vou_data:
            vouchers = []
            for i in range(len(vou_data)):
                vouchers.append(vou_data[i]['cop_id'])
                return jsonify({
                    'code': 200,
                    'msg': '查询成功！',
                    'data': vouchers
                })
        else:
            return jsonify({
                'code': 400,
                'msg': '查询数据库失败！'
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })
