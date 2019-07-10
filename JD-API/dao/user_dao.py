from dao import BaseDao
from logger import api_logger

from libs.crypt import make_password, check_password


class UserDao(BaseDao):

    def save(self, **values):
        api_logger.info('db insert jd_user: <%s>' % values['tel'])
        # values['login_auth_str'] = make_password(values['login_auth_str'])
        return super(UserDao, self).save('jd_user', **values)

    def check_login_name(self, user_name):
        # 检查用户名是否已存在
        result = self.query('select id  from jd_user where user_name=%s' %user_name)
        return not bool(result)

    def check_login_phone(self, phone):
        # 检查联系电话是否存在
        result = self.query('select tel from jd_user where tel=%s'%phone)
        return bool(result)

    def login(self, login_name, login_auth_str):
        sql = 'select id, login_auth_str from app_user_2 ' \
              'where login_name=%s and activated=%s'
        user_data = self.query(sql, login_name, 1)

        if user_data:
            user_id, auth_str = (user_data[0].get('id'),
                                 user_data[0].get('login_auth_str'))

            if check_password(login_auth_str, auth_str):
                # 验证成功
                user_profile = self.get_profile(user_id)
                if user_profile is None:
                    return {
                        'user_id': user_id,
                        'nick_name': login_name
                    }

                return user_profile
            api_logger.warn('用户 %s 的口令不正确' % login_name)
            raise Exception('用户 %s 的口令不正确' % login_name)
        else:
            api_logger.warn('查无此用户 %s' % login_name)
            raise Exception('查无此用户 %s' % login_name)

    def get_profile(self, user_id):
        # 获取用户的详细信息
        sql = "select * from jd_user " \
              "where user_id=%s"
        user_profile = self.query(sql, user_id)
        if user_profile:
            return user_profile


    def save_user_id(self, **values):
        api_logger.info('db insert jd_user: <%s>' % values['user_id'])
        # values['login_auth_str'] = make_password(values['login_auth_str'])
        return super(UserDao, self).save('jd_user', **values)


    def get_asset(self, user_id):
        api_logger.info('db get jd_user: <%s>' % 'user_id')
        # 获取用户的详细信息
        sql = "select user_id,user_name, tel, u_img, u_email, is_val,asset from jd_user " \
              "where user_id=%s"
        user_profile = self.query(sql, user_id)
        if user_profile:
            return user_profile[0]
    def update_asset(self,user_id,asset):
        api_logger.info('db update jd_user: <%s>' % 'user_id')
        sql = "update jd_user set asset=%s" \
              "where user_id=%s"
        user_asset = self.query(sql, asset,user_id)
        if user_asset:
            return True

    def check_real(self, user_id):
        # 验证身份证、银行卡
        sql = 'select u_bank, user_card from jd_user where user_id=%s'
        with self.db as c:
            c.execute(sql, user_id)
            data = c.fetchall()
            if data:
                data = list(data)
            return data

    def get_jd_user(self, phone):
        # 通过电话查user_id
        sql = 'select user_name,user_id,is_val,tel,asset,u_img,u_bank,u_email,u_intg,pay_pwd from jd_user where tel=%s'
        user_profile = self.query(sql, phone)
        return user_profile
