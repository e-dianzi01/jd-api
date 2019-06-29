from apps import app

from views import app_user, order, goods_show_index, cart, classify, groupbuy, cart_order

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

    app.run(**APP_CONFIG)