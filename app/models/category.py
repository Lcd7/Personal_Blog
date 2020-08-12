from app.libs.extensions import db
from app.models.base import Base

class Category(Base):
    """
    文章分类数据表模型
    """
    # __tablename__ = 'Category'

    seqid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(12), nullable = False, unique = True)
    posts = db.relationship("Post", secondary = 'post_category_middle')
    show = db.Column(db.Boolean, default = True)
    alias = db.Column(db.String(24), unique = True, nullable = True)

    def delete(self):
        if self.posts:
            for post in self.posts:
                if len(post.categories) == 1:
                    with db.auto_commit():
                        post.categories = [Category.query.get(1)]
                        db.session.add(post)
                        
        with db.auto_commit():
            db.session.delete(self)