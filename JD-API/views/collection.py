from flask import Blueprint, request, jsonify

from dao import BaseDao
from dao.goods_dao import GoodsDao
from libs.cache import check_token, get_token_user_id

collect_blue = Blueprint('collect_blue', __name__)


@collect_blue.route('/collect/', methods=('POST',))
def collects():
    # 收藏商品或店铺
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        clt_id = req_data.get('clt_id')
        type_id = req_data.get('type_id')
        if (clt_id and type_id)is not None:
            dao = BaseDao()
            save_data = {
                'user_id': user_id,
                'clt_id': clt_id,
                'type_id': type_id}
            result = dao.save('u_clt', **save_data)
            if result:
                return jsonify({'code': 200, 'msg': '收藏成功！'})
            else:
                return jsonify({'code': 400, 'msg': '查询数据库失败！'})
        elif clt_id is not None and type_id is None:   # 取消收藏
            if clt_id:
                dao = GoodsDao()
                delet = dao.del_collect(clt_id)
                if delet:
                    return jsonify({'code': 200, 'msg': '该收藏信息已删除！'})
                else:
                    return jsonify({'code': 400, 'msg': '删除失败！'})
            else:
                return jsonify({'code': 400, 'msg': '未接收到需要删除的ID！'})
        else:
            return jsonify({'code': 400, 'msg': '请上传商铺或商品ID和type类型！'})
    else:
        return jsonify({'code': 400, 'msg': 'token验证失败！'})


@collect_blue.route('/mine/collect/', methods=('POST',))
def collect_pro():
    # “我的” 页面查看收藏的商品和店铺
    req_data = request.get_json()
    token = req_data.get('token')
    if check_token(token):
        user_id = get_token_user_id(token)
        print(user_id,111111111111111111111111111111111111)
        data1 = GoodsDao().check_collect_goods(user_id)
        data2 = GoodsDao().check_collect_shops(user_id)
        if all((data1,data2)):
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            for i in range(len(data1)):
                list1.append(data1[i]['clt_id'])
            for j in list1:
                list2.append(GoodsDao().check_goods2(j))
            for m in range(len(data2)):
                list3.append(data2[m]['clt_id'])
            for n in list3:
                list4.append(GoodsDao().search_shop(n))
            if all((list2, list4)):
                return jsonify({
                    'code': 200,
                    'msg': '查询成功！',
                    'myAttentionList': list2,
                    'myAttentionShop': list4
                })
            else:
                return jsonify({'code': 400, 'msg': '查询数据库失败！'})

        else:return jsonify({'code': 400, 'msg': '你还没有收藏数据！'})
    else:
        return jsonify({'code': 400, 'msg': 'token验证失败！'})