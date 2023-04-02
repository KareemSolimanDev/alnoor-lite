from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'

db=SQLAlchemy(app)

from routes import *
from models import *
# =========================
# deal with db
# =========================
with app.app_context():
    db.create_all()
# =========================
# =========================

if __name__=='__main__':
    app.run(debug=True)