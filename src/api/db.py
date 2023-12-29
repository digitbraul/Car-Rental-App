import traceback
from flask_mysqldb import MySQL
from conf import mysql
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
import datetime

def fetch_user(uname : str, password : str):
    """Fetches user with username and password (for login)"""
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM user WHERE username = %s", (uname,))
        acc = cursor.fetchone()
        if acc and not check_password_hash(acc['pass'], password): # default password for admin = "GIRATINA1a", for users = "test123"
            return None
    except:
        print("Failed to execute statement")
    
    return acc

def fetch_car(**kwargs):
    """Fetches a car from database, or * if no id provided"""

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # fetch one by ID
    id = kwargs.get('id', None)
    # filter result by specific criteria
    make = kwargs.get('make', None)
    seats = kwargs.get('seats', None)
    fuel_type = kwargs.get('fuel_type', None)

    try:
        # if an ID was specified, the caller route is /car/<id>, return the car with given ID
        if id:
            cursor.execute("SELECT * FROM car WHERE id = %s", (id,))
            car = cursor.fetchone()
            return car
        else:
            # prepare statement
            stmt = "SELECT * FROM car WHERE "
            to_filter = []

            # check if kwargs contain filters (by make, fuel_type, seats...)
            if make:
                stmt += "car_make = %s AND "
                to_filter.append(make)
            if seats:
                stmt += "seats = %s AND "
                to_filter.append(seats)
            if fuel_type:
                stmt += "fuel_type = %s AND "
                to_filter.append(fuel_type)
            
            # if kwargs provided, subtract trailing AND, otherwise, remove where
            if len(to_filter):
                stmt = stmt[:-4]
            else:
                if "WHERE" in stmt:
                    stmt = stmt[:-6]

            cursor.execute(stmt, tuple(to_filter))
            car_list = cursor.fetchall()
            return car_list
    except:
        print("Failed to execute statement")
        traceback.print_exc()
    
    return None

def fetch_booking_list(**kwargs):
    """Fetches a list of bookings from database, per user_id or per car_id as defined in the kwargs"""
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # fetch one booking by id
    booking_id = kwargs.get('booking_id', None)
    # fetch a booking per car or per user
    car_id = kwargs.get('car_id', None)
    user_id = kwargs.get('user_id', None)

    try:
        if booking_id:
            cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
            booking = cursor.fetchone()
            return booking
        else:
            # prepare statement to fetch all bookings
            stmt = "SELECT * FROM bookings b, car c, user u WHERE b.car_id = c.id AND b.username = u.username "
            to_filter = []

            # check if kwargs contain car_id / user_id
            if car_id:
                stmt += "car_id = %s AND "
                to_filter.append(car_id)
            if user_id: # username in the database
                stmt += "username = %s AND "
                to_filter.append(user_id)
            
            if len(to_filter):
                stmt = stmt[:-4]
            
            cursor.execute(stmt, tuple(to_filter))
            booking_list = cursor.fetchall()
            return booking_list
    except:
        print("Failed to execute statement")
        traceback.print_exc()
