import flask_login
from . import db

class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    is_authenticated = db.Column(db.Boolean(), unique=False, nullable=False, default=False)
    is_anonymous = False

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return self.id
