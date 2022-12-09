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
# from PIL import Image



def admin_creation(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        org = Admin.query.first()
        if org is None or org == []:
            flash ('Created Test User', 'danger')
            password = 'password'
            org = Admin()
            org.name = 'admin'
            org.username = 'admin'
            org.employee_id = '123'
            org.email = 'admin@authelectric.io'
            org.phone_number = '1234567890'
            org.password = Admin.hash_password(password)
            db.session.add(org)
            db.session.commit()
            admin = Admin.query.filter_by(username = 'admin').first()
            admin_id = admin.id
            product_conf_token = AdminToken.generate_token('admin_activation',admin_id,1800)
            token_info = AdminToken.query.filter_by(token_type='admin_activation').first()
            token = token_info.token
            print('token: ',token)
            url = url_for('admin.register',token=token, _external=True)
            print('URL :', url)
            return redirect(url_for('admin.register',token=token, _external=True))
            # return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return decorated_function

def no_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.first()
        if admin is None or admin == []:
            return redirect(url_for('admin.registration'))
        return func(*args, **kwargs)
    return decorated_function

def super_user(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        org = Admin.query.filter_by(id = current_user.id).first()
        if org is None or org == []:
            flash ('Something went wrong.', 'danger')
            return redirect(url_for('admin.dashboard'))
        print(org.role)
        if org.role == 'admin':
            flash ('Access Denied.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return func(*args, **kwargs)
    return decorated_function