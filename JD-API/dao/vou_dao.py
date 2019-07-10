from dao import BaseDao
from logger import api_logger


class VouDao(BaseDao):
    def check_asset(self, user_id):
        # 查询余额
        sql = 'select asset, u_intg from jd_user where user_id=%s'
        u_asset = self.query(sql, user_id)
        return u_asset

    def check_vouchers(self, user_id):
        # 查询优惠卷
        sql = 'select title, cop_id, minusprice, vuc from jd_coupon where user_id=%s'
        u_vouchers = self.query(sql, user_id)
        return u_vouchers

    def vouchers_0(self, user_id):
        # 查询无门槛优惠卷
        sql = 'select user_id, title, cop_id, minusprice, vuc from jd_coupon where vuc=0 and user_id=%s'
        u_vouchers = self.query(sql, user_id)
        return u_vouchers

    def vouchers_1(self, user_id):
        # 查询满减优惠卷
        sql = 'select user_id, title, cop_id, minusprice, vuc from jd_coupon where vuc=1 and user_id=%s'
        u_vouchers = self.query(sql, user_id)
        return u_vouchers

    def save(self, **values):
        api_logger.info('db insert jd_user: <%s>' % values['user_id'])
        return super(VouDao, self).save('jd_coupon', **values)

    def sort_up(self):
        # 按金额升序排序
        sql = "select * from jd_coupon order by minusprice asc"
        with self.db as c:
            c.execute(sql)
            data = c.fetchall()
            api_logger.info('%s ok!' % sql)
            if data:
                data = list(data)
        return data

    def sort_down(self):
        # 按金额升序排序
        sql = "select * from jd_coupon order by minusprice desc"
        with self.db as c:
            c.execute(sql)
            data = c.fetchall()
            api_logger.info('%s ok!' % sql)
            if data:
                data = list(data)
        return data
