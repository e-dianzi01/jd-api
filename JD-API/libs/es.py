"""
封装ES搜索引擎的SDK
"""
import requests  #可以调用第三方接口
#直接用db

class ESearch():
    def __init__(self,index):
        self.host = '121.199.63.71'
        self.port = '9205'
        self.index = index
    def create_index(self):
        url = f'http://{self.host}:{self.port}/{self.index}/'

        resp = requests.put(url, json = {})

    def add_doc(self,doc_type,id= None, **values):
        url = f'http://{self.host}:{self.port}/{self.index}/{doc_type}'
        if id:
            url += f"{id}"
        resp = requests.post(url,josn = values)
        if resp.get('result') == "create" and \
           resp.get('create'):
            pass
        #数字不能模糊匹配

# def init_index():
#     #连接数据库，将doctor表数据添加到索引中
#     db = DB()
#     c.excute

