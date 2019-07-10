from libs import rd
import uuid

def new_token():
    return uuid.uuid4().hex


def save_token(token, user_id):
    # 保存token
    rd.set(token, user_id)
    rd.expire(token, 12*3600)  # 有效时间： 12小时


def check_token(token):
    # 验证token
    return rd.exists(token)


def get_token_user_id(token):
    # 通过token获取user_id
    if check_token(token):
        return rd.get(token).decode()

