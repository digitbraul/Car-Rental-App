from flask import Flask
from flask_mysqldb import MySQL
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Register web app into app variable
app = Flask(__name__)

app.secret_key = "allmyfellas"

app.config["DEBUG"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/cars_db'

mysql = MySQL(app)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)