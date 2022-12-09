from datetime import datetime, timedelta
from email.policy import default
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
# from tour_management import login_manager

class Itinerary(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(255), nullable=False)
    number_of_days = db.Column(db.Integer, default=0)
    #foreign keys of place, flight details, accomodation, place
    name_of_trip = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __str__(self):
        return 'Itinerary: {}'.format(self.id)