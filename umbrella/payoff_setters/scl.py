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
    self.scl_outcome_to_pay = "high" if rnd <= p else "low"

    # select lottery choice out of list of lotteries
    # ------------------------------------------------------------------------------------------------------------
    lottery_selected = [i for i in self.participant.vars['scl_lotteries'] if i[0] == self.scl_lottery_choice]
    lottery_selected = lottery_selected[0]

    # set player's payoff
    # ------------------------------------------------------------------------------------------------------------
    if self.scl_outcome_to_pay == "high":
        self.payoff = lottery_selected[2]
    else:
        self.payoff = lottery_selected[1]

