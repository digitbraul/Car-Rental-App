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

# writing this so that dumbass me would know what to do
# I'm using sqlalchemy, this is a fresh state after committing
# and created the db (cars or smth), check it out in the phpmyadmin page
# and add the data from the previous db
# create additional dbs and do stuff, idk. im tired ._.

# more todos i guess
# add gearbox (auto, manual), change seats to 5 instead of 4 and add trunk capacity
# rename the car_model to just car DONE
# add pricing information, remove the thumbs and instead of storing them in the database
# store a link to them in a img/car_thumbs folder (from https://www.automobile.tn/)
# and send it to the user

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

    def get(self):
        #db.create_all()
        
        all_cars = CarModel.query.all()#filter_by(request.args['car_make'], request.args['seats'], request.args['fuel_type']).all()
        return jsonify(cars_schema.dump(all_cars))
    
    def post(self):
        # Creates a new car resource
        errors = car_schema.validate(request.form)
        if errors:
            abort(400, str(errors))
        
        car = CarModel(request.form['car_make'], request.form['car_model'], request.form['seats'], request.form['fuel_type'], request.form['thumb'])
        db.session.add(car)
        db.session.commit()
        return car_schema.jsonify(car)

@api.resource('/cars/<int:car_id>')
class Car(Resource):
    """Returns a single car resource using GET"""
    def __init__(self) -> None:
        super(Car, self).__init__()
    
    def get(self, car_id):
        # Fetch car
        car = CarModel.query.get(car_id)
        return car_schema.jsonify(car)
    
    def patch(self, car_id):
        # Update car
        errors = cars_schema.validate(request.form)
        if errors:
            abort(400, str(errors))
        
        car = CarModel.query.get(car_id)
        car.car_make = request.form['car_make']
        car.car_model = request.form['car_model']
        car.seats = request.form['seats']
        car.fuel_type = request.form['fuel_type']
        car.thumb = request.form['thumb']
        db.session.add(car)
        db.session.commit()
        return car_schema.jsonify(car)
    
    def delete(self, car_id):
        car = CarModel.query.filter(id=car_id).delete()

# User routings
@api.resource('/users')
class UserList(Resource):
    def __init__(self) -> None:
        super(UserList, self).__init__()
    
    def get(self):
        all_users = UserModel.query.with_entities(UserModel.id, UserModel.uname).all()
        return jsonify(user_list_schema.dump(all_users))

    # Create a new user
    def post(self):
        errors = user_schema.validate(request.form)
    
        if errors:
            abort(400, str(errors))
        
        passw_hash = generate_password_hash(request.form['upass'])
        user = UserModel(request.form['uname'], passw_hash)
        db.session.add(user)
        db.session.commit()
        return "User added successfully!", 200

@api.resource('/users/<int:user_id>')
class User(Resource):
    """Returns a single user resource using GET"""
    def __init__(self) -> None:
        super(User, self).__init__()
    
    def get(self, user_id):
        # if admin, return user data
        if session.get('id') != int(hashlib.sha1("admin".encode("utf-8")).hexdigest(), 16) % (10 ** 8):
            abort(403)
        
        user_data = UserModel.find_by_id(id)
        return user_schema.jsonify(user_data)
    
    def post(self):
        pass # login?

    def delete(self, user_id):
        CarModel.query.filter(id=user_id).delete()
        db.session.commit()
        return "User deleted successfully!", 200

@api.resource('/bookings')
class BookingList(Resource):
    """Defines a bookings resource (Accepts GET and POST requests to read or create respectively)"""
    def __init__(self) -> None:
        super(BookingList, self).__init__()
   
    def get(self):
        # Fetch resource from api.db (returns a json array)
        pass