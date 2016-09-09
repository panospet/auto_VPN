# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from __init__ import app as app

# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/FlaskApp/FlaskApp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String(80), unique=True, primary_key=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    admin_rights = db.Column(db.Boolean(), default=False)

    def __init__(self, username, password, email, admin_rights):
        self.username = username
        self.password = password
        self.email = email
        self.admin_rights = admin_rights

    def __repr__(self):
        return '<User %r>' % self.username
