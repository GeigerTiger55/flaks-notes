"""flask app for flask_notes"""

from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from flask_bcrypt import Bcrypt
from forms import RegistrationForm

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
            password = form.username.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data
        )
    ######### finish this route#########