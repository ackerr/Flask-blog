import os

from flask import Flask

from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this is my secret_key for ZmJ'  # 防止表单csrf设置的密钥/防止环境变量中
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 不需要跟踪对象变化从而降低内存消耗

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
moment = Moment(app)

from src import form, models  # 貌似需要这句话不然migrate 找不到对象


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=models.User, Role=models.Role)
