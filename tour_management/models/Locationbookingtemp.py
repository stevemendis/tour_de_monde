from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from tour_management.models.utils import rand_pass
from flask_login import UserMixin
from tour_management import db
from tour_management import login_manager

class Locationbookingtemp(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    location_details_id = db.Column(db.Integer, db.ForeignKey('locationdetails.id'), nullable=False)
    cost = db.Column(db.Integer, default=0)
    no_of_people = db.Column(db.Integer, default=0)
    my_orders_id = db.Column(db.Integer, db.ForeignKey('myorderstemp.id'), nullable=False)

    def __str__(self):
        return 'Location Booking Temp :{}'.format(self.id)