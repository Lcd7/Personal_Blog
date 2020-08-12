from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.models.base import Base
from app.libs.extensions import db


class Admin(Base, UserMixin):
    """
    管理员及Blog设置数据表模型类
    """
    seqid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False)
    _password = db.Column(db.String(256), nullable = False)
    nickname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(64), nullable = False)
    blog_title = db.Column(db.String(128), nullable = False)
    blog_subtitle = db.Column(db.String(256), nullable = False)
    blog_about = db.Column(db.Text)
    # 评论每页展示数量
    comment_per_page = db.Column(db.Integer, default=10)
    # 新建一个字段保存 Markdown 格式字符串
    blog_about_markdown = db.Column(db.Text)


    # 处理密码相关的查询、储存、校验工作
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, row):
        self._password = generate_password_hash(row)

    def check_password(self, row):
        return check_password_hash(self._password, row)
        