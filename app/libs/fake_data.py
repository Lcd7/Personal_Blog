import random
from faker import Faker
from app.models import Admin, Category, Comment, Post, Link
from app.libs.extensions import db
from pypinyin import lazy_pinyin

class FakerData:
    '''
    虚拟数据生成
    '''
    FAKER = Faker('zh_cn')

    @classmethod
    def fake_admin(cls):
        '''
        生成admin表虚拟数据
        '''
        # admin1 = Admin.query.filter(Admin.username == 'admin').first()
        # admin1.password = '12345678'
        # db.session.commit()
        with db.auto_commit():
            admin = Admin()
            admin.username = 'admin'
            admin.password = '12345678'
            admin.nickname = '临时管理员昵称'
            admin.email = '1102217785@qq.com'
            admin.blog_title = '临时blog名'
            admin.blog_subtitle  = '临时blog副标题'
            admin.blog_about = cls.FAKER.text(1000)
            db.session.add(admin)

    @classmethod
    def fake_categories(cls, count = 9):
        '''
        生成blog分类虚拟数据
        '''
        while Category.query.count() < count + 1:
            category_name = cls.FAKER.word()
            if Category.query.filter_by(name = category_name).first():
                continue
            with db.auto_commit():
                category = Category()
                category.name = category_name
                category.alias = ''.join(lazy_pinyin(category_name))
                db.session.add(category)

    @classmethod
    def fake_posts(cls, count = 50):
        '''
        生成blog文章虚拟数据
        '''
        for _ in range(count):
            with db.auto_commit():
                post = Post()
                post.title = cls.FAKER.sentence()
                post.content = cls.FAKER.text(4000)
                post.description = post.content[:70]

                category_id_one = random.randint(1, Category.query.count())
                category_id_two = random.randint(1, Category.query.count())

                if category_id_one == 1 or category_id_two == 1:
                    post.categories = [Category.query.get(1)]
                elif category_id_one == category_id_two:
                    post.categories = [Category.query.get(category_id_one)]
                else:
                    post.categories = [
                        Category.query.get(category_id_one),
                        Category.query.get(category_id_two)
                    ]
                db.session.add(post)
        
    @classmethod
    def fake_comments(cls, count = 1000):
        '''
        生成blog文章评论
        '''
        # 50% 已审核评论
        # 5% 未审核评论
        # 10% 管理员评论
        # 35% 回复的评论        
        reviewed_comments_count = int(count * 0.5)
        unreviewed_comments_count = int(count * 0.05)
        admin_comments_count = int(count * 0.1)
        replied_comments_count = int(count * 0.35)

        def _generate_comments(_count, reviewed = True, from_admin = False, is_replied = False):
            '''
            生成评论数据
            :param _count: 生成的评论数量
            :param reviewed: default=True，默认是已审核评论
            :param from_admin: default=False，默认不是管理员评论
            :param is_replied: default=False，默认不是回复评论
            '''
            comment_count = Comment.query.count()
            posts_count = Post.query.count()
            for _ in range(_count):
                comment = Comment()
                
                with db.auto_commit():
                    if not from_admin:
                        comment.author = cls.FAKER.name()
                        comment.email = cls.FAKER.email()
                        comment.site = cls.FAKER.url()
                    else:
                        comment.author = Admin.query.get(1).nickname
                        comment.email = "admin@email.com"
                        comment.site = "localhost:5000"

                    comment.content = cls.FAKER.text(random.randint(40, 200))
                    comment.from_admin = from_admin
                    comment.reviewed = reviewed
                    if is_replied:
                        comment.replied = Comment.query.get(random.randint(1, comment_count))
                        
                    comment.post = Post.query.get(random.randint(1, posts_count))
                    
                    db.session.add(comment)
        
        _generate_comments(reviewed_comments_count)
        _generate_comments(unreviewed_comments_count, reviewed = False)
        _generate_comments(admin_comments_count, from_admin = True)
        _generate_comments(replied_comments_count, is_replied = True)

    @classmethod
    def fake_links(cls):
        """
        生成Blog链接虚拟数据
        :return: None
        """
        with db.auto_commit():
            weibo = Link(name = 'Weibo', url = '#', tag = 'weibo')
            weixin = Link(name = 'Weixin', url = '#', tag = 'weixin')
            douban = Link(name = 'Douban', url = '#', tag = 'douban')
            zhihu = Link(name = 'Zhihu', url = '#', tag = 'zhihu')
            github = Link(name = 'Github', url = '#', tag = 'github')
            twitter = Link(name = 'Twitter', url = '#', tag = 'twitter')
            facebook = Link(name = 'FaceBook', url = '#', tag = 'facebook')
            google = Link(name = 'Google', url = '#', tag = 'google')
            linkedin = Link(name = 'LinkedIn', url = '#', tag = 'linkedin')
            other = Link(name = 'Oter', url = '#', tag = 'other')
            telegram = Link(name = 'Telegram', url = '#', tag = 'telegram')
            frendlink = Link(name = 'FriendLink', url = '#', tag = 'friendLink')
            db.session.add_all([twitter, facebook, google, linkedin, weibo, weixin, douban, zhihu, github, other, telegram, frendlink])
        
if __name__ == "__main__":
    pass