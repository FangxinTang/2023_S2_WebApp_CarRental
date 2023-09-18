from flask import Flask

app = Flask(__name__)
# app.url_map.strict_slashes = False

from app import views
from app import employee_views
from app import connect
from app import db