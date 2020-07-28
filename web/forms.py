# forms.py

from wtforms import Form, StringField, SelectField, validators, DateField
from quads.config import conf


class ModelSearchForm(Form):
    models_list = conf.get("models").split(",")
    models_choices = []
    for model in models_list:
        models_choices.append((model, model))
    model = SelectField('Models:', choices=models_choices)
    start = DateField('Start at', format="%m/%d/%Y")
    end = DateField('End at', format="%m/%d/%Y")
