# here we copypasted Felix structure. We actually don't need to do this via classes,
# but it can be just more readable format than json to locate a game based on the game order for a specific player

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import payoff_setters

class BRETPage:
    @staticmethod
    def get_form_fields(player):
        return  [
        'bret_bomb',
        'bret_boxes_collected',
        'bret_boxes_scheme',
        'bret_bomb_row',
        'bret_bomb_col',
    ]

    # jsonify BRET settings for Javascript application
    @staticmethod
    def vars_for_template(player):
        reset = player.participant.vars.get('reset', False)
        if reset:
            del player.participant.vars['reset']
        input = not Constants.devils_game if not Constants.dynamic else False
        otree_vars = {
            'reset': reset,
            'input': input,
            'random': Constants.random,
            'dynamic': Constants.dynamic,
            'num_rows': Constants.num_rows,
            'num_cols': Constants.num_cols,
            'feedback': Constants.feedback,
            'undoable': Constants.undoable,
            'box_width': Constants.box_width,
            'box_height': Constants.box_height,
            'time_interval': Constants.time_interval,
        }
        return {
            'otree_vars': otree_vars,

        }

    @staticmethod
    def before_next_page(player):
        player.participant.vars['reset'] = True
        player.set_bret_payoff()




class CEMPage:
    @staticmethod
    def get_form_fields(player):
        form_fields = [list(t) for t in zip(*player.participant.vars['cem_choices'])][1]
        return form_fields


    @staticmethod
    def vars_for_template(player):

        # specify info for progress bar
        total = Constants.num_cem_choices
        page = player.subsession.round_number
        progress = page / total * 100


        return {
            'choices': player.participant.vars['cem_choices'],

        }



    @staticmethod
    def before_next_page(player):
        form_fields = [list(t) for t in zip(*player.participant.vars['cem_choices'])][1]
        indices = [list(t) for t in zip(*player.participant.vars['cem_choices'])][0]



        # replace choices in <choices_made>
        for j, choice in zip(indices, form_fields):
            choice_i = getattr(player, choice)
            player.participant.vars['cem_choices_made'][j - 1] = choice_i

        # set payoff
        player.set_cem_payoffs()
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

            }

    # set player's payoff
    # ----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def before_next_page(player):
        form_fields = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][1]
        indices = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][0]


            # replace choices in <choices_made>
        for j, choice in zip(indices, form_fields):
            choice_i = getattr(player, choice)
            player.participant.vars['mpl_choices_made'][j - 1] = choice_i

        # set payoff
        player.set_mpl_payoffs()
        # determine consistency
        player.set_mpl_consistency()
        # set switching row
        player.set_mpl_switching_row()


class SCLPage:
    @staticmethod
    def get_form_fields(player):
        return ['scl_lottery_choice']


    @staticmethod
    def vars_for_template(player):
        return {
            'lotteries': player.participant.vars['scl_lotteries'],
            'prob_hi': "{0:.1f}".format(Constants.scl_probability) + "%",
            'prob_lo': "{0:.1f}".format(100 - Constants.scl_probability) + "%",
            'task_number': player.participant.vars['task_number']
        }


    @staticmethod
    def before_next_page(player):
        player.set_scl_payoffs()



