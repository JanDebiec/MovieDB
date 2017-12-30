from flask import Blueprint

bp = Blueprint('db', __name__)

from app.db import handler
