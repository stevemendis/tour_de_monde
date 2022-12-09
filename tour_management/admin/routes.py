import email
from functools import wraps
from lib2to3.pgen2 import token
import re
from urllib import response
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, current_user, login_required, logout_user
from tour_management.admin.utils import admin_creation, no_admin, super_user
from tour_management.models import (Accomodation, 
                                    Accomodationdetails,
                                    Flightdetails,
                                    Flights,
                                    Location,
                                    Locationdetails,
                                    Place,
                                    Ticket,
                                    Admin,
                                    AdminToken)
from tour_management.models.utils import rand_pass
from tour_management import db, jwt
from tour_management.utilities.util_helpers import send_confirmation_mail
import json
from cerberus import Validator
from tour_management.schemas.admin_apis import admin_signup, admin_login
from flask_api import FlaskAPI, status, exceptions
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
from tour_management.admin.forms import (RegistrationForm,
                                            LoginForm,
                                            ResendEmailConfirmationForm,
                                            ResetPasswordRequestForm,
                                            ResetPasswordForm,
                                            UpdateUsernameForm,
                                            UpdatePasswordForm,
                                            UpdateEmailForm,
                                            SuperUserRegister,
                                            AddAdminsForm,
                                            NewAdminRegistrationForm,
                                            AddAccomodationForm,
                                            CreateFlightForm,
                                            CreateFlightTicketForm,
                                            CreateFlightDetailsForm,
                                            AddPlaceForm,
                                            CreateLocationForm,
                                            AddAccomodationDetailsForm)

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET', 'POST'])
@admin.route('/registration', methods=['GET', 'POST'])
@admin_creation
def registration():
        return redirect(url_for('admin.login'))


@admin.route('/login', methods=['GET', 'POST'])
@admin_creation
@no_admin
# create decorater to check if actually product is validated
def login():
    if current_user.is_authenticated:
        flash('You are aleady logged in.', 'info')
        return redirect(url_for('admin.dashboard'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data.lower()
        password = login_form.password.data
        org = Admin.query.filter_by(username=username).first()
        if org is None or org.check_password(password) is False:
            flash('Incorrect Username or Password', 'danger')
        elif not org.email_verified:
            flash('Your email is not verified Please verify email first', 'danger')
        elif not org.is_active:
            flash('Your Account is disabled.')
        else:
            login_user(org)
            flash('You are logged in successfully', 'info')
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/login.html', form=login_form)

@admin.route('/registration/admin/<string:token>' , methods=['GET','POST'])
@admin_creation
@no_admin
def register(token):
    token_info = AdminToken.query.filter_by(token=token).first()
    if token_info is None:
        flash('Invalid URL Token', 'danger')
        return redirect(url_for('admin.login'))
    else:
        if not token_info.is_valid():
            flash('Token is expired.', 'danger')
            return redirect(url_for('admin.login'))
        # Enter only if the token is valid.
        first_activation_status = Admin.query.filter_by(username='admin').first()
        if first_activation_status is not None:
            first_user = True
            activation_status = Admin.query.filter_by(id=token_info.id).first()
            if activation_status.first_login == False:
                if token_info.token_type == 'admin_activation':
                    form = SuperUserRegister()
                    if form.validate_on_submit():
                        org = Admin.query.filter_by(username='admin').first()
                        org.name = form.name.data
                        org.username = form.username.data.lower()
                        org.employee_id = form.employee_id.data
                        org.email = form.email.data.lower()
                        org.phone_number = form.phone_number.data
                        org.first_login = True
                        org.password = Admin.hash_password(form.password.data)
                        org.role = 'super_user'
                        # Change These Two once email api is working
                        org.email_verified = True
                        org.is_active = True
                        db.session.commit()
                        flash('Admin signed up successfully', 'success')
                        return redirect(url_for('admin.login'))
                    return render_template('admin/register.html', form = form, item = first_user)
                else:
                    flash ('Invalid Token Type', 'danger')
                    return redirect(url_for('admin.login'))
        else:
            first_user = False
            if token_info.token_type == 'admin_token':
                form = NewAdminRegistrationForm()
                if form.validate_on_submit():
                    admin_id = token_info.admin_id
                    org = Admin.query.filter_by(id = admin_id).first()
                    if org is None or org == []:
                        flash('You need to log in to add admins','danger')
                        return redirect(url_for('admin.login'))
                    else:
                        org.name = form.name.data
                        org.username = form.username.data.lower()
                        org.phone_number = form.phone_number.data
                        org.password = Admin.hash_password(form.password.data)
                        db.session.commit()
                        flash('User signed up successfully', 'success')
                        return redirect(url_for('admin.login'))
                return render_template('admin/register.html', form = form, item = first_user)
            else:
                flash ('Invalid Token Type', 'danger')
                return redirect(url_for('admin.login'))



@admin.route('/add/admins' , methods=['GET','POST'])
@login_required
@super_user
def add_admins():
    form = AddAdminsForm()
    if form.validate_on_submit():
        org = Admin()
        org.employee_id = form.employee_id.data
        org.email = form.email.data
        org.role = form.role.data
        db.session.add(org)
        db.session.commit()
        if org.role == 'super_user':
            super_user_conf_token = AdminToken.generate_token('admin_token', org.id, 1800)
            # send_registration_mail(org.email, url_for('.registration_confirmation',token=super_user_conf_token.token, _external=True))
            flash('Super User is successfully created', 'info')
        elif org.role == 'admin':
            admin_token = AdminToken.generate_token('admin_token', org.id, 1800)
            # send_registration_mail(org.email,url_for('.registration_confirmation',token=admin_token.token, _external=True))
            flash('Admin is successfully created', 'info')
        else:
            flash('error detected' , 'danger')
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_admins.html', form=form)


@admin.route('/registration/confirmation/<string:token>')
@admin_creation
def registration_confirmation(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    token_info = AdminToken.query.filter_by(token=token).first()

    if not token_info:
        flash('Invalid registration confirmation token', 'danger')
        return redirect(url_for('admin.login'))
    
    if not token_info.is_valid():
        flash('Token is expired. Please get new registration confirmation link', 'danger')
        return redirect('admin.login')
    token_info.admin.email_verified = True
    token_info.admin.is_active = True
    db.session.commit()
    flash('Email has been verified', 'success')
    return redirect(url_for('admin.register',token=token, _external=True))

@admin.route('/reset-password-request', methods=['GET', 'POST'])
@admin_creation
@no_admin
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        org = Admin.query.filter_by(email=email).first()
        if not org:
            flash('Email address is not registered with us. Please signup', 'info')
            return redirect(url_for('admin.registration'))
        if not org.email_verified:
            flash('Email is not verified. Please verify email first', 'danger')
            return redirect(url_for('admin.login'))
        if not org.is_active:
            flash('Your account has been deactivated Please contact admin', 'info')
            return redirect(url_for('admin.login'))
        reset_password_token = AdminToken.generate_token(
            'reset_password', org.id, 1800)
        # send_reset_password_mail(org.email,
        #                          url_for('admin.reset_password',
        #                                  token=reset_password_token.token, _external=True))
        flash('Reset password link has been sent to your email address', 'info')
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_password_request.html', form=form)

#Password reset
@admin.route('/reset-password/<string:token>', methods=['GET', 'POST'])
@admin_creation
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    token_info = AdminToken.query.filter_by(
        token=token, token_type='reset_password').first()

    if not token_info:
        flash('Invalid Reset password token', 'danger')
        return redirect(url_for('admin.login'))
    if not token_info.is_valid():
        flash('Token is expired. Please get new email confirmation link', 'danger')
        return redirect('admin.login')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        token_info.admin.password = Admin.hash_password(password)
        db.session.commit()
        flash('Your password has been updated. Please login with new password', 'success')
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_password.html', form=form)

@admin.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('admin/profile.html', org=current_user)

@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # user_data = User.query.count()
    # prop_data = Property.query.filter_by(is_active = True).count()
    # bill_data = Metertransactionlog.query.count()
    # server_data = Iotserver.query.filter_by(server_reg_confirm = True).count()
    # admin_data = Admin.query.filter_by(is_active = True).count()
    # device_data = Iotdevice.query.filter_by(device_reg_confirm = True).count()
    # data = [user_data,prop_data,bill_data,server_data,admin_data,device_data]
    # return render_template('admin/dashboard.html', data = data)
    return render_template('admin/dashboard.html')


@admin.route('/logout')
# @login_required
def logout():
    logout_user()
    flash('You are logged out successfully.', 'info')
    return redirect(url_for('admin.login'))
    
    
    
@admin.route('/add/accomodation' ,methods=['GET','POST'])
def create_accomodation():
    place_data = Place.query.all()
    form = AddAccomodationForm()
    if form.validate_on_submit():
        place_name = form.place_name.data.lower()
        place_obj = Place.query.filter_by(place=place_name).first()
        if place_obj is None or place_obj == []:
            flash('Please register a Place', 'info')
            return redirect(url_for('admin.create_accomodation'))
        
        tempAccomodation = Accomodation()
        tempAccomodation.hotel_name = form.hotel_name.data
        tempAccomodation.address = form.address.data
        tempAccomodation.discount_code = form.discount_code.data
        tempAccomodation.description = form.description.data
        tempAccomodation.email = form.email.data
        tempAccomodation.place_id = place_obj.id
        try:
            db.session.add(tempAccomodation)
            db.session.commit()
        except Exception as err:
            flash('Could not register Accomodation', 'info')
            return redirect(url_for('admin.create_accomodation'))
        else:
            flash('Successfully Registed Hotel. Please add Room Types', 'info')
            return redirect(url_for('admin.create_accomodation_details'))
    return render_template('admin/add_accomodation.html', form=form, place=place_data)


    #Take a hotel name, location, discount code and description 
    #Accomodation detial, will take room capacity, rooms availble, min and max prce and a description 

@admin.route('/add/accomodation/details' ,methods=['GET','POST'])
def create_accomodation_details():
    accomodation_data = Accomodation.query.all()
    form = AddAccomodationDetailsForm()
    if form.validate_on_submit():
        
        tempAccDetails = Accomodationdetails()
        tempAccDetails.accomodation_id = form.hotel_id.data
        tempAccDetails.room_name = form.room_name.data
        tempAccDetails.description = form.room_description.data
        tempAccDetails.room_capacity = form.room_capactiy.data
        tempAccDetails.min_price = form.min_price.data
        tempAccDetails.max_price = form.max_price.data
        tempAccDetails.rooms_availble = form.rooms_availble.data
        try:
            db.session.add(tempAccDetails)
            db.session.commit()
        except Exception as err:
            flash('Could Not Register Accomodation Details', 'danger')
            return redirect(url_for('admin.create_accomodation_details'))
        else:
            flash('Added Accomodation Details.', 'info')
            return redirect(url_for('admin.create_accomodation_details'))
    return render_template('admin/add_accomodation_details.html', form=form, items=accomodation_data)


@admin.route('/add/flight' ,methods=['GET','POST'])
def create_flight():
    flight_data = Flights.query.all()
    form = CreateFlightForm()
    if form.validate_on_submit():

        tempFlights = Flights()
        tempFlights.flight_name = form.flight_name.data.lower()
        tempFlights.international = form.international.data
        tempFlights.domestic = form.domestic.data
        tempFlights.discount_code = form.discount_code.data
        
        try:
            db.session.add(tempFlights)
            db.session.commit()
        except Exception as err:
            flash('Data Already Present/ Data Format Incorrect', 'danger')
            return redirect(url_for('admin.create_flight'))
        else:
            flash('Added Flight Data', 'info')
            return redirect(url_for('admin.create_flight'))
    return render_template('admin/create_flight.html', form=form, items=flight_data)

@admin.route('/add/ticket' ,methods=['GET','POST'])
def create_flight_ticket():
    # Add flight company name and pick id from it and add logic to add it to this db
    flight_data = Flightdetails.query.all()
    form = CreateFlightTicketForm()
    if form.validate_on_submit():
        tempTicket = Ticket()
        # flight_id
        tempTicket.flights_id = form.flight_id.data
        tempTicket.type = form.type.data
        tempTicket.min_cost = form.min_cost.data
        tempTicket.max_cost = form.max_cost.data

        try:
            db.session.add(tempTicket)
            db.session.commit()
        except Exception as err:
            flash('Could not register Flight Ticket Data','danger')
            return redirect(url_for('admin.create_flight_ticket'))
        else:
            flash('Ticket Data Added Successfully.','info')
            return redirect(url_for('admin.create_flight_ticket'))
    return render_template('admin/create_flight_ticket.html', form=form, items=flight_data)

@admin.route('/add/flight/details' ,methods=['GET','POST'])
def create_flight_details():
    place_data = Place.query.all()
    flight_data = Flights.query.all()
    form = CreateFlightDetailsForm()
    print('form')
    if form.validate_on_submit():
        print('ENtered')
        source_present = Place.query.filter_by(place = form.source.data.lower()).all()
        destination_present = Place.query.filter_by(place = form.destination.data.lower()).all()
        if form.source.data.lower() == form.destination.data.lower():
            flash('Source And Destination are the same', 'danger')
            return redirect(url_for('admin.create_flight_details'))
        if source_present is None or source_present == [] or destination_present is None or destination_present == []:
            flash('Please Enter Valid Souce or Destination', 'danger')
            return redirect(url_for('admin.create_flight_details'))
        flight_name_res = form.flight_name_res.data
        temp_flights_id = Flights.query.filter_by(flight_name=flight_name_res).first()
        if temp_flights_id is None or temp_flights_id == [] :
            flash('Could not find Flight Company', 'danger')
            return redirect(url_for('admin.create_flight_details'))
        # Change ticket logic. Change dependency with Flight Details.
        temp_flights_details_id = Flightdetails()
        temp_flights_details_id.flight_number = form.flight_number.data
        temp_flights_details_id.arrival_date = form.arrival_date.data
        temp_flights_details_id.departure_date = form.departure_date.data
        temp_flights_details_id.arrival_time = form.arrival_time.data
        temp_flights_details_id.departure_time = form.departure_time.data
        temp_flights_details_id.number_of_seats = form.number_of_seats.data
        temp_flights_details_id.source = form.source.data.lower()
        temp_flights_details_id.destination = form.destination.data.lower()
        temp_flights_details_id.vacant_seats = form.vacant_seats.data
        temp_flights_details_id.flights_id = temp_flights_id.id
        try:
            db.session.add(temp_flights_details_id)
            db.session.commit()
        except Exception as err:
            flash('Could not register Flight Details','danger')
            return redirect(url_for('admin.create_flight_details'))
        else:
            flash('Successfully add flight details.', 'info')
            return redirect(url_for('admin.create_flight_details'))
    return render_template('admin/create_flight_details.html', form=form, items=flight_data, place=place_data)


@admin.route('/add/place' ,methods=['GET', 'POST'])
@login_required
@admin_creation
def create_place():
    place_data = Place.query.all()
    form = AddPlaceForm()
    
    if form.validate():
        if request.form['submit'] == 'delete':
            code = request.form.get('code').lower()
            place = request.form.get('place').lower() 
            print(code)
            print(place)
            place_enter_data = Place.query.filter_by(place = place, code = code).all()
            if place_enter_data is None or place_enter_data == []:
                flash('Data Not Present.', 'danger')
                return redirect(url_for('admin.create_place'))
            else:
                Place.query.filter_by(place = place, code = code).delete()
                db.session.commit()
                flash('Data Deleted.','info')
                return redirect(url_for('admin.create_place'))
        
        elif request.form['submit'] == 'submit':
            tempPlace = Place()

            tempPlace.place = form.place.data.lower()
            tempPlace.code = form.code.data.lower()
            
            try:
                db.session.add(tempPlace)
                db.session.commit()
            except Exception as err:
                flash('Could Not Add New Place', 'danger')
                return redirect(url_for('admin.create_place'))
            else:
                flash('New Location Added', 'info')
                return redirect(url_for('admin.create_place'))
    if place_data is None or place_data == []:
        return render_template('admin/add_place.html', form=form, items=None)        
    else:
        return render_template('admin/add_place.html', form=form, items=place_data)


@admin.route('/add/location' ,methods=['GET','POST'])
@login_required
@admin_creation
def create_location():
    place_data = Place.query.all()
    form = CreateLocationForm()
    if form.validate_on_submit():
        place_name = form.place_name.data
        place_obj = Place.query.filter_by(code=place_name).first()
        if place_obj is None or place_obj == []:
            flash('Please register a Place', 'danger')
            return redirect(url_for('admin.create_location'))
        
        tempLocation = Location()
        tempLocation.name = form.name.data
        tempLocation.season_visit = form.season_visit.data
        tempLocation.place_id = place_obj.id
        try:
            db.session.add(tempLocation)
            db.session.commit()
        except Exception as err:
            flash('Could not register Location', 'danger')
            return redirect(url_for('admin.create_location'))
        else:
            # Need to add unique constraint here
            location_obj = Location.query.filter_by(name=tempLocation.name).first()
            if location_obj is None or location_obj == []:
                flash('Please register a Location', 'danger')
                return redirect(url_for('admin.create_location'))
            
            tempLocationDetails = Locationdetails()
            tempLocationDetails.location_id = location_obj.id
            tempLocationDetails.address = form.address.data
            tempLocationDetails.average_review = form.average_review.data
            tempLocationDetails.average_time = form.average_time.data
            tempLocationDetails.contact_email = form.contact_email.data
            tempLocationDetails.contact_phone = form.contact_phone.data
            tempLocationDetails.owner_name = form.owner_name.data
            # tempLocationDetails.image = request.json.get("image",None)
            tempLocationDetails.description = form.description.data
            tempLocationDetails.cost = form.cost.data
            try:
                db.session.add(tempLocationDetails)
                db.session.commit()
            except Exception as err:
                flash('Could not register Location Details', 'danger')
                return redirect(url_for('admin.create_location'))
            else:
                flash('Added Location and Location Details', 'info')
                return redirect(url_for('admin.create_location'))
    return render_template('admin/create_location.html', form=form, items=place_data)



@admin.route('/view/place' ,methods=['GET','POST'])
def view_place():
    place_data = Place.query.all()
    return render_template('admin/view_place.html', items=place_data)

@admin.route('/view/flights' ,methods=['GET','POST'])
def view_flights():
    flight_data = Flights.query.all()
    return render_template('admin/view_flights.html', items=flight_data)

@admin.route('/view/accomodation' ,methods=['GET','POST'])
def view_accomodation():
    place_accomodation = Accomodation.query.all()
    return render_template('admin/view_accomodation.html', items=place_accomodation)

@admin.route('/view/flight/details' ,methods=['GET','POST'])
def view_flight_details():
    flight_details_data = Flightdetails.query.all()
    return render_template('admin/view_flight_details.html', items=flight_details_data)

@admin.route('/view/accomodation/details' ,methods=['GET','POST'])
def view_accomodation_details():
    accomodation_details_data = Accomodationdetails.query.all()
    return render_template('admin/view_accomodation_details.html', items=accomodation_details_data)

@admin.route('/view/location/details' ,methods=['GET','POST'])
def view_location_details():
    location_details_data = Locationdetails.query.all()
    return render_template('admin/view_location_details.html', items=location_details_data)