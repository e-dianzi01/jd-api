import re
from flask import Blueprint
from flask import request, jsonify

from dao import BaseDao
from dao.goods_dao import GoodsDao
from dao.vou_dao import VouDao
from libs.cache import check_token, get_token_user_id, save_token
from libs.crypt import check_password, make_password
from libs.sms import get_code, send_sms_code, get_uid
from logger import api_logger
from dao.user_dao import UserDao
from services.check import check_login_tel
from datetime import datetime
from libs import cache, rd

blue = Blueprint('user_api', __name__)


@blue.route('/regist/', methods=('POST',))
def user_regist():
    code = get_code()
    req_data = None
    print(code)
    api_logger.info(request.headers)

    if request.headers['Content-Type'].startswith('application/json'):
        req_data = request.get_json()

    if req_data is None:
        api_logger.warn('%s 请求参数未上传-json' % request.remote_addr)
        return jsonify({
            'code': 400,
            'msg': '请上传json数据，且参数必须按api接口标准给定'
        })

    api_logger.debug(req_data)
    if not all((
            req_data.get('tel', False),
            req_data.get('idtf', False))
           ):

        phone = str(req_data.get('tel'))
        ret = re.match(r"^1[35678]\d{9}$", phone)
        if ret:
            result = check_login_tel(phone).get_json()
            if result.get('code') == 400:
                resp = send_sms_code(phone, code).decode()
                if resp[-4:-2] == "OK":
                    rd.set(phone, code)
                    rd.expire(phone, 120)
                    return jsonify({
                        'code': 200,
                        'msg': '验证码发送成功',
                    })
                else:
                    return jsonify({
                        'code': 400,
                        'msg': '验证码发送失败'
                    })
            else:
                return jsonify({
                    'code': 403,
                    'msg': '该账号已注册'
                })
        else:
            return jsonify({
                'code': 400,
                'msg': '请输入正确的手机号'
            })
    else:
        phone = req_data.get('tel')
        idtf = str(req_data.get('idtf'))
        temp2 = rd.get(phone).decode()
        if temp2 == idtf:
            user_id = get_uid()
            dao = UserDao()
            req_data = {'tel': phone,
                        'user_id': user_id,
                        'user_name': user_id,
                        'auth_string': 'jd' + phone,
                        "asset": 0,
                        "u_intg": 100
                        }
            dao.save(**req_data)
            token = cache.new_token()
            rd.set(token, user_id)
            rd.expire(token, 3600 * 12)
            req_data = {'tel': phone,
                        'user_id': user_id,
                        'user_name': user_id,
                        'auth_string': 'jd' + phone,
                        "u_intg":100,
                        "asset":0,
                        "token" :token,
                        'bool_pay_pwd': False
            }
            return jsonify({
                'code': 200,
                'msg': '注册成功',
                'data': req_data
                })
        else:
            return jsonify({
                'code': 400,
                'msg': '注册失败，验证码错误'
            })


@blue.route('/login/', methods=('POST',))
def user_login():
    # 登录
    req_data = request.get_json()
    code = get_code()
    if not all((
            req_data.get('tel', False),
            req_data.get('idtf', False))
            ):
        phone = str(req_data.get('tel'))
        result = check_login_tel(phone).get_json()
        if result.get('code') == 300:
            resp = send_sms_code(phone, code).decode()
            if resp[-4:-2] == "OK":
                rd.set(phone, code)
                rd.expire(phone, 120)
                return jsonify({
                    'code': 200,
                    'msg': '验证码发送成功',
                })
            else:
                return jsonify({
                    'code': 400,
                    'msg': '验证码发送失败'
                })
        else:
            return jsonify({
                'code': 403,
                'msg': '该手机号尚未注册注册！'
            })
    else:
        phone = req_data.get('tel')
        idtf = str(req_data.get('idtf'))
        temp2 = rd.get(phone)
        if not temp2:
            return jsonify({
                'code': 404,
                'msg': '验证码已过期',
            })
        temp2 = temp2.decode()
        if temp2 == idtf:
            token = cache.new_token()
            data = UserDao().get_jd_user(phone)
            user_id = data[0]['user_id']
            pay_pwd = data[0]['pay_pwd']
            if pay_pwd is None:
                result_pwd = False
            else:
                result_pwd = True
            rd.set(token, user_id)
            rd.expire(token, 3600 * 12)
            return jsonify({
                'code': 200,
                'msg': '登录成功！',
                'token': token,
                'data': data[0],
                'bool_pay_pwd': result_pwd

            })
        else:
            return jsonify({
                'code': 400,
                'msg': '注册失败，验证码错误'
            })


@blue.route('/mine/identify/', methods=('POST',))
def user_identify():
    # 添加银行卡和身份证
    u_data = request.get_json()
    token = u_data.get('token')
    if check_token(token):
        dao = UserDao()
        user_id = get_token_user_id(token)
        print(user_id)
        data = dao.check_real(user_id)
        print(data)
        if data:
            u_bank = data[0]['u_bank']
            user_card = data[0]['user_card']
            if (u_bank and user_card) is not None:
                return jsonify({
                    'code': 300,
                    'msg': '您已添加过该信息！'
                })
            else:
                dict1 = {'u_bank': u_data.get('u_bank'), 'user_card': u_data.get('user_card'), 'is_val': 1, 'asset':0}
                for k, v in dict1.items():
                    user_save = dao.update('jd_user', k, v, 'user_id', user_id)
                if user_save:
                    return jsonify({
                        'code': 200,
                        'msg': '验证通过！'
                    })
                else:
                    return jsonify({
                        'code': 400,
                        'msg': '添加失败！'
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


@blue.route('/mine/set/', methods=('POST',))
def user_update():
    # 用户登录后修改自己的个人信息
    u_data = request.get_json()
    token = u_data.get('token')   # 获取token
    print(token)
    old_pwd = u_data.get('old_pwd')  # 获取用户上传的原密码
    new_pwd = u_data.get('new_pwd')  # 获取用户上传的新密码
    if check_token(token):    # 验证token
        user_id = get_token_user_id(token)    # 通过token获取用户的ID
        check_data = UserDao().get_profile(user_id)    # 通过用户ID查询用户的详细信息
        if check_data:    # 如果查询成功
            dao = UserDao()
            if all((old_pwd, new_pwd)):   # 修改支付密码
                pay_pwd = check_data[0]['pay_pwd']    # 获取数据库中的密码
                if old_pwd == pay_pwd:   # 若原密码等于库中的密码
                    user_save = dao.update('jd_user', "pay_pwd", new_pwd, 'user_id', user_id)   # 将新密码存入数据库
                    if user_save:   # 如果保存成功
                        data = {
                            'userPhoto': u_data.get('u_img'),
                            'userID': user_id,
                            'userName': u_data.get('user_name'),
                            'realname': check_data[0]['is_val'],
                            'TEL': check_data[0]['tel'],
                            'Email': check_data[0]['u_email'],
                        }
                        return jsonify({'code': 200, 'msg': '修改成功！','data': data})
                    else:
                        return jsonify({'code': 400, 'msg': '修改失败！'})
                else:
                    return jsonify({'code': 400, 'msg': '原密码输入错误！'})
            elif old_pwd:# 设置支付密码
                user_save = False
                dict1 = {'u_img': u_data.get('u_img'), 'user_name': u_data.get('user_name'),
                         'pay_pwd': u_data.get('old_pwd')}
                for k, v in dict1.items():
                    user_save = dao.update('jd_user', k, v, 'user_id', user_id)
                if user_save:
                    data = {
                        'userPhoto': u_data.get('u_img'),
                        'userID': user_id,
                        'userName': u_data.get('user_name'),
                        'realname': check_data[0]['is_val'],
                        'TEL': check_data[0]['tel'],
                        'Email': check_data[0]['u_email'],
                    }
                    return jsonify({'code': 200, 'msg': '修改成功！', 'data': data})
                else:
                    return jsonify({'code': 400,'msg': '修改失败！'})
            else:# 修改除密码外的其他信息
                user_save = False
                dict1 = {'u_img': u_data.get('u_img'), 'user_name': u_data.get('user_name')}
                for k, v in dict1.items():
                    user_save = dao.update('jd_user', k, v, 'user_id', user_id)
                if user_save:
                    data = {
                        'userPhoto': u_data.get('u_img'),
                        'userID': user_id,
                        'userName': u_data.get('user_name'),
                        'realname': check_data[0]['is_val'],
                        'TEL': check_data[0]['tel'],
                        'Email': check_data[0]['u_email'],
                    }
                    return jsonify({'code': 200, 'msg': '修改成功！', 'data': data})
                else:
                    return jsonify({'code': 200, 'msg': '修改失败！'})
        else:
            return jsonify({'code': 400, 'msg': '查询数据库失败！',})
    else:
        return jsonify({'code': 400, 'msg': 'token验证失败！'})


@blue.route('/logout/', methods=('POST',))
def logout():
    # 用户退出
    u_data = request.get_json()
    token = u_data.get('token')
    if check_token(token):
        rd.DEL(token)
        return jsonify({
            'code': 200,
            'msg': '退出成功！'
        })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })


@blue.route('/mine/', methods=('POST',))
def mine_info():
    # " 我的" 页面所需要的数据信息
    u_data = request.get_json()
    token = u_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        print(user_id)
        user_data = UserDao().get_profile(user_id)   # 查询用户详细信息
        vou_data = VouDao().check_vouchers(user_id)   # 查询优惠卷信息
        coll_data1 = GoodsDao().check_collect_goods(user_id)  # 收藏的商品信息
        coll_data2 = GoodsDao().check_collect_shops(user_id)   # 收藏的店铺信息
        goods_list = GoodsDao().check_goods()    # 从商品详情表中取20组商品信息,元组类型
        print(user_data, vou_data, coll_data1, coll_data2, goods_list)
        if all((user_data, vou_data, coll_data1, coll_data2, goods_list)):
            re_data = {
                "accountInfo": {
                    "userID": user_id,
                    "userName": user_data[0]['user_name'],      # 用户名
                    "userPhoto": user_data[0]['u_img'],         # 头像
                },
                "assetInfo": {
                    "vouchers": vou_data[0]['cop_id'],      # 优惠卷
                    "balance": user_data[0]['asset'],       # 余额
                    "integral": user_data[0]['u_intg'],     # 积分
                    "redPacket":80
                },
                "browseInfo": {
                    "collectProduct": len(coll_data1),    # 收藏的商品的数量
                    "collectShop": len(coll_data2),       # 收藏的店铺的数量
                    "footprint":16
                },
                "productList": goods_list[:20]            # 20 组商品信息
            }
            return jsonify({
                'code': 200,
                'data': re_data
            })
        else:
            re_data = {
                "accountInfo": {
                    "userID": user_id,
                    "userName": user_data[0]['user_name'],  # 用户名
                    "userPhoto": user_data[0]['u_img'],  # 头像
                },
                "assetInfo": {
                    "vouchers": 0,  # 优惠卷
                    "balance": 0,  # 余额
                    "integral": 100,  # 积分
                    "redPacket": 80
                },
                "browseInfo": {
                    "collectProduct": 0,  # 收藏的商品的数量
                    "collectShop": 0,  # 收藏的店铺的数量
                    "footprint": 16
                },
                "productList": goods_list[:20]  # 20 组商品信息
            }
            return jsonify({
                'code': 200,
                'data': re_data
            })
    else:
        return jsonify({
            'code': 400,
            'msg': 'token验证失败！'
        })
