from flask import Flask
from flask_mysqldb import MySQL
from flask_restful import Api

# Register web app into app variable
app = Flask(__name__)

app.secret_key = "myfriendsprobablyhateme"

app.config["DEBUG"] = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cars_db'

mysql = MySQL(app)
api = Api(app)