from umbrella.configs.mpl import Constants
import random
from otree.api import BaseConstants, Currency as cu
from random import randrange

def set_payoffs(self):
    # random draw to determine whether to pay the "high" or "low" outcome of the randomly picked lottery
    # ------------------------------------------------------------------------------------------------------------
    self.mpl_random_draw = randrange(1, len(self.participant.vars['mpl_choices']))

    # set <choice_to_pay> to participant.var['choice_to_pay'] determined creating_session
    # ------------------------------------------------------------------------------------------------------------
    self.mpl_choice_to_pay = self.participant.vars['mpl_choice_to_pay']

    # elicit whether lottery "A" or "B" was chosen for the respective choice
    # ------------------------------------------------------------------------------------------------------------
    self.mpl_option_to_pay = getattr(self, self.mpl_choice_to_pay)

    # set player's payoff
    # ------------------------------------------------------------------------------------------------------------
    if self.mpl_option_to_pay == 'A':
        if self.mpl_random_draw <= self.participant.vars['mpl_index_to_pay']:
            self.payoff = Constants.lottery_a_hi
        else:
            self.payoff = Constants.lottery_a_lo
    else:
        if self.mpl_random_draw <= self.participant.vars['mpl_index_to_pay']:
            self.payoff = Constants.lottery_b_hi
        else:
            self.payoff = Constants.lottery_b_lo

# determine consistency
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_consistency(self):

    n = Constants.num_choices

    # replace A's by 1's and B's by 0's
    self.participant.vars['mpl_choices_made'] = [
        1 if j == 'A' else 0 for j in self.participant.vars['mpl_choices_made']
    ]

    # check for multiple switching behavior
    for j in range(1, n):
        choices = self.participant.vars['mpl_choices_made']
        self.mpl_inconsistent = 1 if choices[j] > choices[j - 1] else 0
        if self.mpl_inconsistent == 1:
            break

# determine switching row
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_switching_row(self):

    # set switching point to row number of first 'B' choice
    if self.mpl_inconsistent == 0:
        self.mpl_switching_row = sum(self.participant.vars['mpl_choices_made']) + 1
