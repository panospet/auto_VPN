# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, current_app, send_file, escape
from functools import wraps
import os
import subprocess


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

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    return render_template('index.html')  # render a template
    # return "Hello, World!"  # return a string

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')  # render a template

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'test' or request.form['password'] != 'test') and (request.form['username'] != 'admin' or request.form['password'] != 'admin'):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('Hello ' + session['username'] + ', you were logged in.')
            create_files()
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

def create_files():
    user_folder = "/var/www/FlaskApp/FlaskApp/" + session['username'] + "_files"
    os.system("mkdir -p " + user_folder)
    os.system("cp /usr/share/easy-rsa/keys/ca.crt " + user_folder)
    print subprocess.check_output('/usr/share/easy-rsa/negotiation.sh ' + session['username'] + ' && cp /usr/share/easy-rsa/keys/' + session['username'] +'* /var/www/FlaskApp/FlaskApp/' + session['username'] + '_files/', shell=True)

@app.route('/logout')
@login_required
def logout():
    os.system("rm -rf /var/www/FlaskApp/FlaskApp/" + session['username'] +"_files")
    os.system("rm -rf /var/www/FlaskApp/FlaskApp/test.txt")
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

@app.route('/file')
@login_required
def file():
#    os.system("echo hello, " + session['username'] + "! > /var/www/FlaskApp/FlaskApp/client_script.sh")
    filename = '/var/www/FlaskApp/FlaskApp/client_script.sh'
    return send_file(filename, as_attachment=True, mimetype='application/text')

@app.route('/cacert')
@login_required
def cacert():
    filename = '/usr/share/easy-rsa/keys/ca.crt'
    return send_file(filename, as_attachment=True, mimetype='application/text')

@app.route('/clientcert')
@login_required
def clientcert():
    user_folder = "/var/www/FlaskApp/FlaskApp/" + session['username'] + "_files/"
    filename = user_folder + session['username'] + ".crt"
    return send_file(filename, as_attachment=True, mimetype='application/text')

@app.route('/clientkey')
@login_required
def clientkey():
    user_folder = "/var/www/FlaskApp/FlaskApp/" + session['username'] + "_files/"
    filename = user_folder + session['username'] + ".key"
    return send_file(filename, as_attachment=True, mimetype='application/text')

@app.route('/deftones')
@login_required
def deftones():
    filename = "Deftones_Gore_2016.zip"
    return send_file(filename, as_attachment=True, mimetype='application/zip')

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)


# R.I.P. Lemmy
