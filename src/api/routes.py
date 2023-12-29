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

    def get(self):
        # Fetch resource from api.db (if request contains args, filter the result based on them)
        all_cars = CarModel.query.all()#filter_by(request.args['car_make'], request.args['seats'], request.args['fuel_type']).all()
        return jsonify(cars_schema.dump(all_cars))
    
    def post(self):
        # Creates a new car resource
        errors = cars_schema.validate(request.form)
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