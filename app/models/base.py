'''
Post 表: 正文表
Admin 表: 管理员及Blog个性化设置表
Category 表: Blog文章分类目录表
Comment 表: 文章评论表
Link 表: 外部链接表
然后我们可以看看想想之间的关系结构：

Admin 与 Link 表都是独立的，不和任何表产生关系。
Post 表与 Category 表之间应该是多对多关系，一篇文章可以包含多个分类，一个分类可以指向多篇文章，所以我们还需要一个中间表来构建多对多关系。
Post 表与 Comment 表之间则是一对多关系，一篇文章包含多条评论。
'''
from app.libs.extensions import db



#基类表

class Base(db.Model):
    '''
    数据表模型基类
    '''
    __abstract__ = True
    # 指明这个类是一个数据表抽象类，也就是不会实际在数据库中创建的数据表类，

    def set_attr(self, attrs_dict):
        '''
        将表单字段传递给数据表模型对应字段
        '''
        for key, value in attrs_dict.items():
            if key != "seqid" and hasattr(self, key):
                if value:
                    setattr(self, key, value)
    
# hasattr()   判断object对象中是否存在name属性
# setattr()   给对象属性赋值