from flask import Blueprint

app = Blueprint('main', __name__)

from src.main import error, views  # noqa: I101, F401
