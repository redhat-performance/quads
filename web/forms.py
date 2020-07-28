# forms.py

from wtforms import SelectField, DateField, validators
from flask_wtf import FlaskForm
from quads.config import conf


class ModelSearchForm(FlaskForm):
    models_list = conf.get("models").split(",")
    models_choices = [("All", "All")]
    for model in models_list:
        models_choices.append((model, model))
    model = SelectField('Models:', choices=models_choices)
    start = DateField('Start at', format="%m/%d/%Y", validators=[validators.data_required()])
    end = DateField('End at', format="%m/%d/%Y", validators=[validators.data_required()])
