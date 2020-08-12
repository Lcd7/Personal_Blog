from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    '''
    登陆表单
    '''
    username = StringField(validators = [DataRequired('用户名不能为空'), Length(3, 30, message = '用户名的长度应该在5到30个字符之间')])
    password = PasswordField(validators = [DataRequired('密码不能为空'), Length(8, 24, message = '密码长度要在8到24个字符之间')])
    remember = BooleanField()