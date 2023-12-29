import json
from flask import Flask, jsonify, request, abort
from flask_restful import Resource
from api.car import CarModel, CarSchema
from conf import app, api, db, ma
import hashlib
import datetime

# Assign schemas
car_schema = CarSchema()
cars_schema = CarSchema(many=True)

# Routings for web service (flask_resful Api object)
@api.resource('/cars')
class CarList(Resource):
    """Defines a car list and handles GET requests (to list cars)"""
    def __init__(self) -> None:
        super(CarList, self).__init__()

    def get(self, car_make, seats, fuel_type):
        # Fetch resource from api.db (if request contains args, filter the result based on them)
        errors = cars_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        
        all_cars = CarModel.query.filter_by(car_make, seats, fuel_type).all()
        return jsonify(cars_schema.dump())
    
    def post(self, car_make, car_model, seats, fuel_type, thumb):
        # Creates a new car resource
        car = CarModel(car_make, car_model, seats, fuel_type, thumb)
        db.session.add(car)
        db.session.commit()
        return car_schema.jsonify(car)

@api.resource('/cars/<int:car_id>')
class Car(Resource):
    """Returns a single car resource using GET"""
    def __init__(self) -> None:
        super(Car, self).__init__()
    
    def get(self):
        # Fetch car
        car = CarModel.query.get(car_id)
        return car_schema.jsonify(car)
    
    def patch(self, car_make, car_model, seats, fuel_type, thumb):
        # Update car
        car = CarModel.query.get(car_id)
        car.car_make = car_make
        car.car_model = car_model
        car.seats = seats
        car.fuel_type = fuel_type
        car.thumb = thumb
        db.session.add(car)
        db.session.commit()
        return car_schema.jsonify(car)
    
    def delete(self):
        pass


# TODO: it works but pwease rewrite this T___T
# @api.resource('/bookings')
# class BookingList(Resource):
#     """Defines a bookings resource (Accepts GET and POST requests to read or create respectively)"""
#     def __init__(self) -> None:
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('user_id', type=str, location='form')
#         self.reqparse.add_argument('car_id', type=str, location='form')
#         self.reqparse.add_argument('start_date', type=datetime.datetime, location='form')
#         super(BookingList, self).__init__()
    
#     def get(self):
#         # Fetch resource from api.db (returns a json array)
#         booking_list = fetch_booking_list()
#         return jsonify(total_results=len(booking_list), result_list=booking_list)