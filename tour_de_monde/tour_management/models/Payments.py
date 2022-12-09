from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
from tour_management import login_manager

class Payments(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    my_orders_id = db.Column(db.Integer, db.ForeignKey('myorders.id'), nullable=False)
    cost = db.Column(db.Integer, default=0)
    payment_method = db.Column(db.String(255),nullable=False)
    completed = db.Column(db.Boolean, nullable = True, default=False)
    confirmation_reference = db.Column(db.String(255),nullable=False)
    billing_addr_1 = db.Column(db.String(255),nullable=False)
    billing_addr_2 = db.Column(db.String(255),nullable=True)
    zip_code = db.Column(db.String(255),nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    
    def __str__(self):
        return 'Payments:{}'.format(self.id)