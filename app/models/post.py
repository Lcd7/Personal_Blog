from datetime import datetime

from app.models.base import Base
from app.libs.extensions import db, whooshee


#该装饰器参数是检索的字段名称
@whooshee.register_model('title', 'content')
class Post(Base):
    '''
    Blog文章数据表模型类
    '''
    # __tablename__ = "Post"

    seqid = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60))
    # 储存 markdown 格式的正文，用以编辑时传递给 markdown 编辑器
    content_markdown = db.Column(db.Text)   
    # 储存 HTML 格式正文，用来展示   
    content = db.Column(db.Text)
    categories = db.relationship('Category', secondary = 'post_category_middle')
    comments = db.relationship('Comment', cascade = 'all, delete-orphan')
    can_comment = db.Column(db.Boolean, default = True)
    description = db.Column(db.String(150))
    trash = db.Column(db.Boolean, default = False)
    published = db.Column(db.Boolean, default = True)
    create_time = db.Column(db.DateTime, default = datetime.utcnow)