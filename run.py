from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import LoginManager,current_user
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
app=Flask(__name__)

app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (current_user.role=='lead') or (current_user.id==1)

class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.role=='lead') or (current_user.id==1)

db=SQLAlchemy(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.login_message='يجب تسجيل الدخول للوصول لهذه الصفحه'
admin = Admin(app, index_view=MyAdminIndexView())

from routes import *
from models import *

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Lesson, db.session))
# =========================
# deal with db
# =========================
with app.app_context():
    db.create_all()
# =========================
# =========================

if __name__=='__main__':
    app.run(debug=True)