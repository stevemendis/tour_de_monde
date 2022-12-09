from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
# from tour_management import login_manager


class Flightdetails(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key= True)
    flight_number = db.Column(db.String(255),nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    number_of_seats = db.Column(db.Integer,default=0)
    source = db.Column(db.String(255),nullable=False)
    destination = db.Column(db.String(255),nullable=False)
    # write logic to self update vacant seats based on no of bookings
    vacant_seats = db.Column(db.Integer,default=0)
    
    flights_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Backref
    tickets_id = db.relationship('Ticket',backref='flightdetails',lazy=True)
    flight_booking_id = db.relationship('Flightbooking', backref='flightdetails', lazy=True)
    flight_booking_temp_id = db.relationship('Flightbookingtemp', backref='flightdetails', lazy=True)
    
    
    def __str__(self):
        return 'Flight Details:{}'.format(self.id)