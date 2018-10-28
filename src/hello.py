from flask import flash, make_response, redirect, render_template, session, url_for

from src import app
from src.form import UsernameForm


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
        old_name = session.get('name')
        if old_name is None and old_name != form.username.data:
            flash('提交成功！')
        session['name'] = form.username.data
        return redirect(url_for('index'))
    return render_template('auth/index.html', name=session.get('name'), form=form)


@app.route('/user')
def user_page():
    return render_template('auth/user.html', name='ZmJ')


if __name__ == '__main__':
    app.run(port=8001, debug=True)
