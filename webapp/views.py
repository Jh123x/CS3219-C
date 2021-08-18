# from app import app
from . import db
from .models import User
from .forms import LoginForm, RegisterForm

import sqlalchemy
from hashlib import sha512
from flask_login.utils import logout_user
from flask_login import login_required, login_user, current_user
from flask import request, render_template, flash, redirect, Blueprint


app = Blueprint("main_page", __name__, template_folder="templates")


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@login_required
@app.route('/profile', methods=["GET"])
def profile():
    if not current_user.is_authenticated:
        flash("You are not logged in")
        return redirect('/')
    return render_template('profile.html', username=current_user.username, user_data=[
        ('Username', current_user.username),
        ('Email', current_user.email),
    ])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect('/')

    if request.method == "GET":
        return render_template('login.html', form=form)

    if not form.validate():
        flash("Error with form submission", "error")
        return redirect('/login')

    # Login and validate the user.
    user = User.query.filter_by(username=form.username.data, password=sha512(
        form.password.data.encode()).hexdigest()).first()
    if user is None:
        flash("Username does not exist", "error")
        return redirect('/login')
    r = login_user(user, remember=form.remember_me)
    user.is_authenticated = True
    db.session.commit()
    if not r:
        flash("Wrong username or password", "error")
        return redirect('/login')

    flash('Logged in successfully.')
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect('/')

    if request.method == "GET":
        return render_template("register.html", form=form)

    if not form.validate():
        flash("Registration unsuccessful", "error")
        return redirect('/register')
    try:
        new_user = User(username=form.username.data, password=sha512(
            form.password.data.encode()).hexdigest(), email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        flash("Email or Username is already taken")
        return redirect('/register')
    return redirect('/login')


@login_required
@app.route('/logout', methods=["GET"])
def logout():
    if not current_user.is_authenticated:
        flash("You are not logged in")
        return redirect('/')
    current_user.is_authenticated = False
    logout_user()
    flash("You have logged out successfully")
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
