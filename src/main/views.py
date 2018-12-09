from flask import make_response, render_template, session

from src.main import app
from src.main.forms import UsernameForm


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
    return render_template('auth/index.html', name=session.get('name'), form=form, known=session.get('known', False))


@app.route('/user')
def user_page():
    return render_template('auth/user.html', name='ZmJ')


if __name__ == '__main__':
    app.run(port=8001, debug=True)
