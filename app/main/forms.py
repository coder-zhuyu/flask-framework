# encoding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class EditProfileForm(Form):
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我描述')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能有字母, '
                                          '数字, 点 or 下划线')])
    confirmed = BooleanField('授权登录')
    role = SelectField('角色', coerce=int)
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我描述')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已使用.')
