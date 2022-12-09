import re
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField, RadioField, DateTimeField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired
from flask_wtf.file import FileField, FileAllowed
from tour_management.models import Admin
from wtforms.fields import DateTimeLocalField

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=255)])
    employee_id = StringField('EmployeeID', validators=[
                               DataRequired(), Length(min=3, max=10)])
    email = StringField('Email', validators=[Email()])
    phone_number = StringField('Phone number', validators=[
                               DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Password Confirmation', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')
    def validate_username(self, username):
        if not re.match('^[A-Za-z]+(?:[-][A-Za-z0-9]+)*$', username.data.lower()):
            raise ValidationError('Please enter valid characters')

        org = Admin.query.filter_by(username=username.data).first()
        if org:
            raise ValidationError('Username is aleady in use.')

    def validate_employee_id(self, employee_id):
        org = Admin.query.filter_by(employee_id=employee_id.data).first()
        if org:
            raise ValidationError('EmployeeID aleady exists.')

    def validate_email(self, email):
        org = Admin.query.filter_by(email=email.data.lower()).first()
        if org:
            raise ValidationError('Email is aleady in use.')

    def validate_phone_number(self, phone_number):
        if not phone_number.data.isdigit():
            raise ValidationError('Only numeric values are allowed')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=255)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    submit = SubmitField('Login')



class ResendEmailConfirmationForm(FlaskForm):
    email = StringField(
        'Enter Email Address', validators=[DataRequired()])
    submit = SubmitField('Resend Email Confirmation')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        'Enter Email Address', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Password Confirmation', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Update new password')


class UpdateUsernameForm(FlaskForm):
    old_username = StringField('Old Username', validators=[
                                DataRequired(), Length(min=1, max=10)])
    username = StringField('Username', validators=[
                                DataRequired(), Length(min=1, max=10)])
    submit = SubmitField('Register')


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[
                             DataRequired(), Length(min=6)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    submit = SubmitField('Register')


class UpdateEmailForm(FlaskForm):
    old_email = StringField('Old Email', validators=[Email()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Register')


class SuperUserRegister(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=255)])
    employee_id = StringField('EmployeeID', validators=[
                               DataRequired(), Length(min=3, max=10)])
    email = StringField('Email', validators=[Email()])
    phone_number = StringField('Phone number', validators=[
                               DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Password Confirmation', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')
    def validate_username(self, username):
        if username == 'admin':
            raise ValidationError('This username is not permitted. Please choose another username')
        
        if not re.match('^[A-Za-z]+(?:[-][A-Za-z0-9]+)*$', username.data.lower()):
            raise ValidationError('Please enter valid characters')

        org = Admin.query.filter_by(username=username.data).first()
        if org:
            raise ValidationError('Username is aleady in use.')

    def validate_employee_id(self, employee_id):
        org = Admin.query.filter_by(employee_id=employee_id.data).first()
        if org:
            raise ValidationError('EmployeeID aleady exists.')

    def validate_password(self, password):
        if password == 'admin':
            raise ValidationError('This password is not permitted. Please choose another')

    def validate_phone_number(self, phone_number):
        if not phone_number.data.isdigit():
            raise ValidationError('Only numeric values are allowed')


class AddAdminsForm(FlaskForm):
    employee_id = StringField('EmployeeID', validators=[
                               DataRequired(), Length(min=3, max=10)])
    email = StringField('Email', validators=[Email()])

    role = RadioField('Role', choices=[('super_user','Super User'),('admin','Admin')])
    
    submit = SubmitField('Submit')

    def validate_employee_id(self, employee_id):
        org = Admin.query.filter_by(employee_id=employee_id.data).first()
        if org:
            raise ValidationError('EmployeeID aleady exists.')

    def validate_email(self, email):
        org = Admin.query.filter_by(email=email.data.lower()).first()
        if org:
            raise ValidationError('Email is aleady in use.')


class NewAdminRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=255)])
    phone_number = StringField('Phone number', validators=[
                               DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Password Confirmation', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')
    def validate_username(self, username):
        if username == 'admin':
            raise ValidationError('This username is not permitted. Please choose another username')
        
        if not re.match('^[A-Za-z]+(?:[-][A-Za-z0-9]+)*$', username.data.lower()):
            raise ValidationError('Please enter valid characters')

        org = Admin.query.filter_by(username=username.data).first()
        if org:
            raise ValidationError('Username is aleady in use.')

    def validate_password(self, password):
        if password == 'admin':
            raise ValidationError('This password is not permitted. Please choose another')

    def validate_phone_number(self, phone_number):
        if not phone_number.data.isdigit():
            raise ValidationError('Only numeric values are allowed')


class AddAccomodationForm(FlaskForm):
    place_name = StringField('HotelName', validators=[
                               DataRequired(), Length(min=3, max=20)])
    hotel_name = StringField('HotelName', validators=[
                               DataRequired(), Length(min=3, max=20)])
    address = StringField('Address', validators=[
                               DataRequired(), Length(min=3, max=40)])
    discount_code = StringField('DiscountCode', validators=[
                               DataRequired(), Length(min=3, max=10)])
    description = StringField('Description', validators=[
                               DataRequired(), Length(min=3, max=60)])
    email = StringField('Email', validators=[
                               DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Submit')

class AddAccomodationDetailsForm(FlaskForm):
    hotel_id = StringField('Hotel ID', validators=[
                               DataRequired(), Length(min=1, max=60)]) 
    room_name = StringField('RoomDescription', validators=[
                               DataRequired(), Length(min=3, max=60)])
    room_description = StringField('RoomDescription', validators=[
                               DataRequired(), Length(min=3, max=60)])
    room_capactiy = StringField('RoomCapactiy', validators=[
                               DataRequired(), Length(min=3, max=10)])
    min_price = StringField('MinPrice', validators=[
                               DataRequired(), Length(min=3, max=10)])
    max_price = StringField('MaxPrice', validators=[
                               DataRequired(), Length(min=3, max=10)])
    rooms_availble = StringField('RoomsAvailble', validators=[
                               DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Submit')


class CreateFlightForm(FlaskForm):
    flight_name = StringField('FlightName', validators=[
                               DataRequired(), Length(min=3, max=20)])
    international = BooleanField('Indternational')
    domestic = BooleanField('Domestic')
    discount_code = StringField('DiscountCode', validators=[
                               DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Submit')


class CreateFlightTicketForm(FlaskForm):
    flight_id = StringField('FlightID', validators=[
                               DataRequired(), Length(min=1, max=20)])
    type = StringField('Type', validators=[
                               DataRequired(), Length(min=3, max=20)])
    min_cost = StringField('MinCost', validators=[
                               DataRequired(), Length(min=3, max=10)])
    max_cost = StringField('MaxCost', validators=[
                               DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Submit')


class CreateFlightDetailsForm(FlaskForm):
    flight_name_res = StringField('FlightNameRes', validators=[
                               DataRequired(), Length(min=3, max=20)])
    flight_number = StringField('FlightMNumber', validators=[
                               DataRequired(), Length(min=3, max=10)])
    departure_date = DateField('Departure Date', format='%Y-%m-%d',
                                validators=[InputRequired()])
    arrival_date = DateField('Arrival Date', format='%Y-%m-%d', 
                                validators=[InputRequired()])                            
    departure_time = TimeField('Departure Time', format='%H:%M',
                                validators=[InputRequired()])
    arrival_time = TimeField('Arrival Time', format='%H:%M',
                                validators=[InputRequired()])
    number_of_seats = StringField('NumberOfSeats', validators=[
                               DataRequired(), Length(min=3, max=10)])
    source = StringField('Source', validators=[
                               DataRequired(), Length(min=3, max=10)])
    destination = StringField('Destination', validators=[
                               DataRequired(), Length(min=3, max=10)])
    vacant_seats = StringField('VacantSeats', validators=[
                               DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Submit')


class AddPlaceForm(FlaskForm):
    place = StringField('Place', validators=[
                               DataRequired(), Length(min=3, max=20)])
    code = StringField('Code', validators=[
                               DataRequired(), Length(min=3, max=10)])
    

class CreateLocationForm(FlaskForm):
    place_name = StringField('PlaceCode', validators=[
                               DataRequired(), Length(min=3, max=20)])
    name = StringField('Name', validators=[
                               DataRequired(), Length(min=3, max=10)])
    season_visit = StringField('SeasonVisit', validators=[
                               DataRequired(), Length(min=3, max=10)])
    address = StringField('Address', validators=[
                               DataRequired(), Length(min=3, max=10)])
    average_review = StringField('AverageReview', validators=[
                               DataRequired(), Length(min=1, max=1)])
    average_time = StringField('AverageTime', validators=[
                               DataRequired(), Length(min=1, max=1)])
    contact_email = StringField('ContactEmail', validators=[
                               DataRequired(), Length(min=3, max=10)])
    contact_phone = StringField('ContactPhone', validators=[
                               DataRequired(), Length(min=3, max=10)])
    owner_name = StringField('OwnerName', validators=[
                               DataRequired(), Length(min=3, max=10)])
    description = StringField('Description', validators=[
                               DataRequired(), Length(min=3, max=10)])
    cost = StringField('Cost', validators=[
                               DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Submit')