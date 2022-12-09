from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
from tour_management import login_manager

class Myorderstemp(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    international = db.Column(db.Boolean, nullable = True, default=True)
    cost = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(255),nullable=False)
    destination = db.Column(db.String(255),nullable=False)
    individual = db.Column(db.Boolean, nullable = True, default=True)
    booking_complete = db.Column(db.Boolean, nullable = True, default=False)
    
    passenger_id = db.relationship('Passenger', backref='myorderstemp', lazy=True)
    accomodation_temp_id = db.relationship('Accomodationbookingtemp', backref='myorderstemp', lazy=True)
    flight_temp_id = db.relationship('Flightbookingtemp', backref='myorderstemp', lazy=True)
    location_temp_id = db.relationship('Locationbookingtemp', backref='myorderstemp', lazy=True)

    
    def __str__(self):
        return 'My Orders Temp:{}'.format(self.id)