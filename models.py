from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
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
        """ Register user - generate password hash and create instance of this
            class (User)
        """
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    @classmethod
    def authenticate(cls, username, password):
        """ Authenticate user credentials
            - If valid username/password, return user instance
            - If invalid username/password, return False
        """
        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


def connect_db(app):
    """Connects this database to Flask app."""

    db.app = app
    db.init_app(app)
