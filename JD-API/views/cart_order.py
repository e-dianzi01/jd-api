from flask import Blueprint, request, jsonify
import datetime
from dao.cart_order import cart_orderDao
from dao.order_dao import OrderDao
from dao.user_dao import UserDao
from libs import cache, rd
from libs.crypt import make_password
from services.order import get_order_num

cart_order_blue = Blueprint('cart_order_blue', __name__)


@cart_order_blue.route('/cart/paycart/', methods=('POST', ))
def paycart():
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        user_id_id = cache.get_token_user_id(token)
        req_data = request.get_json()

        goods_list = req_data["goodsList"]

        dao = cart_orderDao()
        #存储所有商品信息
        cart_orderlist = []
        #存储库存不足商品信息
        unable_list = []
        #存储请求成功后返回的商品信息
        cat_goodslist = []
        #遍历商品列表，校验库存
        print(goods_list[0],len(goods_list),'AAAAAAAA')
        for i in range(0,len(goods_list)):
            print(goods_list[i],"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
            for key, val in goods_list[i].items():
                goods_id = key
                goods_cart_num = val
                #查询商品详细数据
                resp = dao.check_stock(user_id_id,goods_id)
                if not resp:
                    return jsonify({
                                  "code": 400,
                                  "msg":"商品不存在",
                                  "productID":goods_id
                    })
                cart_orderlist.append(resp[0])
                shopID = cart_orderlist[i]['m_id_id']
                shop_name = dao.get_shopname(shopID)["m_username"]
                standard = dao.get_std(goods_id)['properties']
                cat_goodslist.append({"shopname":shop_name,"productID":goods_id,
                                       "productstock":resp[0]['goods_num'],"productnum":goods_cart_num,
                                      "productprice":resp[0]['goods_prices'],"productpic":resp[0]['goods_img'],
                                      "title": resp[0]['goods_name'], "standard":standard
                                      })
                if goods_cart_num >= resp[0]['goods_num']:
                    unable_list.append({"productID":goods_id,"productstock":resp[0]['goods_num']})
        if len(unable_list)>0:
            return jsonify({
                "code": 400,
                "msg":"商品库存不足，请减少购买数量或改天再来",
                "goodslist":unable_list
            })
        cart_cal_num = 0
        for i in range(len(goods_list)):
            for key, val in goods_list[i].items():
                goods_id = key
                goods_cart_num = val
                goods_cal_price = cart_orderlist[i]['goods_prices']
                cart_cal_num += goods_cart_num * goods_cal_price
        # 查询地址，返回默认地址
        address = dao.get_addr(user_id_id)
        # voulist = dao.get_vou_list(user_id_id)
        tel = dao.get_tel(user_id_id)['tel']
        data = {
            "tel":tel,
            # "voulist":voulist,
            "address":address,
            "goodslist": cat_goodslist,
            "total":cart_cal_num
        }
        return jsonify({
            'code': 200,
            'msg': '购物车结算请求成功',
            'data':data
        })

    else:
        return jsonify({
            'code': 400,
            'msg': '您还未登陆，请先登录'
        })




@cart_order_blue.route('/cart/crtord/', methods=('POST', ))
def create_order():
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        #获取请求参数
        user_id_id = cache.get_token_user_id(token)
        req_data = request.get_json()
        print(req_data, type(req_data))
        goods_list = req_data["goodsList"]
        print(goods_list)
        dao = cart_orderDao()
        cart_orderlist = []
        unable_list = []
        for i in range(len(goods_list)):

            for key, val in goods_list[i][0].items():
                goods_id = key
                goods_cart_num = val
            #查询商品详情表
                resp = dao.check_stock(user_id_id, goods_id)
                cart_orderlist.append(resp[0])
                if goods_cart_num >= resp[0]['goods_num']:
                    unable_list.append({"productID": goods_id, "productstock": resp[0]['goods_num']})
        if len(unable_list) > 0:
            return jsonify({
                "code": 400,
                "msg": "商品库存不足，请减少购买数量或改天再来",
                "goodslist": unable_list
            })
        addr = request.get_json().get('addr', None)
        o_conn = request.get_json().get('tel',None)

        if not all((addr,o_conn)):
            return jsonify({
                "code": 400,
                "msg": "地址和电话不能为空"
            })
        cart_cal_num = 0
        cart_cal_rel = 0

        #创建字典，用于存放各个店铺的总价
        cart_shop_dict = {}
        for i in range(len(goods_list)):
            shopID = cart_orderlist[i]['m_id_id']
            #获取商品数量和ID
            for key, val in goods_list[i][0].items():
                goods_id = key
                goods_cart_num = val

                goods_cal_price = cart_orderlist[i]['goods_prices']
                cart_cal_num += goods_cart_num * goods_cal_price
                if shopID in cart_shop_dict:
                    cart_shop_dict[shopID][0] += goods_cart_num * goods_cal_price
                else:
                    cart_shop_dict[shopID] = [goods_cart_num * goods_cal_price]

                cart_shop_dict[shopID].append([goods_id, goods_cart_num,goods_cal_price])

        #优惠券ID
        cart_cal_rel = cart_cal_num
        voucher_id = request.get_json().get('voucher_id', None)
        vou_resp = dao.check_vou(user_id_id,voucher_id)
        if vou_resp:
            if vou_resp[0]['vuc'] == 0:
                vou_price = vou_resp[0]['minusprice']
                cart_cal_rel = cart_cal_num - vou_price

            if vou_resp[0]['vuc'] == 1:
                vou_price = vou_resp[0]['minusprice']
                if cart_cal_num > 200 and cart_cal_num < 500:
                    cart_cal_rel = cart_cal_num - vou_price
                elif cart_cal_num>500 and cart_cal_num < 1000:
                    cart_cal_rel = cart_cal_num - vou_price
                elif cart_cal_num>1000:
                    cart_cal_rel = cart_cal_num - vou_price

        #将订单写入数据库
        order_list = []
        dict1 = {}
        print(cart_shop_dict,33333333333)
        for key in cart_shop_dict.keys():
            o_num = get_order_num()
            order_list.append(o_num)
            cart_shop_dict[key].append(o_num)
            tel = dao.get_tel(user_id_id)["tel"]
            dict1 = {
                "o_num": o_num,
                "o_addr": addr,
                "o_conn": tel,
                "o_time": datetime.datetime.now(),
                "o_status": 0,
                "o_total": cart_shop_dict[key][0],
                "o_relpay": cart_shop_dict[key][0],
                "o_shopper_id": key,
                "o_user_id": user_id_id
            }
            print(dict1)
            dao.save_detail(**dict1)
            for i in range(1,len(cart_shop_dict[key])-1):
                goods_id = cart_shop_dict[key][i][0]
                goods_cart_num = cart_shop_dict[key][i][1]
                dao.update(user_id_id,goods_id,goods_cart_num)
                dao.delete_tab("jd_cart",goods_id,user_id_id)
                dict2 = {
                    "g_num": goods_cart_num,
                    "g_price": cart_shop_dict[key][i][2],
                    "o_goods_id":goods_id,
                    "o_num_id":o_num
                }
                dao.save(**dict2)
                print(dict2,"1"*i+"1")
        rd.rpush(order_list[0],order_list)
        rd.expire(cart_cal_rel,2*60*60)
        # dao.delete_vou(user_id_id, voucher_id)
        data = {
            "order_list":order_list,
            "total":cart_cal_rel
        }
        return jsonify({
            'code': 200,
            'msg': '订单生成成功',
            'data': data
        })

    else:
        return jsonify({
            'code': 400,
            'msg': '您还未登陆，请先登录'
        })


@cart_order_blue.route('/cart/payord/', methods=('POST', ))
def payorder():
    token = request.get_json().get('token', None)
    if cache.check_token(token):
        user_id_id = cache.get_token_user_id(token)
        order_list = request.get_json().get("order_list")
        total = request.get_json().get("total")
        paypassword = request.get_json().get("paypassword")
        dao2 = OrderDao()
        if all((order_list,total)):
            order_rd_list = rd.lindex(order_list[0],0)
            if not order_rd_list:
                #删除订单
                for i in range(len(order_list)):
                    dao2.UpdateOrder(user_id_id, 5, order_list[i])
                return jsonify({
                    'code': 404,
                    'msg': '订单已过期'
                })
            order_rd_list = order_rd_list.decode()[1:-1]
            order_rd_list = order_rd_list.split("'")

            for i in range(len(order_list)):
                print(order_list[i], order_rd_list[i*2+1])
                if order_list[i] != order_rd_list[i*2+1]:
                    return jsonify({
                        'code': 400,
                        'msg': '支付请求出错'
                    })
            dao = UserDao()
            user_info = dao.get_profile(user_id_id)[0]
            asset = user_info['asset']
            pay_pwd = user_info['pay_pwd']
            # paypassword = make_password(paypassword)
            if pay_pwd != paypassword:
                return jsonify({
                            'code': 400,
                            'msg': '支付密码错误，请重新输入'
                        })
            if asset< total:
                return jsonify({
                        'code': 400,
                        'msg': '余额不足，请先充值'
                    })

            asset -= total
            dao.update_asset(user_id_id,asset)

            for i in range(len(order_list)):
                dao2.UpdateOrder(user_id_id,1,order_list[i])

            return jsonify({
                        'code': 200,
                        'msg': '支付成功'
                    })
        else:
            o_num = request.get_json().get("orderid")
            dao3 = UserDao()
            dao4 = OrderDao()
            order_info = dao4.get_oreder_info(o_num)
            if not order_info:
                return jsonify({
                   "code":401,
                    "msg":"订单不存在"
                })
            order_info = order_info[0]
            total1 = order_info['o_relpay']
            user_info = dao3.get_profile(user_id_id)
            asset = user_info['asset']
            pay_pwd = user_info['pay_pwd']
            if pay_pwd != paypassword:
                return jsonify({
                    'code': 400,
                    'msg': '支付密码错误，请重新输入'
                })
            if asset < total1:
                return jsonify({
                    'code': 400,
                    'msg': '余额不足，请先充值'
                })

            asset -= total1
            dao3.update_asset(user_id_id, asset)
            dao4.UpdateOrder(user_id_id, 1, o_num)
            return jsonify({
                'code': 200,
                'msg': '支付成功'
            })


    else:
        return jsonify({
            'code': 400,
            'msg': '您还未登陆，请先登录'
        })
