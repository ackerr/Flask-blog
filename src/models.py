from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)  # 登录账号
    password_hash = db.Column(db.String(128))  # 密码hash值
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __str__(self):
        return self.username

    @property
    def password(self):
        raise AttributeError('打扰了')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    users = db.relationship('User', backref='role')

    def __str__(self):
        return self.name
