"""flask app for flask_notes"""

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, Note
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm, NoteForm, CSRFProtectForm

bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

USER_NAME = 'username'


@app.get('/')
def show_homepage():
    """ redirects user to register page"""

    return redirect('/register')

################ ROUTES FOR USER LOGININ/REGISTRATION ##########################


@app.route('/register', methods=['GET', 'POST'])
def show_registration_form():
    """shows user registration form
        validates user info and adds user to database """

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.register(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        session[USER_NAME] = user.username

        flash(f"User account created with username: {user.username}")
        return redirect(f"/users/{user.username}")
    else:
        return render_template("user_register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """ GET: shows user login form 
            - render user_login.html template
        POST: authenticate user credentials
            - if valid credentials, redirect to /users/user.username
            - if invalid credentials, redirect to login_page
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data,
        )

        if user:
            session[USER_NAME] = user.username
            return redirect(f"/users/{user.username}")
        else:
            flash(f"Username and password combo invalid")
            return render_template("user_login.html", form=form)
    else:
        return render_template("user_login.html", form=form)


@app.get('/users/<username>')
def show_user_page(username):
    """ Show user page if user logged in 
        and username from url matches session username 
        if not redirect to login page """

    if session.get(USER_NAME) != username:
        flash(f"You must login to view that page, you nitwit!")
        return redirect("/login")

    user = User.query.filter_by(username=session[USER_NAME]).one_or_none()

    # Get user's notes
    notes = Note.query.filter_by(owner=session[USER_NAME]).all()

    form = CSRFProtectForm()
    return render_template(
        "user_info_page.html",
        user=user,
        form=form,
        notes=notes,
    )


@app.post('/logout')
def logout_user():
    """logs user out and redirects to homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(USER_NAME, None)

    return redirect('/')


@app.post('/users/<username>/delete')
def delete_user(username):
    """Removes user and all user's notes from database and session"""

    form = CSRFProtectForm()
    # check that user is logged in,
    # logged in user is same as user being deleted,
    # request came from our site
    if session.get(USER_NAME) != username:

        flash(f"You cannot delete a different user, you nitwit!")
        return redirect("/")

    user = User.query.get_or_404(username)

    session.pop(USER_NAME, None)

    Note.query.filter_by(owner=username).delete()
    db.session.delete(user)
    db.session.commit()

    return redirect('/')


################ ROUTES FOR NOTES ##########################

@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def add_note(username):
    """ Add note for user 
        - GET: Renders add note form template
        - POST: saves note data to database, redirects to user info page
    """

    if session.get(USER_NAME) != username:
        flash(f"You must login to view that page, you nitwit!")
        return redirect("/login")

    form = NoteForm()

    if form.validate_on_submit():
        note = Note(
            owner=username,
            title=form.title.data,
            content=form.content.data,
        )

        db.session.add(note)
        db.session.commit()
        return redirect(f"/users/{username}")
    else:
        return render_template("note_add.html", form=form)


@app.route('/notes/<int:note_id>/update', methods=['GET', 'POST'])
def update_note(note_id):
    """ displays a form to update a note
        updates a note and redirects to /users/<username>"""
    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)

    username = note.owner
    if session.get(USER_NAME) != username:

        flash(f"You cannot delete this note, you nitwit!")
        return redirect("/")

    if form.validate_on_submit():

        note.title = form.title.data,
        note.content = form.content.data

        db.session.commit()

        flash(f'Updated {note.title}')
        return redirect(f'/users/{note.owner}')

    else:
        return render_template('note_update.html', form=form, note=note)


@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """removes a note from the database and redirects to
        to users/<username>"""

    note = Note.query.get_or_404(note_id)
    username = note.owner

    if session.get(USER_NAME) != username:

        flash(f"You cannot delete this note, you nitwit!")
        return redirect("/")

    db.session.delete(note)
    db.session.commit()

    return redirect(f'/users/{username}')
