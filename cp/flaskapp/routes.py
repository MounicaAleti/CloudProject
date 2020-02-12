from flaskapp.models import User
from flask import Flask, render_template, request, redirect, url_for, flash

from flaskapp import app, db
from flask_login import login_user, current_user, logout_user


@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        p_uname = request.form["username"]
        p_email = request.form['email']
        p_fname = request.form['firstname']
        p_lname = request.form['lastname']
        p_pwd = request.form['psw']
        p_cpwd = request.form['psw-repeat']
        user = User.query.filter_by(username=p_uname).first()
        if user is None:
            if p_pwd == p_cpwd:
                new_data = User(username=p_uname, email=p_email, fname=p_fname, lname=p_lname, password=p_pwd)
                db.session.add(new_data)
                db.session.commit()
                flash("You are successfully signed up")
                return redirect(url_for('home'))
            else:
                flash("Error with password. Enter same passwords in both fields.")
                return redirect(url_for('register'))
        else:
            flash('Username already exists enter other value')
            return redirect(url_for('register'))

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        p_uname = request.form["uname"]
        p_psw = request.form['psw']
        user = User.query.filter_by(username=p_uname).first()
        if user is None:
            flash("Username doesn't exist")
            return redirect(url_for('login'))
        else:
            if user.password == p_psw:
                login_user(user)
                flash("You've successfully logged in")
                return redirect(url_for('home'))
            else:
                flash("Password entered is wrong")
                return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

