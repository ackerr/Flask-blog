from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src import db
from src.auth import auth
from src.auth.forms import LoginForm, RegisterForm
from src.email import send_mail
from src.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            page = request.args.get('next')
            if not page or not page.startswich('/'):
                page = url_for('main.index')
            return redirect(page)
        flash('无效的用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, '确认用户邮件', 'auth/email/confirm', user=user, token=token)
        flash('邮件已发送至注册邮箱, 需要确认过邮件才能登陆哦')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录啦')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirmed(token):
        db.session.commit()
        flash('你已确认邮件')
    else:
        flash('请先到邮箱确认邮件')
    return redirect('main.index')


@auth.route('/confirm')
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, '确认用户邮件', 'auth/email/confirm', user=current_user, token=token)
    flash('邮件已发送至注册邮箱, 需要确认过邮件才能登陆哦')
    return redirect(url_for('auth.login'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
