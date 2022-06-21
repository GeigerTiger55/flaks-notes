"""flask app for flask_notes"""

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm

bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get('/')
def show_homepage():
    """ redirects user to register page"""

    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def show_registration_form():
    """shows user registration form """

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.register(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data
        )
    
        db.session.add(user)
        db.session.commit()

        flash(f"User account created with username: {user.username}")
        return redirect("/secret")
    else:
        return render_template("user_register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """ GET: shows user login form 
            - render user_login.html template
        POST: authenticate user credentials
            - if valid credentials, redirect to /secret
            - if invalid credentials, redirect to login_page
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username = form.username.data,
            password = form.password.data,
        )
    
        if user: 
            session['username'] = user.username
            return redirect("/secret")
        else:
            flash(f"Username and password combo invalid")
            return render_template("user_login.html", form=form)    
    else:
        return render_template("user_login.html", form=form)


@app.get('/secret')
def show_secret_page():
    """ Show secret page """
    if 'username' not in session:
        flash(f"You must login to view that page, you nitwit!")
        return redirect("/login")
    else:
        return render_template("secret_page.html")