from flask import Blueprint

bp = Blueprint('userinput', __name__)

from app.userinput import handler
