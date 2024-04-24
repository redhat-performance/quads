from wtforms import validators, SelectMultipleField, StringField
from flask_wtf import FlaskForm
from quads.config import Config


class ModelSearchForm(FlaskForm):
    models_list = Config.models.split(",")
    models_choices = []
    for model in models_list:
        models_choices.append((model, model))
    model = SelectMultipleField("Models:", choices=models_choices)
    date_range = StringField("Date Range:", validators=[validators.DataRequired()])
