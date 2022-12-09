from datetime import datetime, timedelta
from email.policy import default
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
# from tour_management import login_manager

# Table related to the flight tickets. Mainly works to show what is the cost of each ticket
class Ticket(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # foreign key flight_details_id
    type = db.Column(db.String(255),nullable=False)
    min_cost = db.Column(db.Integer,default=0)
    max_cost = db.Column(db.Integer,default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    flights_id = db.Column(db.Integer, db.ForeignKey('flightdetails.id'), nullable=False)
    
    flight_details_id = db.relationship('Flightdetails',backref='ticket',lazy=True)

    def __str__(self):
        return 'Ticket: {}'.format(self.id)