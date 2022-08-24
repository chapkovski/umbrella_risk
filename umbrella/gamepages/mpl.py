from umbrella.configs.mpl import Constants
import random
from otree.api import BaseConstants, Currency as cu
from umbrella.payoff_setters import mpl

def get_form_fields(player):
    # unzip list of form_fields from <mpl_choices> list
    form_fields = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][1]
    return form_fields



def vars_for_template(player):
    # specify info for progress bar
    total = len(player.participant.vars['mpl_choices'])
    page = player.subsession.round_number
    progress = page / total * 100

    if Constants.one_choice_per_page:
        return {
            'page': page,
            'total': total,
            'progress': progress,
            'choices': [player.participant.vars['mpl_choices'][page - 1]],
            'lottery_a_lo': c(Constants.lottery_a_lo),
            'lottery_a_hi': c(Constants.lottery_a_hi),
            'lottery_b_lo': c(Constants.lottery_b_lo),
            'lottery_b_hi': c(Constants.lottery_b_hi)
        }
    else:
        return {
            'choices': player.participant.vars['mpl_choices'],
            'lottery_a_lo': c(Constants.lottery_a_lo),
            'lottery_a_hi': c(Constants.lottery_a_hi),
            'lottery_b_lo': c(Constants.lottery_b_lo),
            'lottery_b_hi': c(Constants.lottery_b_hi),

        }



def before_next_page(player):
    form_fields = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][1]
    indices = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][0]

    # replace choices in <choices_made>
    for j, choice in zip(indices, form_fields):
        choice_i = getattr(player, choice)
        player.participant.vars['mpl_choices_made'][j - 1] = choice_i

    # set payoff
    mpl.set_payoffs(player)
    # determine consistency
    mpl.set_consistency(player)
    # set switching row
    mpl.set_switching_row(player)

