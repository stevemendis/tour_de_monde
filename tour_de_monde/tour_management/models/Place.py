import code
from datetime import datetime, timedelta
from email.policy import default
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db


class Place(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    # I think something is wrong here. 
    location_details_id = db.relationship('Location',backref='place',lazy=True)
    accomodation_details_id = db.relationship('Accomodation',backref='place',lazy=True)
    # Back References
    
    def __str__(self):
        return 'Location:{}'.format(self.name)