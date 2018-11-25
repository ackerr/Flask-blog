import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is my secret_key for ZmJ'  # 防止表单csrf设置的密钥/防止环境变量中
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不需要跟踪对象变化从而降低内存消耗

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)  # google 使用TLS
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)  # google 使用TLS
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '1352252181@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ZMJ = '[ZmJ]'
    MAIL_SENDER = 'ZmJ admin <1352252181@qq.com>'
    ZMJ_ADMIN = '1352252181@qq.com'

    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'local.sqlite')


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'product.sqlite')


config = {
    'local': LocalConfig,
    'product': ProductConfig,
}
