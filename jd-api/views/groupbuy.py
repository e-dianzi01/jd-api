from flask import Blueprint, jsonify

groupbuy_blue = Blueprint('groupbuy_blue', __name__)


@groupbuy_blue.route('/groupbuy/', methods=('GET', ))
def groupbuy():
    return jsonify({
        "code":200,
        'msg': 'pinggouye'
    })