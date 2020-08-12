from flask import Flask, render_template, url_for, request
from app.config import configs
from app.libs.extensions import db, migrate, get_login_manager, csrf_protect, mail, whooshee
from app.models import Post, Category, post_category_middle, Comment, Admin, Link
from datetime import datetime
from app.libs.custom_filters import switch_link_tag, get_search_part
# 额外引入 func 通过 func.rand() 获取随机排序的文章
from sqlalchemy import func
# 要处理 csrf 的错误，需要专门引入 CSRFError
from flask_wtf.csrf import CSRFError
# 引入 is_safe_url 判断 request.referrer 的 URL 是否合法
from app.libs.helpers import is_safe_url



def create_app(config = "development"):
    app = Flask(__name__)
    app.config.from_object(configs[config])
    register_exctensions(app)
    register_blueprints(app)
    register_template_context(app)
    add_template_filter(app)
    register_error_templates(app)
    # print(db.Model.metadata.tables)

    #删除更新数据库
    # db.drop_all()
    # db.create_all(app = app)

    #插入虚拟数据
    # from app.libs.fake_data import FakerData
    # FakerData.fake_admin()
    # FakerData.fake_categories()
    # with app.app_context():
    #     FakerData.fake_posts()
    # FakerData.fake_comments()
    # FakerData.fake_links()

    return app

def register_exctensions(app):
    '''
    注册第三方插件
    '''
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager = get_login_manager()
    login_manager.init_app(app)

    csrf_protect.init_app(app)
    mail.init_app(app)
    whooshee.init_app(app)

def register_blueprints(app):
    from app.web import web
    app.register_blueprint(web)

def register_template_context(app):
    '''
    注册模板全局变量
    '''
    @app.context_processor
    def generate_template_context():
        admin = Admin.query.first()
        categories = Category.query.all()
        links = Link.query.all()
        current_year = datetime.now().year
        unreviewed_comment_count = Comment.query.filter_by(reviewed = False, trash = False).count()
        admin_url_info = [
            {'总览': 'web.admin_index'},
            {'文章管理': 'web.manage_post'},
            {'评论管理': 'web.manage_comment'},
            {'分类管理': 'web.manage_category'},
            {'链接管理': 'web.manage_link'},
            {'博客设置': 'web.blog_setting'}
        ]
        return {"admin": admin, "categories": categories, "links": links, "current_year": current_year,
                "unreviewed_comment_count": unreviewed_comment_count, "admin_url_info": admin_url_info}

def add_template_filter(app):
    """
    注册自定义模板验证器
    """
    app.add_template_filter(switch_link_tag)
    app.add_template_filter(get_search_part)

def register_error_templates(app: Flask):
    """
    注册 HTTP 请求错误时页面显示模板
    :param app: Flask 核心对象
    :return: None
    """
    @app.errorhandler(404)
    def not_found(e):
        '''
        处理404错误
        '''
        error_info = {
            'head_title': '找不到您要访问的页面',
            'page_title': '找不到您要访问的页面...',
            'description': f'抱歉，您要访问的页面不存在，您可以<a href="{url_for("web.index")}">返回首页</a>，或者查看以下内容：'
        }
        posts = Post.query.filter_by(published = True, trash = False).order_by(func.random()).limit(5)
        return render_template('error/error.html', posts = posts, error_info = error_info), 404

    @app.errorhandler(500)
    def server_error(e):
        """
        处理 500 错误
        """
        error_info = {
            'head_title': '似乎有什么意外出现了',
            'page_title': '似乎有什么意外出现了...',
            'description': f'抱歉，有不可名状的错误突然出现，您可以<a href="{url_for("web.index")}">返回首页</a>，或者查看以下内容：'
        }
        posts = Post.query.filter_by(published = True, trash = False).order_by(func.random()).limit(5)
        return render_template('error/error.html', posts = posts, error_info = error_info), 500

    @app.errorhandler(CSRFError)
    def csrf_error(e):
        """
        处理 csrf_token 失效错误
        """
        # 因为 csrf 的错误普遍出现在填写表单中，所以为了引导用户回到上一页，这里有必要进行判断
        if is_safe_url(request.referrer):
            back_url = request.referrer
        else:
            back_url = url_for('web.index')
        error_info = {
            'head_title': '您的页面会话已过期',
            'page_title': '您的页面会话已过期',
            'description': f'抱歉，可能您在页面停留过久，导致会话已过期，您可以<a href="{back_url}">返回上一页</a>重新执行操作，或者查看以下内容：'
        }
        posts = Post.query.filter_by(published=True, trash=False).order_by(func.random()).limit(5)
        return render_template('error/error.html', posts = posts, error_info = error_info), 500


if __name__ == "__main__":
    pass