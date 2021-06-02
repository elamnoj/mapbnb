from flask import Blueprint

bp = Blueprint('city', __name__, url_prefix='/city')

from .import routes

