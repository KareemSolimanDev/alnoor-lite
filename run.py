from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'

db=SQLAlchemy(app)

from models import *
from routes import *

if __name__=='__main__':
    app.run(debug=True)