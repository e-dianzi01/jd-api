from flask import Blueprint, request, jsonify

from dao import BaseDao
from dao.address_dao import AddDao
from dao.user_dao import UserDao
from libs.cache import check_token, get_token_user_id

address_blue = Blueprint('address_blue', __name__)


@address_blue.route('/mine/set/address/', methods=('POST',))
def check_address():
    # 查询地址
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        dao = AddDao()
        check_data = dao.check_address(user_id)
        user_data = UserDao().get_profile(user_id)
        if all((check_data, user_data)):
            data = {
                'addressList': [
                    {
                        "receivePersonName": user_data[0]['user_name'],
                        "receiveAddress": check_data[0]['user_address'],
                        "is_default": check_data[0]['is_default'],
                        "receiveTEL": user_data[0]['tel']
                    }
                ]
            }
            return jsonify({'code': 200,'data': data})
        else:
            return jsonify({'code': 400, 'msg': '数据库查询失败！'})
    else:
        return jsonify({'code': 400, 'msg': 'token验证失败！'})


@address_blue.route('/mine/set/address/update/', methods=('POST',))
def update_address():
    # 修改地址
    req_data = request.get_json()
    token = req_data.get('token')
    add_id = req_data.get('address', None)
    re_str = req_data.get('strs', None)
    print(re_str, add_id)
    if check_token(token):
        user_id = get_token_user_id(token)

        if add_id is not None and re_str is None:  # 删除
            dao = BaseDao()
            dao.delete('u_address', 'user_address', add_id)
            return jsonify({'code': 200, 'msg': '该地址已删除！'})
        elif (add_id and re_str)is not None:   # 修改
            dao = AddDao()
            dao.update('u_address', 'user_address', re_str, 'user_address', add_id)
            check_data = dao.check_address(user_id)
            user_data = UserDao().get_profile(user_id)
            if all((check_data, user_data)):
                data = {
                    'addressList': [
                        {
                            "receivePersonName": user_data[0]['user_name'],
                            "receiveAddress": check_data[0]['user_address'],
                            "receiveTEL": user_data[0]['tel']
                        }
                    ]
                }
                return jsonify({'code': 200, 'msg': '地址修改成功！', 'data': data})
            else:
                return jsonify({'code': 400, 'msg': '数据库查询失败！'})

        elif re_str is not None and add_id is None:  # 添加
            print(re_str)
            dao = AddDao()
            save_add = dao.save('u_address', **{"user_id": user_id, "user_address": re_str, "is_default": 0})
            if save_add:
                check_data = dao.check_address(user_id)
                user_data = UserDao().get_profile(user_id)
                if all((check_data, user_data)):
                    data = {
                        'addressList': [
                            {
                                "receivePersonName": user_data[0]['user_name'],
                                "receiveAddress": check_data[0]['user_address'],
                                "receiveTEL": user_data[0]['tel']
                            }
                        ]
                    }
                    return jsonify({'code': 200, 'msg': '地址添加成功！', 'data': data})
                else:
                    return jsonify({'code': 400, 'msg': '数据库查询失败！'})
            else:
                return jsonify({'code': 400, 'msg': '地址添加失败！'})
        else:
            return jsonify({'code': 400, 'msg': '数据上传有误！'})
    else:
        return jsonify({'code': 400, 'msg': 'token验证失败！'})


