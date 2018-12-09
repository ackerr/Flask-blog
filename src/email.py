import os
from threading import Thread

from flask import render_template
from flask_mail import Message

from src import create_app, mail


app = create_app(os.getenv('FLASK_CONFIG', 'local'))


def send_sync_email(instance, msg):
    with instance.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['ZMJ'] + subject, sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_sync_email, args=[app, msg])
    thread.start()
    return thread
