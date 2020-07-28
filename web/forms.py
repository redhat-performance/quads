# forms.py

from wtforms import Form, StringField, SelectField, validators
from quads.config import conf


class ModelSearchForm(Form):
    models_str = conf.get("models")
    models = models_str.split(",")
    models_choices = []
    for model in models:
        models_choices.append((model, model))
    select = SelectField('Models:', choices=models_choices)
