from flask import Blueprint, request, redirect, url_for

from dao import BaseDao

test_blue = Blueprint('test_blue', __name__)


@test_blue.route('/test/<o_num>/<status>/', methods=('POST', 'GET',))
def connect_test(o_num, status):
    print(o_num, status)
    success = BaseDao().update('o_detail', 'o_status', status, 'o_num', o_num)
    if success:
        return redirect('http://10.35.161.62:8888/admin/orders/orderdetail/')
    else:
        return ('操作数据库失败！')