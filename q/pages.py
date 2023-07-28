from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json
import logging

PRODUCER = "P"
INTERPRETER = "I"
logger = logging.getLogger("umbrella.q")

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

class Big5(Page):
    def post(self):
        try:
            data = json.loads(self.request.POST.get('surveyholder')).get('big5')
            print(data)
            
            if data:
                for k, v in data.items():
                    setattr(self.player, k, v.get('col1'))
        except Exception as e:
            print(e)
            logger.error('cant get data from big5 questionnaire')
        return super().post()

     
class Feedback(Page):
    form_model='player'
    form_fields=['feedback']

page_sequence = [
    Q,
    Big5,
    Feedback,
    ]
