from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Category

class PostForm(FlaskForm):
    '''
    编辑于新建文章表单
    '''
    title = StringField(validators = [DataRequired('标题不能为空'), Length(max = 60, message = '标题长度不能超过60个字符')])
    content_markdown = TextAreaField()
    content = TextAreaField()
    categories = SelectMultipleField(validators = [DataRequired('必须选一个分类')], coerce = int)
    can_comment = BooleanField(label = '允许评论')
    description = TextAreaField(validators = [Length(max = 150, message = 'SEO描述信息不能超过150个字符')])
    publish = SubmitField('发布')
    save = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 动态获取分类数据生成 categories 字段选项
        self.categories.choices = [(category.seqid, category.name) for category in Category.query.order_by(Category.seqid.desc()).all()]
    
    def validate_content_markdown(self, field):
        if not field.data:
            raise ValidationError('文章内容不能为空')

