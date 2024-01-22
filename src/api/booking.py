from flask_marshmallow import Schema, fields
from sqlalchemy.types import Enum, Integer, String, Float, Date
from conf import db
from conf import ma

from api.car import CarSchema
from api.user import UserSchema

class BookingModel(db.Model):
    """Model for booking information"""
    __tablename__ = "Bookings"
    car = db.relationship("CarModel", backref=db.backref("Bookings", lazy=True, viewonly=True))
    user = db.relationship("UserModel", backref=db.backref("Bookings", lazy=True, viewonly=True))
    
    id = db.Column(Integer, primary_key=True) # Unique ID
    car_id = db.Column(Integer, db.ForeignKey("Cars.id"))
    user_id = db.Column(Integer, db.ForeignKey("Users.id"))
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date, nullable=False)
    
    def __init__(self, car_id, user_id, start_date, end_date):
        super().__init__()
        self.car_id = car_id
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date

class BookingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = BookingModel
        fields = ('id', 'car_id', 'car', 'user_id', 'user', 'start_date', 'end_date')
        load_instance = True
        include_fk = True
        include_relationships = True
    
    id = ma.auto_field()
    car = ma.Nested(CarSchema)
    user = ma.Nested(UserSchema, only=('id', 'uname'))
    start_date = ma.auto_field()
    end_date = ma.auto_field()
