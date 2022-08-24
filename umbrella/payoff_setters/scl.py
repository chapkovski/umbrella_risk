from umbrella.configs.scl import Constants
import random
from otree.api import BaseConstants, Currency as c


    # set payoffs
    # ----------------------------------------------------------------------------------------------------------------
def set_payoffs(self):

    # choose outcome to pay (high or low) dependent on <probability>
    # ------------------------------------------------------------------------------------------------------------
    p = Constants.probability
    rnd = random.randint(1, 100)
    self.outcome_to_pay = "high" if rnd <= p else "low"

    # select lottery choice out of list of lotteries
    # ------------------------------------------------------------------------------------------------------------
    lottery_selected = [i for i in self.participant.vars['scl_lotteries'] if i[0] == self.lottery_choice]
    lottery_selected = lottery_selected[0]

    # set player's payoff
    # ------------------------------------------------------------------------------------------------------------
    if self.outcome_to_pay == "high":
        self.payoff = lottery_selected[2]
    else:
        self.payoff = lottery_selected[1]

    # set payoff as global variable
    # ------------------------------------------------------------------------------------------------------------
    self.participant.vars['scl_payoff'] = self.payoff
    self.participant.vars['scl_outcome_lo'] = lottery_selected[1]
    self.participant.vars['scl_outcome_hi'] = lottery_selected[2]
    self.participant.vars['scl_lottery_choice'] = self.lottery_choice
    self.participant.vars['scl_outcome_to_pay'] = self.outcome_to_pay

    # set payoff to zero if SCL is not the task to be payed
    # ------------------------------------------------------------------------------------------------------------
    if self.participant.vars['task_to_pay'] != 'scl':
        self.payoff = c(0)
