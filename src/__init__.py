from flask import Flask

from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this is my secret_key for ZmJ'  # 防止表单csrf设置的密钥/防止环境变量中

bootstrap = Bootstrap(app)
moment = Moment(app)
