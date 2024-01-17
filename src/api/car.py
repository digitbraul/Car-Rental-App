from flask_marshmallow import Schema, fields
from sqlalchemy.types import Enum, Integer, String, Float
from conf import db
from conf import ma
import enum

class FuelType(str, enum.Enum):
    Gasoline = 'Gasoline'
    Diesel = 'Diesel'
    Electric = 'Electric'

class Transmission(str, enum.Enum):
    Automatic = 'Automatic'
    Electronic = 'Electronic'
    Manual = 'Manual'

class CarModel(db.Model):
    """Model for a Car resource"""
    __tablename__ = "Cars"
    id = db.Column(Integer, primary_key=True) # Unique identifier
    car_make = db.Column(String(30), nullable=False) # Car manufacturer
    car_model = db.Column(String(30), nullable=False) # Car model
    daily_price = db.Column(Float(precision=2), nullable=False) # Actual daily price
    deductible = db.Column(Float(precision=2), nullable=False) # Caution? (excess) liability pricing
    seats = db.Column(Integer, nullable=False) # number of seats (typically 5)
    fuel_type = db.Column(Enum(FuelType), nullable=False)
    transmission = db.Column(Enum(Transmission))
    location = db.Column(String(30), nullable=False) # current location
    thumb_url = db.Column(String(100), nullable=False) # thumbnail

    # add this in the bookings table as a foreign key
    #user_id = =db.Column(Integer, db.ForeignKey('stores.id'), nullable=False)

    def __init__(self, car_make, car_model, seats, fuel_type, thumb_url, location, daily_price, deductible, transmission) -> None:
        super().__init__()
        self.car_make = car_make
        self.car_model = car_model
        self.seats = seats
        self.fuel_type = fuel_type
        self.thumb_url = thumb_url # url to an image to be encoded in base64
        self.location = location
        self.daily_price = daily_price
        self.deductible = deductible
        self.transmission = transmission

class CarSchema(ma.SQLAlchemyAutoSchema):
    """Auto-gen Schema for Marshmallow serialization / deserialization"""
    class Meta:
        model = CarModel
        fields = ('id', 'car_make', 'car_model', 'seats', 'fuel_type', 'thumb_url', 'location', 'daily_price', 'deductible', 'transmission')
        load_instance = True
        #include_fk = True

# in the bookings schema, add the following before the Meta class definition: items = ma.Nested(ItemSchema, many=True)