from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import db, login_manager
from src.constants import Permission


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)  # 登录账号
    password_hash = db.Column(db.String(128))  # 密码hash值
    confirmed = db.Column(db.Boolean, default=False)  # 判断用户是否确认过邮件
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __str__(self):
        return self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ZMJ_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('打扰了')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf8')

    def confirm(self, token):
        """ 验证是否确认过注册邮件 """
        s = serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf8'))
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer, default=0)  # 这样设置默认值没用？？
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return self.name

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        """ 检查是否有该权限，没用则加上 """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """ 如果有该权限，则移除 """
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        """ 重置权限 """
        self.permissions = 0

    def has_permission(self, perm):
        """ 判断是否有该权限  """
        return self.permissions & perm == perm  # 精妙啊

    @classmethod
    def insert_roles(cls):
        """ 初始化用户 """
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Admin': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser
