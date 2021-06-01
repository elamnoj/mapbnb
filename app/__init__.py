from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .dash_app import create_dash_application, create_austin_application, create_boston_application, create_sf_application, create_dallas_application



app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

create_dash_application(app)
create_austin_application(app)
create_boston_application(app)
create_sf_application(app)
create_dallas_application(app)

from .import routes, models

