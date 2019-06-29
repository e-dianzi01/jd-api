import re
from flask import Blueprint
from flask import request, jsonify

from libs.cache import check_token, get_token_user_id
from libs.sms import get_code, send_sms_code, get_uid
from logger import api_logger
from dao.user_dao import UserDao
from services.check import check_login_tel

blue = Blueprint('user_api', __name__)

from datetime import datetime
from libs import cache, rd


@blue.route('/regist/', methods=('POST',))
def user_regist():
    code = get_code()
    req_data = None
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
            token = cache.new_token()
            rd.set(token, phone)
            rd.expire(token, 60*30)
            req_data ={'tel':phone,
                'user_id': user_id,
                'user_name': user_id,
                        }
            dao.save(**req_data)
            req_data = {'tel': phone,
                        'user_id': user_id,
                        'user_name': user_id,
                        'token': token
                        }

            return jsonify({
                'code': 200,
                'msg': '注册成功',
                'data':req_data
                })
        else:
            return jsonify({
                'code': 400,
                'msg': '注册失败，验证码错误'
            })


@blue.route('/login/', methods=('POST',))
def user_login():
    api_logger.debug('user login get action!')
    # 验证参数
    req_data = request.get_json()
    login_name = req_data.get('user_name', None)
    auth_str = req_data.get('auth_string', None)
    # 获取登录用户的信息
    if all((req_data.get('auth_string'),
            req_data.get('user_name'))):
        print(1111111)
        dao = UserDao()
        try:
            login_user = dao.login(login_name, auth_str)
            # 生成token
            token = cache.new_token()
            # 将token存在redis的缓存中，绑定的数据可以是用户Id也可以是用户的信息
            cache.save_token(token, login_user.get('user_id'))
            return jsonify({
                'code': 200,
                'token': token,
                'user_data': login_user
            })
        except Exception as e:
            return jsonify({
                'code': 202,
                'msg': e
            })
    else:
        phone = req_data.get('tel')
        result = check_login_tel(phone).get_json()
        if result.get('code') == 400:   # 手机号不存在
            return jsonify({
                'code': 400,
                'msg': '该手机号尚未注册！'
            })
        else:  # 手机号已存在
            # 验证token
            token = req_data.get('token')
            print(token,2222)
            if check_token(token):   # token 存在
                return jsonify({
                    'code': 200,
                    'msg': '登录成功！'
                })
            else:  # token 不存在
                return jsonify({
                    'code': 400,
                    'msg': 'token验证失败！'
                })

@blue.route('/mine/identify/', methods=('POST',))
def user_identify():
    # 添加银行卡和身份证
    u_data = request.get_json()
    u_bank = u_data.get('u_bank', None)
    user_card = u_data.get('user_card', None)
    if all((bool(u_bank), bool(user_card))):
        return jsonify({
            'code': 300,
            'msg': '您已添加该信息！'
        })
    else:
        token = u_data.get('token')
        if check_token(token):
            user_id = get_token_user_id(token)
            dao = UserDao()
            dao.save_user_id(**u_data)
        else:
            return jsonify({
                'code': 400,
                'msg': '用户验证失败！'
            })

@blue.route('/mine/set/', methods=('POST',))
def user_update():
    # 用户登录后修改自己的个人信息
    u_data = request.get_json()
    token = u_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        check_data = UserDao().get_profile(user_id)
        u_img = u_data.get('u_img', check_data.get('u_img'))
        user_name = u_data.get('user_name', check_data.get('user_name'))
        tel = u_data.get('tel', check_data.get('tel'))
        u_email = u_data.get('u_email', check_data.get('u_email'))
        is_val = check_data.get('is_val')
        dao = UserDao()
        dao.save_user_id(**u_data)
        data1 = {
            'userPhoto': u_img,
            'userID': user_id,
            'userName': user_name,
            'realname': is_val,
            'TEL': tel,
            'Email': u_email,
        }
        return jsonify({
            'code': 200,
            'msg': '修改成功！',
            'data': data1
        })
        # else:
        #     return jsonify({
        #         'code': 400,
        #         'msg': '查询数据库失败！',
        #         'data': ''
        #     })

    else:
        return jsonify({
            'code': 400,
            'msg': '用户验证失败！'
        })
