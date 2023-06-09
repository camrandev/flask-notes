"""Flask app for Cupcakes"""
import os

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm
from sqlalchemy import exc

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

    #if user is already logged in, redirect them to profile page
    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash(f"user name already exists")
            return render_template('register_form.html', form=form)


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

    if 'username' not in session:
        flash('You must be logged in to view!')
        return redirect('/')

    if session['username'] != username:
        flash('No snooping!')
        return redirect(f'/')

    else:
        user = User.query.get_or_404(username)
        logout_form = CSRFProtectForm()
        delete_form = CSRFProtectForm()
        delete_note_form = CSRFProtectForm()

        return render_template("user_detail.html", user=user, logout_form=logout_form, delete_form=delete_form, notes=user.notes,  delete_note_form=delete_note_form)

@app.post('/logout')
def user_logout():
    """Logs user out and redirects to homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')

@app.route('/notes/<note_id>/update', methods=['GET', 'POST'])
def update_note(note_id):
    """show edit form, update a note, and redirect to user detail page"""

    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()

        flash(f"Note updated!")
        return redirect(f'/users/{note.owner_username}')
    else:
        return render_template('edit_note_form.html', note=note, form=form)

@app.post('/users/<username>/delete')
def delete_user_and_all_notes(username):
    """Delete a user and all associated notes"""

   #protect the route
    if session['username'] != username:
        return redirect(f"/users/{session['username']}")

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

        user = User.query.get_or_404(username)

        for note in user.notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        flash('User deleted!')
        return redirect('/')


    #delete the user
    #delete all notes associated with the user

@app.route('/users/<username>/notes/add', methods=['POST', 'GET'])
def add_notes(username):
    """Show form and add a new note"""

    form = NoteForm()

    if form.validate_on_submit():
        user=User.query.get_or_404(username)
        title = form.title.data
        content = form.content.data

        new_note = Note(title=title, content=content)
        user.notes.append(new_note)

        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('add_note_form.html', form=form, username=username)


