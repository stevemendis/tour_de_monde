from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
from tour_management import login_manager

class Myorders(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    international = db.Column(db.Boolean, nullable = True, default=True)
    cost = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(255),nullable=False)
    destination = db.Column(db.String(255),nullable=False)
    individual = db.Column(db.Boolean, nullable = True, default=True)
    payment_completed = db.Column(db.Boolean, nullable = True, default=False)

    # Backref
    passenger_id = db.relationship('Passenger', backref='myorders', lazy=True)
    accomodation_id = db.relationship('Accomodationbooking', backref='myorders', lazy=True)
    flight_id = db.relationship('Flightbooking', backref='myorders', lazy=True)
    location_id = db.relationship('Locationbooking', backref='myorders', lazy=True)
    payment_id = db.relationship('Payments', backref='myorders', lazy=True)

    def __str__(self):
        return 'My Orders :{}'.format(self.id)