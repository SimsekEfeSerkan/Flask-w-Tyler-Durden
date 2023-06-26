from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_session import Session
import os




app = Flask(__name__)
app.config ['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config ['MYSQL_DB'] = 'mockingbird'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_PERMANENT'] = False
mysql = MySQL(app)




class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')






@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/articles<string:id>')
def articles(id):
    return "Articles id"+id

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['name']
        username = request.form['username'],  
        password = request.form['password']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, username, password, email) VALUES(%s, %s, %s, %s)", (name, username, password, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            flash('You are now logged in', 'success')
            return redirect(url_for('index'))

        else:
            return flash('Incorrect username/password!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))









if __name__ == '__main__':
    app.run(debug=True)
    session["key"] = "value"