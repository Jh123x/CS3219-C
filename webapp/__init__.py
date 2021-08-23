import os
from flask import Flask
from .models import db, User
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from .views import app as main_blueprint


csrf = CSRFProtect()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my-secret-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    login_manager.login_view = 'login'

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app


app = create_app()
app.register_blueprint(main_blueprint)
if not os.path.isfile("database.db"):
    db.create_all(app=app)
