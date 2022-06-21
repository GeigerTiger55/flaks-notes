"""flask app for flask_notes"""

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm, CSRFProtectForm

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

    if 'username' not in session or session[USER_NAME] != username:
        flash(f"You must login to view that page, you nitwit!")
        return redirect("/login")
    
    user = User.query.filter_by(username=session[USER_NAME]).one_or_none()
    form = CSRFProtectForm()
    return render_template("user_info_page.html", user=user, form=form)


@app.post('/logout')
def logout_user():
    """logs user out and redirects to homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(USER_NAME, None)

    return redirect('/')
