from contextlib import nullcontext
from datetime import datetime, timedelta
from email.policy import default
import math,random
from tour_management.models.Activities import Activities
from tour_management.models.Location import Location
from tour_management.models.Locationdetails import LocationDetails
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
from tour_management import login_manager

class Activitylocation(db.Model, UserMixin):
    # Add the id of activity and location. WIll be a mix of both the location and the activity associated. Many-To-Many
    id = db.Column(db.Integer, primary_key=True)
    
    location_id = db.Column(db.Integer, db.ForeignKey('locationdetails.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # location = db.relationship(Locationdetails, backref=db.backref("ActivityLocation", cascade="all, delete-orphan"))
    # activity = db.relationship(Activities, backref=db.backref("ActivityLocation", cascade="all, delete-orphan"))

    def __str__(self):
        return 'ActivityLocation :{}'.format(self.name)