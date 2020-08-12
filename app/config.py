import urllib
from datetime import timedelta
from app.models import Admin, Category, Comment, Link, Post
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig:
    """
    配置基类，公用配置写在这里
    """
    SECRET_KEY = "1234"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # 登陆状态保持31天
    REMEMBER_COOKIE_DURATION = timedelta(days = 31)
    # 默认的session cookie 过期时间，3天过期
    PERMANENT_SESSION_LIFETIME = timedelta(days = 3)
    # MODELS字典，存放模型名称：模型
    MODELS = {'Admin': Admin, 'Category': Category, 'Comment': Comment, 'Link': Link, 'Post': Post}
    # 后台分页数
    ADMIN_PER_PAGE = 20
    # 图片文章上传路径
    UPLOAD_FOLDER = os.path.join(basedir, 'app/uploads')
    # 允许上传的文件格式
    ALLOWED_EXTENSIONS = ("jpg", "jpeg", "gif", "png", "bmp", "webp", 'svg')
    # 最小搜索字符长度
    WHOOSHEE_MIN_STRING_LEN = 2

class DevelopmentConfig(BaseConfig):
    """
    开发环境配置类
    """
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect={}".format(urllib.parse.quote_plus(r"DRIVER={SQL Server Native Client 11.0};SERVER=192.168.8.16;DATABASE=crawler_test;UID=sa;PWD=root123."))
    SEND_FILE_MAXAGE_DEFAULT = timedelta(seconds = 1)
    # 邮件配置项
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TSL = False
    MAIL_USERNAME = "1102217785@qq.com"
    MAIL_PASSWORD = "password"

class TestConfig(BaseConfig):
    """
    测试环境配置类
    """
    pass


class ProductionConfig(BaseConfig):
    """
    生产环境配置类
    """
    pass
    
# 配置类字典，根据传递的 key 选择不同的配置类
configs = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig
}