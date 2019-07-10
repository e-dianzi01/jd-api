from dao import BaseDao


class AddDao(BaseDao):
    def check_address(self, user_id):
        # 查询用户添加的地址
        sql = 'select user_address, is_default from u_address where user_id_id=%s'
        user_address = self.query(sql, user_id)
        return user_address




