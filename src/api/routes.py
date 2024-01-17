import json

from flask import Flask, jsonify, request, abort, session
from flask_restful import Resource

from werkzeug.security import generate_password_hash, check_password_hash

from api.car import CarModel, CarSchema
from api.user import UserModel, UserSchema
from api.booking import BookingModel, BookingSchema

from conf import app, api, db, ma
import hashlib
import datetime

# Assign schemas
car_schema = CarSchema()
cars_schema = CarSchema(many=True)

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# Car routings
@api.resource('/cars')
class CarList(Resource):
    """Defines a car list and handles GET requests (to list cars)"""
    def __init__(self) -> None:
        super(CarList, self).__init__()

    def get(self) -> None:
        #db.create_all()

        filtered_req = False
        filters = []

        if 'car_make' in request.args:
            filtered_req = True
            filters.append(CarModel.car_make == request.args['car_make'])
        
        if 'seats' in request.args:
            filtered_req = True
            filters.append(CarModel.seats == request.args['seats'])
        
        if 'search' in request.args:
            filtered_req = True
            filters.append(CarModel.car_make.like(str(request.args['search']) + '%'))

        if filtered_req:
            res_cars = CarModel.query.filter(*filters)
            return cars_schema.dump(res_cars), 200
        else:
            # if no filter, return full list
            res_cars = CarModel.query.all()
            return cars_schema.dump(res_cars), 200
    
    def post(self):
        # Creates a new car resource
        errors = car_schema.validate(request.form)
        if errors:
            return {"message" : str(errors)}, 400
        
        car = CarModel(\
                request.form['car_make'], \
                request.form['car_model'], \
                request.form['seats'], \
                request.form['fuel_type'], \
                request.form['thumb_url'], \
                request.form['location'], \
                request.form['daily_price'], \
                request.form['deductible'], \
                request.form['transmission'])
        db.session.add(car)
        db.session.commit()
        return car_schema.dump(car), 200

@api.resource('/cars/<int:car_id>')
class Car(Resource):
    """Returns a single car resource using GET"""
    def __init__(self) -> None:
        super(Car, self).__init__()
    
    def get(self, car_id):
        # Fetch car
        car = CarModel.query.get(car_id)
        return car_schema.dump(car), 200
    
    def patch(self, car_id):
        # Update car
        errors = cars_schema.validate(request.form)
        if errors:
            return {"message" : str(errors)}, 400
        
        car = CarModel.query.get(car_id)
        car.car_make = request.form['car_make']
        car.car_model = request.form['car_model']
        car.seats = request.form['seats']
        car.fuel_type = request.form['fuel_type']
        car.thumb = request.form['thumb']
        db.session.add(car)
        db.session.commit()
        return car_schema.dump(car)
    
    def delete(self, car_id):
        car = CarModel.query.filter(CarModel.id == car_id).delete()
        db.session.commit()
        return {"message" : "Car deleted successfully!"}, 200

# User routings
@api.resource('/users')
class UserList(Resource):
    def __init__(self) -> None:
        super(UserList, self).__init__()
    
    def get(self):
        all_users = UserModel.query.with_entities(UserModel.id, UserModel.uname).all()
        return user_list_schema.dump(all_users), 200

    # Create a new user
    def post(self):
        errors = user_schema.validate(request.form)
    
        if errors: #abort()
            return {"message" : str(errors)}, 400
        
        # If username already exists, abort
        if UserModel.query.filter(UserModel.uname == request.form['uname']).first() is not None:
            return {"message" : "Username already exists!"}, 400

        passw_hash = generate_password_hash(request.form['upass'])
        user = UserModel(request.form['uname'], passw_hash)
        db.session.add(user)
        db.session.commit()
        return {"message" : "User added successfully!"}, 200

@api.resource('/users/<string:uname>')
class User(Resource):
    """Returns a single user resource using GET, modifyable only by admin"""
    def __init__(self) -> None:
        super(User, self).__init__()
    
    def get(self, uname):
        # if admin, return user data
        if session.get('id') != int(hashlib.sha1("admin".encode("utf-8")).hexdigest(), 16) % (10 ** 8):
            return {"message" : "Cannot access content unless logged in as admin"}, 403
        
        current_user = UserModel.query.filter(UserModel.uname == uname).first()
        return user_schema.dump(current_user), 200

    def delete(self, uname):
        if session.get('id') != int(hashlib.sha1("admin".encode("utf-8")).hexdigest(), 16) % (10 ** 8):
            return {"message" : "Cannot access content unless admin"}, 403

        UserModel.query.filter(UserModel.uname == uname).delete()
        db.session.commit()
        return {"message" : "User deleted successfully!"}, 200
    
    def patch(self, uname):
        # if current_user, update password
        if 'id' not in session:
            return {"message" : "No user currently logged in!"}, 401

        if session.get('id') != int(hashlib.sha1(uname.encode("utf-8")).hexdigest(), 16) % (10 ** 8):
            return {"message" : "Username and Session ID mismatch"}, 401
        
        if 'upass' not in request.form:
            return {"message" : "No new password provided!"}, 401

        UserModel.query.filter(UserModel.uname == uname).update({UserModel.upass : generate_password_hash(request.form['upass'])})
        db.session.commit()
        return {"message" : "Password updated!"}, 200

@api.resource('/bookings')
class BookingList(Resource):
    """Defines a bookings resource (Accepts GET and POST requests to read or create respectively)"""
    def __init__(self) -> None:
        super(BookingList, self).__init__()
   
    def get(self):
        filtered_req = False
        filters = []

        if 'user_id' in request.args:
            filtered_req = True
            filters.append(BookingModel.user_id == int(request.args['user_id']))
        if 'car_id' in request.args:
            filtered_req = True
            filters.append(BookingModel.car_id == int(request.args['car_id']))

        if filtered_req:
            res_bookings = BookingModel.query.filter(*filters)
            return bookings_schema.dump(res_bookings), 200
        else:
            # if no filter, return full list
            #all_bookings = db.session.query(BookingModel, CarModel).join(CarModel, BookingModel.car_id == CarModel.id).all()
            all_bookings = BookingModel.query.all()
            return bookings_schema.dump(all_bookings), 200

    def post(self):
        # Creates a new booking resource
        errors = booking_schema.validate(request.form)
        if errors:
            return {"message" : str(errors)}, 400
        
        # Create booking only for user with the current Session ID or abort if not logged in
        if 'id' not in session:
            return {"message" : "No user currently logged in!"}, 401
        
        current_user = UserModel.query.filter(UserModel.id == int(request.form['user_id'])).first()
        if session.get('id') != int(hashlib.sha1(current_user.uname.encode("utf-8")).hexdigest(), 16) % (10 ** 8):
            return {"message" : "User ID mismatch!"}
        
        booking = BookingModel(\
                request.form['car_id'], \
                request.form['user_id'], \
                request.form['start_date'], \
                request.form['end_date'])
        db.session.add(booking)
        db.session.commit()
        return booking_schema.dump(booking), 200

@api.resource('/bookings/<int:booking_id>')
class Booking(Resource):
    """Defines a single booking resource"""
    def __init__(self) -> None:
        super(Booking, self).__init__()
    
    def get(self, booking_id):
        current_booking = BookingModel.query.filter(BookingModel.id == booking_id).first()
        return booking_schema.dump(current_booking), 200
    
    # Update booking start or end date
    def patch(self, booking_id):
        if 'start_date' in request.form and 'end_date' in request.form:
            BookingModel.query.filter(BookingModel.id == booking_id).update({BookingModel.start_date : request.form['start_date'], BookingModel.end_date : request.form['end_date']})
            db.session.commit()
            return {"message" : "Booking start and end date updated!"}, 200
        else:
            return {"message" : "No data provided!"}, 404
    
    def delete(self, booking_id):
        BookingModel.query.filter(BookingModel.id == booking_id).delete()
        db.session.commit()
        return {"message" : "Booking deleted successfully!"}, 200

# in the bookings/<int:user_id>/<int:car_id> the client app will send a request
# using the car_id from the /cars/car_id