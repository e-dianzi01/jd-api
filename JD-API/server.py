from apps import app

from views import app_user, order, goods_show_index, cart, classify, groupbuy, cart_order, paycost, collection, address, \
    asset, shop, goodsdetails, test

APP_CONFIG={
    'host': '0.0.0.0',
    'port': 9005,
    'debug': True
}

if __name__ == '__main__':

    app.register_blueprint(app_user.blue)
    app.register_blueprint(order.order_blue)
    app.register_blueprint(goods_show_index.blue1)
    app.register_blueprint(cart.cart_blue)
    app.register_blueprint(groupbuy.groupbuy_blue)
    app.register_blueprint(classify.classify_blue)
    app.register_blueprint(cart_order.cart_order_blue)
    app.register_blueprint(paycost.paycost_blue)
    app.register_blueprint(collection.collect_blue)
    app.register_blueprint(address.address_blue)
    app.register_blueprint(test.test_blue)
    app.register_blueprint(asset.asset_blue)
    app.register_blueprint(shop.blue_shop)
    app.register_blueprint(goodsdetails.goodsdetails_blue)
    app.run(**APP_CONFIG)