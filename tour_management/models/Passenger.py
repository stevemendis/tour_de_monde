from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
# from tour_management import login_manager


class Passenger(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=True)
    phone_number = db.Column(db.String(255), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(255), nullable=False)
    passport_number = db.Column(db.String(255), nullable=False)
    my_orders_id = db.Column(db.Integer, db.ForeignKey('myorders.id'), nullable=True)
    temp_orders_id = db.Column(db.Integer, db.ForeignKey('myorderstemp.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    
    def __str__(self):
        return 'Passenger : {}'.format(self.name)