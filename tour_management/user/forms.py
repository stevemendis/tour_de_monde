import re
from flask_wtf import FlaskForm, Form
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField , SelectField, DateTimeLocalField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired
from flask_wtf.file import FileField, FileAllowed
from tour_management.models import User, Place

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    phone_number = StringField('Phone number', validators=[
        DataRequired(), Length(min=10, max=10)])
    dob = DateField('Date Of Birth',
                                validators=[InputRequired()])
    sex = StringField('Gender', validators=[
        DataRequired(), Length(min=1, max=10)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[Email()])
    
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Password Confirmation', validators=[
                                     DataRequired(), EqualTo('password')])
    terms_and_conditions = BooleanField(
        'I agree to the Security terms and conditions', validators=[DataRequired()])

    submit = SubmitField('Signup')
    # def validate_username(self, username):
    #     if not re.match('^[A-Za-z]+(?:[-][A-Za-z0-9]+)*$', username.data.lower()):
    #         raise ValidationError('Please enter valid characters')

    #     org = User.query.filter_by(username=username.data.lower()).first()
    #     if org:
    #         raise ValidationError('Username is aleady in use.')

    # def validate_email(self, email):
    #     org = User.query.filter_by(email=email.data.lower()).first()
    #     if org:
    #         raise ValidationError('Email is aleady in use.')

    # def validate_phone_number(self, phone_number):
    #     if not phone_number.data.isdigit():
    #         raise ValidationError('Only numeric values are allowed')
    
    # def validate_aadhar_number(self, aadhar_number):
    #     if not aadhar_number.data.isdigit():
    #         raise ValidationError('Only numeric values are allowed')


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


class LoginWithEmailForm(FlaskForm):
    email = StringField(
        'Enter Email Address', validators=[DataRequired()])
    submit = SubmitField('Login')

class ValidateotpForm(FlaskForm):
    otp = StringField(
        'Enter OTP', validators=[DataRequired()])
    submit = SubmitField('Verify')


class ResendValidateotpForm(FlaskForm):
    phone = StringField(
        'Enter Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_phone_number(self, phone_number):
        if not phone_number.data.isdigit():
            raise ValidationError('Only numeric values are allowed')


class DashboardForm(FlaskForm):
    source = StringField('Choose your source', [DataRequired()])
    destination = StringField('Choose your destination', [DataRequired()])
    inputCheckIn = DateField('Check In Date', validators=[InputRequired()])
    inputCheckOut = DateField('Check Out Date', validators=[InputRequired()])
    # submit = SubmitField('Submit')

    def validate_source(self, source):
        org = Place.query.filter_by(place=source.data.lower()).first()
        print("\n\n\n\n\n Hey Soruce Check")
        if org is None or org == []:
            raise ValidationError('Sorry we do not serve that location yet')
    
    def validate_destination(self, destination):
        org = Place.query.filter_by(place=destination.data.lower()).first()
        if org is None or org == []:
            raise ValidationError('Sorry we do not serve that location yet')

class FlightBookingForm(FlaskForm):
    source = StringField('Choose your source', [DataRequired()])
    destination = StringField('Choose your destination', [DataRequired()])
    adults = SelectField('Adults' , choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10')],validators=[InputRequired()])
    children = SelectField('Children' , choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')],validators=[InputRequired()])
    departure_date = DateField('Departure Date', format='%Y-%m-%d', validators=[InputRequired()])
    arrival_date = DateField('Arrival Date', format='%Y-%m-%d', validators=[InputRequired()])
    cabin_class = SelectField('Cabin Class' , choices=[('economy','Economy'), ('premium','Premium'), ('business','Business'), ('first','First')],validators=[InputRequired()])
    submit = SubmitField('Submit')

    def validate_source(self, source):
        org = Place.query.filter_by(place=source.data.lower()).first()
        print("\n\n\n\n\n Hey Soruce Check")
        if org is None or org == []:
            raise ValidationError('Sorry we do not serve that location yet')
    
    def validate_destination(self, destination):
        org = Place.query.filter_by(place=destination.data.lower()).first()
        if org is None or org == []:
            raise ValidationError('Sorry we do not serve that location yet')

class HotelBookingForm(FlaskForm):
    source = StringField('Choose your source', [DataRequired()])
    no_of_rooms = SelectField('How many rooms?' , choices=[('1','1 Room'), ('2','2 Rooms'), ('3','3 Rooms'), ('4','4 Rooms'), ('5','5 Rooms')],validators=[InputRequired()])
    adults = SelectField('Adults' , choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10')],validators=[InputRequired()])
    children = SelectField('Children' , choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')],validators=[InputRequired()])
    inputCheckIn = DateField('Check In Date', format='%Y-%m-%d', validators=[InputRequired()])
    inputCheckOut = DateField('Check Out Date', format='%Y-%m-%d', validators=[InputRequired()])
    submit = SubmitField('Submit')

    def validate_source(self, source):
        org = Place.query.filter_by(place=source.data.lower()).first()
        print("\n\n\n\n\n Hey Soruce Check")
        if org is None or org == []:
            raise ValidationError('Sorry we do not serve that location yet')
    
class MyordersForm(FlaskForm):
    username = StringField('Enter Your Username', validators=[
        DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Submit')


class PassengerInfo(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    dob = DateField('Date Of Birth',
                                validators=[InputRequired()])
    sex = StringField('Gender', validators=[
        DataRequired(), Length(min=1, max=10)])
    passport_number = StringField('Passport Number', validators=[
                           DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[Email()])
    
    submit = SubmitField('Next Passenger')

class PassengerInfoHotel(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(min=2, max=255)])
    dob = DateField('Date Of Birth',
                                validators=[InputRequired()])
    sex = StringField('Gender', validators=[
        DataRequired(), Length(min=1, max=10)])
    email = StringField('Email', validators=[Email()])
    
    submit = SubmitField('Next Passenger')



class LocationBookingForm(FlaskForm):
    source = StringField('Choose your source', [DataRequired()])
    activity_types = StringField('Choose your Activity Type')
    adults = SelectField('Adults' , choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10')],validators=[InputRequired()])
    children = SelectField('Children' , choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')],validators=[InputRequired()])
    inputCheckIn = DateField('Check In Date', format='%Y-%m-%d', validators=[InputRequired()])
    inputCheckOut = DateField('Check Out Date', format='%Y-%m-%d', validators=[InputRequired()])
    submit = SubmitField('Submit')

    def validate_source(self, source):
        org = Place.query.filter_by(place=source.data.lower()).first()
        
        if org is None or org == []:
            raise ValidationError('Sorry we do not serve that location yet')


class PaymentsForm(FlaskForm):
    
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    username = StringField('Username', [DataRequired()])
    address_1 = StringField('Address Line 1', [DataRequired()])
    address_2 = StringField('Address Line 2')
    email = StringField('Email', validators=[Email()])
    country = SelectField('Country' , choices=[('1','United States')],validators=[InputRequired()])
    state = SelectField('State' , choices=[('1','Florida'), ('2','Indiana'), ('3','Texas')],validators=[InputRequired()])
    zip_code = StringField('Zip Code', [DataRequired()])
    credit_card = StringField('Credit Card', [DataRequired()])
    name_on_card = StringField('Name On Card', [DataRequired()])
    expiration_date = StringField('Expiration Date', [DataRequired()])
    cvv_card =  StringField('CVV', [DataRequired()])
    submit = SubmitField('Submit')