from flask import Blueprint, jsonify,request
from dao.classify_dao import ClassifyDao
classify_blue = Blueprint('classify_blue', __name__)


@classify_blue.route('/classify/', methods=('GET', ))
def classify():
    #创建ClassifyDao对象
    cd = ClassifyDao()
    #查询
    left_sql = "select one_type_name,one_type_id from goods_type1 limit 0,15"
    left = cd.query(left_sql)
    cln = []
    list2 = []
    for c in left:
        cln.append(c['one_type_name'])
        print(c['one_type_id'],type(c['one_type_id']))
        sec_sql = "select remark,type_img as banner from goods_type1 " \
              "where one_type_id=%d"%(c['one_type_id'])
        secondmsg = cd.query(sec_sql)
        slist = secondmsg[0]['remark'].split('#')
        list1 = []
        dict1 = {}
        dict2 = {}

        for s in slist:
            dict1['title'] = s.split(':')[0]
            twotypeid = int(s.split(':')[1])
            gmsg_sql = "select type_img as img,two_type_id as productTypeID,two_type_name as text " \
                    "from goods_type2 where two_type_id=%d"%(twotypeid)
            gmsg = cd.query(gmsg_sql)

            dict1['rightSmall'] = gmsg
            list1.append(dict1)
            dict2['rightList'] = list1
        dict2['banner'] = secondmsg[0]['banner']
        list2.append(dict2)


    return jsonify({
        "code":200,
        'msg': '分类页',
        'left':cln,
        'right':list2
    })


@classify_blue.route('/classify/list/', methods=('GET', ))
def classifylist():
    cd = ClassifyDao()
    goodtypeid = request.args.get("productTypeID")

    goodslist_sql = "select goods_name,goods_img,goods_prices,goods_id,m_id_id " \
                      "from goods_details where two_category_id=%d limit 0,20"%(int(goodtypeid))
    goodslist = cd.query(goodslist_sql)

    list1 = []
    for i in goodslist:

         shopmsg_sql = "select m_id,m_name from jd_shopper where m_id=%d"%int(i['m_id_id'])
         shopmsg = cd.query(shopmsg_sql)
         comment_sql = "select count(*) as num from order_comment where goods_id_id=%d"%int(i['goods_id'])
         comment = cd.query(comment_sql)
         price = '%.2f'%i['goods_prices']
         price = str(price)


         dict1 ={}
         dict1['productID'] = i['goods_id']
         dict1['goodsdescribe'] = i['goods_name']
         dict1['img'] = i['goods_img']
         dict1['price'] = price
         dict1['shopID'] = shopmsg[0]['m_id']
         dict1['shopName'] = shopmsg[0]['m_name']
         dict1['evaluate'] = comment[0]['num']
         dict1['rateEvaluate'] = '98%'
         list1.append(dict1)
    return jsonify({
        "code": 200,
        'msg': '分类页商品列表',
        'productList':list1
    })