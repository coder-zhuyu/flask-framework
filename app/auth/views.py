# encoding: utf-8
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from ..decorators import admin_required


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码不正确.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #           'auth/email/confirm', user=user, token=token)
        flash('注册申请已提交, 等待管理员确认.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/list-users')
@login_required
@admin_required
def list_users():
    page = request.args.get('page', 1, type=int)
    query = User.query
    pagination = query.paginate(
        page, per_page=current_app.config['FLASKY_USERS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('auth/confirm.html', pagination=pagination, users=users)


@auth.route('/confirm/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def confirm(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.confirm()
    flash('授权成功.')
    return redirect(url_for('auth.list_users'))


@auth.route('/unconfirm/<int:user_id>')
@login_required
@admin_required
def unconfirm(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.unconfirm()
    flash('取消授权成功.')
    return redirect(url_for('auth.list_users'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
