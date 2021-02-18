from flask import render_template
from flask_mail import Message
from app import mail, app
from app.models import User


def send_email(subject, sender, recipients, text_body, html_body):
    with app.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)


def send_auth_link(user, expiration):
    text = render_template('email/auth.txt', token=user.auth_link, exp=expiration)
    html = render_template('email/auth.html', token=user.auth_link, exp=expiration)
    send_email('Authorization link',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=text,
               html_body=html)

