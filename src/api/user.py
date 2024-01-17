from flask_marshmallow import Schema, fields
from sqlalchemy.types import Enum, Integer, String, Float
from conf import db
from conf import ma
import enum

class UserModel(db.Model):
    """Model for a user resource"""
    __tablename__ = "Users"
    id = db.Column(Integer, primary_key=True) # Unique identifier
    uname = db.Column(String(30), nullable=False, unique=True) # Username
    upass = db.Column(String(255), nullable=False)

    def __init__(self, uname, upass):
        super().__init__()
        self.uname = uname
        self.upass = upass

    @classmethod
    def find_by_uname(cls, name) -> "UserModel":
        return cls.query(UserModel).with_entities(UserModel.id, UserModel.uname).filter_by(uname=name).first()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True