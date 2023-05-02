from umbrella.configs.scl import Constants
import random
from otree.api import BaseConstants, Currency as c
from umbrella.payoff_setters import scl


def get_form_fields(player):
    return ['scl_lottery_choice']


def vars_for_template(player):
    num_lotteries = Constants.num_lotteries + \
        1 if Constants.risk_loving else Constants.num_lotteries
    return {
        'lotteries': player.participant.vars['scl_lotteries'],
        'prob_hi': "{0:.1f}".format(Constants.probability) + "%",
        'prob_lo': "{0:.1f}".format(100 - Constants.probability) + "%",
        'num_lotteries': num_lotteries
    }


def before_next_page(player):
    # set payoff
    scl.set_payoffs(player)
