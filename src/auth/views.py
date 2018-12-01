from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from src import db
from src.auth import auth
from src.auth.forms import LoginForm, RegisterForm
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
        flash('注册成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录啦')
    return redirect(url_for('main.index'))
