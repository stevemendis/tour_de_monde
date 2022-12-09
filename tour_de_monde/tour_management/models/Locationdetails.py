from contextlib import nullcontext
from datetime import datetime, timedelta
from email.policy import default
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
# from tour_management import login_manager

# Similar to the activity table. Gives more details about what the activity is

class Locationdetails(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    average_review = db.Column(db.Integer, default=0)
    average_time = db.Column(db.Integer, nullable=True)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(255), nullable=False)
    owner_name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Integer, default=0)
    # activity_id = db.relationship("Activities", secondary=ActivityLocation)
    # activity_id = db.relationship('Activities', secondary=db.backref('Activity_location'), lazy='subquery',
        # backref=db.backref('Location_details', lazy=True))
    # activity_id = db.relationship('Activity_location',backref=db.backref('location_details'),lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Backref
    location_booking_id = db.relationship('Locationbooking',backref='locationdetails',lazy=True)
    location_booking_temp_id = db.relationship('Locationbookingtemp',backref='locationdetails',lazy=True)

    def __str__(self):
        return 'Location Details :{}'.format(self.name)