from flask import Blueprint, jsonify

classify_blue = Blueprint('classify_blue', __name__)


@classify_blue.route('/classify/', methods=('GET', ))
def classify():
    return jsonify({
        "code":200,
        'msg': '分类页'
    })