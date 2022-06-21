from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
bcrypt = Bcrypt()

############# USER CLASS #########################################
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
        """ Register user - generate password hash and return instance of this
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


############# NOTES CLASS #########################################
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True,
    )
    title = db.Column(
        db.String(100),
        nullable=False,
    )
    content = db.Column(
        db.Text,
        nullable=False,
    )
    owner = db.Column(
        db.String(30),
        db.ForeignKey('users.username'),
        nullable=False,
    )

    user = db.relationship('User', backref='notes')


def connect_db(app):
    """Connects this database to Flask app."""

    db.app = app
    db.init_app(app)
