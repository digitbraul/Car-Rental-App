import json
from flask import Flask, jsonify, make_response, redirect, render_template, request, session, url_for
from flask_restful import Resource, reqparse
from api.db import *
from conf import app, api
import hashlib
import datetime

# Routings for web service (flask_resful Api object)
@api.resource('/cars')
class CarList(Resource):
    """Defines a car list and handles GET requests (to list cars)"""
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('make', type=str, location = 'args')
        self.reqparse.add_argument('seats', type=int, location = 'args')
        self.reqparse.add_argument('fuel_type', type=str, location = 'args')
        super(CarList, self).__init__()

    def get(self):
        # Fetch resource from api.db (if request contains args, filter the result based on them)
        args = self.reqparse.parse_args()
        car_list = fetch_car(make=args['make'], seats=args['seats'], fuel_type=args['fuel_type'])
        return jsonify(total_results=len(car_list), result_list=car_list)

@api.resource('/cars/<int:car_id>')
class Car(Resource):
    """Returns a single car resource using GET"""
    def get(self, car_id):
        # Fetch resource from api.db
        car = fetch_car(id=car_id)
        return jsonify(car)

@api.resource('/bookings')
class BookingList(Resource):
    """Defines a bookings resource (Accepts GET and POST requests to read or create respectively)"""
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=str, location='form')
        self.reqparse.add_argument('car_id', type=str, location='form')
        self.reqparse.add_argument('start_date', type=datetime.datetime, location='form')
        super(BookingList, self).__init__()
    
    def get(self):
        # Fetch resource from api.db (returns a json array)
        booking_list = fetch_booking_list()
        return jsonify(total_results=len(booking_list), result_list=booking_list)

# Routings for web app (Jinja for server-side templating and jQuery in target pages)
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/api/add_cars", methods = ['GET', 'POST'])
def add_car():
    if not session.get('logged-in'):
        return redirect(url_for('login.html'))
    
    if request.method == 'GET':
        return render_template('car_creator.html')
    
    elif request.method == 'POST':
        # Read the values posted from the form
        _car_make = request.form['car_make']
        _car_model = request.form['car_model']
        _car_seats = request.form['car_seats']
        _car_thumb = request.form['car_thumb'] # in base 64
        _fuel_type = request.form['car_fuel'] # select option from the client side, TODO: check if it equals "Gasoline" / "Electric" / "Diesel" in the api.db

        # TODO: Add car to the database


@app.route("/admin", methods = ['GET', 'POST'])
def admin_login():
    if session.get('logged-in'):
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        # Read the values posted from the form
        _uname = request.form['username']
        _upass = request.form['userpass']

        # Validate input
        if not (_uname and _upass):
            return render_template('login.html', msg="Please check input!")

        # Fetch user and pass from database
        acc = fetch_user(uname=_uname, password=_upass)
        if acc:
            session['logged-in'] = True
            session['id'] = int(hashlib.sha1(acc['username'].encode("utf-8")).hexdigest(), 16) % (10 ** 8)
            msg = "Logged in successfully!"
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', msg="Wrong username or password!")

@app.route('/logout')
def logout():
    session.pop('logged-in', None)
    session.pop('id', None)
    return redirect(url_for('admin_login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged-in'):
        return redirect(url_for('admin_login'))
    
    return render_template('dashboard.html')

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# MAIN
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)