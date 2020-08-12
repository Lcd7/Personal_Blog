from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from app.models import Link

class NewLinkForm(FlaskForm):
    name = StringField(validators = [DataRequired('链接名称不能为空'), Length(max = 60, message = '链接名称最大不能超过 60 个字符')])
    url = StringField(validators = [DataRequired('链接地址不能为空'), URL(message = 'url格式不正确'), Length(6, 255, message = 'url长度在6~255')])
    tag = SelectField(
        label = '标签',
        validators = [DataRequired('必须选择一个标签')],
        render_kw = {
            'class': 'custom-select my-1 mr-sm-2'
        },

        # 元组的第一个元素是 <option> 标签 value 属性的值，第二个元素是 <option> 标签显示的文本
        choices = [
            ('weixin', '微信'),
            ('weibo', '微博'),
            ('douban', '豆瓣'),
            ('zhihu', '知乎'),
            ('google', '谷歌'),
            ('linkedin', '领英'),
            ('twitter', '推特'),
            ('facebook', '脸书'),
            ('github', 'Github'),
            ('telegram', 'Telegram'),
            ('other', '其它'),
            ('friendLink', '友情链接')
        ],
        default = 'other',
        coerce = str
    )

    def validate_name(self, field):
        if Link.query.filter_by(name = field.data).first():
            raise ValidationError('链接名已存在')

    def validate_url(self, field):
        if Link.query.filter_by(url = field.data).first():
            raise ValidationError('链接已存在')

class EditLinkForm(NewLinkForm):
    seqid = HiddenField()

    def _get_record_by_id(self):
        return Link.query.get(self.seqid.data)

    def validate_name(self, field):
        link_by_id = self._get_record_by_id()
        link_by_name = Link.query.filter_by(name = field.data).first()
        if link_by_name and link_by_name.id != link_by_id.id:
            raise ValidationError('链接名已存在')

    def validate_url(self, field):
        link_by_id = self._get_record_by_id()
        link_by_url = Link.query.filter_by(url = field.data).first()
        if link_by_url and link_by_id.id != link_by_url.id:
            raise ValidationError('链接名已存在')

