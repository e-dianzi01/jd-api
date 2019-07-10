from flask import Blueprint, request, jsonify
from dao.cart_dao import CartDao
from libs import cache

cart_blue = Blueprint('cart_blue', __name__)

@cart_blue.route('/cart/', methods=('POST',))
def cart():
    cart_data = eval(request.get_data())
    token = cart_data['token']

    if token is None:
        return jsonify({
            'code': 400,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })

    if cache.check_token(token):
        userid = cache.get_token_user_id(token)

        cart_sql = "select jd_shopper.m_name as shopName," \
                   "jd_shopper.m_id as shopID," \
                 "goods_details.goods_img as img," \
                 "goods_details.goods_id as productID," \
                 "goods_details.goods_name as goodsdescribe," \
                 "goods_sku.properties as model," \
                 "goods_details.goods_prices as price," \
                 "goods_details.goods_num as stock," \
                 "jd_cart.c_goods_num as productNum " \
                 "from (((goods_details join jd_cart on goods_details.goods_id = jd_cart.c_goods_id) " \
                 "join jd_shopper on jd_cart.c_shopper_id = jd_shopper.m_id) " \
                 "join goods_sku on goods_sku.goods_id = goods_details.goods_id)" \
                 "join jd_user on jd_cart.c_user_id = jd_user.user_id " \
                 "where jd_user.user_id ='{}' and goods_details.goods_state = 1".format(userid)

        plist_sql = "select goods_img as img," \
                    "goods_id as productID," \
                    "goods_name as title," \
                    "goods_prices as price " \
                    "from goods_details " \
                    "where goods_state =1 limit 0,20"

        plist = CartDao().query(plist_sql)
        cartmsg = CartDao().query(cart_sql)
        print(cartmsg)
        list1 = []

        list2 = []
        if not cartmsg:
            return jsonify({
            'code': 200,
            'msg': '购物车还是空的，先去添加点商品吧！！！',
            'cartShopList': list2,
            'ProuductList': plist,
            'checked': False
            })
        for c in cartmsg:
            c['checked'] = False
            if c['shopID'] not in list1:
                list1.append(c['shopID'])

        for t in list1:
            list3 = []
            dict1 = {}
            for cmsg in cartmsg:
                c = cmsg['shopID']
                if t==c:
                    dict1['shopID'] = t
                    dict1['shopName'] = cmsg['shopName']
                    dict1['checked'] = False
                    list3.append(cmsg)
            dict1['productList'] = list3
            list2.append(dict1)

        for l in list2:
             for p in l['productList']:
                 p.pop('stock')
                 p.pop('shopID')
                 p.pop('shopName')

        for price in cartmsg:
            price['price'] = str(price['price'])

        return jsonify({
            'code': 200,
            'msg': '购物车商品列表',
            'cartShopList':list2,
            'ProuductList':plist,
            'checked':False
        })

    else:
        return jsonify({
            'code': 401,
            'msg': '用户未登录',
        })

@cart_blue.route('/cart/updata/', methods=('POST',))
def updata_cart():
    cart_data = eval(request.get_data())
    token = cart_data['token']

    if token is None:
        return jsonify({
            'code': 400,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })

    if cache.check_token(token):
        goods_id = cart_data['productID']
        c_goods_num = cart_data['productNum']

        if not all((goods_id,c_goods_num)) or int(c_goods_num) < 0:
            return jsonify({
                'code': 400,
                'msg': '请求中的商品ID、数量获取失败'
            })

        else:
            goodsid_islive_sql="select count(*) as c, goods_num as stock from goods_details " \
                               "where goods_state =1 and goods_id = %s"%(int(goods_id))
            carthas_sql = "select count(*) as cart_count from jd_cart " \
                                 "where  c_goods_id = %s" % (int(goods_id))
            goodsnum_sql = "select c_goods_num as goodsnum from jd_cart " \
            "where  c_goods_id = %s" % (int(goods_id))
            shopid_sql = "select m_id_id as c_shopper_id from goods_details " \
                         "where goods_id = %s"%(int(goods_id))
            user_id = cache.get_token_user_id(token)
            userid_sql = "select user_id as c_goods_id from jd_user where user_id='{}'".format(user_id)


            goodsid_islive =CartDao().query(goodsid_islive_sql)
            carthas = CartDao().query(carthas_sql)
            goodsnum = CartDao().query(goodsnum_sql)
            shopid = CartDao().query(shopid_sql)
            userid = CartDao().query(userid_sql)

            if goodsid_islive[0]['c'] == 0:
                return jsonify({
                    "code": 404,
                    'msg': '该商品不存在'
                })
            else:
                if carthas[0]['cart_count'] == 0:
                    if int(c_goods_num) <= goodsid_islive[0]['stock']:
                        cart_dict = {}
                        cart_dict['c_goods_num'] = int(c_goods_num)
                        cart_dict['c_goods_id'] = int(goods_id)
                        cart_dict['c_freight'] = 10
                        cart_dict['c_shopper_id'] = shopid[0]['c_shopper_id']
                        cart_dict['c_user_id'] = userid[0]['c_goods_id']
                        CartDao().save('jd_cart',**cart_dict)
                        return jsonify({
                            "code": 200,
                            'msg': '新增商品到购物车'
                        })
                    else:
                        return jsonify({
                            "code": 404,
                            'msg': '库存不足，新增商品失败'
                        })
                else:
                    if goodsnum[0]['goodsnum'] > int(c_goods_num):
                        productnum = CartDao().update('jd_cart','c_goods_num',
                                                       c_goods_num,'c_goods_id',goods_id)
                        return jsonify({
                            "code": 200,
                            'msg': '该商品数量减少为%s'%int(c_goods_num),
                            'productNum':productnum
                        })
                    elif goodsnum[0]['goodsnum'] < int(c_goods_num) and int (c_goods_num) <= goodsid_islive[0]['stock']:
                        productnum = CartDao().update('jd_cart', 'c_goods_num',
                                                     c_goods_num, 'c_goods_id', goods_id)
                        return jsonify({
                            "code": 200,
                            'msg': '该商品数量增加到%s'%int(c_goods_num),
                            'productNum': productnum
                        })
                    elif int(c_goods_num) > goodsid_islive[0]['stock']:
                        return jsonify({
                            "code": 404,
                            'msg': '库存不足'
                        })
                    else:
                        return jsonify({
                            "code": 200,
                            'msg': '该商品数量未改变'
                        })

    else:
        return jsonify({
            'code': 401,
            'msg': '用户未登录',
        })




@cart_blue.route('/cart/delete/', methods=('POST',))
def del_cart():
    cart_data = eval(request.get_data())
    token = cart_data['token']

    if token is None:
        return jsonify({
            'code': 400,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })

    if cache.check_token(token):
        goods_id = cart_data['productID']
        dellist = goods_id.strip('[').strip(']').split(',')

        if dellist:
            is_live = True
            for goodid in dellist:
                goodsid_islive_sql = "select count(*) as c from goods_details " \
                                     "where goods_state =1 and goods_id = %s" % (int(goodid))
                carthas_sql = "select count(*) as cart_count from jd_cart " \
                              "where  c_goods_id = %s" % (int(goodid))

                goodsid_islive = CartDao().query(goodsid_islive_sql)
                carthas = CartDao().query(carthas_sql)

                if goodsid_islive[0]['c'] == 0:
                    is_live = False
                else:
                    if carthas[0]['cart_count'] == 0:
                        is_live = False
                    else:
                        CartDao().delete('jd_cart','c_goods_id',int(goodid))
            if is_live:
                return jsonify({
                    "code": 200,
                    'msg': '商品删除成功'
                })
            else:
                return jsonify({
                    "code": 404,
                    'msg': '商品不存在或不在购物车中'
                })

        else:
            return jsonify({
                "code": 400,
                'msg': '未获取到商品ID'
            })

    else:
        return jsonify({
            'code': 401,
            'msg': '用户未登录',
        })





