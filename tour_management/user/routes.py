from functools import wraps
from lib2to3.pgen2 import token
from urllib import response
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, current_user, login_required, logout_user
from tour_management.models import (User, 
                                    UserToken,
                                    Myorders, 
                                    Location, 
                                    Place, 
                                    Myorderstemp,
                                    Myorders,
                                    Accomodation,
                                    Flights,
                                    Flightdetails,
                                    Locationdetails,
                                    Accomodationdetails,
                                    Ticket,
                                    Flightbookingtemp,
                                    Flightbooking,
                                    Passenger,
                                    Accomodationbookingtemp,
                                    Accomodationbooking,
                                    Locationbooking,
                                    Locationbookingtemp,
                                    Payments)

from tour_management.models.utils import rand_pass
from tour_management import db, jwt
from tour_management.utilities.util_helpers import send_confirmation_mail
import json
import random, string
from cerberus import Validator
from tour_management.schemas.user_apis import user_signup, user_login
from flask_api import FlaskAPI, status, exceptions
from tour_management.user.utils import send_reset_password_mail
from tour_management.user.forms import (SignupForm,
                                        LoginForm,
                                        ValidateotpForm,
                                        ResendValidateotpForm,
                                        ResendEmailConfirmationForm,
                                        ResetPasswordRequestForm,
                                        ResetPasswordForm,
                                        DashboardForm,
                                        HotelBookingForm,
                                        FlightBookingForm,
                                        MyordersForm,
                                        PassengerInfo,
                                        PassengerInfoHotel,
                                        LocationBookingForm,
                                        PaymentsForm)

user = Blueprint('user', __name__)



@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('You are aleady logged in.', 'info')
        return redirect(url_for('.dashboard'))
    signup_form = SignupForm()
    print("Entered Signup")
    if signup_form.validate_on_submit():
        print("Entered Signup Now")
        org = User()
        print("User Object Created")
        org.first_name = signup_form.first_name.data
        org.last_name = signup_form.last_name.data
        org.phone_number = signup_form.phone_number.data
        org.dob = signup_form.dob.data
        org.sex = signup_form.sex.data
        org.username = signup_form.username.data.lower()
        org.email = signup_form.email.data
        org.password = User.hash_password(signup_form.password.data)
        print("Accepted Data")
        try :
            db.session.add(org)
            db.session.commit()
        except Exception as err:
            print ('Error Logged : ', err)
            flash('Signup Failed', 'danger')
            return redirect(url_for('user.signup'))
        else:
            email_conf_token = UserToken.generate_token(
                'email_confirmation', org.id, 1800)
            otp = User.generate_smcode(org.id, 180)
            try:
                send_confirmation_mail(org.email,
                                   url_for('user.email_confirmation',
                                           token=email_conf_token.token, _external=True), otp=otp)
            except Exception as err:
                print ('Error Logged : ', err)
                flash('Email sending failed', 'danger')
                return redirect(url_for('user.signup'))
            else:
                return redirect(url_for('user.validate_OTP'))

    return render_template('user/signup.html', form=signup_form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are aleady logged in.', 'info')
        return redirect(url_for('.dashboard'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data.lower()
        password = login_form.password.data
        org = User.query.filter_by(username=username).first()
        if org is None or org.check_password(password) is False:
            flash('Incorrect Username or Password', 'danger')
        elif not org.email_verified:
            flash('Your email is not verified Please verify email first', 'danger')
            return redirect(url_for('user.send_email_confirmation'))
        elif not org.valid_sm_code:
            flash('Your OTP is not verified Please verify OTP first', 'danger')
            return redirect(url_for('user.resend_validate_OTP'))
        elif not org.is_active:
            flash('Your Account is disabled. Please contact admin')
        else:
            login_user(org, remember=True)
            flash('You have logged in successfully', 'info')
            
            return redirect(url_for('user.dashboard'))
    return render_template('user/login.html', form=login_form)


# Validate users OTP
@user.route('/validate_otp', methods=['GET', 'POST'])
def validate_OTP():
    if current_user.is_authenticated:
        flash('You are aleady logged in.', 'info')
        return redirect(url_for('user.dashboard'))
    otp_form = ValidateotpForm()
    if otp_form.validate_on_submit():
        valid_sm = User.query.filter_by(sm_code=otp_form.otp.data).first()

        if valid_sm is None:
            flash('Invalid OTP', 'danger')
            return redirect(url_for('user.login'))

        if not valid_sm.is_valid():
            flash('OTP is expired. Please get new OTP', 'danger')
            return redirect('.login')
        else:
            valid_sm.valid_sm_code = True
            db.session.commit()
            flash('OTP verified', 'success')
            flash('User signed up successfully', 'success')
            return redirect(url_for('user.login'))
    return render_template('user/validate_otp.html', form=otp_form)



# Resend OTP incase of expiry
@user.route('/resend_validate_otp', methods=['GET', 'POST'])
def resend_validate_OTP():
    if current_user.is_authenticated:
        flash('You are aleady logged in.', 'info')
        return redirect(url_for('.dashboard'))
    otp_form = ResendValidateotpForm()
    if otp_form.validate_on_submit():
        valid_smcode = User.query.filter_by(phone_number=otp_form.phone.data).first()
    
        if valid_smcode is None:
            flash('Mobile Number Not Registered', 'danger')
            return redirect(url_for('.signup'))
        elif valid_smcode.valid_sm_code:
            flash('OTP Already Validated', 'danger')
            return redirect(url_for('.login'))
        else:
            User.generate_smcode(valid_smcode.id, 1800)
            flash('OTP Sent', 'success')
            return redirect(url_for('.validate_OTP'))
    return render_template('user/resend_validate_otp.html', form=otp_form)
    

@user.route('/' , methods=['GET', 'POST'])
def index():
    # dashboard_form = DashboardForm()
    return render_template('user/index.html')


@user.route('/dashboard' , methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardForm()
    if form.validate_on_submit():
        source = form.source.data.lower()
        destination = form.destination.data.lower()
        
        # Add booking Id, No of People, No of rooms to every request              
        flash('We Do serve your source and destination. Go ahead book flights, hotels, activities', 'info')
        
        return redirect(url_for('user.dashboard'))
    return render_template('user/dashboard.html', form=form)

@user.route('/booking/flights/start/<string:booking_id>/<string:no_of_people>/<string:no_of_rooms>' , methods=['GET', 'POST'])
@login_required
def book_flights(booking_id, no_of_people, no_of_rooms):
    my_orders_temp = Myorderstemp.query.filter_by(id=booking_id).first()
    if my_orders_temp is None or my_orders_temp == []:
        flash('Booking Failed. Please start again', 'danger')
        return redirect(url_for('user.dashboard'))
    # Invoice.query.filter(Invoice.invoicedate >= date.today())
    source = my_orders_temp.source
    destination = my_orders_temp.destination
    start_date = my_orders_temp.start_date

    # flights_data = Flightdetails.query.filter_by(source=source, destination=destination, departure_date_time=start_date, ).all()
    # if flights_data is None or flights_data == []:
        
    #     Myorderstemp.query.filter_by(id = booking_id).delete()
    return "Wait. Work in Progress"



@user.route('/location_booking' , methods=['GET', 'POST'])
@login_required
def location_booking():
    
    items = None
    form = LocationBookingForm()
    if form.validate_on_submit():
        source = form.source.data.lower()
        activity_types = form.activity_types.data.lower()
        number_of_people = int(form.adults.data) + int(form.children.data)
        departure_date = form.inputCheckIn.data
        arrival_date = form.inputCheckOut.data
        adults = int(form.adults.data)
        children = int(form.children.data)

        place_temp = Place.query.filter_by(place=source).first()
        
        location_details = (db.session.query(Location, Locationdetails)
                .join(Location, Locationdetails.location_id == Location.id)
                .filter(Location.place_id == place_temp.id)
                .all())
        
        items = []
        for acc, acc_d in location_details:
            # print("\n\n\n\n\n\n\n",acc.hotel_name, acc_d.rooms_availble)
            temp_dict = {}
            temp_dict['location_name'] = acc.name
            temp_dict['location_id'] = acc_d.id
            temp_dict['activity_types'] = acc.activity_types
            temp_dict['no_of_people'] = number_of_people
            temp_dict['cost'] = acc_d.cost
            temp_dict['season_visit'] = acc.season_visit
            temp_dict['start_date'] = departure_date
            temp_dict['address'] = acc_d.address
            temp_dict['average_review'] = acc_d.average_review
            temp_dict['average_time'] = acc_d.average_time
            temp_dict['description'] = acc_d.description
            temp_dict['end_date'] = arrival_date
            print(temp_dict)
            items.append(temp_dict)
        print(items)
        print("ASD",items)
        return render_template('user/location_booking.html', form=form, items = items)
        
    return render_template('user/location_booking.html', form=form, items = items)


@user.route('/location_booking/confim/<string:location_name>/<string:no_of_people>/<string:cost>/<string:season_visit>/<string:start_date>/<string:address>/<string:average_review>/<string:average_time>/<string:description>/<string:end_date>/<string:location_id>' , methods=['GET', 'POST'])
@login_required
def location_booking_confirm(location_name, no_of_people, cost, season_visit, start_date, address, average_review, average_time, description, end_date, location_id):
    location_name = location_name
    no_of_people = no_of_people
    cost = cost
    season_visit = season_visit
    start_date = start_date
    address = address
    average_review = average_review
    average_time = average_time
    description = description
    end_date = end_date
    location_id = location_id
    user_id = current_user.id

    temp_orders = Myorderstemp()
    temp_orders.user_id = user_id
    temp_orders.international = True
    temp_orders.cost = int(cost)*int(no_of_people)
    temp_orders.start_date = start_date
    temp_orders.end_date = end_date
    temp_orders.source = "location"
    temp_orders.destination = "location"
    temp_orders.individual = True
    temp_orders.booking_complete = False
    db.session.add(temp_orders)
    db.session.commit()
    temp_orders = Myorderstemp.query.filter_by(user_id = user_id, international = True, start_date = start_date, end_date=end_date, source = 'location', destination = 'location', booking_complete=False).first()
    
    location_booking_temp = Locationbookingtemp()
    location_booking_temp.location_details_id = location_id
    location_booking_temp.cost = int(cost)*int(no_of_people)
    location_booking_temp.no_of_people = int(no_of_people)
    location_booking_temp.my_orders_id = temp_orders.id
    db.session.add(location_booking_temp)
    db.session.commit()
    # return redirect(url_for('user.hotelpassengerinfo', booking_id=temp_orders.id,no_of_people=no_of_rooms, current_passenger=1, _external=True))
    return redirect(url_for('user.payments', booking_id=temp_orders.id, cost=cost, flights=0 ,hotels=0 ,location=1 ,_external=True))
    



@user.route('/hotel_booking' , methods=['GET', 'POST'])
@login_required
def hotel_booking():
    
    items = None
    form = HotelBookingForm()
    if form.validate_on_submit():
        source = form.source.data.lower()
        number_of_people = int(form.adults.data) + int(form.children.data)
        number_of_rooms = int(form.no_of_rooms.data)
        departure_date = form.inputCheckIn.data
        arrival_date = form.inputCheckOut.data
        no_of_rooms = int(number_of_rooms)
        adults = int(form.adults.data)
        children = int(form.children.data)
        
        print("\n\n\n\n\n Hey Rooms Check", no_of_rooms, adults, children)
        if (2*no_of_rooms) < (adults+children):
            flash('Please Add more rooms as 1 Room Serves 2 People.', 'danger')
            return render_template('user/hotel_booking.html', form=form, items = items)
        
        place_temp = Place.query.filter_by(place=source).first()
        
        hotel_details = (db.session.query(Accomodation, Accomodationdetails)
                .join(Accomodation, Accomodationdetails.accomodation_id == Accomodation.id)
                .filter(Accomodation.place_id == place_temp.id)
                .all())
        
        items = []
        for acc, acc_d in hotel_details:
            print("\n\n\n\n\n\n\n",acc.hotel_name, acc_d.rooms_availble)
            temp_dict = {}
            temp_dict['hotel_name'] = acc.hotel_name
            temp_dict['description'] = acc.description
            temp_dict['no_of_rooms'] = number_of_rooms
            temp_dict['cost'] = str(random.randrange(acc_d.min_price,acc_d.max_price)) 
            temp_dict['room_name'] = acc_d.room_name
            temp_dict['start_date'] = departure_date
            temp_dict['end_date'] = arrival_date
            temp_dict['rooms_availble'] = acc_d.rooms_availble
            temp_dict['room_description'] = acc_d.description
            temp_dict['accomodation_details_id'] = acc_d.id
            # temp_dict = json.dumps(temp_dict)
            print(temp_dict)
            items.append(temp_dict)
        print(items)
        # items = json.dumps(items)
        # items = json.loads(items)
        print("ASD",items)
        return render_template('user/hotel_booking.html', form=form, items = items)
        
    return render_template('user/hotel_booking.html', form=form, items = items)




@user.route('/hotel_booking/confim/<string:hotel_name>/<string:description>/<string:no_of_rooms>/<string:room_name>/<string:accomodation_details_id>/<string:room_description>/<string:rooms_availble>/<string:start_date>/<string:end_date>/<string:cost>' , methods=['GET', 'POST'])
@login_required
def hotel_booking_confirm(hotel_name, description, no_of_rooms, room_name, accomodation_details_id, room_description, rooms_availble, start_date, end_date, cost):
    hotel_name = hotel_name
    description = description
    no_of_rooms = no_of_rooms
    room_name = room_name
    accomodation_details_id = accomodation_details_id
    room_description = room_description
    rooms_availble = rooms_availble
    start_date = start_date
    end_date = end_date
    cost = cost
    user_id = current_user.id
    # Booking Temp Orders
    temp_orders = Myorderstemp()
    temp_orders.user_id = user_id
    #change later
    temp_orders.international = True
    temp_orders.cost = int(cost)*int(no_of_rooms)
    temp_orders.start_date = start_date
    temp_orders.end_date = end_date
    temp_orders.source = "hotel"
    temp_orders.destination = "hotel"
    temp_orders.individual = True
    temp_orders.booking_complete = False
    db.session.add(temp_orders)
    db.session.commit()
    temp_orders = Myorderstemp.query.filter_by(user_id = user_id, international = True, start_date = start_date, end_date=end_date, source = 'hotel', destination = 'hotel', booking_complete=False).first()
    
    
    hotel_booking_temp = Accomodationbookingtemp()
    hotel_booking_temp.accomodation_details_id = accomodation_details_id
    hotel_booking_temp.cost = int(cost)*int(no_of_rooms)
    hotel_booking_temp.no_of_rooms = no_of_rooms
    hotel_booking_temp.start_date = start_date
    hotel_booking_temp.end_date = end_date
    hotel_booking_temp.my_orders_id = temp_orders.id
    db.session.add(hotel_booking_temp)
    db.session.commit()
    return redirect(url_for('user.hotelpassengerinfo', booking_id=temp_orders.id,no_of_people=no_of_rooms, cost=cost, current_passenger=1, _external=True))

@user.route('/hotel_booking/passenger/<string:booking_id>/<string:no_of_people>/<string:cost>/<string:current_passenger>' , methods=['GET', 'POST'])
@login_required
def hotelpassengerinfo(booking_id, no_of_people, cost, current_passenger):
    booking_id = booking_id
    no_of_people = int(no_of_people)
    current_passenger = int(current_passenger)
    if int(current_passenger) > int(no_of_people):
        return redirect(url_for('user.payments', booking_id=booking_id, cost=cost, flights=0 ,hotels=1 ,location=0 ,_external=True))
    form = PassengerInfoHotel()
    if form.validate_on_submit():
        passenger_temp = Passenger()
        passenger_temp.first_name = form.first_name.data.lower()
        passenger_temp.last_name = form.last_name.data.lower()
        passenger_temp.email = form.email.data
        passenger_temp.dob = form.dob.data
        passenger_temp.sex = form.sex.data.lower()
        passenger_temp.passport_number = "N/A"
        passenger_temp.temp_orders_id = booking_id
        db.session.add(passenger_temp)
        db.session.commit()
        current_passenger += 1
        return redirect(url_for('user.hotelpassengerinfo', booking_id=booking_id, no_of_people=no_of_people, cost=cost, current_passenger=current_passenger, _external=True))

    return render_template('user/Passenger_info_hotel.html', form=form, current_passenger = current_passenger, no_of_people=no_of_people)






@user.route('/my_orders' , methods=['GET', 'POST'])
@login_required
def my_orders():
    form = MyordersForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        return redirect(url_for('user.my_orders_details', username=username, _external=True))
    return render_template('user/my_orders_temp.html', form=form)


@user.route('/my_orders/<string:username>' , methods=['GET', 'POST'])
@login_required
def my_orders_details(username):
    user_temp = User.query.filter_by(username = username).first()
    my_orders_temp = Myorders.query.filter_by(user_id = user_temp.id).all()
    if my_orders_temp is None or my_orders_temp == []:
        flash ("Sorry you do not have any orders placed", "danger")
        return redirect(url_for('user.dashboard'))
    
    hotels_json = []
    flights_json = []
    activities_json = []
    for my_order in my_orders_temp:
        payments_temp = Payments.query.filter_by(my_orders_id = my_order.id).first()
        
        # Check Flights
        flights_temp = Flightbooking.query.filter_by(my_orders_id = my_order.id).first()
        if flights_temp is not None:
            temp_flights = {}
            flight_details = Flightdetails.query.filter_by(id = flights_temp.flight_details_id).first()
            temp_flights['confirmation'] = payments_temp.confirmation_reference
            temp_flights['source'] = flight_details.source
            temp_flights['destination'] = flight_details.destination
            temp_flights['start_date'] = str(flight_details.departure_date)
            temp_flights['end_date'] = str(flight_details.arrival_date)
            temp_flights['start_time'] = str(flight_details.departure_time)
            temp_flights['end_time'] = str(flight_details.arrival_time)
            temp_flights['no_of_people'] = flights_temp.no_of_people
            temp_flights['cost'] = my_order.cost
            temp_flights['flight_number'] = flight_details.flight_number
            temp_flights['my_order_id'] = my_order.id
            flights_json.append(temp_flights)
            continue
        # Check Hotels
        hotel_temp = Accomodationbooking.query.filter_by(my_orders_id = my_order.id).first()
        if hotel_temp is not None:
            temp_hotels = {}
            hotel_details = Accomodationdetails.query.filter_by(id = hotel_temp.accomodation_details_id).first()
            hotel_main_details = Accomodation.query.filter_by(id = hotel_details.accomodation_id).first()
            temp_hotels['confirmation'] = payments_temp.confirmation_reference
            temp_hotels['hotel_name'] = hotel_main_details.hotel_name
            temp_hotels['no_of_rooms'] = hotel_temp.no_of_rooms
            temp_hotels['room_name'] = hotel_details.room_name
            temp_hotels['cost'] = my_order.cost
            temp_hotels['start_date'] = str(my_order.start_date)
            temp_hotels['end_date'] = str(my_order.end_date)
            temp_hotels['source'] = my_order.source
            temp_hotels['my_order_id'] = my_order.id
            hotels_json.append(temp_hotels)
            continue
        # Check Activities
        location_temp = Locationbooking.query.filter_by(my_orders_id = my_order.id).first()
        if location_temp is not None:
            temp_location = {}
            location_details = Locationdetails.query.filter_by(id = location_temp.location_details_id).first()
            location_main_details = Location.query.filter_by(id = location_details.location_id).first()
            temp_location['confirmation'] = payments_temp.confirmation_reference
            temp_location['name'] = location_main_details.name
            temp_location['no_of_people'] = location_temp.no_of_people
            temp_location['cost'] = my_order.cost
            temp_location['start_date'] = str(my_order.start_date)
            temp_location['my_order_id'] = my_order.id
            activities_json.append(temp_location)
            continue
    items = {}
    items['flights'] = flights_json
    items['hotels'] = hotels_json
    items['location'] = activities_json
    print('\n\n\n\n\n\n\n\n\n\n\n\n', items)
    return render_template('user/my_orders.html', items = items, user_name = user_temp.username)


@user.route('/flight_booking' , methods=['GET', 'POST'])
@login_required
def flight_booking():

    items = None
    form = FlightBookingForm()
    if form.validate_on_submit():
        print("E")
        
        source = form.source.data.lower()
        destination = form.destination.data.lower()
        number_of_people = int(form.adults.data) + int(form.children.data)
        departure_date = form.departure_date.data
        arrival_date = form.arrival_date.data
        cabin_class = form.cabin_class.data
        
        print("\n\n\n\n\n\n\n\n\n\n",cabin_class)
        flight_details = (db.session.query(Flightdetails, Ticket)
                .join(Flightdetails, Flightdetails.id == Ticket.flights_id)
                .filter(Flightdetails.source == source,
                            Flightdetails.destination == destination,
                            Flightdetails.departure_date == departure_date,
                            Ticket.type == cabin_class)
                .all())
        
        print('\n\n\n\n\n\n\n\n\n', flight_details)
        items = []
        for flight_det, tickets in flight_details:
            if flight_det.vacant_seats < int(number_of_people):
                continue
            temp_dict = {}
            temp_dict['flight_number'] = flight_det.flight_number
            temp_dict['source'] = flight_det.source
            temp_dict['destination'] = flight_det.destination
            temp_dict['no_of_people'] = str(number_of_people)
            temp_dict['departure_date'] = str(flight_det.departure_date)
            temp_dict['departure_time'] = str(flight_det.departure_time)
            temp_dict['arrival_date'] = str(flight_det.arrival_date)
            temp_dict['arrival_time'] = str(flight_det.arrival_time)
            temp_dict['cost'] = str(random.randrange(tickets.min_cost,tickets.max_cost))
            # temp_dict = json.dumps(temp_dict)
            print(temp_dict)
            items.append(temp_dict)
        print(items)
        # items = json.dumps(items)
        # items = json.loads(items)
        print("ASD",items)
        return render_template('user/flight_booking.html', form=form, items = items)
    return render_template('user/flight_booking.html', form=form, items = items)

@user.route('/flight_booking/confim/<string:flight_number>/<string:source>/<string:destination>/<string:no_of_people>/<string:departure_date>/<string:departure_time>/<string:arrival_date>/<string:arrival_time>/<string:cost>' , methods=['GET', 'POST'])
@login_required
def flight_booking_confirm(flight_number, source, destination, no_of_people, departure_date, departure_time, arrival_date, arrival_time, cost):
    flight_number = flight_number
    source = source
    destination = destination
    no_of_people = no_of_people
    departure_date = departure_date
    departure_time = departure_time
    arrival_date = arrival_date
    arrival_time = arrival_time
    cost = cost
    user_id = current_user.id
    # Booking Temp Orders
    temp_orders = Myorderstemp()
    temp_orders.user_id = user_id
    #change later
    temp_orders.international = True
    temp_orders.cost = int(cost)*int(no_of_people)
    temp_orders.start_date = departure_date
    temp_orders.end_date = arrival_date
    temp_orders.source = source
    temp_orders.destination = destination
    temp_orders.individual = True
    temp_orders.booking_complete = False
    db.session.add(temp_orders)
    db.session.commit()
    temp_orders = Myorderstemp.query.filter_by(user_id = user_id, international = True, start_date = departure_date, end_date=arrival_date, source=source, destination=destination, booking_complete=False).first()
    flight_details = Flightdetails.query.filter_by(flight_number=flight_number).first()
    flight_booking_temp = Flightbookingtemp()
    flight_booking_temp.flight_details_id = flight_details.id
    flight_booking_temp.cost = int(cost)*int(no_of_people)
    flight_booking_temp.no_of_people = no_of_people
    flight_booking_temp.my_orders_id = temp_orders.id
    db.session.add(flight_booking_temp)
    db.session.commit()
    return redirect(url_for('user.flightpassengerinfo', booking_id=temp_orders.id,no_of_people=no_of_people, cost=cost ,current_passenger=1, _external=True))

@user.route('/flight_booking/passenger/<string:booking_id>/<string:no_of_people>/<string:cost>/<string:current_passenger>' , methods=['GET', 'POST'])
@login_required
def flightpassengerinfo(booking_id, no_of_people, cost, current_passenger):
    booking_id = booking_id
    no_of_people = int(no_of_people)
    current_passenger = int(current_passenger)
    if int(current_passenger) > int(no_of_people):
        return redirect(url_for('user.payments', booking_id=booking_id, cost=cost, flights=1 ,hotels=0 ,location=0 ,_external=True))
    form = PassengerInfo()
    if form.validate_on_submit():
        passenger_temp = Passenger()
        passenger_temp.first_name = form.first_name.data.lower()
        passenger_temp.last_name = form.last_name.data.lower()
        passenger_temp.email = form.email.data
        passenger_temp.dob = form.dob.data
        passenger_temp.sex = form.sex.data.lower()
        passenger_temp.passport_number = form.passport_number.data
        passenger_temp.temp_orders_id = booking_id
        db.session.add(passenger_temp)
        db.session.commit()
        current_passenger += 1
        return redirect(url_for('user.flightpassengerinfo', booking_id=booking_id, no_of_people=no_of_people, cost=cost , current_passenger=current_passenger, _external=True))

    return render_template('user/Passenger_info.html', form=form, current_passenger = current_passenger, no_of_people=no_of_people)

@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('user/profile.html', org=current_user)

@user.route('/testing', methods=['GET', 'POST'])
@login_required
def testing():
    return render_template('user/testing.html')

@user.route('/payments/<string:booking_id>/<string:cost>/<string:flights>/<string:hotels>/<string:location>', methods=['GET', 'POST'])
@login_required
def payments(booking_id, cost, flights, hotels, location):
    booking_id = booking_id
    cost = cost
    flights = flights
    hotels = hotels
    location = location
    form = PaymentsForm()
    if form.validate_on_submit():
        print('\n\n\n\n\n\n\n\n\n\n\nData Added')
        user_temp = User.query.filter_by(username=form.username.data.lower()).first()
        
        
        # Remove from temp_orders
        temp_orders = Myorderstemp.query.filter_by(id=booking_id).first()
        temp_orders.booking_complete = True
        db.session.commit()

        # Add to my orders
        my_orders_temp = Myorders()
        my_orders_temp.user_id = user_temp.id
        my_orders_temp.international = True
        my_orders_temp.cost = cost
        my_orders_temp.start_date = temp_orders.start_date
        my_orders_temp.end_date = temp_orders.end_date
        my_orders_temp.source = temp_orders.source
        my_orders_temp.destination = temp_orders.destination
        my_orders_temp.individual = temp_orders.individual
        my_orders_temp.payment_completed = True
        db.session.add(my_orders_temp)
        db.session.commit()




        temp_main_orders = Myorders.query.filter_by(user_id = user_temp.id, international = True, start_date = temp_orders.start_date, end_date=temp_orders.end_date, source=temp_orders.source, destination=temp_orders.destination, payment_completed=True).first()
            
        passenger_temp = Payments()
        passenger_temp.user_id = user_temp.id
        passenger_temp.my_orders_id = temp_main_orders.id
        passenger_temp.cost = cost
        passenger_temp.payment_method = str(form.credit_card.data) + str(form.name_on_card.data.lower()) + str(form.expiration_date.data) + str(form.cvv_card.data)
        passenger_temp.completed = True
        confirmation = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        passenger_temp.confirmation_reference = confirmation
        passenger_temp.billing_addr_1 = form.address_1.data
        if form.address_2.data is not None or form.address_2.data != '':
            passenger_temp.billing_addr_2 = form.address_2.data
        
        passenger_temp.zip_code = form.zip_code.data
        db.session.add(passenger_temp)
        db.session.commit()
        
        
        # Add to respective flights, hotels, locations
        # Remove from respective flights , hotels, locations
        if int(flights) == 1:
            flight_booking_temp = Flightbookingtemp.query.filter_by(my_orders_id= booking_id).first()
            
            flight_main_booking_temp = Flightbooking()
            flight_main_booking_temp.flight_details_id = flight_booking_temp.flight_details_id
            flight_main_booking_temp.cost = flight_booking_temp.cost
            flight_main_booking_temp.no_of_people = flight_booking_temp.no_of_people
            flight_main_booking_temp.my_orders_id = temp_main_orders.id
            db.session.add(flight_main_booking_temp)
            db.session.commit()
            Flightbookingtemp.query.filter_by(my_orders_id= booking_id).delete()
            db.session.commit()
            
        elif int(hotels) == 1:
            accomodation_booking_temp = Accomodationbookingtemp.query.filter_by(my_orders_id= booking_id).first()
            
            accomodation_main_booking_temp = Accomodationbooking()
            accomodation_main_booking_temp.accomodation_details_id = accomodation_booking_temp.accomodation_details_id
            accomodation_main_booking_temp.cost = accomodation_booking_temp.cost
            accomodation_main_booking_temp.no_of_rooms = accomodation_booking_temp.no_of_rooms
            accomodation_main_booking_temp.my_orders_id = temp_main_orders.id
            db.session.add(accomodation_main_booking_temp)
            db.session.commit()
            
            Accomodationbookingtemp.query.filter_by(my_orders_id= booking_id).delete()
            db.session.commit()
            
        elif int(location) == 1:
            location_booking_temp = Locationbookingtemp.query.filter_by(my_orders_id= booking_id).first()

            location_main_booking_temp = Locationbooking()
            location_main_booking_temp.location_details_id = location_booking_temp.location_details_id
            location_main_booking_temp.cost = location_booking_temp.cost
            location_main_booking_temp.no_of_people = location_booking_temp.no_of_people
            location_main_booking_temp.my_orders_id = temp_main_orders.id
            db.session.add(location_main_booking_temp)
            db.session.commit()

            Locationbookingtemp.query.filter_by(my_orders_id=booking_id).delete()
            db.session.commit()
            
        # Passenger Info change temp_orders_id and update my_orders_id
        passenger_temp = Passenger.query.filter_by(temp_orders_id = booking_id).all()
        for temp in passenger_temp:
            temp.temp_orders_id = None
            temp.my_orders_id = temp_main_orders.id
            db.session.commit()
        
        Myorderstemp.query.filter_by(id=booking_id).delete()
        db.session.commit()
        flash ("Your Order Has Been Successfully Placed.", 'info')
        return redirect(url_for('user.dashboard'))
    return render_template('user/payments1.html', form=form)

# @user.route('/flight-booking' , methods=['GET', 'POST'])
# @login_required
# def flight_booking():
#     flight_booking_form = DashboardForm()
#     return render_template('user/flight_booking.html', form=flight_booking_form)

# @user.route('/hotel-booking' , methods=['GET', 'POST'])
# @login_required
# def hotel_booking():
#     hotel_booking_form = DashboardForm()
#     return render_template('user/hotel_booking.html', form=hotel_booking_form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out successfully.', 'info')
    return redirect(url_for('user.login'))

# Confirm whether users email is verified or not
@user.route('/confirmation/<string:token>')
def email_confirmation(token):
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))

    token_info = UserToken.query.filter_by(
        token=token, token_type='email_confirmation').first()

    if not token_info:
        flash('Invalid email confirmation token', 'danger')
        return redirect(url_for('.login'))
    if not token_info.is_valid():
        flash('Token is expired. Please get new email confirmation link', 'danger')
        return redirect('.login')
    token_info.user.email_verified = True
    token_info.user.is_active = True
    
    db.session.commit()
    flash('Email has been verified', 'success')
    return redirect(url_for('.login'))


# Send email to user for verification
@user.route('/resend-confirmation', methods=['GET', 'POST'])
def send_email_confirmation():
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))

    form = ResendEmailConfirmationForm()
    if form.validate_on_submit():
        email = form.email.data
        org = User.query.filter_by(email=email).first()
        if not org:
            flash('Email address is not registered with us. Please signup', 'info')
            return redirect(url_for('.signup'))

        if org.email_verified:
            flash('Email address is already verified Please login', 'info')
            return redirect(url_for('.login'))

        email_conf_token = UserToken.generate_token(
            'email_confirmation', org.id, 1800)
        send_confirmation_mail(org.email,
                               url_for('.email_confirmation',
                                       token=email_conf_token.token, _external=True))
        flash('The email confirmation link has been sent to your email. Please check your email', 'info')
        return redirect(url_for('.login'))
    return render_template('user/resend_email_confirmation.html', form=form)


# Reset password incase forgotten
@user.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        org = User.query.filter_by(email=email).first()
        if not org:
            flash('Email address is not registered with us. Please signup', 'info')
            return redirect(url_for('.signup'))
        if not org.email_verified:
            flash('Email is not verified. Please verify email first', 'danger')
            return redirect(url_for('.login'))
        if not org.is_active:
            flash('Your account has been deactivated Please contact admin', 'info')
            return redirect(url_for('.login'))
        reset_password_token = UserToken.generate_token(
            'reset_password', org.id, 1800)
        try:
            send_reset_password_mail(org.email,
                                 url_for('.reset_password',
                                         token=reset_password_token.token, _external=True))
        except Exception as err:
            print ('Error Logged : ', err)
            flash('Email sending failed', 'danger')
            return redirect(url_for('user.login')) 
        else:
            flash('Reset password link has been sent to your email address', 'info')
            return redirect(url_for('.login'))
    return render_template('user/reset_password_request.html', form=form)


# Reset password
@user.route('/reset-password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))

    token_info = UserToken.query.filter_by(
        token=token, token_type='reset_password').first()

    if not token_info:
        flash('Invalid Reset password token', 'danger')
        return redirect(url_for('.login'))
    if not token_info.is_valid():
        flash('Token is expired. Please get new email confirmation link', 'danger')
        return redirect('.login')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        token_info.user.password = User.hash_password(password)
        db.session.commit()
        flash('Your password has been updated. Please login with new password', 'success')
        return redirect(url_for('.login'))
    return render_template('user/reset_password.html', form=form)
