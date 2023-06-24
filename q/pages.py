from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Q(Page):
    form_model = "player"
    form_fields = [
        "age",
        "gender",
        "marital",
        "employment",
        "income",
        "instructions_clarity",
    ]


page_sequence = [Q]
