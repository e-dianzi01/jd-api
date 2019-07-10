import time
from datetime import datetime
from libs.sms import get_code
def get_order_num():
    return datetime.now().strftime("%Y%m%d")[2:] + get_code() + str(int(time.time()))[-4:]


# def get_tra_asset(traffic):
#     asset = 0
#     if traffic == "30M":
#         asset = 3
#     elif traffic == "50M":
#         asset = 5
#     elif traffic == "100M":
#         asset = 10
#     elif traffic == "200M":
#         asset = 15
#     elif traffic == "500M":
#         asset = 30
#     elif traffic == "1G":
#         asset = 50
#
#     return asset