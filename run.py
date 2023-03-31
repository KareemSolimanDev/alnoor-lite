from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask()

app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'

db=SQLAlchemy(app)


if __name__=='__main__':
    app.run(debug=True)