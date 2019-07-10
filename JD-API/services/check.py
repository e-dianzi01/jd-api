from flask import request, jsonify
from dao.user_dao import UserDao

def check_login_tel(phone):
    # 查询参数

    if UserDao().check_login_phone(phone):

        return jsonify({
        'code':300,
        'msg':'该账号已注册！'
          })
    return jsonify({
            'code': 400,
            'msg': '账号不存在！'})





def check_login_name(user_name):
    result = {
        'code': 400,
        'msg': '用户名不存在'
    }
    if not UserDao().check_login_name(user_name):
        result['code'] = 300
        result['msg'] = '用户名已存在'

    return jsonify(result)