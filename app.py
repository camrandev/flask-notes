"""Flask app for Cupcakes"""
import os

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

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

# FIXME: add validation if logged in, no need to go to register or log in page
# (-> go straight to user detail page)
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user) #integrity error for duplicated value TODO: try catch only this line (need to import the error)
        db.session.commit()

        session['username'] = user.username

        return redirect(f'/users/{username}')

    else:
        return render_template('register_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Accepts GET, POST
    GET: render the login page
    POST: attempt to credential the user and login if successful
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f'users/{user.username}')

        else:
            form.username.errors = ["username/password mismatch"]

    return render_template('login_form.html', form=form)

@app.get('/users/<username>')
def user_detail_page(username):
    """user detail page only viewable if logged in"""

    if 'username' not in session: #FIXME: only logged in user (1. logged in? 2. that specific user?)
        flash('You must be logged in to view!')
        return redirect('/')

    else:
        user = User.query.filter_by(username=username).get_or_404()
        form = CSRFProtectForm()

        return render_template("user_detail.html", user=user, form=form)

@app.post('/logout')
def user_logout():
    """Logs user out and redirects to homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')