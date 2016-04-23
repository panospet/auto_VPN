from flask import Flask, render_template, redirect, url_for, request, session, flash, current_app, send_file, escape
from flask.ext.login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run()
