from umbrella.configs.scl import Constants
import random
from otree.api import BaseConstants, Currency as c


def creating_session(self):
    for p in self.get_players():

        n = Constants.num_lotteries

        # create list of lottery indices
        # --------------------------------------------------------------------------------------------------------
        indices = [j for j in range(1, n + 1)]

        # create list of low and high outcomes (matched by index)
        # --------------------------------------------------------------------------------------------------------
        outcomes_lo = [c(Constants.sure_payoff - Constants.delta_lo * j) for j in range(0, n)]
        outcomes_hi = [c(Constants.sure_payoff + Constants.delta_hi * j) for j in range(0, n)]

        # append indices and outcomes by "risk loving" lottery if <risk_loving = True>
        # --------------------------------------------------------------------------------------------------------
        if Constants.risk_loving:
            indices.append(n + 1)
            outcomes_lo.append(c(outcomes_lo[-1] - Constants.delta_hi))
            outcomes_hi.append(c(outcomes_hi[-1] + Constants.delta_hi))

        # create list of lotteries
        # --------------------------------------------------------------------------------------------------------
        p.participant.vars['scl_lotteries'] = list(
            zip(indices, outcomes_lo, outcomes_hi)
        )

        # randomize order of lotteries if <random_order = True>
        # --------------------------------------------------------------------------------------------------------
        if Constants.random_order:
            random.shuffle(
                p.participant.vars['scl_lotteries']
            )

