from flask import Blueprint
from flask import jsonify

from dao.goods_dao import GoodsDao

blue1 = Blueprint('show_index_api', __name__)


@blue1.route('/index/')
def show_index():
    # 获取首页的轮播商品的信息 8
    dao = GoodsDao()
    index_sql = "select img_urls from slideshow WHERE page_name='index_img'"
    banner = dao.query(index_sql)

    # 获取广告图
    ad_sql = "select img_urls from slideshow WHERE page_name='ad_img'"
    ad = dao.query(ad_sql)

    # 获取首页分类信息
    indexClassify_sql = "select page_text,img_urls from nav WHERE page_name='page_index'"
    indexClassify = dao.query(indexClassify_sql)
    print(indexClassify)

    # 获取秒杀商品信息 10
    seckill_goods_sql = "SELECT gd.good_img FROM goods_seckill as gs JOIN goods_details as gd ON " \
                    "gs.goods_id= gd.id  "
    seckill_goods = dao.query(seckill_goods_sql)

    # 获取首页商品信息 20条
    product_list_sql = "select good_img,goods_name,goods_prices,two_category_id,id from " \
                       "goods_details where id<10"
    product_list = dao.query(product_list_sql)


    return jsonify({
        "banner":[item['img_urls'] for item in banner],
        "ad":(ad[0])['img_urls'],
        "indexClassify":{"img":(indexClassify)},
        "seckill_goods":seckill_goods,
        "product_list": [item for item in product_list]



    })

# 家电
@blue1.route('/index/appliance/')
def appliance():
    return jsonify({
        "code":200,
        "msg":"请求成功"
    })

# 轮播图商品、猜你喜欢
@blue1.route('/index/appliance/detail/<int:id>')
def appliance_detail(id):
    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 商品列表、福利社、今日大牌、大牌特惠、本周热卖等
@blue1.route('/index/appliance/productListID/')
def productList(id):
    return jsonify({
        "code": 200,
        "msg": "ok"
    })
#
# 推荐
@blue1.route('/index/appliance/advise/')
def advise():
    return jsonify({
        "code": 200,
        "msg": "ok"
    })


# 拍卖
@blue1.route('/index/auction/')
def auction():

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 美妆首页
@blue1.route('/index/beautyMakeup/')
def beautyMakeup():
    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 彩妆
@blue1.route('/index/beautyMakeup/01')
def beautyMakeup01():
    return jsonify({
        "code": 200,
        "msg": "ok"
    })



