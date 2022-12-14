from datetime import datetime, timedelta
from email.policy import default
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db


class Location(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # change activity_types to many to many with the ActivityLocation - DONE
    activity_types = db.Column(db.String(255),nullable = True)
    season_visit = db.Column(db.String(255),nullable = True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    # I think something is wrong here. 
    location_details_id = db.relationship('Locationdetails',backref='location',lazy=True)
    # Back References
    

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


    def __str__(self):
        return 'Location:{}'.format(self.name)
