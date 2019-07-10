from flask import Blueprint, jsonify,request
from dao.goodsdetails_dao import GoodsDetailsDao
from libs import cache

goodsdetails_blue = Blueprint('goodsdetails_blue', __name__)

@goodsdetails_blue.route('/detail/', methods=('GET','POST','OPTIONS' ))
def goodsdetails():
    gd = GoodsDetailsDao()
    goods_id = request.args.get('productID')
    token = request.args.get('token')

    address = "北京朝阳区三环到四环之间"
    if not token:
        address = "北京朝阳区三环到四环之间"
    else:
        if len(token) > 5 :
            user_id = cache.get_token_user_id(token)
            address_sql = "select u_address.user_address as address " \
                          "from u_address join jd_user " \
                          "where u_address.is_default =1 and jd_user.user_id ={}".format(user_id)
            address = gd.query(address_sql)[0]['address']

    goodimg_sql = "select img_urls from goods_imgs where goods_id_id = %d"%(int(goods_id))
    goodimg = gd.query(goodimg_sql)
    banner = goodimg[0]['img_urls'].split('#')

    goodmsg_sql = "select goods_prices as price,goods_name as title," \
                  "two_category_id as typeid,m_id_id as m_id " \
                  "from goods_details " \
                  "where goods_id = %d"%(int(goods_id))
    goodmsg = gd.query(goodmsg_sql)

    shopid = gd.query(goodmsg_sql)[0]['m_id']
    shopname_sql = "select m_name from jd_shopper where m_id = %d"%(int(shopid))
    shopname = gd.query(shopname_sql)

    fansnum_sql = "select count(*) from u_clt " \
                  "where type_id = 1 and clt_id = %d"%(int(shopid))
    fansnum = gd.query(fansnum_sql)

    productNum_sql = "select count(*) from goods_details " \
                     "where m_id_id = %d"%(int(shopid))
    productNum = gd.query(productNum_sql)

    shoprec_sql = "select goods_id as productID,goods_img as img," \
                  "goods_name as title,goods_prices as price " \
                  "from goods_details where m_id_id = %d limit 0,30"%(int(shopid))
    shoprec = gd.query(shoprec_sql)
    shopRecommend = [shoprec[i:i + 6] for i in range(0, len(shoprec), 6)]

    shopdict = {}
    shopdict['shopID'] = int(shopid)
    shopdict['shopName'] = shopname[0]['m_name']
    shopdict['fansNumber'] = int(fansnum[0]['count(*)'])
    shopdict['allProductNumber'] = int(productNum[0]['count(*)'])
    shopdict['shopRecommend'] = shopRecommend

    commentnum_sql = "select count(comment_content) as num from order_comment " \
                     "where goods_id_id = %d limit 0,2" % (int(goods_id))
    commentnum = gd.query(commentnum_sql)
    comment_sql = "select order_comment.comment_content as content," \
                  "order_comment.comment_time as ConmmentTime," \
                  "jd_user.user_name as UserName " \
                  "from (order_comment join o_detail " \
                  "on order_comment.order_id_id = o_detail.o_num) " \
                  "join jd_user on o_detail.o_user_id = jd_user.user_id " \
                  "where goods_id_id = %d limit 0,2" % (int(goods_id))
    comment = gd.query(comment_sql)

    commentdict = {}
    commentdict['rate'] = "98%"
    commentdict['number'] = int(commentnum[0]['num'])
    commentdict['comment'] = comment
    return jsonify({
        "code": 200,
        'msg': '商品详情页',
        'proudctID':goods_id,
        'banner':banner,
        'price':goodmsg[0]['price'],
        'title':goodmsg[0]['title'],
        'productModel':goodmsg[0]['typeid'],
        'address':address,
        'shopInfo':shopdict,
        'evaluate':commentdict,
    })

@goodsdetails_blue.route('/detail/comment/', methods=('GET', ))
def goodscomment():
    gd = GoodsDetailsDao()
    goods_id = request.args.get('productID')

    comment_sql = "select order_comment.comment_content as content," \
                  "order_comment.comment_time as ConmmentTime," \
                  "jd_user.user_name as UserName " \
                  "from (order_comment join o_detail " \
                  "on order_comment.order_id_id = o_detail.o_num) " \
                  "join jd_user on o_detail.o_user_id = jd_user.user_id " \
                  "where goods_id_id = %d"%(int(goods_id))
    comment = gd.query(comment_sql)

    return jsonify({
        "code": 200,
        'msg': '商品评论页',
        'productCommentList':comment
    })


@goodsdetails_blue.route('/detail/add/', methods=('POST', ))
def detailadd():
    success = False
    gd = GoodsDetailsDao()
    detailadd_data = eval(request.get_data())

    token = detailadd_data['token']
    goods_id = detailadd_data['productID']
    shopid = detailadd_data['shopID']
    goodsnum = detailadd_data['productNum']

    if token is None:
        return jsonify({
            'code': 400,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })

    if cache.check_token(token):
        user_id = cache.get_token_user_id(token)

        user_id_sql = "select user_id from jd_user where user_id={}".format(user_id)

        user_id = gd.query(user_id_sql)
        userid = user_id[0]['user_id']

        goodcheck_sql = "select c_goods_num from jd_cart where c_user_id=%s and c_goods_id=%d"%(userid,goods_id)
        goodcheck = gd.query(goodcheck_sql)

        if not goodcheck:
            gd.add(goodsnum, goods_id, shopid, userid)
            check = gd.query(goodcheck_sql)

            if check:
                success = True
        else:

            checknum = goodcheck[0]['c_goods_num']
            checknum += goodsnum
            gd.change(checknum,goods_id,userid)

            check = gd.query(goodcheck_sql)

            if check:
                success = True
        if success:
            return jsonify({
                'code': 200,
                'msg': '商品添加到购物车'
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '商品添加失败'
            })
    else:
        return jsonify({
            'code': 401,
            'msg': '用户未登录',
        })
