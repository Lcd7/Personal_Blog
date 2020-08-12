from flask import render_template, request, flash, url_for, redirect, session, abort
from flask_login import login_user, current_user, logout_user

from app.web import web
from app.forms.login import LoginForm
from app.models import Admin

@web.before_request
def test():
    print('测试一下before_request功能')

@web.route('/login/', methods = ['GET', 'POST'])
def login():
    """登录视图"""
    # 判断用户是否为已登录状态
    # 如果用户已登录则跳转回首页
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))

    # 实例化 LoginForm 表单类，并且向它传递一个参数
    # request 对象可以用来获取客户端传递的各种数据
    # request.form 就是得到前端表单中填写的数据
    # 向表单类传递 request.form 不是必须的，但是如果登录失败，用户填写的数据会保留在表单的输入框中，增加用户体验
    # 保留用户填写的数据除了要在这里传入 request.form，前端表单也需要接收，后面会提到
    form = LoginForm(request.form)

    # flask-wtf 独有的方法，它等同于下面这种写法：
    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        admin = Admin.query.filter(Admin.username == form.username.data).first()
        if admin and admin.check_password(form.password.data):
            # 配置 session 的 permanent 的值为 True
            # 使 PERMANENT_SESSION_LIFETIME 配置项生效
            session.permanent = True

            # 数据校验通过，执行 login_user 方法
            # 这个方法有一个必须参数，就是登录用户的查询实例
            # remember 参数控制是否记住用户，也就是浏览器关闭之后，再次打开，是否保留登录状态
            #login_user方法自动将登陆信息保存到cookies
            login_user(admin, remember = form.remember.data)

            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)

        else:
            flash('登陆失败！请检查用户名或密码', 'error')


    return render_template('login/login.html', form = form)

@web.route('/logout/')
def logout():
    '''
    登出视图
    '''
    if not current_user.is_authenticated:
        abort(404)
    
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('web.login'))