from otree.api import Currency as cu, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _
from random import choice
from StartApp.pages import Page

# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    return {
        'lottery_lo':  cu(Constants.lottery_lo),
        'lottery_hi':  cu(Constants.lottery_hi),
        'probability': "{0:.1f}".format(Constants.probability) + "%"
    }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1

# variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        return {
            'hi' : cu(Constants.lottery_hi),
            'lo' : cu(Constants.lottery_lo),
            'p' :  "{0:.1f}".format(Constants.probability) + "%",
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
    def get_form_fields(self):

        # unzip list of form_fields from <cem_choices> list
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices'])][1]

        # provide form field associated with pagination or full list
        if Constants.one_choice_per_page:
            page = self.subsession.round_number
            return [form_fields[page - 1]]
        else:
            return form_fields

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # specify info for progress bar
        total = Constants.num_choices
        page = self.subsession.round_number
        progress = page / total * 100


        if Constants.one_choice_per_page:
            return {
                'page':      page,
                'total':     total,
                'progress':  progress,
                'choices':   [self.player.participant.vars['cem_choices'][page-1]],
            }
        else:
            return {
                'choices':   self.player.participant.vars['cem_choices'],
                'task_number': self.player.participant.vars['task_number']
            }

    # set payoff, determine consistency, and set switching row
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):
       # self.participant.vars['task_to_pay'] = 'cem'
        self.player.participant.vars['task_number'] = self.player.participant.vars['task_number']+1
        # unzip indices and form fields from <cem_choices> list
        round_number = self.subsession.round_number
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices'])][1]
        indices = [list(t) for t in zip(*self.participant.vars['cem_choices'])][0]
        index = indices[round_number - 1]

        # if choices are displayed sequentially
        # ------------------------------------------------------------------------------------------------------------
        if Constants.one_choice_per_page:

            # replace current choice in <choices_made>
            current_choice = getattr(self.player, form_fields[round_number - 1])
            self.participant.vars['cem_choices_made'][index - 1] = current_choice

            # if current choice equals index to pay ...
            if index == self.player.participant.vars['cem_index_to_pay']:
                # set payoff
                self.player.set_payoffs()

            # after final choice
            if round_number == Constants.num_choices:
                # determine consistency
                self.player.set_consistency()
                # set switching row
                self.player.set_switching_row()

        # if choices are displayed in tabular format
        # ------------------------------------------------------------------------------------------------------------
        if not Constants.one_choice_per_page:

            # replace choices in <choices_made>
            for j, choice in zip(indices, form_fields):
                choice_i = getattr(self.player, choice)
                self.participant.vars['cem_choices_made'][j - 1] = choice_i

            # set payoff
            self.player.set_payoffs()
            # determine consistency
            self.player.set_consistency()
            # set switching row
            self.player.set_switching_row()


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

        # unzip <cem_choices> into list of lists
        choices = [list(t) for t in zip(*self.participant.vars['cem_choices'])]
        probabilities = choices[2]
        lottery_hi = choices[3]
        lottery_lo = choices[4]
        sure_payoffs = choices[5]

        zipped = list(
            zip(
                probabilities,
                lottery_hi,
                lottery_lo,
                sure_payoffs,
                self.participant.vars['cem_choices_made']
            )
        )


        return {
            'choices':   zipped
        }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision, 
                #Survey
                ]

if Constants.instructions:
    page_sequence.insert(0, Instructions)
