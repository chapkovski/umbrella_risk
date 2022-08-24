from umbrella.configs.mpl import Constants
import random
from otree.api import BaseConstants, Currency as cu


def set_payoffs(self):
    # random draw to determine whether to pay the "high" or "low" outcome of the randomly picked lottery
    # ------------------------------------------------------------------------------------------------------------
    self.random_draw = randrange(1, len(self.participant.vars['mpl_choices']))

    # set <choice_to_pay> to participant.var['choice_to_pay'] determined creating_session
    # ------------------------------------------------------------------------------------------------------------
    self.choice_to_pay = self.participant.vars['mpl_choice_to_pay']

    # elicit whether lottery "A" or "B" was chosen for the respective choice
    # ------------------------------------------------------------------------------------------------------------
    self.option_to_pay = getattr(self, self.choice_to_pay)

    # set player's payoff
    # ------------------------------------------------------------------------------------------------------------
    if self.option_to_pay == 'A':
        if self.random_draw <= self.participant.vars['mpl_index_to_pay']:
            self.payoff = Constants.lottery_a_hi
        else:
            self.payoff = Constants.lottery_a_lo
    else:
        if self.random_draw <= self.participant.vars['mpl_index_to_pay']:
            self.payoff = Constants.lottery_b_hi
        else:
            self.payoff = Constants.lottery_b_lo

    # set payoff as global variable
    # ------------------------------------------------------------------------------------------------------------
    self.participant.vars['mpl_payoff'] = self.payoff
    self.participant.vars['mpl_option_to_pay'] = self.option_to_pay

    # set payoff to zero if MPL is not the task to be payed
    # ------------------------------------------------------------------------------------------------------------
    if self.participant.vars['task_to_pay'] != 'mpl':
        self.payoff = c(0)

