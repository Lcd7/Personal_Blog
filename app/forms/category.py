from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Category

class NewCategoryForm(FlaskForm):
    '''
    新增分类表单类
    '''
    name = StringField(validators = [DataRequired('分类名不能为空'), Length(max = 12, message = '分类名长度小于12')])
    alias = StringField(validators = [DataRequired('别名不能为空'), Length(max = 24, message = '别名长度小于24')])
    show = BooleanField()

    def validate_name(self, field):
        if Category.query.filter_by(name = field.data).first():
            raise ValidationError('分类名已存在')

    def validate_alias(self, field):
        if Category.query.filter_by(name = field.data).first():
            raise ValidationError('分类别名已存在')

class EditCategoryForm(NewCategoryForm):
    '''
    编辑分类表单类
    '''
    seqid = HiddenField()

    def _get_recond_by_id(self):
        return Category.query.filter_by(self.seqid.data)

    def validate_name(self, field):
        category_by_id = self._get_recond_by_id()
        category_by_name = Category.query.filter_by(name = field.data).first()
        if category_by_name and category_by_name.seqid != category_by_id.seqid:
            raise ValidationError('分类名已存在')

    def validate_alias(self, field):
        category_by_id = self._get_recond_by_id()
        category_by_alias = Category.query.filter_by(alias = field.data).first()
        if category_by_alias and category_by_alias.seqid != category_by_id.seqid:
            raise ValidationError('分类别名已存在')