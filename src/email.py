import os

from flask_mail import Message

from src import create_app, mail


app = create_app(os.getenv('FLASK_CONFIG', 'local'))


def send_mail(to, subject):
    msg = Message(app.config['ZMJ'] + subject, sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = '???????????'
    msg.html = "<a href='www.baidu.com'>百度</a>"
    mail.send(msg)
