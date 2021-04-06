
# app.py

from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
Bootstrap(app)

app.config.from_object(Config)
