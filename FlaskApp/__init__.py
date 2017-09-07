#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file, escape  # NOQA
from functools import wraps
import os
import subprocess
from auth import *  # NOQA
from add_user_to_db import add_user
import threading
import datetime
import time
from pbkdf2.pbkdf2 import crypt

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
    user = User.query.filter_by(username=session.get('username')).first()
    if user.timer_name is not None:
        minutes = 'You are authorized to use the VPN application for another ' + str(calculate_remaining_time(user.timer_start_time, user.timer_minutes)) + ' minutes.'
    else:
        minutes = 'You are not authorized to use the application (no time left). Please apply for more.'
    return render_template('index.html', minutes=minutes)


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
        if User.query.filter_by(username=username, password=crypt(password, '1we1505f7', 26000)).first() is None:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('Hello ' + session['username'] + ', you were logged in.')
            # flash('You are authorized to use the application for another ' + minutes + ' minutes.')
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


@app.route('/linux_download', methods=['GET', 'POST'])
@login_required
def file():
    create_files()
    minutes = request.form['minutes']
    if minutes == '':
        minutes = '60'
    log('User ' + session.get('username') + ' requested linux_app for ' + minutes + ' minutes' + "\n")
    set_timer_for_revoke(session.get('username'), float(minutes))
    filename = '/var/www/FlaskApp/linux_app.tar.gz'
    return send_file(filename, as_attachment=True, mimetype='application/gzip')


@app.route('/windows_download', methods=['GET', 'POST'])
@login_required
def windows_file():
    create_files()
    minutes = request.form['minutes']
    if minutes == '':
        minutes = '60'
    log('User ' + session.get('username') + ' requested windows_app for ' + minutes + ' minutes' + "\n")
    set_timer_for_revoke(session.get('username'), minutes)
    filename = '/var/www/FlaskApp/windows_app.tar.gz'
    return send_file(filename, as_attachment=True, mimetype='application/gzip')


def set_timer_for_revoke(username, time):
    unrevoke_client(username)
    t = threading.Timer(time * 60, revoke_client, [username])
    user = User.query.filter_by(username=session.get('username')).first()
    user.timer_name = t.getName()
    user.timer_start_time = datetime.datetime.now().replace(microsecond=0)
    user.timer_minutes = time
    db.session.commit()
    log('User ' + username + ' was set a timer with name ' + user.timer_name + ' for ' + str(time) + ' minutes.' + "\n")
    t.start()
    log('Timer ' + t.getName() + ' started.' + "\n")


def revoke_client(client_name):
    log('Revoke script for client ' + client_name + ' about to be called.' + "\n")
    os.system("/var/www/FlaskApp/FlaskApp/key_management_scripts/revoke.sh " + client_name)
    user = User.query.filter_by(username=client_name).first()
    user.timer_name = None
    user.timer_start_time = None
    user.timer_minutes = None
    db.session.commit()
    log('Revoke script for client ' + client_name + ' called and finished.' + "\n")


def unrevoke_client(client_name):
    log('Unrevoke operation for client ' + client_name + ' started.' + "\n")
    user = User.query.filter_by(username=client_name).first()
    if user.timer_name is not None:
        for thr in threading.enumerate():
            if thr.getName() == user.timer_name:
                log('Timer ' + thr.getName() + ' is about to be canceled, due to newer request' + "\n")
                thr.cancel()
    user.timer_name = None
    db.session.commit()
    os.system("/var/www/FlaskApp/FlaskApp/key_management_scripts/unrevoke.sh " + client_name)
    log('Unrevoke operation finished for client ' + client_name + '.' + "\n")


@app.route('/online_users', methods=['GET', 'POST'])
@login_required
def online_users():
    users = User.query.all()
    for u in users:
        if u.timer_name is not None:
            flash('User ' + u.username + ', timer: ' + u.timer_name + ', remaining:' + str(calculate_remaining_time(u.timer_start_time, u.timer_minutes)) + "\n")
    return render_template('online_users.html')


def log(string):
    with open('/var/www/FlaskApp/FlaskApp/timing_log.log', 'a') as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': ' + string)
        f.close


def calculate_remaining_time(timer_start_time, minutes):
    fmt = '%Y-%m-%d %H:%M:%S'
    timer_start_time = datetime.datetime.strptime(timer_start_time, fmt)
    now = datetime.datetime.now()

    d1_ts = time.mktime(timer_start_time.timetuple())
    d2_ts = time.mktime(now.timetuple())

    remaining = minutes - int((d2_ts - d1_ts) / 60)
    if remaining < 0:
        remaining = 0

    return remaining


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
