from run import db,login_manager
from datetime import datetime
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String,nullable=False)
    uname=db.Column(db.String,nullable=False,unique=True)
    email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.String(5),nullable=False,default='user')
    lessons=db.relationship('Lesson',backref='author',lazy=True)
    request=db.relationship('Request',backref='user',lazy=True)

class Lesson(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    image=db.Column(db.String,nullable=False,default='default.jpg')
    title=db.Column(db.String,nullable=False,unique=True)
    content=db.Column(db.Text,nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))


class Request(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    time=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)