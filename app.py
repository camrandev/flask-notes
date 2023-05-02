"""Flask app for Cupcakes"""
import os

from flask import Flask, render_template, redirect, flash, jsonify, request, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.get('/')
def home():
    """Redirecting to register page"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user: show form and register/create a user"""

    form = RegisterForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        user=User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session['username'] = username

        return redirect(f'/users/{username}')

    else:
        return render_template('form.html', form=form)






