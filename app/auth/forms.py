# encoding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('下次自动登录')
    submit = SubmitField('登录')


class RegistrationForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名只能有字母, '
                                          '数字, 点 or 下划线')])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='密码不一致.')])
    password2 = PasswordField('密码确认', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已注册.')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('提交')
