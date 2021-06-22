from flask import Flask, config, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from .dash_app import create_dash_application, create_denver_application, create_boston_application, create_sf_application, create_la_application

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__,  static_url_path='/static')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app,db)
    login_manager.login_view = 'auth.login'

    create_dash_application(app)
    create_denver_application(app)
    create_boston_application(app)
    create_sf_application(app)
    create_la_application(app)

    from app.blueprints.authentication import bp as auth
    app.register_blueprint(auth)

    from app.blueprints.city import bp as cities
    app.register_blueprint(cities)
    
    with app.app_context():
        from .import routes

    from .import models

    return app



