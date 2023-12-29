from flask_marshmallow import Schema, fields
from conf import db
from conf import ma

class CarModel(db.Model):
    """Model for a Car resource"""
    id = db.Column(db.Integer, primary_key=True)
    car_make = db.Column(db.String(30))
    car_model = db.Column(db.String(30))
    seats = db.Column(db.Integer)
    fuel_type = db.Column(db.String(30))
    thumb = db.Column(db.String(256)) # TODO: check MariaDB for the exact values?

    def __init__(self, car_make, car_model, seats, fuel_type) -> None:
        super().__init__()
        self.car_make = car_make
        self.car_model = car_model
        self.seats = seats
        self.fuel_type = fuel_type
        self.thumb = thumb # base64 encoded image file

class CarSchema(ma.SQLAlchemyAutoSchema):
    """Auto-gen Schema for Marshmallow serialization / deserialization"""
    class Meta:
        model = CarModel