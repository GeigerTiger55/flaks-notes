"""flask app for flask_notes"""

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)



