from flask import Blueprint, jsonify
from dao.goods_dao import GoodsDao
from dao.gb_dao import gbDao
groupbuy_blue = Blueprint('groupbuy_blue', __name__)


@groupbuy_blue.route('/groupBuy/', methods=('GET', ))
def groupbuy():
    dao = GoodsDao()
    bnr_sql = "select img_urls from slideshow where page_name='首页'"
    gb1 = gbDao().check(bnr_sql,3)
    bnr = []
    for g1 in gb1:
        bnr.append(g1['img_urls'])

    gBC_sql = "select img_urls as img,page_text as text from nav"
    gb2 = gbDao().check(gBC_sql,10)


    gBe_sql = "select goods_details.goods_img as img,group_buy.gbp as groupBuyPeople," \
              "group_buy.buy_price as groupBuyPrice,group_buy.gbn as groupBuyNum " \
              "from group_buy join goods_details " \
              "on group_buy.goods_id_id = goods_details.goods_id "
    gb3 = gbDao().check(gBe_sql,15)
    # n = 3
    # list3= [gb3[i:i + n] for i in range(0, len(gb3), n)]
    # dict3 = {}
    # list33 = []
    # dict3['banner'] = list3
    # list33.append(dict3)
    # print(list3)
    # print(gb3)

    gBE_sql = "SELECT goods_details.goods_img as img," \
              "goods_details.goods_name as goodsdescribe," \
              "group_buy.gbn as numberofpersons," \
              "group_buy.buy_price as price," \
              "goods_type2.two_type_name as productType," \
              "goods_details.goods_id as productID " \
              "FROM (group_buy JOIN goods_details " \
              "ON group_buy.goods_id_id = goods_details.goods_id)" \
              "JOIN goods_type2 ON goods_details.two_category_id = goods_type2.two_type_id"

    gb4 = gbDao().check(gBE_sql,10)
    return jsonify({
        "code":200,
        'msg': '拼购页',
        'banner':bnr,
        'grouyBuyClassify':gb2,
        'groupBuyeveryone':gb3,
        'groupBuyEveryone':gb4
    })

