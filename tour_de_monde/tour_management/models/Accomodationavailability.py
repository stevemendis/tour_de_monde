from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
from tour_management import login_manager

class Accomodationavailability(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    accomodation_details_id = db.Column(db.Integer, db.ForeignKey('accomodationdetails.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    no_of_rooms = db.Column(db.Integer, default=0)
    

    def __str__(self):
        return 'Accomodation Availability :{}'.format(self.id)