from flask import Flask
# from flask_api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from tour_management.config import DevelopmentConfig
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from twilio.rest import Client


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()
sms_client = Client(DevelopmentConfig.TWILIO_ACCOUNT_SID, DevelopmentConfig.TWILIO_AUTH_TOKEN)
# sms_client = Client()
login_manager = LoginManager()
login_manager.login_message = 'Please login to continue'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
# limiter = Limiter(key_func=get_remote_address)

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    jwt.init_app(app)
    db.init_app(app)
    # sms_client.init_app(app)
    # limiter.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    mail.init_app(app)
    from tour_management.models.Accomodation import Accomodation
    from tour_management.models.Accomodationdetails import Accomodationdetails
    from tour_management.models.User import User
    from tour_management.models.UserToken import UserToken
    from tour_management.models.Admin import Admin
    from tour_management.models.AdminToken import AdminToken
    from tour_management.models.Flights import Flights
    from tour_management.models.Flightdetails import Flightdetails
    from tour_management.models.Itinerary import Itinerary
    from tour_management.models.Itinerarytype import Itinerarytype
    from tour_management.models.Location import Location
    from tour_management.models.Locationdetails import Locationdetails
    from tour_management.models.Myorders import Myorders
    from tour_management.models.Myorderstemp import Myorderstemp
    from tour_management.models.Ticket import Ticket
    from tour_management.models.Activities import Activities
    from tour_management.models.Place import Place
    from tour_management.models.Accomodationavailability import Accomodationavailability
    from tour_management.models.Accomodationbooking import Accomodationbooking
    from tour_management.models.Accomodationbookingtemp import Accomodationbookingtemp
    from tour_management.models.Flightbooking import Flightbooking
    from tour_management.models.Flightbookingtemp import Flightbookingtemp
    from tour_management.models.Locationbooking import Locationbooking
    from tour_management.models.Locationbookingtemp import Locationbookingtemp
    from tour_management.models.Passenger import Passenger
    from tour_management.models.Payments import Payments
    from tour_management.auth import utils
    from tour_management.error_handler.routes import handle_error_404, handle_error_500, handle_error_429
    from tour_management.user.routes  import user
    from tour_management.admin.routes import admin
    from tour_management.main.routes import main
    # from iot_security.api.routes import api
    app.register_error_handler(404, handle_error_404)
    app.register_error_handler(500, handle_error_500)
    app.register_error_handler(429, handle_error_429)
    # app.register_blueprint(user)
    login_manager.blueprint_login_views = {
        'admin' : '/admin/login',
        'user' : '/user/login'
    }
    app.register_blueprint(main)
    app.register_blueprint(admin,url_prefix='/admin')
    app.register_blueprint(user,url_prefix='/user')
    

    with app.app_context():
        db.create_all()
        db.session.commit()
    return app
