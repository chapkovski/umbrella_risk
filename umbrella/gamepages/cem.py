from umbrella.configs.cem import Constants
import random
from otree.api import BaseConstants, Currency as cu
from umbrella.payoff_setters import cem


def get_form_fields(player):
    form_fields = [list(t) for t in zip(*player.participant.vars['cem_choices'])][1]
    return form_fields


def vars_for_template(player):
    # specify info for progress bar
    total = Constants.num_cem_choices
    page = player.subsession.round_number
    progress = page / total * 100

    return {
        'choices': player.participant.vars['cem_choices'],

    }


def before_next_page(player):
    form_fields = [list(t) for t in zip(*player.participant.vars['cem_choices'])][1]
    indices = [list(t) for t in zip(*player.participant.vars['cem_choices'])][0]

    # replace choices in <choices_made>
    for j, choice in zip(indices, form_fields):
        choice_i = getattr(player, choice)
        player.participant.vars['cem_choices_made'][j - 1] = choice_i

    # set payoff
    cem.set_payoffs(player)
    # determine consistency
    cem.set_consistency(player)
    # set switching row
    cem.set_switching_row(player)
