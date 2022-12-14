import os
from functools import wraps
from secrets import token_hex
from tour_management.models import Admin, AdminToken
from flask import redirect, url_for, render_template, current_app, flash
from flask_login import current_user
from flask_mail import Message
from tour_management import mail
from hashlib import md5
from datetime import datetime
from tour_management import db

def send_reset_password_mail(reciever_email, link):
    html_message = render_template(
        'emails/reset_password_link.html', link=link)
    text_message = render_template('emails/reset_password_link.txt', link=link)
    msg = Message('Reset password link', recipients=[reciever_email])
    msg.body = text_message
    msg.html = html_message
    mail.send(msg)