from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from random import choice
from StartApp.pages import Page


# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    return {
        'prob_hi': "{0:.1f}".format(Constants.probability) + "%",
        'prob_lo': "{0:.1f}".format(100 - Constants.probability) + "%"
    }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        num_lotteries = Constants.num_lotteries + 1 if Constants.risk_loving else Constants.num_lotteries


        return {
            'num_lotteries': num_lotteries,
            'prob_hi': "{0:.1f}".format(Constants.probability) + "%",
            'prob_lo': "{0:.1f}".format(100 - Constants.probability) + "%",
            'task_number': self.player.participant.vars['task_number']
        }


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form model
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'

    # form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_fields = ['lottery_choice']

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        return {
            'lotteries': self.player.participant.vars['scl_lotteries'],
            'prob_hi': "{0:.1f}".format(Constants.probability) + "%",
            'prob_lo': "{0:.1f}".format(100 - Constants.probability) + "%",
            'task_number': self.player.participant.vars['task_number']
        }

    # set payoff
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):
        self.player.set_payoffs()
        self.player.participant.vars['task_number'] = self.player.participant.vars['task_number']+1


# ******************************************************************************************************************** #
# *** PAGE SURVEY *** #
# ******************************************************************************************************************** #
class Survey(Page):

    # form model and model fields
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'
    form_fields = ['riskiness', 'confidence']

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        
        return {
            'lotteries': self.player.participant.vars['scl_lotteries'],
            'choice':    self.player.lottery_choice,
            'prob_hi': "{0:.1f}".format(Constants.probability) + "%",
            'prob_lo': "{0:.1f}".format(100 - Constants.probability) + "%"
        }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision,
                #Survey
                ]

if Constants.instructions:
    page_sequence.insert(0, Instructions)
