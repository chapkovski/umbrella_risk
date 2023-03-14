from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class FirstPage(Page):
    def is_displayed(self):
        return self.round_number == 1


page_sequence = [FirstPage]
