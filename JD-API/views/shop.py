from flask import Blueprint, jsonify

from dao.goods_dao import GoodsDao

blue_shop = Blueprint('shop_api', __name__)


# 进入商铺
@blue_shop.route('/shop/shopIndex/<int:shopid>/')
def shop(shopid):
    dao = GoodsDao()
    # 获取 shopid ,img, tit(店铺名字） coolect
    shop_sql = "select m_id,m_img as img,m_name as tit,clt as collect from jd_shopper where m_id=%s" % shopid
    shop_info = dao.query(shop_sql)

    # 获取商铺轮播图
    banner_sql = "select img from  shopper_img where remark='首页轮播图' and m_id_id = %s" % shopid
    banner = dao.query(banner_sql)

    # 获取主页推荐图
    rec_img_sql = "select img from  shopper_img where remark='推荐' and m_id_id = %s" % shopid
    imgs = dao.query(rec_img_sql)

    # 获取5个商品id
    product_sql = "select goods_id as productID from " \
                  "goods_details where m_id_id=%s limit 0,5" % shopid
    product_id = dao.query(product_sql)

    # 获取商品列表10
    product_sql = "select goods_id as productID,goods_img as img,goods_name as tit,goods_prices as pic,evaluate,rate" \
                  " from goods_details where  label !='拍卖'  and  m_id_id=%s limit 0,10 " % shopid
    productList = dao.query(product_sql)
    if len(shop_info)>0:
        shop_info = {
            "shopID": shopid,
            "header": {
                "img": shop_info[0]['img'],
                "tit": shop_info[0]['tit'],
                "collect": shop_info[0]['collect']
            },
        }
        imgs1 = (imgs[0]['img'].split("#"))[0:2]
        # print("imgs1",imgs1)
        imgs2 = (imgs[0]['img'].split("#"))[2:3]
        # print("imgs2", imgs2)

    else:
        print("为获取到数据")
    banner = banner[0]['img'].split("#")
    productModel = {
        "img": imgs2,
        "productIDList": [i['productID'] for i in product_id],
    }
    return jsonify({
        **shop_info,
        "banner": banner,
        "imgs": imgs1,
        "productModel": productModel,
        "roductList": productList

    })


# 商铺 ----分类
@blue_shop.route('/shop/<int:shopid>/classify/')
def shop_classify(shopid):
    dao = GoodsDao()

    # 获取顶部图
    shop_sql = "select m_id,m_img as img,m_name as tit,clt as collect from jd_shopper where m_id=%s" % shopid
    shop_info = dao.query(shop_sql)
    shop_info = {
        "shopID": shopid,
        "header": {
            "img": shop_info[0]['img'],
            "tit": shop_info[0]['tit'],
            "collect": shop_info[0]['collect']
        },
    }

    # 获取商铺分类导航
    left_sql = "select type_name from shopper_type where m_id_id = %s" % shopid
    left = dao.query(left_sql)
    left_info = [item['type_name'].split("#") for item in left]
    print(len(left_info), left_info)
    if len(left_info) > 0:
        left = left_info[0]
    else:
        print("暂无数据")
    # 商品分类
    goods_detils = []

    for g_type in left:
        items = {}
        sql = "SELECT gd.goods_id AS productID,gd.goods_img AS img,gd.goods_name AS text,gd.goods_prices AS price," \
              "gd.evaluate AS evaluate,gd.rate AS evaluateRate FROM jd_shopper AS js JOIN goods_details AS gd ON " \
              "js.m_id = gd.m_id_id  WHERE gd.label='{}' and gd.m_id_id = '{}' ".format(g_type, shopid)
        goods_type = dao.query(sql)
        items['text'] = g_type
        items['children'] = goods_type
        goods_detils.append(items)

    return jsonify({
        **shop_info,
        "items": goods_detils

    })


#  商铺 ----促销
@blue_shop.route('/shop/<int:shopid>/pomotion/')
def pomotion_product(shopid):
    dao = GoodsDao()
    product_sql = "select goods_id as productID,goods_img as img,goods_name as title,goods_prices as oldPrice," \
                  "kill_prices as price from goods_details where m_id_id='{}' and label='热销' limit 0,15".format(shopid)
    productList = dao.query(product_sql)

    # 顶部图
    shop_sql = "select m_id,m_img as img,m_name as tit,clt as collect from jd_shopper where m_id=%s" % shopid
    shop_info = dao.query(shop_sql)
    shop_info = {
        "shopID": shopid,
        "header": {
            "img": shop_info[0]['img'],
            "tit": shop_info[0]['tit'],
            "collect": shop_info[0]['collect']
        },
    }
    return jsonify({
        **shop_info,
        "productList": productList
    })


#  商铺 ----所有商品
@blue_shop.route('/shop/<int:shopid>/all/')
def product_all(shopid):
    dao = GoodsDao()
    product_sql = "select goods_id as productID,goods_img as img,goods_name as tit,goods_prices as pic,evaluate " \
                  "as evaluate,rate as rate  from goods_details where label !='拍卖' AND m_id_id='{}' ORDER by " \
                  "goods_id desc ".format(
        shopid)
    productList = dao.query(product_sql)

    # 获取顶部图
    shop_sql = "select m_id,m_img as img,m_name as tit,clt as collect from jd_shopper where m_id=%s" % shopid
    shop_info = dao.query(shop_sql)
    shop_info = {
        "shopID": shopid,
        "header": {
            "img": shop_info[0]['img'],
            "tit": shop_info[0]['tit'],
            "collect": shop_info[0]['collect']
        },
    }

    # 销量降序
    desc_sql = "select goods_id as productID,goods_img as img,goods_name as tit,goods_prices as pic,evaluate " \
               "as evaluate,rate as rate  from goods_details where  m_id_id='{}' ORDER by sales desc ".format(shopid)
    salesList = dao.query(desc_sql)

    # 价格升序
    price_sql = "select goods_id as productID,goods_img as img,goods_name as tit,goods_prices as pic,evaluate " \
                "as evaluate,rate as rate  from goods_details where  m_id_id='{}' ORDER by goods_prices asc ".format(
        shopid)
    priceList = dao.query(price_sql)

    return jsonify({
        **shop_info,
        "productList": productList,
        "salesList": salesList,
        "priceList": priceList,
    })
