import os
from functools import wraps
from secrets import token_hex
from flask import redirect, url_for, render_template, current_app, flash
from flask_login import current_user
from flask_mail import Message
from tour_management import mail
from hashlib import md5
from datetime import datetime
# from PIL import Image



def send_confirmation_mail(reciever_email, link, otp):
    html_message = render_template('emails/email_confirmation.html', link=link, otp=otp)
    text_message = render_template('emails/email_confirmation.txt', link=link, otp=otp)
    msg = Message('Email Activation link', recipients=[reciever_email])
    msg.body = text_message
    msg.html = html_message
    mail.send(msg)

    