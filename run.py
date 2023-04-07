from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import LoginManager

app=Flask(__name__)

app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'

db=SQLAlchemy(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

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