from contextlib import nullcontext
from datetime import datetime, timedelta
from email.policy import default
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
# from tour_management import login_manager

class Activities(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    
    # location_id = db.relationship('Activity_location',backref='activities',lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


    def __str__(self):
        return 'Activities :{}'.format(self.name)
    
    
    # location_id = db.relationship("Location", secondary="ActivityLocation")