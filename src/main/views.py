from flask import make_response, redirect, render_template, session, url_for

from src import db
from src.email import send_mail
from src.main import app
from src.main.forms import UsernameForm
from src.models import User


@app.route('/hello')
def hello():
    """ 测试API """
    response = make_response('<h2>this is a response having a cookie</h2>')
    response.set_cookie('name', 'zmj')
    return response


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = UsernameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data)
            db.session.add(user)
            session['known'] = False
            if app.config.get('ZMJ_ADMIN'):
                send_mail('1352252181@qq.com', 'New User')
            db.session.commit()
        else:
            session['known'] = True
        session['name'] = form.username.data
        form.username.data = ''
        return redirect(url_for('main.index'))
    return render_template('auth/index.html', name=session.get('name'), form=form, known=session.get('known', False))


@app.route('/user')
def user_page():
    return render_template('auth/user.html', name='ZmJ')


if __name__ == '__main__':
    app.run(port=8001, debug=True)
