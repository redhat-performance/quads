# forms.py

from wtforms import DateField, validators, SelectMultipleField
from flask_wtf import FlaskForm
from quads.config import Config


class ModelSearchForm(FlaskForm):
    models_list = Config.models.split(",")
    models_choices = []
    for model in models_list:
        models_choices.append((model, model))
    model = SelectMultipleField("Models:", choices=models_choices)
    start = DateField(
        "Start at", format="%m/%d/%Y", validators=[validators.data_required()]
    )
    end = DateField(
        "End at", format="%m/%d/%Y", validators=[validators.data_required()]
    )
