'''
实例化第三方插件
'''

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_whooshee import Whooshee

csrf_protect = CSRFProtect()

#复写SQLAlchemy类， 新增专门处理数据库写入错误的回滚操作
class SQLALCHEMY(_SQLAlchemy):
    '''
    数据库写入操作的异常都必须要处理，必须要执行数据库回滚操作，不然一旦出现异常，
    除非重启应用，不然后续的所有的数据库操作都会报错。
    '''
    @contextmanager
    def auto_commit(self):
        try:
            yield 
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

db = SQLALCHEMY()
migrate = Migrate()


def get_login_manager():
    '''
    配置并返回LoginManager实例
    '''
    login_manager = LoginManager()

    @login_manager.user_loader
    def get_user(uid):
        '''
        处理访问控制
        '''
        from app.models.admin import Admin
        return Admin.query.get(int(uid))

    # 访问控制 访问需要登录的页面重定向到登录页面
    login_manager.login_view = 'web.login'                              #登陆视图的endpoint
    login_manager.login_message = '无权访问此页面， 请先登录'            #重定向Flash信息
    login_manager.login_message_category = 'error'                      #重定向Flask信息分类

    return login_manager

# 邮箱插件
mail = Mail()

whooshee = Whooshee()

if __name__ == "__main__":
    pass