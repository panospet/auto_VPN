#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file, escape  # NOQA
from functools import wraps
import os
import subprocess
from auth import *  # NOQA
from add_user_to_db import add_user
from threading import Timer

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


@app.route('/test')
def test():
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # also email must be specified
        add_user(username, password, '', False)
        # must clean out the form and redirect somewhere
    return render_template('register.html')


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username, password=password).first() is None:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('Hello ' + session['username'] + ', you were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


# route for handling the admin login page logic
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin':
            if User.query.filter_by(username=username, password=password).first() is None:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash('Hello ' + session['username'] + ', you were logged in.')
                return redirect(url_for('register'))
        else:
            error = 'Invalid credentials, please login as an administrator.'
    return render_template('admin_login.html', error=error)


def create_files():
    password = User.query.filter_by(username=session['username']).first().password
    edit_client_script(session.get('username'), password)
    user_folder = "/var/www/FlaskApp/FlaskApp/" + session['username'] + "_files"
    os.system("mkdir -p " + user_folder)
    os.system("cp /usr/share/easy-rsa/keys/ca.crt " + user_folder)
    os.system("tar -czvf /var/www/FlaskApp/linux_app.tar.gz -C /var/www/FlaskApp/ linux_app")
    os.system("tar -czvf /var/www/FlaskApp/windows_app.tar.gz -C /var/www/FlaskApp/ windows_app")
    print subprocess.check_output(
        '/usr/share/easy-rsa/negotiation.sh ' + session['username'] + ' && cp /usr/share/easy-rsa/keys/' + session[
            'username'] + '* /var/www/FlaskApp/FlaskApp/' + session['username'] + '_files/', shell=True)


def edit_client_script(username, password):
    with open('/var/www/FlaskApp/linux_app/client_script.py', 'r') as file:
        linux_file_lines = file.readlines()
    linux_file_lines[18] = unicode("post_data = {'username': '" + username + "', 'password': '" + password + "'}" + "\n")
    with open('/var/www/FlaskApp/linux_app/client_script.py', 'w') as file:
        file.writelines(linux_file_lines)

    with open('/var/www/FlaskApp/windows_app/script.py', 'r') as file:
        windows_file_lines = file.readlines()
    windows_file_lines[14] = "post_data = {'username': '" + username + "', 'password': '" + password + "'}" + "\n"
    with open('/var/www/FlaskApp/windows_app/script.py', 'w') as file:
        file.writelines(windows_file_lines)


@app.route('/logout')
@login_required
def logout():
    os.system("rm -rf /var/www/FlaskApp/FlaskApp/" + session['username'] + "_files")
    os.system("rm -rf /var/www/FlaskApp/linux_app.tar.gz")
    os.system("rm -rf /var/www/FlaskApp/windows_app.tar.gz")
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


@app.route('/linux_download', methods=['GET', 'POST'])
@login_required
def file():
    create_files()
    minutes = request.form['minutes']
    with open('/var/www/FlaskApp/FlaskApp/timing_log.log', 'a') as f:
        f.write(session.get('username') + ' requested linux_app for ' + minutes + ' minutes' + "\n")
        f.close()
    filename = '/var/www/FlaskApp/linux_app.tar.gz'
    return send_file(filename, as_attachment=True, mimetype='application/gzip')


@app.route('/windows_download', methods=['GET', 'POST'])
@login_required
def windows_file():
    create_files()
    minutes = request.form['minutes']
    with open('/var/www/FlaskApp/FlaskApp/timing_log.log', 'a') as f:
        f.write(session.get('username') + ' requested windows_app for ' + minutes + ' minutes' + "\n")
        f.close()
    filename = '/var/www/FlaskApp/windows_app.tar.gz'
    return send_file(filename, as_attachment=True, mimetype='application/gzip')


@app.route('/cacert')
@login_required
def cacert():
    filename = '/usr/share/easy-rsa/keys/ca.crt'
    return send_file(filename, as_attachment=True, mimetype='application/text')


@app.route('/clientcert')
@login_required
def clientcert():
    filename = '/usr/share/easy-rsa/keys/' + session['username'] + '.crt'
    return send_file(filename, as_attachment=True, mimetype='application/text')


@app.route('/clientkey')
@login_required
def clientkey():
    filename = '/usr/share/easy-rsa/keys/' + session['username'] + '.key'
    return send_file(filename, as_attachment=True, mimetype='application/text')


def set_timer_for_revoke(username, time):
    t = Timer(time, revoke_client, [username])
    t.start()


def revoke_client(username):
    os.system("/var/www/FlaskApp/FlaskApp/key_management_scripts/revoke.sh " + username)


def unrevoke_client(username):
    os.system("/var/www/FlaskApp/FlaskApp/key_management_scripts/unrevoke.sh " + username)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
