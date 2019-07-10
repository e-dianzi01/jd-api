import random

from flask import Blueprint, request
from flask import jsonify

from dao.goods_dao1 import GoodsDao

blue1 = Blueprint('show_index_api', __name__)

@blue1.route('/', methods=("GET",))
@blue1.route('/index/', methods=("GET",))
def show_index():
    # 获取首页的轮播商品的信息 8
    dao = GoodsDao()
    index_sql = "select img_urls from slideshow WHERE page_name='首页'"
    banner = dao.query(index_sql)

    # 获取广告图
    ad_sql = "select img_urls from slideshow WHERE page_name='首页广告图'"
    ad = dao.query(ad_sql)

    # 获取首页分类信息
    indexClassify_sql = "select img_urls as img,page_text as text from nav WHERE page_name='首页导航'"
    indexClassify = dao.query(indexClassify_sql)
    #
    # # 获取秒杀商品信息 10
    # seckill_goods_sql = "SELECT gd.good_img as img,gd.kill_prices as seckillPrice,gd.goods_prices as originalPrice" \
    #                     " FROM goods_seckill as gs JOIN goods_details as gd ON gs.goods_id_id= gd.id  " \
    #                     " WHERE kill_prices>0"
    # seckill_goods = dao.query(seckill_goods_sql)

    # yard 查询二级分类表
    # yard_sql = "SELECT one_category_id,page_name,remark,img_urls FROM goods_rec "
    yard_sql = "SELECT two_type_name as contentTitle ,type_img,remark as contentDescribe FROM goods_type2 WHERE " \
               "two_type_id=0"
    yard_content = dao.query(yard_sql)
    contentbottom = {"contentbottom": yard_content[2:6]}
    yard = {

        "contenttop": [{
            "contentTitle": yard_content[0]['contentTitle'],
            "contentDescribe": yard_content[0]['contentDescribe'],
            "imgs": (yard_content[0]['type_img']).split("#")
        }, {
            "contentTitle": yard_content[1]['contentTitle'],
            "contentDescribe": yard_content[1]['contentDescribe'],
            "imgs": (yard_content[1]['type_img']).split("#")
        }],
        **contentbottom

    }

    # print("yard_content",yard_content)

    # 获取首页商品信息 20条
    product_list_sql = "select goods_img as img,goods_name as title,goods_prices as price,two_category_id as " \
                       "productType,goods_id as productID from goods_details order by goods_id desc limit 0,20"
    product_list = dao.query(product_list_sql)

    # news 返回新闻列表5条
    news = ["百搭短袖T恤男，彰显潮流品味生活",
            "生活东奔西走需要来杯好酒助助力",
            "心俱疲的时候可以追追剧读读书",
            "华为Mate X：麒麟985+巴龙5000+5G", ]
    data = {
        "banner": [item['img_urls'] for item in banner],
        "ad": (ad[0])['img_urls'],
        "indexClassify": [indexClassify[0:10], indexClassify[10:]],
        # "seckill":{"time":"time时间","seckillContext":seckill_goods},
        "yard": yard,
        "news": news,
        # "footprint":"",
        "product_list": product_list
    }

    return jsonify({
        **data
    })


# 家电
@blue1.route('/index/appliance/')
def appliance():
    dao = GoodsDao()
    # 家电首页轮播图 获取8个URL
    apl_banner_sql = "select img_urls from slideshow WHERE page_name='家电轮播'"
    banner = dao.query(apl_banner_sql)

    # 猜你喜欢 获取三组数据 img_url   price  这里是随机取的三条
    guessLike_sql = "select goods_img as img, goods_prices as price ,goods_id as productID from goods_details " \
                    "limit 0,10"
    guessLike = dao.query(guessLike_sql)

    # 家电分类   取5个分类

    aplCls_sql = "select type_img as img,two_type_name as title,two_type_id as productType from goods_type2 where " \
                 "remark ='applianceClassify'  limit 0,5"
    aplCls = dao.query(aplCls_sql)
    print("applianceClassify", aplCls)
    # "welfare(福利社)": 两组数据
    #  url:
    welfare_sql = "SELECT two_type_name AS title,remark as describes,type_img as img  FROM  " \
                  "goods_type2 where two_type_id =101 "
    welfare = dao.query(welfare_sql)

    # ad:url 一张广告图
    ad_sql = "select img_urls from nav WHERE page_name='家电首页广告'"
    ad = dao.query(ad_sql)

    # brand  三组数据{大牌特惠，大牌上新，热门好店} title url
    brand_sql = "SELECT two_type_name AS title,remark as describes,type_img as img  FROM  goods_type2 where" \
                " two_type_id =102 "
    brand = dao.query(brand_sql)

    # weekHot 3类 每类10条

    weekHot_sql = "select goods_img as img,goods_name as describes,goods_prices,goods_id as productID,goods_prices" \
                  " as price from goods_details WHERE " \
                  "label='热销' limit 0,15"

    weekHot = dao.query(weekHot_sql)
    if len(weekHot) > 14:
        data = {
            "weekHot": weekHot[0:5],
            "peopleTop": weekHot[5:10],
            "greatRecommend": weekHot[10:],
        }
    else:
        print("")

    # television 五十条数据根据类型各返回十条  类型属于家电的商品 类型：电视，空调，冰箱，洗衣机，厨卫大电
    # 电视
    tele_sql1 = "SELECT gd.two_category_id AS TYPE,gd.goods_img AS img,gd.goods_name AS describes,gd.kill_prices AS " \
                "originalPrice,gd.goods_prices AS seckillPrice,gd.goods_id AS productID FROM goods_type2 AS gt2 JOIN " \
                "goods_details gd ON gd.two_category_id = gt2.two_type_id where gt2.remark = '电视' LIMIT 0,100"

    # 空调
    tele_sql2 = "SELECT gd.two_category_id AS TYPE,gd.goods_img AS img,gd.goods_name AS describes,gd.kill_prices AS " \
                "originalPrice,gd.goods_prices AS seckillPrice,gd.goods_id AS productID FROM goods_type2 AS gt2 JOIN " \
                "goods_details gd ON gd.two_category_id = gt2.two_type_id where gt2.remark = '空调' LIMIT 0,100"

    # 冰箱
    tele_sql3 = "SELECT gd.two_category_id AS TYPE,gd.goods_img AS img,gd.goods_name AS describes,gd.kill_prices AS " \
                "originalPrice,gd.goods_prices AS seckillPrice,gd.goods_id AS productID FROM goods_type2 AS gt2 JOIN " \
                "goods_details gd ON gd.two_category_id = gt2.two_type_id where gt2.remark = '冰箱' LIMIT 0,100"
    # 洗衣机
    tele_sql4 = "SELECT gd.two_category_id AS TYPE,gd.goods_img AS img,gd.goods_name AS describes,gd.kill_prices AS " \
                "originalPrice,gd.goods_prices AS seckillPrice,gd.goods_id AS productID FROM goods_type2 AS gt2 JOIN " \
                "goods_details gd ON gd.two_category_id = gt2.two_type_id where gt2.remark = '洗衣机' LIMIT 0,100"
    # 厨卫大电
    tele_sql5 = "SELECT gd.two_category_id AS TYPE,gd.goods_img AS img,gd.goods_name AS describes,gd.kill_prices AS " \
                "originalPrice,gd.goods_prices AS seckillPrice,gd.goods_id AS productID FROM goods_type2 AS gt2 JOIN " \
                "goods_details gd ON gd.two_category_id = gt2.two_type_id where gt2.remark = '厨房小电' LIMIT 0,100"

    television = dao.query(tele_sql1)
    airConditioner = dao.query(tele_sql2)
    refrigerator = dao.query(tele_sql3)
    washingMachine = dao.query(tele_sql4)
    kitchen = dao.query(tele_sql5)

    return jsonify({
        "banner": [item['img_urls'] for item in banner],
        "guessLike": random.sample(guessLike, 3),
        "applianceClassify": aplCls,
        "welfare": welfare,
        # "ad": ad,
        "brand": brand,
        **data,
        "television": random.sample(television, 10),
        "airConditioner": random.sample(airConditioner, 10),
        "refrigerator": random.sample(refrigerator, 10),
        "washingMachine": random.sample(washingMachine, 10),
        "kitchen": random.sample(kitchen, 10)

    })


# 轮播图商品、猜你喜欢
@blue1.route('/index/appliance/detail/<int:productID>/', methods=["GET"])
def appliance_detail(productID):
    dao = GoodsDao()
    # 通过id获取商品详情
    sql = "SELECT  gd.goods_img AS img,gd.goods_name AS productName,gi.img_urls AS img_details ,gd.goods_prices" \
          " AS price FROM goods_details AS gd JOIN goods_imgs AS gi ON gd.goods_id = gi.goods_id_id" \
          " where gd.goods_id =%s" % productID
    g_details = dao.query(sql)
    # a = str([item["img_details"].split("#") for item in g_details])
    # print(a)
    return jsonify({
        "g_details": g_details

    })


# 商品列表、福利社、今日大牌、大牌特惠、本周热卖等
@blue1.route('/index/appliance/<int:productListID>/')
def productList(productListID):
    dao = GoodsDao()
    sql = "select goods_id as productID,goods_img AS img, goods_name  AS productName,goods_prices as price from " \
          "goods_details WHERE two_category_id = %s  ORDER BY goods_id desc limit 0,10" % productListID
    goods_list = dao.query(sql)
    # print(random.sample(goods_list, 1))

    return jsonify({
        "productList": goods_list
    })


#
# # 推荐
# @blue1.route('/index/appliance/advise/')
# def advise():
#     dao = GoodsDao()
#     # 随机推荐商品
#     sql = "select goods_id as productID,goods_img AS img, goods_name  AS productName,goods_prices as price " \
#           "from goods_details where label ='推荐商品' ORDER BY goods_id desc limit 0,10"
#     rec = dao.query(sql)
#     return jsonify({
#          "rec":rec
#
#     })


# 拍卖
@blue1.route('/index/auction/')
def auction():
    dao = GoodsDao()
    # 获取拍卖商品
    sql1 = "SELECT gd.goods_id AS auctionID ,gd.goods_img AS img,gd.goods_name AS title ,ga.clickcount AS clickCount" \
           " FROM goods_details AS gd JOIN  goods_auction AS ga ON gd.goods_id = ga.goods_id_id " \
           " AND ga.describe = '已开始'"
    auction = dao.query(sql1)

    # 获取预告商品
    sql2 = "SELECT gd.goods_id AS auctionID ,gd.goods_img AS img,gd.goods_name AS title ,ga.clickcount AS clickCount" \
           " FROM goods_details AS gd JOIN  goods_auction AS ga ON gd.goods_id = ga.goods_id_id  AND ga.describe = '预告'"
    auctionPrediction = dao.query(sql2)

    return jsonify({
        "auction": auction,
        "auctionPrediction": auctionPrediction

    })


# 拍拍
@blue1.route('/index/patPat/')
def patpat():
    dao = GoodsDao()
    # 拍拍首页轮播图 获取4个URL
    apl_banner_sql = "select img_urls from slideshow WHERE page_name='拍拍'"
    banner = dao.query(apl_banner_sql)
    #
    # # 拍拍首页顶部导航 4 个
    # navigation_sql = "select img_urls as img,page_text as text from nav WHERE page_name='拍拍顶部导航' " \
    #                  "ORDER BY id desc limit 0,4"
    # top_navigation = dao.query(navigation_sql)

    # 猜你喜欢 4个对象
    like_sql = "select goods_img as img,goods_name as describes,goods_prices as price,goods_id as productID " \
               "from goods_details where label='猜你喜欢' "
    likeintroduce = dao.query(like_sql)

    # 闲置卖钱 3个对象 查询二级分类表 给一个 分类：手机回收，笔记本回收，旧衣回收
    # Spare_money_sql = "select img_urls as img,id as productID from goods_details ORDER BY id desc limit 0,3 "
    # Spare_money_sql = "select type_img as img from goods_type2 ORDER BY id desc limit 0,3 "
    # Spare_money = dao.query(Spare_money_sql)

    # 拍拍专享  拍拍自营#排行榜单#Apple专区
    exclusive_sql = "select img_urls as img from slideshow where page_name='拍拍专享' "
    exclusive = dao.query(exclusive_sql)
    # 专属推荐
    brilliant_sql = "select goods_img as img,goods_name as describes,goods_prices as price,goods_id as productID " \
                    "from goods_details where label='专属推荐' "
    brilliant = dao.query(brilliant_sql)

    return jsonify({
        "banner": [item['img_urls'] for item in banner],
        "likeintroduce": likeintroduce,
        # "Spare_money": Spare_money,
        "exclusive": [item['img'] for item in exclusive],
        "brilliant": brilliant

    })


# 充值
@blue1.route('/index/payCost/', methods=["GET", ])
def payCost():
    dao = GoodsDao()
    # 充话费
    telphone_sql = "select goods_name,goods_prices as price from goods_details where two_category_id='3' "
    telphone = dao.query(telphone_sql)
    # 充流量
    flow_sql = "select goods_name,goods_prices as price from  goods_details where two_category_id= '4'"
    flow = dao.query(flow_sql)
    # print("telphone", telphone)
    # print("flow", flow)

    return jsonify({
        "payCostAmountList": [telphone, flow],
    })


# 充话费
@blue1.route('/index/payCost/add/', methods=('POST',))
def payCost_phone():
    dao = GoodsDao()
    if request.method == "POST":
        tel = request.get_json().get("tel", None)
        money = request.get_json().get('money', None)
        token = request.get_json().get('token', None)
        # print(tel, money, token)

    return jsonify({

    })


# 充流量
@blue1.route('/index/payCost/traffic/add/', methods=["GET", "POST"])
def payCost_flow():
    dao = GoodsDao()
    if request.method == "POST":
        tel = request.get_json().get("tel", None)
        money = request.get_json().get('money', None)
        token = request.get_json().get('token', None)
        # print(tel, money, token)

    return jsonify({

    })


# 领券
@blue1.route('/index/vouchers/', methods=["GET", "POST"])
def neck_vouchers():
    dao = GoodsDao()
    # 获取15个优惠券
    led_sql = "select minusprice as vouchersUseCondition,vuc as minusPrice,title,id as vouchersID,user_id from " \
              "jd_coupon  ORDER BY id desc limit 0,15"
    led = dao.query(led_sql)

    # 获取我的优惠券

    return jsonify({
        "ledList": led
    })


# 薅羊毛
@blue1.route('/index/wool/')
def wool():
    dao = GoodsDao()
    # # 顶部图
    # banner_sql = "select img_urls as img from slideshow WHERE page_name='薅羊毛顶部图'"
    # banner = dao.query(banner_sql)
    #
    # # 领券中心 5个对象
    # vouchers_sql = "select img_urls as img from slideshow WHERE page_name='领券中心图片' ORDER BY id desc"
    # vouchers = dao.query(vouchers_sql)
    #
    # # 导航 2个对象
    # wool_index_sql = "select img_urls as img from nav WHERE page_name='薅羊毛导航'"
    # wool = dao.query(wool_index_sql)

    # 今日爆品 6个对象

    woolProduct_sql = "select goods_id as productID,goods_img as img,goods_name as title,goods_prices as oldPrice," \
                      "evaluate as evaluate,kill_prices as price,rate as evaluateRate  from goods_details where" \
                      " label ='今日爆品' ORDER BY goods_id desc limit 0,6"
    woolProduct = dao.query(woolProduct_sql)
    return jsonify({
        "woolProduct": woolProduct
    })
