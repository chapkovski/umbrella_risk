from umbrella.configs.cem import Constants
import random
from otree.api import BaseConstants, Currency as cu


def set_payoffs(self):
    # random draw to determine whether to pay the "high" or "low" outcome of the randomly picked lottery
    # ------------------------------------------------------------------------------------------------------------
    self.random_draw = randrange(1, 100)

    # set <choice_to_pay> to participant.var['choice_to_pay'] determined creating_session
    # ------------------------------------------------------------------------------------------------------------
    self.choice_to_pay = self.participant.vars['cem_choice_to_pay']

    # determine whether the lottery (option "A") or the sure payoff (option "B") was chosen
    # ------------------------------------------------------------------------------------------------------------
    self.option_to_pay = getattr(self, self.choice_to_pay)

    # set player's payoff
    # ------------------------------------------------------------------------------------------------------------
    indices = [list(t) for t in zip(*self.participant.vars['cem_choices'])][0]
    index_to_pay = indices.index(self.participant.vars['cem_index_to_pay']) + 1
    choice_to_pay = self.participant.vars['cem_choices'][index_to_pay - 1]

    if self.option_to_pay == 'A':
        if self.random_draw <= choice_to_pay[2]:
            self.payoff = Constants.endowment + choice_to_pay[3]
        else:
            self.payoff = Constants.endowment + choice_to_pay[4]
    else:
        self.payoff = Constants.endowment + choice_to_pay[5]

    # set payoff as global variable
    # ------------------------------------------------------------------------------------------------------------
    self.participant.vars['cem_payoff'] = self.payoff
    self.participant.vars['cem_option_to_pay'] = self.option_to_pay

    # set payoff to zero if CEM is not the task to be payed
    # ------------------------------------------------------------------------------------------------------------
    if self.participant.vars['task_to_pay'] != 'cem':
        self.payoff = cu(0)
 def set_consistency(self):

        n = Constants.num_choices

        # replace A's by 1's and B's by 0's
        self.participant.vars['cem_choices_made'] = [
            1 if j == 'A' else 0 for j in self.participant.vars['cem_choices_made']
        ]

        # check for multiple switching behavior
        for j in range(1, n):
            choices = self.participant.vars['cem_choices_made']
            self.inconsistent = 1 if choices[j] > choices[j - 1] else 0
            if self.inconsistent == 1:
                break

    # determine switching row
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_switching_row(self):

        # set switching point to row number of first 'B' choice
        if self.inconsistent == 0:
            self.switching_row = sum(self.participant.vars['cem_choices_made']) + 1
