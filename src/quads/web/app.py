# app.py

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = "flask rocks!"
Bootstrap(app)
