from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
app = Flask(__name__)
csrf=CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus_database.db'
app.config['SECRET_KEY']='27421cc728c4d29ea7e1ee43'
db = SQLAlchemy(app)
from Buses import routes
