# here we copypasted Felix structure. We actually don't need to do this via classes,
# but it can be just more readable format than json to locate a game based on the game order for a specific player

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class BRETPage:
    template_name='JOPA'

class CEMPage:
    @staticmethod
    def get_form_fields(player):
        # unzip list of form_fields from <cem_choices> list
        form_fields = [list(t) for t in zip(*player.participant.vars['cem_choices'])][1]
        return form_fields

        # variables for template
        # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def vars_for_template(player):

        # specify info for progress bar
        total = Constants.num_choices
        page = player.subsession.round_number
        progress = page / total * 100


        return {
            'choices': player.participant.vars['cem_choices'],
            'task_number': player.participant.vars['task_number']
        }

        # set payoff, determine consistency, and set switching row
        # ----------------------------------------------------------------------------------------------------------------


    @staticmethod
    def before_next_page(player):
        # self.participant.vars['task_to_pay'] = 'cem'
        player.participant.vars['task_number'] = player.participant.vars['task_number'] + 1
        # unzip indices and form fields from <cem_choices> list
        round_number = player.subsession.round_number
        form_fields = [list(t) for t in zip(*player.participant.vars['cem_choices'])][1]
        indices = [list(t) for t in zip(*player.participant.vars['cem_choices'])][0]
        index = indices[round_number - 1]


        # replace choices in <choices_made>
        for j, choice in zip(indices, form_fields):
            choice_i = getattr(player, choice)
            player.participant.vars['cem_choices_made'][j - 1] = choice_i

        # set payoff
        player.set_payoffs()
        # determine consistency
        player.set_consistency()
        # set switching row
        player.set_switching_row()

class MPLPage:
    @staticmethod
    def get_form_fields(player):

        # unzip list of form_fields from <mpl_choices> list
        form_fields = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][1]
        return form_fields

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    @staticmethod
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
                'task_number': player.participant.vars['task_number']
            }

    # set player's payoff
    # ----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def before_next_page(player):
        player.participant.vars['task_number'] = player.participant.vars['task_number'] + 1
        # unzip indices and form fields from <mpl_choices> list
        round_number = player.subsession.round_number
        form_fields = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][1]
        indices = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][0]
        index = indices[round_number - 1]

        # if choices are displayed sequentially

            # replace choices in <choices_made>
        for j, choice in zip(indices, form_fields):
            choice_i = getattr(player, choice)
            player.participant.vars['mpl_choices_made'][j - 1] = choice_i

        # set payoff
        player.set_payoffs()
        # determine consistency
        player.set_consistency()
        # set switching row
        player.set_switching_row()


class SCLPage:
    @staticmethod
    def get_form_fields(player):
        return ['lottery_choice']

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def vars_for_template(player):
        return {
            'lotteries': player.participant.vars['scl_lotteries'],
            'prob_hi': "{0:.1f}".format(Constants.probability) + "%",
            'prob_lo': "{0:.1f}".format(100 - Constants.probability) + "%",
            'task_number': player.participant.vars['task_number']
        }

    # set payoff
    # ----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def before_next_page(player):
        player.set_payoffs()
        player.participant.vars['task_number'] = player.participant.vars['task_number'] + 1



