from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(
        db.String(20),
        primary_key=True,
    )
    password = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )
    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, 
                username, 
                password, 
                email, 
                first_name, 
                last_name):
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username, password=hashed)





def connect_db(app):
    """Connects this database to Flask app."""

    db.app = app
    db.init_app(app)