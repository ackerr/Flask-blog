from flask import make_response, render_template

from src import app


@app.route('/hello')
def hello():
    """ 测试API """
    response = make_response('<h2>this is a response having a cookie</h2>')
    response.set_cookie('name', 'zmj')
    return response


@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'ZmJ'}
    return render_template('auth/index.html', user=user)


@app.route('/user')
def user_page():
    return render_template('auth/user.html', name='ZmJ')


if __name__ == '__main__':
    app.run(port=8001, debug=True)
