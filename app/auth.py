from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, Blueprint, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash 
from .models import User 
from . import db 

auth = Blueprint("auth",__name__) 

@auth.route("/login/", methods=['GET', 'POST'])
def login(): 
    if request.method == "POST":
        email = request.form.get('em')
        password = request.form.get('pwd')
        user = User.query.filter_by(email=email).first()
        if not user: 
            flash("Incorrect email or password!", category="error")
            return render_template("login.html", user=current_user)
        if check_password_hash(user.password, password):
            login_user(user=user, remember=True)
            flash("Logged in successfully!", category="success")
            return redirect(url_for('views.myfiles', user=current_user))
        else: 
            flash("Incorrect email or password!", category="error")
    return render_template('login.html', user=current_user)

@auth.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('usr')
        email = request.form.get('em')
        password = request.form.get('pwd')
        password2 = request.form.get('pwd2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("A user already exists with this email address!", category="error")
        elif not(password == password2):
            flash("Passwords don't match!", category="error")
        elif len(email) < 4: 
            flash("Email is too short!", category="error")
        elif len(password) < 4:
            flash("Password is too short!", category="error")
        else: 
            user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully!", category="success")
            return redirect(url_for('auth.login', user=current_user))
    return render_template('register.html', user=current_user)
    
@auth.route('/logout/')
@login_required
def logout(): 
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for('views.home', user=current_user))

#test







