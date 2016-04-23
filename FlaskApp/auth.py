from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from __init__ import app as app

# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/FlaskApp/FlaskApp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String(80), unique=True, primary_key=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


    def __repr__(self):
        return '<User %r>' % self.username


# @app.route('/')
# def hello_world():
    # x = User('panos', 'panos', 'panos@test.com')
    # db.session.add(x)
    # db.session.commit()
    # users = User.query.all()
    # print users
    # if User.query.filter_by(username='test').first() != None:
        # return 'user exists'
    # else:
        # return 'paparia exists'
    #return str(users)

# if __name__ == '__main__':
    # db.create_all()
    # app.run()
